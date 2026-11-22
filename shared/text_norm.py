"""Urdu transcript normalization (Phase 0).

Goals (from the plan): pure-Urdu, Unicode-stable, deterministic, WER-friendly.
- Unicode NFC normalization.
- Convert Arabic-script presentation forms to canonical letters.
- Strip ZWNJ/ZWJ (zero-width formatting, not speech content).
- Map Urdu digits -> ASCII digits (stable for models; G2P/tokenizer handle both).
- Remove punctuation (vowels spacing), collapse spaces, strip ends.
- Do NOT change script or diacritics beyond the above (G2P maps to phones).
"""

from __future__ import annotations

import unicodedata

from shared.constants import ASCII_DIGITS, URDU_DIGITS, ZERO_WIDTH

# Arabic-script presentation forms A/B that commonly appear in Urdu text
# (e.g., in typography or OCR output) -> canonical base letters.
_PRESENTATION_FORMS = {
    "ﻻ": "لا", "ﻼ": "لا", "ﻵ": "لا", "ﻶ": "لا", "﻿": "",
    "ﮋ": "ی", "ﮌ": "ی", "ﮍ": "ی", "ﮎ": "ک", "ﮏ": "ک", "ﮐ": "گ", "ﮑ": "گ",
    "ﮒ": "ل", "ﮓ": "ل", "ﮔ": "م", "ﮕ": "م", "ﮖ": "ن", "ﮗ": "ن",
    "ﮘ": "و", "ﮙ": "و", "ﮚ": "ہ", "ﮛ": "ہ", "ﮜ": "ی", "ﮝ": "ی",
    "ﮞ": "ا", "ﮟ": "ا", "ﮠ": "ب", "ﮡ": "ب", "ﮢ": "پ", "ﮣ": "پ",
    "ﮤ": "ت", "ﮥ": "ت", "ﮦ": "ٹ", "ﮧ": "ٹ", "ﮨ": "ث", "ﮩ": "ث",
    "ﮪ": "ج", "ﮫ": "ج", "ﮬ": "چ", "ﮭ": "چ", "ﮮ": "ح", "ﮯ": "ح",
    "ﮰ": "خ", "ﮱ": "خ", "ﯾ": "ا", "ﯿ": "ا",
}


def _strip_zero_width(text: str) -> str:
    for ch in ZERO_WIDTH:
        text = text.replace(ch, "")
    return text


def _to_ascii_digits(text: str) -> str:
    return "".join(
        str(ASCII_DIGITS[URDU_DIGITS.index(ch)]) if ch in URDU_DIGITS else ch
        for ch in text
    )


def _remove_punctuation_and_control(text: str) -> str:
    out = []
    for ch in text:
        if ch in "۔؟،؛«»()[]{}<>«»:;,.!?…":
            out.append(" ")
        elif ord(ch) < 32 and ch not in "\n\t":
            out.append(" ")
        else:
            out.append(ch)
    return "".join(out)


def normalize_transcript(text: str, lang: str = "ur") -> str:
    """Normalize an Urdu transcript to a canonical form (pure, deterministic).

    - NFC Unicode normalization.
    - Presentation forms -> canonical letters.
    - Zero-width format chars removed; punctuation -> spaces; spaces collapsed.
    - Urdu digits -> ASCII digits.
    - NFKC (compat) pass for ligature-like sequences.
    """
    if not isinstance(text, str):
        raise TypeError(f"normalize_transcript expects str, got {type(text)}")

    text = text.strip()
    text = unicodedata.normalize("NFC", text)
    for src, dst in _PRESENTATION_FORMS.items():
        text = text.replace(src, dst)
    text = _strip_zero_width(text)
    if lang == "ur":
        text = _to_ascii_digits(text)
    text = _remove_punctuation_and_control(text)
    text = unicodedata.normalize("NFC", text)
    text = " ".join(text.split())
    return text


def contains_non_urdu(text: str) -> bool:
    """Best-effort check for foreign (non-Arabic-script) content."""
    from shared.constants import URDU_GRAPHEME_SET

    return any(ch not in URDU_GRAPHEME_SET for ch in normalize_transcript(text))


if __name__ == "__main__":  # pragma: no cover
    print(normalize_transcript("پہلی جملہ۔ یہ دوسری جملہ ہے!"))
