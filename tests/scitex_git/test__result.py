#!/usr/bin/env python3

"""Tests for git result dataclasses."""

import pytest

pytest.importorskip("git")

from scitex_git._result import BranchResult, CommitResult, GitResult


class TestGitResult:
    """Tests for GitResult dataclass."""

    def test_success_result_records_success_true(self):
        # Arrange
        # Act
        result = GitResult(success=True)
        # Assert
        assert result.success is True

    def test_success_result_defaults_error_to_none(self):
        # Arrange
        # Act
        result = GitResult(success=True)
        # Assert
        assert result.error is None

    def test_success_result_defaults_stdout_to_none(self):
        # Arrange
        # Act
        result = GitResult(success=True)
        # Assert
        assert result.stdout is None

    def test_success_result_defaults_stderr_to_none(self):
        # Arrange
        # Act
        result = GitResult(success=True)
        # Assert
        assert result.stderr is None

    def test_failure_result_records_success_false(self):
        # Arrange
        # Act
        result = GitResult(
            success=False,
            error="Operation failed",
            stderr="fatal: error message",
        )
        # Assert
        assert result.success is False

    def test_failure_result_records_error(self):
        # Arrange
        # Act
        result = GitResult(
            success=False,
            error="Operation failed",
            stderr="fatal: error message",
        )
        # Assert
        assert result.error == "Operation failed"

    def test_failure_result_records_stderr(self):
        # Arrange
        # Act
        result = GitResult(
            success=False,
            error="Operation failed",
            stderr="fatal: error message",
        )
        # Assert
        assert result.stderr == "fatal: error message"

    def test_explicit_stdout_value_is_preserved(self):
        # Arrange
        stdout_value = "command output"
        # Act
        result = GitResult(success=True, stdout=stdout_value)
        # Assert
        assert result.stdout == stdout_value

    def test_full_fields_preserves_stderr(self):
        # Arrange
        # Act
        result = GitResult(
            success=True,
            error=None,
            stdout="output",
            stderr="warning",
        )
        # Assert
        assert result.stderr == "warning"

    def test_equal_dataclasses_compare_equal(self):
        # Arrange
        result1 = GitResult(success=True, error=None)
        result2 = GitResult(success=True, error=None)
        # Act
        equal = result1 == result2
        # Assert
        assert equal is True

    def test_unequal_dataclasses_compare_not_equal(self):
        # Arrange
        result1 = GitResult(success=True)
        result2 = GitResult(success=False)
        # Act
        equal = result1 == result2
        # Assert
        assert equal is False


class TestCommitResult:
    """Tests for CommitResult dataclass."""

    def test_success_commit_records_hash(self):
        # Arrange
        commit_hash = "abc123def456"
        # Act
        result = CommitResult(success=True, commit_hash=commit_hash)
        # Assert
        assert result.commit_hash == commit_hash

    def test_success_commit_records_success_true(self):
        # Arrange
        # Act
        result = CommitResult(success=True, commit_hash="x")
        # Assert
        assert result.success is True

    def test_failure_commit_defaults_hash_to_none(self):
        # Arrange
        # Act
        result = CommitResult(success=False, error="Nothing to commit")
        # Assert
        assert result.commit_hash is None

    def test_failure_commit_records_error(self):
        # Arrange
        # Act
        result = CommitResult(success=False, error="Nothing to commit")
        # Assert
        assert result.error == "Nothing to commit"

    def test_commit_result_is_git_result_instance(self):
        # Arrange
        # Act
        result = CommitResult(success=True)
        # Assert
        assert isinstance(result, GitResult)

    def test_commit_result_exposes_commit_hash_attribute(self):
        # Arrange
        # Act
        result = CommitResult(
            success=True,
            stdout="output",
            stderr="warning",
            commit_hash="abc123",
        )
        # Assert
        assert hasattr(result, "commit_hash")


class TestBranchResult:
    """Tests for BranchResult dataclass."""

    def test_success_branch_records_branch_name(self):
        # Arrange
        branch_name = "feature/new-feature"
        # Act
        result = BranchResult(success=True, branch_name=branch_name)
        # Assert
        assert result.branch_name == branch_name

    def test_success_branch_records_success_true(self):
        # Arrange
        # Act
        result = BranchResult(success=True, branch_name="x")
        # Assert
        assert result.success is True

    def test_failure_branch_defaults_name_to_none(self):
        # Arrange
        # Act
        result = BranchResult(success=False, error="Branch operation failed")
        # Assert
        assert result.branch_name is None

    def test_failure_branch_records_error(self):
        # Arrange
        # Act
        result = BranchResult(success=False, error="Branch operation failed")
        # Assert
        assert result.error == "Branch operation failed"

    def test_branch_result_is_git_result_instance(self):
        # Arrange
        # Act
        result = BranchResult(success=True)
        # Assert
        assert isinstance(result, GitResult)

    def test_branch_result_exposes_branch_name_attribute(self):
        # Arrange
        # Act
        result = BranchResult(
            success=True,
            stdout="output",
            stderr="warning",
            branch_name="main",
        )
        # Assert
        assert hasattr(result, "branch_name")


class TestResultInheritance:
    """Tests for result class inheritance."""

    def test_commit_result_inherits_git_result(self):
        # Arrange
        # Act
        result = CommitResult(success=True)
        # Assert
        assert isinstance(result, GitResult)

    def test_branch_result_inherits_git_result(self):
        # Arrange
        # Act
        result = BranchResult(success=True)
        # Assert
        assert isinstance(result, GitResult)

    def test_git_result_has_success_attribute(self):
        # Arrange
        # Act
        result = GitResult(success=True, stdout="out", stderr="err")
        # Assert
        assert hasattr(result, "success")

    def test_commit_result_has_success_attribute(self):
        # Arrange
        # Act
        result = CommitResult(success=True, stdout="out", stderr="err")
        # Assert
        assert hasattr(result, "success")

    def test_branch_result_has_success_attribute(self):
        # Arrange
        # Act
        result = BranchResult(success=True, stdout="out", stderr="err")
        # Assert
        assert hasattr(result, "success")


class TestResultUsagePatterns:
    """Tests for common usage patterns."""

    def test_success_result_carries_commit_hash_when_read(self):
        # Arrange
        success_result = CommitResult(success=True, commit_hash="abc123")
        # Act
        observed_hash = success_result.commit_hash if success_result.success else None
        # Assert
        assert observed_hash == "abc123"

    def test_failure_result_carries_error_when_read(self):
        # Arrange
        failure_result = CommitResult(success=False, error="Failed")
        # Act
        observed_error = (
            failure_result.error if not failure_result.success else None
        )
        # Assert
        assert observed_error == "Failed"

    def test_result_branch_name_propagates_into_context_dict(self):
        # Arrange
        result = BranchResult(
            success=True,
            branch_name="develop",
            stdout="Switched to branch 'develop'",
        )
        # Act
        context = {
            "success": result.success,
            "branch": result.branch_name,
            "output": result.stdout,
        }
        # Assert
        assert context["branch"] == "develop"

    def test_result_success_propagates_into_context_dict(self):
        # Arrange
        result = BranchResult(
            success=True,
            branch_name="develop",
            stdout="Switched to branch 'develop'",
        )
        # Act
        context = {
            "success": result.success,
            "branch": result.branch_name,
            "output": result.stdout,
        }
        # Assert
        assert context["success"] is True


# EOF

if __name__ == "__main__":
    import os

    import pytest

    pytest.main([os.path.abspath(__file__)])
