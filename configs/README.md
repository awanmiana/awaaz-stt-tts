# Configs index

## STT (`configs/stt/`)

- `small.yaml` — default tier for squeeze-to-perfect (target: <100M params)
- `medium.yaml` — 100–250M
- `large.yaml` — 250–500M

Overrides:

```bash
python -m stt.train --config configs/stt/small.yaml --override stt.d_model=256
```

## TTS (`configs/tts/`)

- `default.yaml` — codec-LM setup (Phase 0; tuned in Phase 2/5/6)

## Per-deployment overrides

Every config is a YAML tree; `--override key=value` (from `shared/config_util.py`) patches it.
