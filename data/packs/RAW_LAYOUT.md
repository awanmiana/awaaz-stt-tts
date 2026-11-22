# Voice Pack Raw Layout (Phase 1)

## Directory tree

```
data/packs/
  raw/<voice-id>/
    <file-id>.wav              # utterance recordings (16-24kHz, 16-bit PCM)
    ...
  manifests/<voice-id>.jsonl   # per-voice manifest (shared/manifest.py schema)
  enrollment/<voice-id>/*.wav  # enrollment clips (Phases 5/7; separate from main recording)
  style_prompts/<voice-id>/<style>.jsonl  # style variants used per voice (Phase 6)
```

## File naming

`<voice-id>-<seq>-<style>.wav` (e.g., `spk-01-0001-warm.wav`) or `<utterance_id>.wav`.

## Metadata CSV (per voice): `data/packs/<voice-id>_metadata.csv`

```
audio_path,text,speaker_id,style,domain
raw/spk-01/spk-01-0001.wav,یہ جملہ ہے,spk-01,warm,everyday
```

Manifest creation (per voice):

```
python -m data.scripts.make_manifest --root data/packs/raw/spk-01 --out data/packs/manifests/spk-01.jsonl --metadata data/packs/spk-01_metadata.csv
```

## QC

- `python -m data.scripts.audio_qc --dir data/packs/raw/spk-01 --out data/packs/qc_spk-01.csv` (duration/SNR/hash)
- `python -m data.scripts.qc_sample --manifest data/packs/manifests/spk-01.jsonl --n 100 --out data/packs/qc_spk-01_sample.csv`

## Notes

- 16-bit PCM, 16kHz minimum (24kHz preferred); mono.
- Consent: `data/packs/CONSENT_TEMPLATE.md` (signed before recording); registry: `data/packs/speakers_registry.csv`.
- Targets/gates: `docs/phase1_goals.md`.
