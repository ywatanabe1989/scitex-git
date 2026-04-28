---
name: scitex-git
description: Programmatic git operations — `clone_repo`, `git_init`, `git_commit`, `git_add_all`, `git_branch_rename`, `git_checkout_new_branch`, `find_parent_git`, `init_git_repo`, `get_remote_url`, `is_cloned_from`, `git_retry`, `setup_branches`. Drop-in replacement for shelling out to `git` via `subprocess.run` and parsing stdout.
primary_interface: python
interfaces:
  python: 3
  cli: 1
  mcp: 0
  skills: 2
  hook: 0
  http: 0
canonical-location: scitex-git/src/scitex_git/_skills/scitex-git/SKILL.md
tags: [scitex-git, scitex-package]
---

> **Interfaces:** Python ⭐⭐⭐ · CLI ⭐ · MCP — · Skills ⭐⭐ · Hook — · HTTP —

# scitex-git

Programmatic git operations — `clone_repo`, `git_init`, `git_commit`, `git_add_all`, `git_branch_rename`, `git_checkout_new_branch`, `find_parent_git`, `init_git_repo`, `get_remote_url`, `is_cloned_from`, `git_retry`, `setup_branches`. Drop-in replacement for shelling out to `git` via `subprocess.run` and parsing stdout.

See README.md and the package's public `__init__.py` for the full
function list. This skill leaf exists so agents discover the package
exists and roughly what shape it has — refer to the source for
signatures.

<!-- EOF -->
