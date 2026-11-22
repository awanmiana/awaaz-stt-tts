# TTS Voice Packs (Phase 1)

3 pack voices (`spk-01`..`spk-03`) per `configs/tts/default.yaml` — open enrollment for others (Phases 5/7).

## Layout

```
data/packs/
  README.md
  VOICES.yaml                            # pack spec: styles per voice, targets (docs/phase1_goals.md)
  CONSENT_TEMPLATE.md                    # consent form (opt-in, opt-out, disclosure)
  speakers_registry.csv                  # registry template
  raw/<voice-id>/<file>.wav              # recorded audio (16–24kHz, consent-signed)
  manifests/<voice-id>.jsonl             # per-voice manifests
  style_prompts/<voice-id>/<style>.jsonl # style-variant prompts (Phase 6)
```

## Style variants (VOICES.yaml)

From the roadmap styles: warm, neutral, energetic, academic, poetic, debate, street, casual.

## Pipeline

1. Record pack voice audio into `data/packs/raw/<voice-id>/` (prompts: `data/dev/prompts/*.jsonl` + story excerpts).
2. Metadata CSV: `audio_path,text,speaker_id,style,domain`.
3. Manifest: `python -m data.scripts.make_manifest --root data/packs/raw/spk-01 --out data/packs/manifests/spk-01.jsonl --metadata data/packs/spk-01_metadata.csv`
4. Consent: sign `data/packs/CONSENT_TEMPLATE.md`; register in `data/packs/speakers_registry.csv`.
5. Enrollment: short clips (~10–30s) per pack voice for the speaker encoder (Phases 5/7).

## Targets & gates: `docs/phase1_goals.md`.
