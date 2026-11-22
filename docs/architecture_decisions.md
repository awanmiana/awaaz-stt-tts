# Architecture Decisions (Phase 0–2) — ADR-style records

From-scratch design decisions, with tradeoffs. Original spec in [architecture.md](architecture.md).

## ADR-01: STT encoder — FastConformer (relative-pos MHA + depthwise conv, 8× subsampling)

**Context:** Need high-quality, streaming-capable ASR encoder for pure Urdu; from scratch.

**Options considered:**
- Full-rate Conformer (no subsampling) — more FLOPs/latency.
- FastConformer (8× subsampling + depthwise conv module) — standard for streaming.
- Mamba-based — less proven for ASR at this stage.
- Whisper-style encoder (conv + full-rate) — doable but no subsampling; open-class reference is whisper-large-v3; we want to lead.

**Decision:** FastConformer (stt/model/fastconformer.py): ConvSubsampling(8x) + ConformerBlocks (MHSA with relative positions + depthwise conv + FFN).

**Why:** Speed + strong open-class behavior; relative positions for variable-length Urdu utterances; streaming-friendly subsampling. Small tier target: d_model=128, n_layers=8 (<100M).

## ADR-02: STT pretraining — wav2vec 2.1/HuBERT on pure-Urdu audio

**Context:** Pure-Urdu speech data may be limited; SSL can boost quality.

**Options considered:**
- Skip SSL, train on labeled data only.
- wav2vec 2.1 (contrastive).
- HuBERT (cluster-target masked LM).

**Decision:** wav2vec 2.1 or HuBERT on all available Urdu audio, then fine-tune STT (Phase 3). Pseudo-label self-training as supplement if data is short (Phase 4).

**Why:** Biggest lever for low-resource Urdu; self-supervised on unlabeled data.

## ADR-03: TTS acoustic — Codec-LM (CosyVoice-class), streaming

**Context:** Need expressive, controllable, streaming-capable TTS (styles: poetry, debate, street...), from scratch.

**Options considered:**
- NaturalSpeech 3 (diffusion over codec latents) — strong quality, high complexity.
- VITS/flow (HiFi-Gan vocoder) — proven, less expressive.
- Codec-LM (GPT-like LM over speech tokens from a trained codec) — streaming-friendly, style-controllable.

**Decision:** Codec-LM (tts/model/codec_lm.py): text + speaker + style → transformer LM → speech tokens → codec → waveform.

**Why:** Streaming support, controllable style, proven at top-open scale (CosyVoice-class); simpler training than diffusion. Alternatives kept open for comparison during Phase 6 evals.

## ADR-04: Codec — Encodec-style RVQ, 8 codebooks × 1024, ~12.5 fps

**Context:** Codec for TTS (Phase 5).

**Options considered:**
- Encodec-style (conv encoder + RVQ + decoder).
- FSQ (finite scalar quantization).
- DAC (descriptive audio codec).

**Decision:** Encodec-style RVQ (tts/codec/*): ConvEncoder → ResidualVQ(8×1024) → ConvDecoder (HiFi-Gan-ish).

**Why:** Well-studied, streaming-friendly, standard codec token rate; 12.5 fps gives good quality/latency tradeoff; documented reconstruction metrics to verify.

## ADR-05: Speaker encoder + style system — ECAPA-TDNN-class + style embedder (from scratch)

**Context:** Voice enrollment + style control (Phase 5/7).

**Decision:** ECAPA-TDNN-class SpeakerEncoder (192-d, from scratch, margin/contrastive training); StyleEmbedder (tag + continuous style; from scratch); StyleClassifier for eval.

**Why:** Standard, compact, robust to short clips; style conditioning needs continuous vectors for expression.

## ADR-06: STT targets — graphemes

**Context:** Needed for eval design.

**Decision:** STT outputs Urdu graphemes (like Whisper targets text). G2P (shared/g2p/urdu_g2p.py, rule-based v0; trained disambiguator Phase 2) is used on the TTS text frontend.

**Why:** Avoids phoneme→grapheme inverse for STT eval; phoneme set used by TTS LM (tts/model/codec_lm.py).

---

All decisions: from-scratch (no pretrained weights); public datasets/libraries as allowed (see data/collections).
