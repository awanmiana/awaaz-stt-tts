"""k-means cluster targets for HuBERT (Phase 3).

Pipeline: dump SSL latents -> cluster (MiniBatchKMeans) -> unit IDs per frame.
- `cluster_features(latents)` — offline clustering utility.
"""

from __future__ import annotations

import numpy as np
from sklearn.cluster import MiniBatchKMeans


def cluster_features(latents: np.ndarray, n_clusters: int = 320, seed: int = 42) -> np.ndarray:
    """Cluster SSL latents (2D array [N, D]) -> cluster IDs (1D, [N]).

    latents: [num_frames, latent_dim] float array (e.g., from SSL model dump).
    """
    latents = np.asarray(latents, dtype=np.float32)
    if latents.ndim != 2:
        raise ValueError(f"latents must be 2D [N, D], got {latents.shape}")
    km = MiniBatchKMeans(n_clusters=n_clusters, random_state=seed, batch_size=4096, max_iter=10)
    return km.fit_predict(latents).astype(np.int32)


if __name__ == "__main__":  # pragma: no cover
    rng = np.random.default_rng(0)
    ids = cluster_features(rng.random((1000, 128)))
    print("ids:", ids.shape, ids.min(), ids.max())
