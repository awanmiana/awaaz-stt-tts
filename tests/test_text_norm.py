"""shared/text_norm tests."""

from shared.text_norm import normalize_transcript


def test_digits():
    assert normalize_transcript("۲۰۲۶") == "2026"


def test_punctuation():
    assert normalize_transcript("پہلا جملہ۔") == "پہلا جملہ"


def test_zero_width_and_space_collapse():
    assert normalize_transcript("ہی\u200c لو") == "ہی لو"


def test_strip_and_nfc():
    assert normalize_transcript("  کی ") == "کی"
