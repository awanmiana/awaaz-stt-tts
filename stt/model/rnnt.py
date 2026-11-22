"""RNN-T variant (Phase 0 skeleton; implemented in Phase 2/4).

Design: text targets as UTF-8 bytes (from shared/text_norm) instead of graphemes,
since RNN-T uses byte-level vocab; weights start from scratch.

Components:
- Predictor: embedding of bytes + conv/LSTM stack.
- Joint: encoder output x predictor -> vocab logits over bytes + blank.
- Loss: RNNT (alpha/beta recursion) — use torchaudio.functional.rnnt_loss or
  a custom recursion; see Phase 2.
"""

from __future__ import annotations

import torch
import torch.nn as nn

from stt.model.fastconformer import FastConformerConfig, FastConformerEncoder


class RNNTPredictor(nn.Module):
    def __init__(self, vocab_size: int, n_mels: int = 80, cfg: FastConformerConfig | None = None):
        super().__init__()
        # Predictor operates on text targets (bytes, shared/text_norm)
        self.emb = nn.Embedding(vocab_size, 128)
        self.conv = nn.Conv1d(128, 128, 3, padding=1)
        self.out = nn.Linear(128, 128)

    def forward(self, y: torch.Tensor) -> torch.Tensor:
        # y: [B, S] (byte ids) -> [B, S, 128]
        x = self.emb(y).transpose(1, 2)
        x = torch.relu(self.conv(x))
        return self.out(x.transpose(1, 2))


class RNNTJoint(nn.Module):
    def __init__(self, vocab_size: int, d_model: int):
        super().__init__()
        self.enc_proj = nn.Linear(d_model, d_model)
        self.pred_proj = nn.Linear(d_model, d_model)
        self.out = nn.Linear(d_model, vocab_size + 1)  # +1 for blank

    def forward(self, enc: torch.Tensor, pred: torch.Tensor) -> torch.Tensor:
        # enc: [B, T, D], pred: [B, S, D] -> logits [B, T, S, V]
        return self.out(self.enc_proj(enc).unsqueeze(2) + self.pred_proj(pred).unsqueeze(1))


class RNNTModel(nn.Module):
    def __init__(self, vocab_size: int, d_model: int, n_mels: int = 80):
        super().__init__()
        self.encoder = FastConformerEncoder(FastConformerConfig(d_model=d_model), n_mels)
        self.predictor = RNNTPredictor(vocab_size, n_mels)
        self.joint = RNNTJoint(vocab_size, d_model)

    def forward(self, x: torch.Tensor, y: torch.Tensor):
        enc = self.encoder(x)
        pred = self.predictor(y)
        logits = self.joint(enc, pred)
        return logits


if __name__ == "__main__":  # pragma: no cover
    torch.manual_seed(0)
    m = RNNTModel(vocab_size=256, d_model=128)
    enc = m.encoder(torch.randn(2, 100, 80))
    pred = m.predictor(torch.zeros(2, 5, dtype=torch.long))
    logits = m.joint(enc, pred)
    print("joint logits:", logits.shape)
