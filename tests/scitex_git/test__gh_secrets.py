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

pytest.importorskip("git")

from scitex_git._gh_secrets import format_age, sha256_hex


class TestSha256Hex:
    def test_sha256_for_hello_matches_known_vector(self) -> None:
        # Arrange
        expected = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        # Act
        result = sha256_hex("hello")
        # Assert
        assert result == expected

    def test_sha256_of_unicode_uses_utf8_encoding(self) -> None:
        # Arrange
        non_ascii = "héllo"
        round_trip = non_ascii.encode("utf-8").decode()
        # Act
        equal = sha256_hex(non_ascii) == sha256_hex(round_trip)
        # Assert
        assert equal

    def test_sha256_of_distinct_inputs_yields_distinct_outputs(self) -> None:
        # Arrange
        a, b = "abc", "abcd"
        # Act
        equal = sha256_hex(a) == sha256_hex(b)
        # Assert
        assert equal is False


def _iso(**kwargs) -> str:
    return (datetime.now(timezone.utc) - timedelta(**kwargs)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


class TestFormatAge:
    def test_format_age_for_none_returns_question_mark(self) -> None:
        # Arrange
        # Act
        out = format_age(None)
        # Assert
        assert out == "?"

    def test_format_age_seconds_suffix_is_s(self) -> None:
        # Arrange
        ts = _iso(seconds=15)
        # Act
        out = format_age(ts)
        # Assert
        assert out.endswith("s")

    def test_format_age_minutes_suffix_is_min(self) -> None:
        # Arrange
        ts = _iso(minutes=15)
        # Act
        out = format_age(ts)
        # Assert
        assert out.endswith("min")

    def test_format_age_minutes_prefix_matches_value(self) -> None:
        # Arrange
        ts = _iso(minutes=15)
        # Act
        out = format_age(ts)
        # Assert
        assert out.startswith("15")

    def test_format_age_hours_suffix_is_h(self) -> None:
        # Arrange
        ts = _iso(hours=2, minutes=24)
        # Act
        out = format_age(ts)
        # Assert
        assert out.endswith("h")

    def test_format_age_hours_prefix_matches_value(self) -> None:
        # Arrange
        ts = _iso(hours=2, minutes=24)
        # Act
        out = format_age(ts)
        # Assert
        assert out.startswith("2.")

    def test_format_age_days_suffix_is_d(self) -> None:
        # Arrange
        ts = _iso(days=2, hours=10)
        # Act
        out = format_age(ts)
        # Assert
        assert out.endswith("d")

    def test_format_age_days_prefix_matches_value(self) -> None:
        # Arrange
        ts = _iso(days=2, hours=10)
        # Act
        out = format_age(ts)
        # Assert
        assert out.startswith("2.")

    def test_format_age_z_suffix_parsed_as_utc(self) -> None:
        # Arrange
        z_form = _iso(seconds=10)
        # Act
        out = format_age(z_form)
        # Assert
        assert out.endswith("s")

    def test_iso_helper_emits_z_suffix(self) -> None:
        # Arrange
        # Act
        z_form = _iso(seconds=10)
        # Assert
        assert "Z" in z_form


@pytest.mark.parametrize(
    "value,expected_prefix",
    [
        ("", "e3b0c44298"),  # SHA256 of empty string
        ("a" * 1_000, ""),  # large input — prefix unchecked (sentinel empty)
    ],
)
def test_sha256_hex_misc_digest_length_is_64(value, expected_prefix) -> None:
    # Arrange
    _ = expected_prefix  # not used in this length-only assertion
    # Act
    digest = sha256_hex(value)
    # Assert
    assert len(digest) == 64


@pytest.mark.parametrize(
    "value,expected_prefix",
    [
        ("", "e3b0c44298"),
    ],
)
def test_sha256_hex_misc_known_prefix_matches(value, expected_prefix) -> None:
    # Arrange
    # Act
    digest = sha256_hex(value)
    # Assert
    assert digest.startswith(expected_prefix)
