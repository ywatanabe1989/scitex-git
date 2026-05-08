# Changelog

All notable changes to `scitex-git` are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.2.0] — 2026-05-08

### Added

- ``_gh_secrets`` module with thin wrappers around the ``gh`` CLI for
  GitHub Actions secrets and variables: ``set_secret`` /
  ``list_secrets`` / ``get_secret_metadata`` / ``set_variable`` /
  ``get_variable``.
- ``set_secret_with_sha_sidecar(repo, name, value)`` — pushes a secret
  AND a SHA256 fingerprint as a sibling repo variable
  (``{name}_SHA256``). Lets callers detect drift between local and
  remote without exposing the secret value (GitHub's Actions secrets
  API is write-only by design).
- ``format_age(updated_iso)`` — single-unit relative-date renderer
  (``15min`` / ``2.4d``) for CLI reports, mirroring ``git
  relative_date``.
- ``sha256_hex(value)`` — client-side fingerprint helper, paired with
  the sidecar variable for drift detection.
- Tests covering the pure helpers (hash + age formatting); the
  ``gh``-touching wrappers are exercised end-to-end by downstream
  callers (e.g. ``sac dev upload-apikey-from-credentials-to-github``).

## [0.1.0]

- Initial CHANGELOG entry — see git log for prior history.
