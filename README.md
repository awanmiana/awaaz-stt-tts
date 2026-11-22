# awaaz-stt-tts

Professional Urdu-first STT + TTS models built **from scratch** (no pretrained models).

## What this is

Two systems built from zero:

- **STT (Speech-to-Text / ASR)** — Conformer-based encoder + CTC/RNN-T decoder trained on pure-Urdu audio, with optional wav2vec2.1/HuBERT-style self-supervised pretraining.
- **TTS (Text-to-Speech)** — Encodec-style neural codec + codec-LM generative model (CosyVoice-class) + from-scratch speaker encoder + style embedding; voice enrollment for cloned voices.

Style coverage: neutral, warm, energetic, academic, poetic, debate/rhetoric, street vernacular, casual.

## Status & roadmap

See [docs/roadmap.md](docs/roadmap.md). **Current:** Phase 0 (foundation) committed; Phase 1 data collection executing; Phase 2 architecture locked; Phase 3 SSL prep; Phase 4 starts when audits pass.

## Where it lives

- **GitHub** (`awaniana/awaaz-stt-tts`): code, docs, configs, data pipelines.
- **Hugging Face Hub** (`awaniana/awaaz-stt-tts`): model weights (STT/TTS checkpoints) during training; public release as ready.
- TTS voice packs: private (consent-based, see `data/packs/`).

## Layout

```
awaaz-stt-tts/
├── README.md
├── docs/            # architecture, roadmap, tuning, api
├── configs/         # per-model YAML (stt/ + tts/)
├── shared/          # text utils, Urdu G2P, phoneme inventory, manifests
├── data/            # manifests, raw audio (gitignored), collection scripts
├── stt/             # model/, train.py, eval.py, serve/
├── tts/             # codec/, speaker_encoder, model/, train_*.py, eval.py
├── api/             # FastAPI app (OpenAI-compatible + streaming)
├── train/           # launchers (torchrun)
├── eval/            # WER, speaker similarity, benchmark harnesses
└── tests/           # unit tests (pytest)
```

## Install (Phase 0)

```bash
pip install -e .          # installs deps: torch, fastapi, sentencepiece, ...
```

See `requirements.txt` for the full list.

## Quickstart (coming soon: training/serving after Phases 1–7)

```bash
python -m tests.run_tests        # phase-0 sanity checks
```

## Working agreement

- Pure Urdu data. No Hindi for training (benchmark references measure against public products).
- From scratch. Model weights start from zero; public datasets/libraries only.
- Squeeze-to-perfect: smallest tier passing the objectives matrix.
