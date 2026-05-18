#!/usr/bin/env python3
# File: /home/ywatanabe/proj/scitex-code/tests/scitex/git/test_init.py

"""Tests for git init module."""

import tempfile
from pathlib import Path

import pytest

pytest.importorskip("git")
from git import Repo

from scitex_git._init import (
    create_child_git,
    find_parent_git,
    init_git_repo,
    remove_child_git,
)


class TestFindParentGit:
    def test_find_parent_returns_none_when_no_parent_git(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir) / "project"
            project_dir.mkdir()
            # Act
            result = find_parent_git(project_dir)
            # Assert
            assert result is None

    def test_find_parent_returns_parent_when_git_exists_above(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            parent_dir = Path(temp_dir)
            Repo.init(parent_dir)
            child_dir = parent_dir / "child"
            child_dir.mkdir()
            # Act
            result = find_parent_git(child_dir)
            # Assert
            assert result == parent_dir


class TestRemoveChildGit:
    def test_remove_child_git_deletes_existing_dot_git(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            git_dir = project_dir / ".git"
            git_dir.mkdir()
            # Act
            remove_child_git(project_dir)
            # Assert
            assert not git_dir.exists()

    def test_remove_child_git_is_noop_when_dot_git_missing(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            git_dir = project_dir / ".git"
            # Act
            remove_child_git(project_dir)
            # Assert
            assert not git_dir.exists()


class TestCreateChildGit:
    def test_create_child_git_returns_project_dir_on_success(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            # Act
            result = create_child_git(project_dir)
            # Assert
            assert result == project_dir

    def test_create_child_git_creates_dot_git_directory(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            # Act
            create_child_git(project_dir)
            # Assert
            assert (project_dir / ".git").exists()

    def test_create_child_git_first_call_returns_project_dir(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            # Act
            first_result = create_child_git(project_dir)
            # Assert
            assert first_result == project_dir

    def test_create_child_git_second_call_returns_project_dir(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            create_child_git(project_dir)
            # Act
            second_result = create_child_git(project_dir)
            # Assert
            assert second_result == project_dir


class TestInitGitRepo:
    def test_init_git_repo_with_none_strategy_returns_none(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            # Act
            result = init_git_repo(project_dir, git_strategy=None)
            # Assert
            assert result is None

    def test_init_git_repo_with_child_returns_project_dir(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            # Act
            result = init_git_repo(project_dir, git_strategy="child")
            # Assert
            assert result == project_dir

    def test_init_git_repo_with_child_creates_dot_git(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            # Act
            init_git_repo(project_dir, git_strategy="child")
            # Assert
            assert (project_dir / ".git").exists()

    def test_init_git_repo_parent_strategy_no_parent_returns_project_dir(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            # Act
            result = init_git_repo(project_dir, git_strategy="parent")
            # Assert
            assert result == project_dir

    def test_init_git_repo_parent_strategy_no_parent_creates_dot_git(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            # Act
            init_git_repo(project_dir, git_strategy="parent")
            # Assert
            assert (project_dir / ".git").exists()

    def test_init_git_repo_invalid_strategy_raises_value_error(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            # Act
            ctx = pytest.raises(ValueError, match="invalid")
            # Assert
            with ctx:
                init_git_repo(project_dir, git_strategy="invalid")

    def test_find_parent_git_walks_up_nested_structure(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            Repo.init(root)
            nested = root / "a" / "b" / "c" / "d"
            nested.mkdir(parents=True)
            # Act
            result = find_parent_git(nested)
            # Assert
            assert result == root

    def test_init_git_repo_parent_with_existing_parent_returns_parent(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            parent_dir = Path(temp_dir)
            Repo.init(parent_dir)
            child_dir = parent_dir / "child"
            child_dir.mkdir()
            # Act
            result = init_git_repo(child_dir, git_strategy="parent")
            # Assert
            assert result == parent_dir

    def test_init_git_repo_parent_with_existing_parent_removes_child_dot_git(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            parent_dir = Path(temp_dir)
            Repo.init(parent_dir)
            child_dir = parent_dir / "child"
            child_dir.mkdir()
            # Act
            init_git_repo(child_dir, git_strategy="parent")
            # Assert
            assert not (child_dir / ".git").exists()

    def test_init_git_repo_parent_with_existing_parent_keeps_parent_dot_git(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            parent_dir = Path(temp_dir)
            Repo.init(parent_dir)
            child_dir = parent_dir / "child"
            child_dir.mkdir()
            # Act
            init_git_repo(child_dir, git_strategy="parent")
            # Assert
            assert (parent_dir / ".git").exists()


# EOF

if __name__ == "__main__":
    import os

    import pytest

    pytest.main([os.path.abspath(__file__)])
