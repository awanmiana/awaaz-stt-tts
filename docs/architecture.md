# High-level architecture (Phase 0 — draft)

## STT (Speech-to-Text)

```
audio (wav/pcm)
   │
   ▼
Frontend (80-bin log-mel, win=25ms, hop=10ms)
   │
   ▼
FastConformerEncoder  (ConvSubsampling 8× + Conformer blocks: rel-pos MHA + conv module + FFN)
   │
   ├─▶ CTC head → log-probs over Urdu phoneme set (CTC auxiliary head)
   └─▶ RNN-T (optional alternative: predictor + joint network)
   │
   ▼
Beam search decode (rel-pos aware, external KenLM fusion at eval)
   │
   ▼
transcript (Urdu graphemes), word segments, confidence
```

Variants:
- Small: d_model=128, n_layers=8 (~<100M params)
- Medium: d_model=256, n_layers=16 (~100–250M)
- Large: d_model=512, n_layers=24 (~250–500M)

Optional SSL stage: wav2vec 2.1 / HuBERT (pure-Urdu audio) → fine-tune above.

## TTS (Text-to-Speech)

```
text (Urdu)
   │
   ▼
Urdu G2P + text norm (shared/)  → phonemes + prosody priors (duration/pitch from alignment)
   │
   ▼
SpeakerEncoder (ECAPA-TDNN-class) ──→ speaker embedding
StyleEmbedder ───────────────────────→ style embedding (emotion/pace/timbre)
   │
   ▼
CodecLM (transformer over speech tokens; text+speaker+style conditioning; streaming)
   │
   ▼
ResidualVQ Decoder → codec latents
   │
   ▼
HiFi-Gan-ish Vocoder → waveform
```

Voice enrollment: upload consent-recorded clip → speaker encoder → cloneable voice.

## API (Phase 7)

OpenAI-compatible REST: `/v1/audio/transcriptions`, `/v1/audio/speech` (+ streaming variants, `/v1/voice/enroll`, health/config endpoints). SaaS multi-tenant with quotas, caching, consent APIs.
