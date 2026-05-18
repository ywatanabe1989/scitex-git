#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

import pytest

pytest.importorskip("git")

from scitex_git._commit import git_add_all, git_commit


def _init_empty_repo(tmp_path: Path) -> Path:
    from scitex_git._clone import git_init

    repo_path = tmp_path / "repo"
    repo_path.mkdir()
    git_init(repo_path, verbose=False)
    return repo_path


class TestGitCommit:
    def test_add_all_returns_true_after_staging_files(self, tmp_path):
        # Arrange
        repo_path = _init_empty_repo(tmp_path)
        (repo_path / "test.txt").write_text("test")
        # Act
        result = git_add_all(repo_path, verbose=False)
        # Assert
        assert result is True

    def test_commit_returns_true_for_staged_change(self, tmp_path):
        # Arrange
        repo_path = _init_empty_repo(tmp_path)
        (repo_path / "test.txt").write_text("test")
        git_add_all(repo_path, verbose=False)
        # Act
        result = git_commit(repo_path, "Test commit", verbose=False)
        # Assert
        assert result is True

    def test_commit_records_supplied_message_on_head(self, tmp_path):
        # Arrange
        from git import Repo

        repo_path = _init_empty_repo(tmp_path)
        (repo_path / "test.txt").write_text("test")
        git_add_all(repo_path, verbose=False)
        commit_msg = "Test commit"
        git_commit(repo_path, commit_msg, verbose=False)
        # Act
        head_msg = Repo(repo_path).head.commit.message.strip()
        # Assert
        assert head_msg == commit_msg

    def test_commit_without_changes_returns_false(self, tmp_path):
        # Arrange
        repo_path = _init_empty_repo(tmp_path)
        # Act
        result = git_commit(repo_path, "Empty commit", verbose=False)
        # Assert
        assert result is False

    def test_commit_multiple_files_returns_true(self, tmp_path):
        # Arrange
        repo_path = _init_empty_repo(tmp_path)
        (repo_path / "file1.txt").write_text("content 1")
        (repo_path / "file2.txt").write_text("content 2")
        (repo_path / "file3.txt").write_text("content 3")
        git_add_all(repo_path, verbose=False)
        # Act
        result = git_commit(repo_path, "Add three files", verbose=False)
        # Assert
        assert result is True

    def test_commit_multiple_files_records_three_tree_entries(self, tmp_path):
        # Arrange
        from git import Repo

        repo_path = _init_empty_repo(tmp_path)
        (repo_path / "file1.txt").write_text("content 1")
        (repo_path / "file2.txt").write_text("content 2")
        (repo_path / "file3.txt").write_text("content 3")
        git_add_all(repo_path, verbose=False)
        git_commit(repo_path, "Add three files", verbose=False)
        # Act
        traversed = list(Repo(repo_path).head.commit.tree.traverse())
        # Assert
        assert len(traversed) == 3


# EOF

if __name__ == "__main__":
    import os

    import pytest

    pytest.main([os.path.abspath(__file__)])
