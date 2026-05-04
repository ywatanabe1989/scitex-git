---
description: |
  [TOPIC] Python API
  [DETAILS] Public callables — clone/init, commit, branches, parent-git discovery, remote inspection, retry, workflow setup.
tags: [scitex-git-python-api]
---

# Python API

## Imports

```python
from scitex_git import (
    # clone + init
    clone_repo, git_init,
    # commit
    git_add_all, git_commit,
    # branches
    git_branch_rename, git_checkout_new_branch,
    # init / parent discovery
    create_child_git, find_parent_git, init_git_repo, remove_child_git,
    # remote inspection
    get_head_hash, get_remote_url, is_cloned_from, ls_remote,
    # retry
    git_retry,
    # composite workflow
    setup_branches,
)
```

## Clone + init

| Callable                              | Purpose                                  |
|---------------------------------------|------------------------------------------|
| `clone_repo(url, dest, ...)`          | Clone a remote                           |
| `git_init(path)`                      | `git init` at a path                     |
| `init_git_repo(path)`                 | Init + sensible defaults                 |
| `create_child_git(parent, child)`     | Add a nested git repo                    |
| `remove_child_git(child)`             | Remove a nested git repo cleanly         |

## Commit

| Callable                              | Purpose                                  |
|---------------------------------------|------------------------------------------|
| `git_add_all(path)`                   | `git add -A`                             |
| `git_commit(path, message=...)`       | `git commit -m`                          |

## Branches

| Callable                              | Purpose                                  |
|---------------------------------------|------------------------------------------|
| `git_checkout_new_branch(path, name)` | `git checkout -b`                        |
| `git_branch_rename(path, old, new)`   | Rename a branch                          |
| `setup_branches(path, main, develop)` | Create a main/develop topology           |

## Discovery + inspection

| Callable                              | Purpose                                  |
|---------------------------------------|------------------------------------------|
| `find_parent_git(path)`               | Walk up to enclosing `.git/`             |
| `get_remote_url(path, name="origin")` | Fetch the remote URL                     |
| `get_head_hash(path)`                 | HEAD commit SHA                          |
| `is_cloned_from(path, url)`           | True if origin matches                   |
| `ls_remote(url)`                      | List remote refs without cloning         |

## Retry

```python
git_retry(["push"], cwd=".", attempts=3, backoff=2.0)
```

Wraps any `git` subcommand in exponential backoff for transient network
failures.

## Notes

All callables return either `None` or stdout-as-str; failures raise
`subprocess.CalledProcessError` (or a subclass).
