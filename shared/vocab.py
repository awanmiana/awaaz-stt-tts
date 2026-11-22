"""STT character vocabulary for decoding (Phase 0; filled in Phase 2/4).

STT targets Urdu graphemes (like Whisper targets text). Vocab = Urdu alphabet
+ digits + spaces + punctuation + specials.
"""

from __future__ import annotations

from shared.constants import (
    ASCII_DIGITS,
    URDU_BASE_LETTERS,
    URDU_PUNCTUATION,
    URDU_VOWEL_LETTERS,
)


def build_stt_vocab() -> list[str]:
    chars: list[str] = ["<pad>", "<blank>", "<unk>", " "]
    for ch in (
        URDU_BASE_LETTERS + URDU_VOWEL_LETTERS + "".join(ASCII_DIGITS) + URDU_PUNCTUATION + "\t"
    ):
        if ch not in chars:
            chars.append(ch)
    return chars


STT_VOCAB = build_stt_vocab()
STT_VOCAB_SIZE = len(STT_VOCAB)
STT_TOKEN_TO_ID = {t: i for i, t in enumerate(STT_VOCAB)}

if __name__ == "__main__":  # pragma: no cover
    print(f"STT_VOCAB_SIZE={STT_VOCAB_SIZE}")
    print("".join(STT_VOCAB[:40]))
