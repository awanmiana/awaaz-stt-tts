"""Residual Vector Quantization (RVQ) for TTS codec (Phase 0 skeleton; filled in Phase 5).

Design: n_codebooks x codebook_size, learned codebooks, commitment loss.
From scratch: losses = MSE reconstruction + commitment (straight-through where used).
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class ResidualVectorQuantizer(nn.Module):
    def __init__(self, latent_dim: int = 64, n_codebooks: int = 8, codebook_size: int = 1024):
        super().__init__()
        self.latent_dim = latent_dim
        self.n_codebooks = n_codebooks
        self.codebook_size = codebook_size
        self.codebooks = nn.ParameterList(
            [nn.Parameter(torch.randn(codebook_size, latent_dim) * 0.02) for _ in range(n_codebooks)]
        )

    def _nearest(self, z: torch.Tensor, cb: torch.Tensor) -> torch.Tensor:
        # z: [B, T, D]; cb: [S, D] -> idx: [B, T]
        d = torch.cdist(z, cb.unsqueeze(0).expand(z.shape[0], -1, -1))
        return d.argmin(dim=-1)

    def encode(self, z: torch.Tensor) -> torch.Tensor:
        # z: [B, D, T] -> ids: [B, K, T]
        zt = z.transpose(1, 2)
        B, T, D = zt.shape
        ids = []
        residual = zt
        for cb in self.codebooks:
            idx = self._nearest(residual, cb)  # [B, T]
            zq = cb[idx]  # [B, T, D]
            residual = residual - zq
            ids.append(idx)
        return torch.stack(ids, dim=1)

    def decode(self, ids: torch.Tensor) -> torch.Tensor:
        # ids: [B, K, T] -> z: [B, D, T]
        out = torch.zeros(ids.shape[0], ids.shape[2], self.latent_dim, device=ids.device)
        for k in range(self.n_codebooks):
            out = out + self.codebooks[k][ids[:, k]]
        return out.transpose(1, 2)

    def losses(self, z: torch.Tensor, z_hat: torch.Tensor) -> dict[str, torch.Tensor]:
        # commitment loss on codebook residuals (filled with exact form in Phase 5)
        return {"recon": F.mse_loss(z, z_hat), "commitment": torch.zeros(1, device=z.device)}


if __name__ == "__main__":  # pragma: no cover
    torch.manual_seed(0)
    vq = ResidualVectorQuantizer()
    z = torch.randn(2, 64, 10)
    ids = vq.encode(z)
    z_hat = vq.decode(ids)
    print("ids:", ids.shape, "recon:", F.mse_loss(z, z_hat).item())
