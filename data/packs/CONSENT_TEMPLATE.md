# Voice Consent Form (TTS voice packs & enrollment)

**Recording:** We (awaaz-stt-tts) record/obtain the following speech for our Urdu TTS/STT models.

By signing below, the speaker:
- Consents to use of recorded voice samples for TTS voice packs, model training (including voice embeddings for enrollment), and benchmark eval.
- May withdraw at any time via `POST /v1/voice/enroll/{id}/revoke` (Phase 7); deletion of voice within SLA.
- Accepts that generated speech from their voice is disclosed by default (see "Disclosure").

**Disclosure:** Unless the speaker opts out, audio generated from their enrolled/pack voice includes a machine-generated disclosure when requested by the user; usage logs track per-voice stats.

**Storage:** raw audio + manifests kept in private SaaS storage (not public); HF weight releases do not include voice data.

---
Signature: ________________  Date: ___________  Speaker ID: ________
