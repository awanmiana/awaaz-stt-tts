# Architecture (Phase 0–2)

## STT (Speech-to-Text)

```
audio (wav/pcm, 16–24kHz)
   │  stt/features/frontend.py — log-mel 80-bin, 25ms/10ms
   ▼
FastConformerEncoder (stt/model/fastconformer.py)
   │  ConvSubsampling 8x → RelPos MHA + depthwise conv module + FFN blocks
   ├─▶ CTC head (logits over STT grapheme vocab, shared/vocab.py, 81)
   └─▶ RNN-T (optional: stt/model/rnnt.py — predictor+joint)
   │  stt/decode/beam.py — greedy CTC decode + beam search + LM fusion (KenLM, Phase 4)
   ▼
transcript (Urdu graphemes), word segments (timestamps), confidence
```

- From scratch: no pretrained weights.
- Size tiers (configs/stt/): small <100M, medium 100–250M, large 250–500M.
- SSL stage (Phase 3): wav2vec2.1/HuBERT on pure-Urdu audio → fine-tune.
- Decoding: beam + external KenLM trained on Urdu text (shared/text_norm.py input).

## TTS (Text-to-Speech)

```
text (Urdu)
   │  shared/g2p/urdu_g2p.py (rule-based v0; trained disambiguator Phase 2) + shared/text_norm.py
   │  → phonemes + prosody priors (durations/pitch from alignment, Phase 5)
   ▼
SpeakerEncoder (tts/speaker_encoder.py — ECAPA-TDNN-class, 192-d, from scratch)
StyleEmbedder (tts/style_embedder.py — tag + continuous style; Phase 5/6)
   │
   ▼
CodecLM (tts/model/codec_lm.py — transformer over speech tokens; text+speaker+style conditioning; Phase 6)
   │
   ▼
ResidualVQ Decoder (tts/codec/quantizer.py) → codec latents (12.5 fps, 8×1024; Phase 5)
   │
   ▼
ConvDecoder (tts/codec/decoder.py — HiFi-Gan-ish; Phase 5) → waveform
```

- Voice enrollment: user uploads consented clip → speaker encoder → cloneable voice (Phases 5/7).
- Streaming: codec-LM generates chunk-by-chunk (Phase 7/8).

## API (Phase 7)

OpenAI-compatible REST: `/v1/audio/transcriptions`, `/v1/audio/speech` (+stream), `/v1/voice/enroll` (api/main.py).

Decisions: [docs/architecture_decisions.md](architecture_decisions.md) (ADR-01..06).
