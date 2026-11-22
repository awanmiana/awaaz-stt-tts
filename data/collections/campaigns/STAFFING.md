# Staffing Plan (Phase 1)

## Recorders

- Hire 3–4 studio recorders (full-time or contract) with Urdu fluency + regional accents (balanced: Lahore/Karachi/Islamabad).
- Training week: style guide (natural reads, avoid hyper-annunciation), dictation drills.

## Equipment

- Studio-grade mic per recorder; quiet recording room; pop filter; monitoring.
- Capture: 16-bit PCM, 16–24kHz, mono, ~0.5–1.0x real-time for QC.

## Throughput targets

- STT: ~40–60 hrs/month/recorder → 2,000 hrs in 3–4 months (see STT campaign plan).
- TTS: ~2–3 hrs/voice/week → 3 voices in 3–4 months (see TTS campaign plan).

## QC

- QC sample: `python -m data.scripts.qc_sample --manifest data/manifests/train.jsonl --n 200 --out data/qc_sample.csv`
- Audio QC: `python -m data.scripts.audio_qc --dir data/packs/raw/spk-01 --out data/packs/qc_spk-01.csv`
- Rotate QA roles; train recorders on the style guide and style variants (docs/phase1_goals.md, roadmap §Style coverage).
