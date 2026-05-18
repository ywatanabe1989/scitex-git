"""Compile-only stub for examples/quickstart.py (PS303)."""

import subprocess
import sys
from pathlib import Path

QUICKSTART = Path(__file__).parents[2] / "examples" / "quickstart.py"


def test_quickstart_script_file_exists_on_disk():
    # Arrange
    expected = QUICKSTART
    # Act
    is_file = expected.is_file()
    # Assert
    assert is_file, f"missing {expected}"


def test_quickstart_script_passes_py_compile():
    # Arrange
    cmd = [sys.executable, "-m", "py_compile", str(QUICKSTART)]
    # Act
    completed = subprocess.run(cmd, check=False)
    # Assert
    assert completed.returncode == 0
