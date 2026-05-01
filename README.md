# scitex-git

<!-- scitex-badges:start -->
[![PyPI](https://img.shields.io/pypi/v/scitex-git.svg)](https://pypi.org/project/scitex-git/)
[![Python](https://img.shields.io/pypi/pyversions/scitex-git.svg)](https://pypi.org/project/scitex-git/)
[![Tests](https://github.com/ywatanabe1989/scitex-git/actions/workflows/test.yml/badge.svg)](https://github.com/ywatanabe1989/scitex-git/actions/workflows/test.yml)
[![Install Test](https://github.com/ywatanabe1989/scitex-git/actions/workflows/install-test.yml/badge.svg)](https://github.com/ywatanabe1989/scitex-git/actions/workflows/install-test.yml)
[![Coverage](https://codecov.io/gh/ywatanabe1989/scitex-git/graph/badge.svg)](https://codecov.io/gh/ywatanabe1989/scitex-git)
[![Docs](https://readthedocs.org/projects/scitex-git/badge/?version=latest)](https://scitex-git.readthedocs.io/en/latest/)
[![License: AGPL v3](https://img.shields.io/badge/license-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
<!-- scitex-badges:end -->

<p align="center">
  <a href="https://scitex.ai">
    <img src="docs/scitex-logo-blue-cropped.png" alt="SciTeX" width="400">
  </a>
</p>

<p align="center"><b>Git operations and utilities — clone, init, branch, remote, retry decorator.</b></p>

<p align="center">
  <a href="https://scitex-git.readthedocs.io/">Full Documentation</a> · <code>pip install scitex-git</code>
</p>

---

## Installation

```bash
pip install scitex-git
```

## Quick Start

```python
import scitex_git as sxg

sxg.clone_repo("https://github.com/foo/bar", "./bar")
sxg.git_add_all("./bar")
sxg.git_commit("./bar", message="initial")
```

## 1 Interfaces

<details>
<summary><strong>Python API</strong></summary>

<br>

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

</details>

## Status

Standalone fork of `scitex.git`. `scitex.logging.getLogger` is replaced by stdlib
`logging.getLogger`; the `scitex.sh.sh` shell wrapper is replaced by a tiny
~70-LOC `_vendor_sh.py` that supports just the call-shape used here. The
optional `scitex.writer.verify_tree_structure` validation step in
`create_child_git` is gated behind a `try/except` so it only runs when
`scitex-writer` is installed.

The umbrella package's `scitex.git` import path is preserved via a
`sys.modules`-alias bridge so existing code continues to work.

## Part of SciTeX

`scitex-git` is part of [**SciTeX**](https://scitex.ai).

>Four Freedoms for Research
>
>0. The freedom to **run** your research anywhere — your machine, your terms.
>1. The freedom to **study** how every step works — from raw data to final manuscript.
>2. The freedom to **redistribute** your workflows, not just your papers.
>3. The freedom to **modify** any module and share improvements with the community.
>
>AGPL-3.0 — because we believe research infrastructure deserves the same freedoms as the software it runs on.

## License

AGPL-3.0-only (see [LICENSE](./LICENSE)).

---

<p align="center">
  <a href="https://scitex.ai" target="_blank"><img src="docs/scitex-icon-navy-inverted.png" alt="SciTeX" width="40"/></a>
</p>
