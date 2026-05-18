#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: /home/ywatanabe/proj/scitex-code/tests/scitex/git/test_utils.py

"""Tests for git utilities."""

import tempfile
from pathlib import Path

import pytest

pytest.importorskip("git")

from scitex_git._utils import _in_directory


class TestUtils:
    def test_in_directory_changes_cwd_inside_block(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir).resolve()
            # Act
            with _in_directory(temp_path):
                inside = Path.cwd()
            # Assert
            assert inside == temp_path

    def test_in_directory_restores_cwd_after_block(self):
        # Arrange
        cwd_original = Path.cwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            # Act
            with _in_directory(temp_path):
                pass
            # Assert
            assert Path.cwd() == cwd_original

    def test_in_directory_restores_cwd_on_exception(self):
        # Arrange
        cwd_original = Path.cwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            # Act
            try:
                with _in_directory(temp_path):
                    raise ValueError("test exception")
            except ValueError:
                pass
            # Assert
            assert Path.cwd() == cwd_original


# EOF

if __name__ == "__main__":
    import os

    import pytest

    pytest.main([os.path.abspath(__file__)])
