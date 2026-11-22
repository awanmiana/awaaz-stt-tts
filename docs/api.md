# API spec — Phase 7 target

## Auth

- API key via `Authorization: Bearer <key>` header.
- Multi-tenant (org/user); per-tier rate limits.
- Telemetry of usage per voice/style (privacy opt-in).

## Endpoints (public shapes)

| Method | Path | Description |
|---|---|---|
| POST | `/v1/audio/transcriptions` | Upload audio → `{text, segments, language, duration}`; params: `language`, `timestamps` (word segments), decoding knobs |
| POST | `/v1/audio/speech` | `{model, voice, input, speed, pitch, style, format}` → audio bytes; `?stream=true` → chunked PCM |
| POST | `/v1/voice/enroll` | Upload consent clip → `{voice_id, embedding_hash}` |
| GET | `/v1/voices` | List pack voices + enrolled voices |
| GET | `/v1/models` | List model versions (STT + TTS) |
| GET | `/v1/version` | Version info |

## Error codes

- `400` malformed requests, `401` bad key, `429` rate limited, `503` models not loaded, `500` internal.

## Examples (to fill in Phase 7)

```
curl -X POST -F file=@utterance.wav http://localhost:8000/v1/audio/transcriptions
curl -X POST -H 'Content-Type: application/json' \
     -d '{"model":"tts-v1.0","voice":"spk-01","input":"سلام دنیا","speed":1.0}' \
     http://localhost:8000/v1/audio/speech -o out.wav
```
