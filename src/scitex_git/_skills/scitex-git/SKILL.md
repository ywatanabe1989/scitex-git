---
name: scitex-git
description: |
  [WHAT] Programmatic git operations — clone/init/commit/branch/remote/retry helpers (`clone_repo`, `git_init`, `git_commit`, `git_branch_rename`, `find_parent_git`, `get_remote_url`, `is_cloned_from`, `git_retry`, `setup_branches`, ...).
  [WHEN] Automating git workflows from Python without shelling out and parsing stdout — repo init, commits, branch setup, parent-git discovery.
  [HOW] `from scitex_git import clone_repo, git_init, git_commit, git_add_all, git_retry, ...` — wraps subprocess `git`.
tags: [scitex-git]
primary_interface: python
interfaces:
  python: 3
  cli: 0
  mcp: 0
  skills: 2
  http: 0
---

> **Interfaces:** Python ⭐⭐⭐ · CLI — · MCP — · Skills ⭐⭐ · Hook — · HTTP —

# scitex-git

Programmatic git operations — `clone_repo`, `git_init`, `git_commit`, `git_add_all`, `git_branch_rename`, `git_checkout_new_branch`, `find_parent_git`, `init_git_repo`, `get_remote_url`, `is_cloned_from`, `git_retry`, `setup_branches`. Drop-in replacement for shelling out to `git` via `subprocess.run` and parsing stdout.

## Sub-skills

- [01_installation.md](01_installation.md) — pip install + system `git` requirement
- [02_quick-start.md](02_quick-start.md) — clone, init, commit, branch, retry
- [03_python-api.md](03_python-api.md) — full public surface

See README.md and the package's public `__init__.py` for the full
function list.
