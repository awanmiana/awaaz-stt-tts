"""HuBERT-style masked latent pretraining (Phase 0 skeleton; filled Phase 3).

Loss: cross-entropy over cluster targets (stt/ssl/cluster.py) on masked frames
(+ optional CTC aux head in STT fine-tuning — Phase 4).
"""

from __future__ import annotations

import torch
import torch.nn as nn

from stt.ssl.wav2vec2 import TransformerEncoder


class Hubert(nn.Module):
    def __init__(self, d_model: int = 256, n_layers: int = 6, n_heads: int = 4, vocab_size: int = 320):
        super().__init__()
        self.feature_extractor = nn.Sequential(
            nn.Conv1d(1, 256, 5, stride=2, padding=2), nn.GroupNorm(8, 256), nn.ReLU(),
            nn.Conv1d(256, 256, 5, stride=2, padding=2), nn.GroupNorm(8, 256), nn.ReLU(),
            nn.Conv1d(256, d_model, 5, stride=2, padding=2), nn.GroupNorm(8, d_model), nn.ReLU(),
        )
        self.encoder = TransformerEncoder(d_model, n_layers, n_heads)
        self.proj = nn.Linear(d_model, vocab_size)

    def masked_unit_loss(self, logits: torch.Tensor, targets: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        """Cross-entropy on masked frames (Phase 3).

        logits: [B, T, V] (encoder latents projected); targets: [B, T] cluster IDs; mask: [B, T] bool.
        """
        logits_m = logits[mask]  # [N, V]
        targets_m = targets[mask]  # [N]
        return torch.nn.functional.cross_entropy(logits_m, targets_m)


if __name__ == "__main__":  # pragma: no cover
    torch.manual_seed(0)
    m = Hubert()
    x = m.feature_extractor(torch.randn(2, 16000)).transpose(1, 2)
    print("feats:", x.shape, "enc:", m.encoder(x).shape)
