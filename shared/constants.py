"""Shared constants: Urdu alphabet, digits, diacritics, style vocabulary.

Urdu notes:
- Arabic script. Base letters: 28 consonants + 3 vowels (ی ے ا).
- Extension letters: ے, ء/و/, چھ, جھ, کھ?, ڑ, غ, خ, ح, س، ش، ص، ض، ط، ظ، ع، ق، ک, گ, ل، م، ن، و، ہ، ی، آ، ژ, ذ.
- Code-switching: Hindi/English words appear in speech; G2P passes non-Urdu scripts through.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Urdu alphabet
# ---------------------------------------------------------------------------

URDU_BASE_LETTERS = "ابپتٹثجچحخڈژذرڑسشصضطظعغفقکگلمنوہی"
# Exception/vowel letters:
URDU_VOWEL_LETTERS = "آاعے"
# Digits (Urdu) <-> ASCII
URDU_DIGITS = "۱۲۳۴۵۶۷۸۹۰"
ASCII_DIGITS = "1234567890"

# Punctuation / control characters common in Urdu text
URDU_PUNCTUATION = "۔؟،؛«»‐‑‒–—―“”‘’()[]{}<>«»:;,.!?‑ـ"

# Diacritics and zero-width characters (stripped during normalization)
URDU_DIACRITICS = "\u0651\u064e\u064f\u0650\u0654\u0653\u0656\u0611"  # shadda, fatha, damma, kasra, hamza, shadda+dot, inverse?
ZERO_WIDTH = ["\u200c", "\u200d", "\u200b"]  # ZWNJ, ZWJ, ZWSP

# Word-level special forms used by the G2P (see shared/g2p/urdu_g2p.py)
URDU_GRAPHEME_SET = set(URDU_BASE_LETTERS + URDU_VOWEL_LETTERS)

# ---------------------------------------------------------------------------
# Speech style vocabulary (used by STT dev sets + TTS conditioning)
# ---------------------------------------------------------------------------

STYLES = [
    "neutral",
    "warm",
    "energetic",
    "academic",
    "poetic",
    "debate",
    "street",
    "casual",
]

# Speech domains (STT dev-set tagging)
DOMAINS = [
    "news",
    "academic",
    "poetry",
    "debate",
    "fictional",
    "everyday",
    "street",
    "technical",
    "medical",
]
