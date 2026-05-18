#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: /home/ywatanabe/proj/scitex-code/tests/scitex/git/test__types.py

"""Tests for git result types."""

import pytest

pytest.importorskip("git")

from scitex_git._types import BranchResult, CloneResult, CommitResult, GitResult


class TestGitResult:
    def test_success_result_records_success_true(self):
        # Arrange
        message = "Operation succeeded"
        # Act
        result = GitResult(success=True, message=message)
        # Assert
        assert result.success is True

    def test_success_result_records_message(self):
        # Arrange
        message = "Operation succeeded"
        # Act
        result = GitResult(success=True, message=message)
        # Assert
        assert result.message == message

    def test_success_result_defaults_stdout_to_none(self):
        # Arrange
        # Act
        result = GitResult(success=True, message="ok")
        # Assert
        assert result.stdout is None

    def test_success_result_defaults_stderr_to_none(self):
        # Arrange
        # Act
        result = GitResult(success=True, message="ok")
        # Assert
        assert result.stderr is None

    def test_success_result_defaults_exit_code_to_none(self):
        # Arrange
        # Act
        result = GitResult(success=True, message="ok")
        # Assert
        assert result.exit_code is None

    def test_failure_result_records_success_false(self):
        # Arrange
        # Act
        result = GitResult(
            success=False,
            message="Operation failed",
            stderr="fatal: error message",
            exit_code=1,
        )
        # Assert
        assert result.success is False

    def test_failure_result_records_stderr(self):
        # Arrange
        # Act
        result = GitResult(
            success=False,
            message="Operation failed",
            stderr="fatal: error message",
            exit_code=1,
        )
        # Assert
        assert result.stderr == "fatal: error message"

    def test_failure_result_records_exit_code(self):
        # Arrange
        # Act
        result = GitResult(
            success=False,
            message="Operation failed",
            stderr="fatal: error message",
            exit_code=1,
        )
        # Assert
        assert result.exit_code == 1

    def test_explicit_stdout_value_is_preserved(self):
        # Arrange
        # Act
        result = GitResult(
            success=True, message="Success", stdout="command output", exit_code=0
        )
        # Assert
        assert result.stdout == "command output"


class TestCommitResult:
    def test_success_commit_records_hash(self):
        # Arrange
        commit_hash = "abc123def456"
        # Act
        result = CommitResult(success=True, message="Commit created", commit_hash=commit_hash)
        # Assert
        assert result.commit_hash == commit_hash

    def test_success_commit_records_success_true(self):
        # Arrange
        # Act
        result = CommitResult(success=True, message="Commit created", commit_hash="abc")
        # Assert
        assert result.success is True

    def test_commit_result_is_git_result_instance(self):
        # Arrange
        # Act
        result = CommitResult(success=True, message="ok")
        # Assert
        assert isinstance(result, GitResult)

    def test_failure_commit_defaults_hash_to_none(self):
        # Arrange
        # Act
        result = CommitResult(success=False, message="Nothing to commit")
        # Assert
        assert result.commit_hash is None


class TestCloneResult:
    def test_success_clone_records_repo_path(self):
        # Arrange
        repo_path = "/path/to/repo"
        # Act
        result = CloneResult(success=True, message="Repository cloned", repo_path=repo_path)
        # Assert
        assert result.repo_path == repo_path

    def test_success_clone_records_success_true(self):
        # Arrange
        # Act
        result = CloneResult(success=True, message="ok", repo_path="/p")
        # Assert
        assert result.success is True

    def test_clone_result_is_git_result_instance(self):
        # Arrange
        # Act
        result = CloneResult(success=True, message="ok")
        # Assert
        assert isinstance(result, GitResult)

    def test_failure_clone_defaults_repo_path_to_none(self):
        # Arrange
        # Act
        result = CloneResult(success=False, message="Clone failed")
        # Assert
        assert result.repo_path is None

    def test_failure_clone_records_stderr(self):
        # Arrange
        # Act
        result = CloneResult(
            success=False, message="Clone failed", stderr="fatal: repository not found"
        )
        # Assert
        assert result.stderr == "fatal: repository not found"


class TestBranchResult:
    def test_success_branch_records_branch_name(self):
        # Arrange
        branch_name = "feature/new-feature"
        # Act
        result = BranchResult(
            success=True, message="Branch created", branch_name=branch_name
        )
        # Assert
        assert result.branch_name == branch_name

    def test_success_branch_records_success_true(self):
        # Arrange
        # Act
        result = BranchResult(success=True, message="ok", branch_name="x")
        # Assert
        assert result.success is True

    def test_branch_result_is_git_result_instance(self):
        # Arrange
        # Act
        result = BranchResult(success=True, message="ok")
        # Assert
        assert isinstance(result, GitResult)

    def test_failure_branch_defaults_name_to_none(self):
        # Arrange
        # Act
        result = BranchResult(success=False, message="Branch operation failed")
        # Assert
        assert result.branch_name is None


class TestResultInheritance:
    def test_commit_result_inherits_git_result(self):
        # Arrange
        # Act
        result = CommitResult(success=True)
        # Assert
        assert isinstance(result, GitResult)

    def test_clone_result_inherits_git_result(self):
        # Arrange
        # Act
        result = CloneResult(success=True)
        # Assert
        assert isinstance(result, GitResult)

    def test_branch_result_inherits_git_result(self):
        # Arrange
        # Act
        result = BranchResult(success=True)
        # Assert
        assert isinstance(result, GitResult)


# EOF

if __name__ == "__main__":
    import os

    import pytest

    pytest.main([os.path.abspath(__file__)])
