"""Shared pytest fixtures for scitex-git tests.

Ensures git has an author identity in environments (e.g. CI runners) where
no global git config is set, so that `git commit` does not fail with
"Author identity unknown".
"""


import pytest


@pytest.fixture(autouse=True)
def _git_identity(monkeypatch):
    """Set git author/committer env vars so commits work in any environment."""
    monkeypatch.setenv("GIT_AUTHOR_NAME", "Test User")
    monkeypatch.setenv("GIT_AUTHOR_EMAIL", "test@example.com")
    monkeypatch.setenv("GIT_COMMITTER_NAME", "Test User")
    monkeypatch.setenv("GIT_COMMITTER_EMAIL", "test@example.com")
    # Also unset any HOME-based config that might pick up an empty user.email
    yield
