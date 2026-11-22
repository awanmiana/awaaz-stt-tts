"""Urdu phoneme inventory (Phase 0).

Custom IPA-ish set (from-scratch; we define it, don't pull from elsewhere).
All G2P output is expected to use these symbols.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Consonants
# ---------------------------------------------------------------------------
CONSONANTS = [
    # Stops
    "p", "b", "t", "d", "k", "g",
    "ṭ", "ɖ", "c", "ɟ", "tʃ", "tʃʰ", "ɟʰ",
    "ɡ", "gʰ",
    # Fricatives
    "f", "v", "s", "z", "ʃ", "ʒ", "x", "ɣ", "q", "h",
    "sˤ", "zˤ",
    # Nasals
    "m", "n", "ɲ", "ŋ", "ɳ",
    # Liquids
    "l", "r", "ɽ", "w", "j",
]

# ---------------------------------------------------------------------------
# Vowels (length-marked where meaningful)
# ---------------------------------------------------------------------------
VOWELS = [
    "ɑ", "ɑː", "a",
    "i", "iː",
    "u", "uː",
    "e", "eː",
    "o", "oː",
    "ɛ", "ɛː",
    "ɔ", "ɔː",
    "ə",
]

PHONEMES = CONSONANTS + VOWELS

PHONEME_TO_ID = {p: i for i, p in enumerate(PHONEMES)}
ID_TO_PHONEME = {i: p for i, p in enumerate(PHONEMES)}

# Length of the (growing) inventory — used for vocab sizes in configs.
N_PHONEMES = len(PHONEMES)

# Urdu-specific emphasis on aspirated/geminate stops and Urdu vowel inventory
URDU_VOWELS = ["ɑː", "i", "u", "e", "o", "ɛ", "ɔ", "ə", "iː", "uː", "eː", "oː", "ɛː", "ɔː", "a"]

if __name__ == "__main__":  # pragma: no cover
    print(f"N_PHONEMES={N_PHONEMES}")
    print("VOWELS:", " ".join(VOWELS))
