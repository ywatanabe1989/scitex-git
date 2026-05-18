"""Smoke tests: every example script must run to completion."""

import subprocess
import sys
from pathlib import Path

import pytest

EXAMPLES = list(Path(__file__).parents[2].joinpath("examples").glob("*.py"))


def test_examples_directory_contains_scripts():
    # Arrange
    found = EXAMPLES
    # Act
    count = len(found)
    # Assert
    assert count > 0, "no example scripts found"


@pytest.mark.parametrize("example_path", EXAMPLES, ids=[p.name for p in EXAMPLES])
def test_example_script_runs_to_completion(example_path, tmp_path):
    # Arrange
    cmd = [sys.executable, str(example_path)]
    # Act
    completed = subprocess.run(
        cmd,
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=60,
    )
    # Assert
    assert completed.returncode == 0, f"{example_path.name} failed: {completed.stderr}"
