# awaaz-stt-tts — data directory (Phase 0: skeleton; fill in Phase 1)

```
data/
  raw/                    # gitignored: raw audio (WAV/MP3/FLAC/PCM/Ogg)
    <speaker-id>/         # e.g. spk-01/
      utterances/
        <utterance-id>.wav
      ...
  manifests/              # gitignored except curated samples
    train.jsonl
    dev.jsonl
    test.jsonl
  scripts/                # data pipeline CLIs
```

## Manifest entry schema (`shared/manifest.py`)

| field | type | notes |
|---|---|---|
| `audio_path` | str | absolute or root-relative |
| `text` | str | transcript (Urdu) — normalized on entry |
| `speaker_id` | str | e.g., `spk-01` |
| `language` | str | default `ur` |
| `domain` | str? | news / academic / poetry / debate / street / ... |
| `style` | str? | neutral / warm / energetic / academic / poetic / debate / street / casual |
| `duration_s` | float? | filled by `make_manifest` |
| `sample_rate` | int? | filled by `make_manifest` |
| `split` | str | train/dev/test |

## Pipeline (Phase 1)

1. Collect raw audio into `data/raw/` + metadata CSV (`audio_path,text,speaker_id,domain,style`).
2. `python -m data.scripts.normalize_transcripts --manifest data/manifests/train.jsonl`
3. Align text↔audio with MFA: `python -m data.scripts.forced_align ...` (filled Phase 5).
4. `python -m data.scripts.split_manifest` — create train/dev/test (add script in Phase 1).

## Notes for collection (Phase 1)

- Pure Urdu (no Hindi in training). Consent forms for TTS voice packs (opt-in, revocable).
- Record at 16–24kHz, 16-bit PCM preferred; normalize later via `sox`/`pydub`.
- Style coverage: poetry, debate/argument, academic, street vernacular (measured in dev sets per roadmap).
