"""Urdu G2P: grapheme to phoneme converter (Phase 0, updated in Phase 2).

Rule-based v0. Higher-quality mechanism (trained disambiguator, trained on
aligned Urdu corpora) lands in Phase 2 — no other-language data used.
"""

from __future__ import annotations

from shared.constants import URDU_GRAPHEME_SET
from shared.phoneme_inventory import PHONEME_TO_ID
from shared.text_norm import normalize_transcript


# ---------------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------------

# Letter -> default phone(s). Multi-letter graphemes handled below.
_LETTER_TO_PHONES = {
    "ا": ["ɑ"],
    "آ": ["ɑː"],
    "ب": ["b"],
    "پ": ["p"],
    "ت": ["t"],
    "ٹ": ["ṭ"],
    "ث": ["s"],
    "ج": ["ʒ"],
    "چ": ["tʃ"],
    "چھ": ["tʃʰ"],
    "جھ": ["ɟʰ"],
    "ح": ["h"],
    "خ": ["x"],
    "ڈ": ["ɖ"],
    "ژ": ["ʒ"],
    "ذ": ["z"],
    "ر": ["r"],
    "ڑ": ["ɽ"],
    "س": ["s"],
    "ش": ["ʃ"],
    "ص": ["sˤ"],
    "ض": ["zˤ"],
    "ط": ["t"],
    "ظ": ["zˤ"],
    "ع": ["ɑ"],
    "غ": ["ɣ"],
    "ف": ["f"],
    "ق": ["q"],
    "ک": ["k"],
    "گ": ["g"],
    "ل": ["l"],
    "م": ["m"],
    "ن": ["n"],
    "و": ["w"],
    "ہ": ["h"],
    "ے": ["ɛː"],
    "ی": ["i"],
}

# Diphthongs and vowel clusters (two-letter graphemes): char_seq -> phones.
_DIPHTHONGS = {
    "یا": ["i", "ɑː"],
    "یے": ["i", "ɛː"],
    "او": ["ɑ", "w"],
    "ای": ["ɑ", "i"],
    "ائی": ["ɑ", "i"],
    "اے": ["ɑ", "ɛː"],
}

# High-frequency irregular word forms (word-level overrides; G2P v0).
# To be extended by the trained disambiguator in Phase 2.
_WORD_OVERRIDES = {
    "کہ": ["k", "ɛ"],
    "ہے": ["h", "ɛ"],
    "ہیں": ["h", "eː", "n"],
    "جہاں": ["ʤ", "ɑː", "n"],
    "وہ": ["w", "ɑː"],
    "کیا": ["k", "i", "ɑː"],
    "ایک": ["ɑ", "i", "k"],
    "دو": ["d", "o"],
    "ان": ["ɑ", "n"],
    "کا": ["k", "ɑː"],
    "کی": ["k", "i"],
    "کیہ": ["k", "i"],
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_consonant_letter(ch: str) -> bool:
    # ع is pronounced as an epenthetic/semivocalic segment; treat as consonant-like.
    return ch in _LETTER_TO_PHONES and ch not in ("ا", "ع")


def _word_to_phonemes(word: str) -> list[str]:
    override = _WORD_OVERRIDES.get(word)
    if override is not None:
        return list(override)

    phones: list[str] = []
    i = 0
    n = len(word)
    while i < n:
        # Multi-letter grapheme check (diphthongs)
        matched = False
        if i + 2 <= n:
            seq = word[i : i + 2]
            if seq in _DIPHTHONGS:
                phones.extend(_DIPHTHONGS[seq])
                i += 2
                matched = True
        if matched:
            continue

        ch = word[i]
        if ch in _LETTER_TO_PHONES:
            phones.extend(_LETTER_TO_PHONES[ch])
        elif ch == "ع":
            phones.append("ɑ")  # epenthetic schwa
        else:
            # Code-switch: pass through other scripts (e.g., Latin, Devanagari)
            phones.append(ch)
        i += 1

    # Epenthesis: between adjacent consonants with no vowel, insert "ɑ".
    out: list[str] = []
    for idx, ph in enumerate(phones):
        out.append(ph)
        if idx + 1 < len(phones):
            next_ph = phones[idx + 1]
            # Naive adjacency: if both current and next are "consonant-like"
            # and the transition doesn't look like a valid cluster, add "ɑ".
            if _is_consonant_letter(_PH_TO_LETTER.get(ph, ph)) and _is_consonant_letter(
                _PH_TO_LETTER.get(next_ph, next_ph)
            ):
                out.append("ɑ")
    return out


# Reverse map for epenthesis heuristic.
_PH_TO_LETTER = {v: k for k, vs in _LETTER_TO_PHONES.items() for v in vs}


def to_phonemes(text: str) -> list[str]:
    """Urdu graphemes -> IPA-ish phoneme sequence (list of symbols)."""
    norm = normalize_transcript(text, lang="ur")
    out: list[str] = []
    for word in norm.split():
        out.extend(_word_to_phonemes(word))
        out.append(" ")
    if out:
        out.pop()  # trailing space
    return [p for p in out if p]


def to_phoneme_string(text: str) -> str:
    return " ".join(to_phonemes(text))


def to_ids(text: str) -> list[int]:
    from shared.phoneme_inventory import PHONEME_TO_ID

    return [PHONEME_TO_ID.get(p, PHONEME_TO_ID.get("ə")) for p in to_phonemes(text)]


if __name__ == "__main__":  # pragma: no cover
    print(to_phoneme_string("آج کیا ہوا؟"))
