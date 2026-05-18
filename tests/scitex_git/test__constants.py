#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: /home/ywatanabe/proj/scitex-code/tests/scitex/git/test_constants.py

"""Tests for git constants."""

import pytest

pytest.importorskip("git")

from scitex_git._constants import EXIT_FAILURE, EXIT_SUCCESS


class TestConstants:
    def test_exit_success_value_is_zero(self):
        # Arrange
        expected = 0
        # Act
        value = EXIT_SUCCESS
        # Assert
        assert value == expected

    def test_exit_failure_value_is_one(self):
        # Arrange
        expected = 1
        # Act
        value = EXIT_FAILURE
        # Assert
        assert value == expected

    def test_exit_success_and_failure_differ(self):
        # Arrange
        a, b = EXIT_SUCCESS, EXIT_FAILURE
        # Act
        equal = a == b
        # Assert
        assert equal is False


# EOF

if __name__ == "__main__":
    import os

    import pytest

    pytest.main([os.path.abspath(__file__)])
