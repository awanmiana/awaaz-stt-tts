# TTS benchmark table (Phase 6 — fill after training)

Automated gates (roadmap objectives):

| Metric | Objective |
|---|---|
| UTMOS (our proxy model) | ≥ top-open tier (CosyVoice-2/NaturalSpeech-3-class) |
| Speaker similarity (cosine, our speaker encoder) | ≥ 0.85 for pack voices |
| Style classifier accuracy | ≥ 85% (style_embedder.StyleClassifier, trained Phase 6) |
| Speed control | t ≈ requested within ±10% |

## Per-voice metrics

| Voice | UTMOS | Sim | Style-acc | Notes |
|---|---|---|---|---|
| spk-01 | | | | |
| spk-02 | | | | |
| spk-03 | | | | |

## Human (MOS, listening trials) — per tier per style (10 prompts each)

| Tier | MOS (poetry) | MOS (debate) | MOS (academic) | MOS (street) | MOS (everyday) |
|---|---|---|---|---|---|
| Small (<100M) | | | | | |
| Medium (100–250M) | | | | | |
| Large (250–500M) | | | | | |

Notes:
- MOS scale 1–5 (Likert). Human trials organized after Phase 6 (see docs/benchmarks/README.md).
- Style eval: listen, classify (poetry/debate/academic/street/everyday), accuracy target ≥85% per tier/style.
- Fill in; decide final model size per squeeze-to-perfect (docs/phase1_goals.md, roadmap §Size tiers).
