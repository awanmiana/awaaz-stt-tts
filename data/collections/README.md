# Data Collections (Phase 1)

Sources for STT corpus + TTS voice packs (pure Urdu, no Hindi).

## Campaign plans (data/collections/campaigns/)

- [STT Narration Campaign](campaigns/STT_narration_campaign_plan.md) — ≥2,000 hrs corpus.
- [TTS Voice Pack Campaign](campaigns/TTS_voice_pack_campaign_plan.md) — 3 pack voices.
- [Recording Contracts](campaigns/RECORDING_CONTRACTS.md) — legal templates.
- [Staffing Plan](campaigns/STAFFING.md) — hires, equipment, throughput.
- [Coverage Matrix](campaigns/COVERAGE_MATRIX.md) — style/domain targets.

## 1. Public corpora (STT, licenses reviewed & approved — see Legal)

- **Common Voice (Urdu subset)** — Mozilla Common Voice; license requires written review for commercial SaaS use (check current terms).
- **FLEURS (Urdu)** — CC BY 4.0 (attribution required — track in `docs/attributions.md`).
- **OpenSLR / other public Urdu corpora** — audit license list: OpenSLR series (check per-corpus licenses).
- **Malach-style corpora if available in Urdu** — check.
- **YouTube news/public-domain narrated audio** — if rights cleared.

Legal review checklist (confirm with team):
- License permits commercial use + derivative models (SaaS revenue).
- Required attributions tracked (`docs/attributions.md`).
- Any anonymization needs.

## 2. Internal campaigns (no public data)

See [campaigns/](campaigns/).

## 3. Crowdsourced small sets (supplement)

- Annotated utterances (target: +10–20% hours if needed).

## Milestones (Phase 1, 3–5 months)

- M1 (Month 1): public corpora license review + initial public download; consent forms + registry; dev sets scaffolded (data/dev/).
- M2 (Month 2–3): narration campaigns ongoing; style dev sets filled (20 utts/style); QC pass.
- M3 (Month 3–5): ≥2,000 hrs STT (or as gates require); 3 pack voices with ≥1.5h each; TTS style eval prompts ready.
- Exit: Phase 1 gates (docs/phase1_goals.md).
