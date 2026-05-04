---
description: |
  [TOPIC] Installation
  [DETAILS] pip install scitex-git. Pure-Python wrapper around the system `git` binary; you must have `git` installed on PATH.
tags: [scitex-git-installation]
---

# Installation

## Standard

```bash
pip install scitex-git
```

Pure-Python; no Python deps. Wraps the system `git` binary via `subprocess`.

## Required system tool

| Tool   | Install                                                  |
|--------|----------------------------------------------------------|
| `git`  | `apt install git` / `brew install git` / https://git-scm.com/ |

```bash
git --version                                # must be on PATH
```

## Verify

```bash
python -c "import scitex_git; print(scitex_git.__version__)"
python -c "from scitex_git import clone_repo, git_init, git_commit, git_retry; print('ok')"
```

## Editable install (development)

```bash
git clone https://github.com/ywatanabe1989/scitex-git
cd scitex-git
pip install -e .
```

## Used by

Pulled in transitively by ecosystem packages that need programmatic git
operations (e.g. scitex-cloud's three-way sync, project scaffolding).
