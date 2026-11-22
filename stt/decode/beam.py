"""STT decoding helpers (Phase 0 skeleton; filled in Phase 2/4).

- greedy_ctc_decode: argmax over CTC logits + blank/collapse removal.
- beam_search_stt: RNN-T / CTC beam search with KenLM fusion (Phase 2/4).
"""

from __future__ import annotations

import torch

from shared.vocab import STT_VOCAB, STT_VOCAB_SIZE

BLANK_ID = 0  # matches FastConformerCTC.blank_id (reserved at index 0)


def greedy_ctc_decode(logits: torch.Tensor) -> list[int]:
    """logits: [T, V] or [B, T, V] -> list of token IDs (collapsed, blank removed)."""
    logits = logits.squeeze(0) if logits.dim() == 3 and logits.shape[0] == 1 else logits
    preds = logits.argmax(dim=-1).tolist()
    out: list[int] = []
    prev = -1
    for p in preds:
        if p != BLANK_ID and p != prev:
            out.append(p)
        prev = p
    return out


def ids_to_text(ids: list[int]) -> str:
    return "".join(STT_VOCAB[i] if 0 <= i < STT_VOCAB_SIZE else "" for i in ids)


def greedy_decode_text(logits: torch.Tensor) -> str:
    return ids_to_text(greedy_ctc_decode(logits))


def beam_search_stt(
    logits: torch.Tensor, beam_size: int = 4, lm_weight: float = 0.0, lm: object | None = None
) -> tuple[str, float]:
    """Simplified CTC beam search; full LM fusion + word timestamps in Phase 4.

    Returns (text, total_logprob).
    """
    # Simple prefix-extension beam search on CTC log-probs (implementation in Phase 2/4).
    raise NotImplementedError("beam_search_stt implemented in Phase 2/4 (KenLM fusion, timestamps).")


if __name__ == "__main__":  # pragma: no cover
    torch.manual_seed(0)
    logits = torch.randn(10, STT_VOCAB_SIZE)
    print("greedy text:", greedy_decode_text(logits))
