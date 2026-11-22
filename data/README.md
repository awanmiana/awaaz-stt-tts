# Data (Phase 0–1)

Raw audio, manifests, collection plans, and TTS voice packs.

```
data/
  raw/                   # gitignored: raw audio (WAV/MP3/FLAC/PCM/Ogg)
    <speaker-id>/        # e.g., spk-01/
      utterances/
        <utterance-id>.wav
  packs/                 # TTS voice packs (Phase 1) — consent-signed
    README.md, VOICES.yaml, CONSENT_TEMPLATE.md, speakers_registry.csv
    raw/<voice-id>/<file>.wav
    manifests/<voice-id>.jsonl
    style_prompts/<voice-id>/<style>.jsonl
  dev/                   # dev sets (Phase 1)
    README.md, prompts/*.jsonl, dev_<style>.jsonl
  manifests/             # gitignored except curated samples
  collections/           # campaign plans (Phase 1)
  scripts/               # data pipeline CLIs
```

## Manifest entry schema (`shared/manifest.py`)

| field | type | notes |
|---|---|---|
| `audio_path` | str | absolute or root-relative |
| `text` | str | transcript (Urdu) — normalized on entry |
| `speaker_id` | str | e.g., `spk-01` |
| `language` | str | default `ur` |
| `domain` | str? | news / academic / poetry / debate / street / everyday / ... |
| `style` | str? | neutral / warm / energetic / academic / poetic / debate / street / casual |
| `duration_s` | float? | filled by `make_manifest` |
| `sample_rate` | int? | filled by `make_manifest` |
| `split` | str | train/dev/test |

## Pipeline (Phase 1)

1. Collect raw audio into `data/raw/` + metadata CSV (`audio_path,text,speaker_id,domain,style`)
   — or into `data/packs/` for voice packs (consent signed).
2. Normalize: `python -m data.scripts.normalize_transcripts --manifest data/manifests/train.jsonl`
3. Align text↔audio with MFA: `python -m data.scripts.forced_align ...` (filled Phase 5).
4. Split: `python -m data.scripts.split_manifest --manifest data/manifests/train.jsonl --out-prefix corpus`
5. QC: `python -m data.scripts.qc_sample --manifest data/manifests/train.jsonl --n 200 --out data/qc_sample.csv`

See [docs/phase1_goals.md](../docs/phase1_goals.md) (Phase 1 targets & gates) and
[collections/README.md](collections/README.md) (campaign plan).
