"""Quickstart for scitex_git.

Initializes a temp repo, makes a commit, then reads back the HEAD hash.
"""

import subprocess
import tempfile
from pathlib import Path

import scitex_git as sg


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "demo"
        repo.mkdir()

        # init + identity (so commit works in CI / sandbox)
        sg.git_init(repo)
        subprocess.run(
            ["git", "-C", str(repo), "config", "user.email", "demo@example.com"],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(repo), "config", "user.name", "demo"], check=True
        )

        # write a file, stage everything, commit
        (repo / "README.md").write_text("# demo\nHello scitex_git\n")
        sg.git_add_all(repo)
        sg.git_commit(repo, "initial commit")

        # read state via the public API
        head = sg.get_head_hash(repo)
        parent = sg.find_parent_git(repo / "README.md")

        print(f"HEAD hash: {head}")
        print(f"Parent .git directory: {parent}")
        assert head and len(head) >= 7
        assert parent is not None
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
