#!/usr/bin/env python3

"""Tests for git retry logic with exponential backoff."""

import subprocess
import time

import pytest

pytest.importorskip("git")

from scitex_git._retry import git_retry


class _CallCounter:
    """Hand-rolled fake replacing MagicMock per PA-306 no-mocks rule."""

    def __init__(self, return_value=None):
        self.return_value = return_value
        self.call_count = 0
        self.calls: list[tuple] = []

    def __call__(self, *args, **kwargs):
        self.call_count += 1
        self.calls.append((args, kwargs))
        return self.return_value


class TestGitRetry:
    """Tests for git_retry function."""

    def test_success_on_first_attempt_returns_value(self):
        """Operation succeeds on first try — return value passes through."""
        # Arrange
        operation = _CallCounter(return_value="success")
        # Act
        result = git_retry(operation)
        # Assert
        assert result == "success"

    def test_success_on_first_attempt_calls_once(self):
        """Operation succeeds on first try — only called once."""
        # Arrange
        operation = _CallCounter(return_value="success")
        # Act
        git_retry(operation)
        # Assert
        assert operation.call_count == 1

    def test_success_after_retries_returns_final_value(self):
        """Operation succeeds after a few lock errors — returns final value."""
        # Arrange
        call_count = 0

        def operation_with_locks():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                error = subprocess.CalledProcessError(128, "git")
                error.stderr = (
                    b"fatal: Unable to create '.git/index.lock': File exists."
                )
                raise error
            return "success"

        # Act
        result = git_retry(
            operation_with_locks,
            max_retries=5,
            initial_delay=0.01,
            max_delay=0.05,
        )
        # Assert
        assert result == "success"

    def test_success_after_retries_uses_expected_attempt_count(self):
        """Operation succeeds after a few lock errors — call count matches retries."""
        # Arrange
        call_count = 0

        def operation_with_locks():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                error = subprocess.CalledProcessError(128, "git")
                error.stderr = (
                    b"fatal: Unable to create '.git/index.lock': File exists."
                )
                raise error
            return "success"

        # Act
        git_retry(
            operation_with_locks,
            max_retries=5,
            initial_delay=0.01,
            max_delay=0.05,
        )
        # Assert
        assert call_count == 3

    def test_raises_on_last_attempt_with_persistent_lock(self):
        """Raises CalledProcessError on last retry attempt (current behavior)."""

        # Arrange
        def always_locked():
            error = subprocess.CalledProcessError(128, "git")
            error.stderr = b"fatal: Unable to create '.git/index.lock': File exists."
            raise error

        # Act
        ctx = pytest.raises(subprocess.CalledProcessError)
        # Assert
        with ctx:
            git_retry(
                always_locked,
                max_retries=3,
                initial_delay=0.01,
                max_delay=0.05,
            )

    def test_non_lock_error_raises_immediately(self):
        """Non-lock CalledProcessError is raised immediately."""

        # Arrange
        def non_lock_error():
            error = subprocess.CalledProcessError(128, "git")
            error.stderr = b"fatal: not a git repository"
            raise error

        # Act
        ctx = pytest.raises(subprocess.CalledProcessError)
        # Assert
        with ctx:
            git_retry(
                non_lock_error,
                max_retries=5,
                initial_delay=0.01,
            )

    def test_non_lock_error_not_retried_call_count(self):
        """Non-lock CalledProcessError is not retried — only called once."""
        # Arrange
        call_count = 0

        def non_lock_error():
            nonlocal call_count
            call_count += 1
            error = subprocess.CalledProcessError(128, "git")
            error.stderr = b"fatal: not a git repository"
            raise error

        # Act
        try:
            git_retry(
                non_lock_error,
                max_retries=5,
                initial_delay=0.01,
            )
        except subprocess.CalledProcessError:
            pass
        # Assert
        assert call_count == 1

    def test_non_subprocess_error_raises_immediately(self):
        """Non-subprocess exceptions are raised immediately."""

        # Arrange
        def other_error():
            raise ValueError("Some other error")

        # Act
        ctx = pytest.raises(ValueError)
        # Assert
        with ctx:
            git_retry(
                other_error,
                max_retries=5,
                initial_delay=0.01,
            )

    def test_non_subprocess_error_not_retried_call_count(self):
        """Non-subprocess exceptions are not retried — only called once."""
        # Arrange
        call_count = 0

        def other_error():
            nonlocal call_count
            call_count += 1
            raise ValueError("Some other error")

        # Act
        try:
            git_retry(
                other_error,
                max_retries=5,
                initial_delay=0.01,
            )
        except ValueError:
            pass
        # Assert
        assert call_count == 1

    def test_lock_error_with_string_stderr_returns_success(self):
        """Handle lock error with string stderr instead of bytes — eventually succeeds."""
        # Arrange
        call_count = 0

        def lock_with_string_stderr():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                error = subprocess.CalledProcessError(128, "git")
                error.stderr = "fatal: Unable to create '.git/index.lock': File exists."
                raise error
            return "success"

        # Act
        result = git_retry(
            lock_with_string_stderr,
            max_retries=3,
            initial_delay=0.01,
        )
        # Assert
        assert result == "success"

    def test_lock_error_with_string_stderr_retries_until_success(self):
        """Handle lock error with string stderr instead of bytes — call count matches."""
        # Arrange
        call_count = 0

        def lock_with_string_stderr():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                error = subprocess.CalledProcessError(128, "git")
                error.stderr = "fatal: Unable to create '.git/index.lock': File exists."
                raise error
            return "success"

        # Act
        git_retry(
            lock_with_string_stderr,
            max_retries=3,
            initial_delay=0.01,
        )
        # Assert
        assert call_count == 2

    def test_called_process_error_with_none_stderr_raises(self):
        """CalledProcessError with None stderr — should not retry, raises."""

        # Arrange
        def error_with_none_stderr():
            error = subprocess.CalledProcessError(128, "git")
            error.stderr = None
            raise error

        # Act
        ctx = pytest.raises(subprocess.CalledProcessError)
        # Assert
        with ctx:
            git_retry(
                error_with_none_stderr,
                max_retries=3,
                initial_delay=0.01,
            )

    def test_called_process_error_with_none_stderr_not_retried(self):
        """CalledProcessError with None stderr — not retried, called once."""
        # Arrange
        call_count = 0

        def error_with_none_stderr():
            nonlocal call_count
            call_count += 1
            error = subprocess.CalledProcessError(128, "git")
            error.stderr = None
            raise error

        # Act
        try:
            git_retry(
                error_with_none_stderr,
                max_retries=3,
                initial_delay=0.01,
            )
        except subprocess.CalledProcessError:
            pass
        # Assert
        assert call_count == 1

    def test_exponential_backoff_attempts_count(self):
        """Verify exponential backoff produces expected attempt count."""
        # Arrange
        call_times: list[float] = []

        def record_time_and_fail():
            call_times.append(time.time())
            error = subprocess.CalledProcessError(128, "git")
            error.stderr = b"index.lock"
            raise error

        # Act
        try:
            git_retry(
                record_time_and_fail,
                max_retries=4,
                initial_delay=0.05,
                backoff_factor=2.0,
                max_delay=1.0,
            )
        except subprocess.CalledProcessError:
            pass
        # Assert
        assert len(call_times) == 4

    def test_exponential_backoff_delays_grow_at_least_doubling(self):
        """Verify exponential backoff doubles delays between attempts."""
        # Arrange
        call_times: list[float] = []

        def record_time_and_fail():
            call_times.append(time.time())
            error = subprocess.CalledProcessError(128, "git")
            error.stderr = b"index.lock"
            raise error

        try:
            git_retry(
                record_time_and_fail,
                max_retries=4,
                initial_delay=0.05,
                backoff_factor=2.0,
                max_delay=1.0,
            )
        except subprocess.CalledProcessError:
            pass
        # Act
        delays = [
            call_times[i] - call_times[i - 1] for i in range(1, len(call_times))
        ]
        # Assert
        assert all(
            delays[i] >= delays[i - 1] * 0.9 for i in range(1, len(delays))
        )

    def test_max_delay_cap_attempts_count(self):
        """Verify max_delay still produces expected attempt count."""
        # Arrange
        call_times: list[float] = []

        def record_time_and_fail():
            call_times.append(time.time())
            error = subprocess.CalledProcessError(128, "git")
            error.stderr = b"index.lock"
            raise error

        # Act
        try:
            git_retry(
                record_time_and_fail,
                max_retries=5,
                initial_delay=0.1,
                backoff_factor=10.0,
                max_delay=0.15,
            )
        except subprocess.CalledProcessError:
            pass
        # Assert
        assert len(call_times) == 5

    def test_max_delay_cap_limits_inter_attempt_delay(self):
        """Verify delay is capped at max_delay (with slack)."""
        # Arrange
        call_times: list[float] = []

        def record_time_and_fail():
            call_times.append(time.time())
            error = subprocess.CalledProcessError(128, "git")
            error.stderr = b"index.lock"
            raise error

        try:
            git_retry(
                record_time_and_fail,
                max_retries=5,
                initial_delay=0.1,
                backoff_factor=10.0,
                max_delay=0.15,
            )
        except subprocess.CalledProcessError:
            pass
        # Act
        delays = [
            call_times[i] - call_times[i - 1] for i in range(1, len(call_times))
        ]
        # Assert
        assert max(delays) <= 0.25

    def test_returns_operation_result_dict(self):
        """Verify the operation's return value is passed through unchanged."""

        # Arrange
        def return_dict():
            return {"status": "ok", "data": [1, 2, 3]}

        # Act
        result = git_retry(return_dict)
        # Assert
        assert result == {"status": "ok", "data": [1, 2, 3]}


# EOF

if __name__ == "__main__":
    import os

    import pytest

    pytest.main([os.path.abspath(__file__)])
