#!/usr/bin/env python3

"""Tests for git branch operations."""

from pathlib import Path

import pytest

pytest.importorskip("git")

from scitex_git._branch import git_branch_rename, git_checkout_new_branch


def _make_initialized_repo(tmp_path: Path) -> Path:
    """Create a tmp git repo with one commit; reused across tests."""
    from scitex_git._clone import git_init
    from scitex_git._commit import git_add_all, git_commit

    repo_path = tmp_path / "repo"
    repo_path.mkdir()
    git_init(repo_path, verbose=False)
    (repo_path / "test.txt").write_text("test")
    git_add_all(repo_path, verbose=False)
    git_commit(repo_path, "Initial commit", verbose=False)
    return repo_path


class TestGitBranchRename:
    """Tests for git_branch_rename function."""

    def test_branch_rename_returns_true_on_success(self, tmp_path):
        # Arrange
        repo_path = _make_initialized_repo(tmp_path)
        # Act
        result = git_branch_rename(repo_path, "main", verbose=False)
        # Assert
        assert result is True

    def test_branch_rename_returns_false_for_non_git_dir(self, tmp_path):
        # Arrange
        non_git_path = tmp_path / "not_a_repo"
        non_git_path.mkdir()
        # Act
        result = git_branch_rename(non_git_path, "main", verbose=False)
        # Assert
        assert result is False

    def test_branch_rename_returns_false_for_nonexistent_path(self, tmp_path):
        # Arrange
        nonexistent = tmp_path / "does_not_exist"
        # Act
        result = git_branch_rename(nonexistent, "main", verbose=False)
        # Assert
        assert result is False

    def test_branch_rename_returns_false_for_empty_name(self, tmp_path):
        # Arrange
        repo_path = _make_initialized_repo(tmp_path)
        # Act
        result = git_branch_rename(repo_path, "", verbose=False)
        # Assert
        assert result is False

    def test_branch_rename_returns_false_for_name_with_space(self, tmp_path):
        # Arrange
        repo_path = _make_initialized_repo(tmp_path)
        # Act
        result = git_branch_rename(repo_path, "branch name", verbose=False)
        # Assert
        assert result is False

    def test_branch_rename_returns_false_for_name_starting_with_dash(self, tmp_path):
        # Arrange
        repo_path = _make_initialized_repo(tmp_path)
        # Act
        result = git_branch_rename(repo_path, "-branch", verbose=False)
        # Assert
        assert result is False


class TestGitCheckoutNewBranch:
    """Tests for git_checkout_new_branch function."""

    def test_checkout_new_branch_returns_true_on_success(self, tmp_path):
        # Arrange
        repo_path = _make_initialized_repo(tmp_path)
        # Act
        result = git_checkout_new_branch(repo_path, "feature", verbose=False)
        # Assert
        assert result is True

    def test_checkout_new_branch_returns_false_for_non_git_dir(self, tmp_path):
        # Arrange
        non_git_path = tmp_path / "not_a_repo"
        non_git_path.mkdir()
        # Act
        result = git_checkout_new_branch(non_git_path, "feature", verbose=False)
        # Assert
        assert result is False

    def test_checkout_new_branch_returns_false_for_nonexistent_path(self, tmp_path):
        # Arrange
        nonexistent = tmp_path / "does_not_exist"
        # Act
        result = git_checkout_new_branch(nonexistent, "feature", verbose=False)
        # Assert
        assert result is False

    def test_checkout_new_branch_returns_false_for_empty_name(self, tmp_path):
        # Arrange
        repo_path = _make_initialized_repo(tmp_path)
        # Act
        result = git_checkout_new_branch(repo_path, "", verbose=False)
        # Assert
        assert result is False

    def test_checkout_new_branch_returns_false_for_special_chars(self, tmp_path):
        # Arrange
        repo_path = _make_initialized_repo(tmp_path)
        # Act
        result = git_checkout_new_branch(repo_path, "branch~1", verbose=False)
        # Assert
        assert result is False

    def test_checkout_feature_branch_with_slash_returns_true(self, tmp_path):
        # Arrange
        repo_path = _make_initialized_repo(tmp_path)
        # Act
        result = git_checkout_new_branch(repo_path, "feature/auth", verbose=False)
        # Assert
        assert result is True

    def test_checkout_feature_branch_with_slash_sets_active_branch(self, tmp_path):
        # Arrange
        from git import Repo

        repo_path = _make_initialized_repo(tmp_path)
        # Act
        git_checkout_new_branch(repo_path, "feature/auth", verbose=False)
        # Assert
        assert Repo(repo_path).active_branch.name == "feature/auth"


class TestBranchSwitching:
    """Tests for branch switching workflows."""

    def test_branch_switching_sets_active_branch_name(self, tmp_path):
        # Arrange
        from git import Repo

        repo_path = _make_initialized_repo(tmp_path)
        # Act
        git_checkout_new_branch(repo_path, "feature", verbose=False)
        # Assert
        assert Repo(repo_path).active_branch.name == "feature"

    def test_branch_switching_and_commit_records_two_commits(self, tmp_path):
        # Arrange
        from git import Repo

        from scitex_git._commit import git_add_all, git_commit

        repo_path = _make_initialized_repo(tmp_path)
        git_checkout_new_branch(repo_path, "feature", verbose=False)
        (repo_path / "feature.txt").write_text("feature content")
        git_add_all(repo_path, verbose=False)
        git_commit(repo_path, "Add feature", verbose=False)
        # Act
        commits = list(Repo(repo_path).iter_commits())
        # Assert
        assert len(commits) == 2

    def test_checkout_duplicate_branch_first_call_returns_true(self, tmp_path):
        # Arrange
        repo_path = _make_initialized_repo(tmp_path)
        # Act
        result = git_checkout_new_branch(repo_path, "feature", verbose=False)
        # Assert
        assert result is True

    def test_checkout_duplicate_branch_second_call_returns_false(self, tmp_path):
        # Arrange
        repo_path = _make_initialized_repo(tmp_path)
        git_checkout_new_branch(repo_path, "feature", verbose=False)
        # Act
        result2 = git_checkout_new_branch(repo_path, "feature", verbose=False)
        # Assert
        assert result2 is False


# EOF

if __name__ == "__main__":
    import os

    import pytest

    pytest.main([os.path.abspath(__file__)])
