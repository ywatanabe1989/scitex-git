# scitex-git

Git operations and utilities extracted from the [SciTeX](https://github.com/ywatanabe1989/scitex-python) ecosystem as a standalone package.

## Install

```bash
pip install scitex-git
```

## API

```python
import scitex_git as sxg

# Clone / init
sxg.clone_repo(url, dest_dir)
sxg.git_init(repo_path)

# Add / commit
sxg.git_add_all(repo_path)
sxg.git_commit(repo_path, message="…")

# Branch
sxg.git_checkout_new_branch(repo_path, branch_name)
sxg.git_branch_rename(repo_path, old, new)
sxg.setup_branches(repo_path, template_name)

# Repo init / discovery
sxg.init_git_repo(project_dir, git_strategy="parent")
sxg.find_parent_git(project_dir)
sxg.create_child_git(project_dir)
sxg.remove_child_git(project_dir)

# Remote
sxg.get_remote_url(repo_path)
sxg.is_cloned_from(repo_path, url)
sxg.ls_remote(url)
sxg.get_head_hash(repo_path)

# Retry decorator
@sxg.git_retry(max_attempts=3)
def maybe_flaky_operation(): ...
```

## Status

Standalone fork of `scitex.git`. `scitex.logging.getLogger` is replaced by stdlib
`logging.getLogger`; the `scitex.sh.sh` shell wrapper is replaced by a tiny
~70-LOC `_vendor_sh.py` that supports just the call-shape used here. The
optional `scitex.writer.verify_tree_structure` validation step in
`create_child_git` is gated behind a `try/except ImportError` so it only runs
when `scitex-writer` is installed.

The umbrella package's `scitex.git` import path is preserved via a
`sys.modules`-alias bridge so existing code continues to work.

## License

AGPL-3.0-only (see [LICENSE](./LICENSE)).
