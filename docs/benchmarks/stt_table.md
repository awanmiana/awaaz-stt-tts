# STT benchmark table (Phase 4 — fill after training)

Per-style dev sets: `data/dev/dev_<style>.jsonl`.

## Objective tier: Small (<100M params)

Gate (roadmap): whisper-large-v3 WER + margin.

| Tier | Poetry | Debate | Academic | Street | Everyday | Neutral |
|---|---|---|---|---|---|---|
| Our STT (small) | | | | | | |
| whisper-large-v3 | | | | | | |
| Google Gemini Live | | | | | | |
| OpenAI Whisper API | | | | | | |
| Microsoft Azure STT | | | | | | |
| Meta SeamlessM4T v2 | | | | | | |

## Notes

- WER = word error rate on normalized Urdu text (`eval/wer.py`).
- "Big-five refs" = Google (Gemini Live), OpenAI (ChatGPT/Whisper), Microsoft (Azure), Meta (SeamlessM4T v2) + whisper-large-v3.
- Fill in per roadmap objectives (docs/roadmap.md §Objectives matrix) after Phase 4 training + benchmark runs.
