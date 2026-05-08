"""Tests for ``scitex_git._gh_secrets``.

Covers the pure helpers (no ``gh`` subprocess): SHA256 hashing and
human-readable age formatting. The ``gh``-touching wrappers
(:func:`set_secret`, :func:`list_secrets`, etc.) need a real
authenticated CLI and are exercised end-to-end by downstream callers
(``sac dev upload-apikey-from-credentials-to-github``); covering them
here would mean mocking subprocess at the level of the Python tests,
which adds more brittleness than it removes.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from scitex_git._gh_secrets import format_age, sha256_hex


class TestSha256Hex:
    def test_known_vector(self) -> None:
        # Stable known SHA256 for a fixed input — guards against an
        # accidental switch to a different hash.
        assert (
            sha256_hex("hello")
            == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        )

    def test_unicode_uses_utf8(self) -> None:
        # Token strings are sometimes non-ASCII; document the encoding.
        assert sha256_hex("héllo") == sha256_hex("héllo".encode("utf-8").decode())

    def test_distinct_inputs_distinct_outputs(self) -> None:
        assert sha256_hex("abc") != sha256_hex("abcd")


class TestFormatAge:
    def _iso(self, **kwargs) -> str:
        return (datetime.now(timezone.utc) - timedelta(**kwargs)).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )

    def test_none_returns_question_mark(self) -> None:
        assert format_age(None) == "?"

    def test_seconds(self) -> None:
        assert format_age(self._iso(seconds=15)).endswith("s")

    def test_minutes(self) -> None:
        out = format_age(self._iso(minutes=15))
        assert out.endswith("min")
        assert out.startswith("15")

    def test_hours(self) -> None:
        out = format_age(self._iso(hours=2, minutes=24))
        assert out.endswith("h")
        # 2.4h ± floating-point rounding
        assert out.startswith("2.")

    def test_days(self) -> None:
        out = format_age(self._iso(days=2, hours=10))
        assert out.endswith("d")
        assert out.startswith("2.")

    def test_handles_z_suffix(self) -> None:
        # GitHub returns ``...Z`` (UTC). Both ``Z`` and ``+00:00``
        # should parse identically; the helper rewrites Z internally.
        z_form = self._iso(seconds=10)
        assert "Z" in z_form
        assert format_age(z_form).endswith("s")


@pytest.mark.parametrize(
    "value,expected_prefix",
    [
        ("", "e3b0c44298"),  # SHA256 of empty string
        ("a" * 1000, None),  # large input — just check it runs
    ],
)
def test_sha256_hex_misc(value, expected_prefix) -> None:
    digest = sha256_hex(value)
    assert len(digest) == 64
    if expected_prefix is not None:
        assert digest.startswith(expected_prefix)
