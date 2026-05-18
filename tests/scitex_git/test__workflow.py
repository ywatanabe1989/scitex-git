#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: /home/ywatanabe/proj/scitex-code/tests/scitex/git/test_workflow.py

"""Tests for git workflow operations."""

import tempfile
from pathlib import Path

import pytest

pytest.importorskip("git")

from scitex_git._clone import git_init
from scitex_git._workflow import setup_branches


class TestWorkflow:
    def test_setup_branches_returns_true_on_initialized_repo(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)
            git_init(repo_path)
            test_file = repo_path / "test.txt"
            test_file.write_text("test content")
            # Act
            result = setup_branches(repo_path, "test-template", verbose=False)
            # Assert
            assert result is True

    def test_setup_branches_returns_false_for_non_git_dir(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)
            test_file = repo_path / "test.txt"
            test_file.write_text("test content")
            # Act
            result = setup_branches(repo_path, "test-template", verbose=False)
            # Assert
            assert result is False

    def test_complete_workflow_records_single_commit(self):
        # Arrange
        from git import Repo

        from scitex_git._commit import git_add_all, git_commit

        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)
            git_init(repo_path, verbose=False)
            (repo_path / "test.txt").write_text("initial content")
            git_add_all(repo_path, verbose=False)
            git_commit(repo_path, "Initial commit", verbose=False)
            # Act
            commits = list(Repo(repo_path).iter_commits())
            # Assert
            assert len(commits) == 1

    def test_complete_workflow_records_commit_message(self):
        # Arrange
        from git import Repo

        from scitex_git._commit import git_add_all, git_commit

        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)
            git_init(repo_path, verbose=False)
            (repo_path / "test.txt").write_text("initial content")
            git_add_all(repo_path, verbose=False)
            git_commit(repo_path, "Initial commit", verbose=False)
            # Act
            head_msg = Repo(repo_path).head.commit.message.strip()
            # Assert
            assert head_msg == "Initial commit"

    def test_branch_rename_sets_active_branch_name_to_main(self):
        # Arrange
        from git import Repo

        from scitex_git._branch import git_branch_rename
        from scitex_git._commit import git_add_all, git_commit

        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)
            git_init(repo_path, verbose=False)
            (repo_path / "test.txt").write_text("initial content")
            git_add_all(repo_path, verbose=False)
            git_commit(repo_path, "Initial commit", verbose=False)
            git_branch_rename(repo_path, "main", verbose=False)
            # Act
            active = Repo(repo_path).active_branch.name
            # Assert
            assert active == "main"

    def test_multi_file_commit_records_message(self):
        # Arrange
        from git import Repo

        from scitex_git._commit import git_add_all, git_commit

        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)
            git_init(repo_path, verbose=False)
            (repo_path / "file1.txt").write_text("content 1")
            (repo_path / "file2.txt").write_text("content 2")
            (repo_path / "file3.txt").write_text("content 3")
            git_add_all(repo_path, verbose=False)
            git_commit(repo_path, "Add multiple files", verbose=False)
            # Act
            head_msg = Repo(repo_path).head.commit.message.strip()
            # Assert
            assert head_msg == "Add multiple files"

    def test_multi_file_commit_records_three_tree_entries(self):
        # Arrange
        from git import Repo

        from scitex_git._commit import git_add_all, git_commit

        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)
            git_init(repo_path, verbose=False)
            (repo_path / "file1.txt").write_text("content 1")
            (repo_path / "file2.txt").write_text("content 2")
            (repo_path / "file3.txt").write_text("content 3")
            git_add_all(repo_path, verbose=False)
            git_commit(repo_path, "Add multiple files", verbose=False)
            # Act
            traversed = list(Repo(repo_path).head.commit.tree.traverse())
            # Assert
            assert len(traversed) == 3


# EOF

if __name__ == "__main__":
    import os

    import pytest

    pytest.main([os.path.abspath(__file__)])
