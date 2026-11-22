"""shared/g2p tests (Phase 0/2 G2P)."""

from shared.g2p import to_phonemes
from shared.phoneme_inventory import PHONEMES


def test_all_in_inventory():
    for w in ["مل", "کہ", "آج"]:
        assert all(p in PHONEMES for p in to_phonemes(w))


def test_word_override():
    assert to_phonemes("کہ") == ["k", "ɛ"]


def test_epenthesis_between_consonants():
    # "مل" -> م + ɑ + ل (epenthetic schwa inserted between consonants)
    assert to_phonemes("مل") == ["m", "ɑ", "l"]
