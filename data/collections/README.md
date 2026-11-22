# Data Collections (Phase 1)

Sources for STT corpus + TTS voice packs (pure Urdu, no Hindi).

## 1. Public corpora (STT, licenses reviewed & approved — see Legal)

- **Common Voice (Urdu subset)** — Mozilla Common Voice; license requires written review for commercial SaaS use (check current terms).
- **FLEURS (Urdu)** — CC BY 4.0 (attribution required — track in `docs/attributions.md`).
- **OpenSLR / other public Urdu corpora** — audit license list below:
  - OpenSLR series (check per-corpus licenses)
- **Malach-style corpora if available in Urdu** — check.
- **YouTube news/public-domain narrated audio** — if rights cleared.

Legal review checklist (confirm with team):
- License permits commercial use + derivative models (SaaS revenue).
- Required attributions tracked (`docs/attributions.md`).
- Any anonymization needs.

## 2. Internal campaigns (no public data)

- **STT narration campaign (3–5 months, target ≥2,000 hrs):**
  - Sample: news articles, public-domain literature, Urdu Wikipedia sentences, technical documentation.
  - Recording: professional narration; accents/region coverage (Lahore/Karachi/Islamabad/Rawalpindi etc.); gender balance.
  - Style sets (dev coverage): poetry, debate, academic, street vernacular, everyday + neutral.
  - Throughput target: ~40–60 hrs/month/recorder; hire/assign ~3–4 recorders.
  - Metadata: per-utterance (speaker, domain, style, duration) — CSV format in data/README.md.
- **TTS voice-pack campaigns (3–5 months, 3 pack voices + enrollment):**
  - Voice-by-voice studio recording (≥1.5h each), style variants per VOICES.yaml.
  - Read-aloud prompts: data/dev/prompts/*.jsonl + story excerpts; balanced vowel coverage.
  - Enrollment clips: 10–30s clips per voice.

## 3. Crowdsourced small sets (supplement)

- Annotated utterances (target: +10–20% hours if needed).

## Milestones (Phase 1, 3–5 months)

- M1 (Month 1): public corpora license review + initial public download; consent forms + registry; dev sets scaffolded (data/dev/).
- M2 (Month 2–3): narration campaigns ongoing; style dev sets filled (20 utts/style); QC pass.
- M3 (Month 3–5): ≥2,000 hrs STT (or as gates require); 3 pack voices with ≥1.5h each; TTS style eval prompts ready.
- Exit: Phase 1 gates (docs/phase1_goals.md).
