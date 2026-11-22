# Recording Contracts & Agreements (Phase 1, legal templates)

Define before campaign execution. Involve a lawyer for the SaaS product before execution.

## 1. Terms of Engagement (employer/agency)

- Scope: voice recording sessions for awaaz-stt-tts (Urdu STT/TTS models).
- Deliverables: raw audio (16–24kHz, 16-bit PCM, WAV), metadata CSV (`audio_path,text,speaker_id,style,domain`).
- Rate: agreed before start (hourly rate for studio capture; e.g., per-hour for recorders, per-minute for read-aloud — fill in).
- Timeline: assigned weeks per recorder.

## 2. Voice Consent (per voice pack) — see data/packs/CONSENT_TEMPLATE.md

- Opt-in/opt-out; disclosure by default; usage logs tracked per voice.

## 3. Ownership / Rights

- We (awaaz-stt-tts) obtain full rights to record, store, train models (incl. voice embeddings), publish model weights (HF Hub), and use in SaaS (the "Recorder").
- Recorder grants license to use the output; acknowledges use in training/derivatives/hosting.
- For public corpora: sources must have cleared commercial/derivative rights (see data/collections/README.md).

## 4. Payment & Milestones

- Milestone-based: recorded hours + QC pass per week.

## 5. Confidentiality

- Voice data, agreements, pricing, client list: confidential to awaaz-stt-tts (non-disclosure).
