"""FastAPI app — Phase 0 skeleton; endpoints wired in Phase 7.

OpenAI-compatible endpoints (public API shapes):
- POST /v1/audio/transcriptions — audio upload -> {text, segments, language, ...}
- POST /v1/audio/speech — text -> audio bytes (?stream=true -> chunked PCM)

Custom/extended endpoints (Phase 7/8):
- POST /v1/voice/enroll — consent-recorded voice → speaker embedding
- GET  /v1/voices — pack voices + enrolled voices

Platform endpoints:
- GET /healthz, GET /v1/models, GET /config
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from pydantic import BaseModel

from api.config import CONFIG

app = FastAPI(title="awaaz-stt-tts", version="0.1.0")

TTS_CFG = CONFIG.get("tts", {})


def _tts_version() -> str:
    return str(TTS_CFG.get("version", "tts-v0.1"))


@app.get("/healthz")
def healthz() -> dict[str, Any]:
    return {"status": "ok", "version": _tts_version()}


@app.get("/v1/models")
def list_models() -> dict[str, Any]:
    return {"models": [{"kind": "tts", "version": _tts_version()}], "config": CONFIG}


@app.get("/config")
def get_config() -> dict[str, Any]:
    return {"config": CONFIG}


@app.get("/v1/voices")
def list_voices() -> dict[str, Any]:
    return {"voices": TTS_CFG.get("speakers", [])}


class SpeechRequest(BaseModel):
    model: str | None = None
    voice: str | None = None
    input: str
    speed: float = 1.0
    pitch: float | None = None
    style: str | None = None
    language: str = "ur"
    format: str = "wav"
    stream: bool = False


class EnrollRequest(BaseModel):
    voice_id: str
    style: str | None = None
    language: str = "ur"


@app.post("/v1/audio/transcriptions")
async def transcriptions(
    file: UploadFile = File(None),
    language: str = "ur",
    timestamps: bool = False,
) -> dict[str, Any]:
    # Phase 7: STT inference on audio upload -> {text, segments, ...}
    raise HTTPException(
        status_code=503,
        detail="STT inference starts Phase 2–4; endpoint wired in Phase 7.",
    )


@app.post("/v1/audio/speech")
def speech(req: SpeechRequest, stream: bool = Query(False)) -> Any:
    # Phase 7: TTS inference -> wav bytes (or chunked PCM if stream=true)
    raise HTTPException(
        status_code=503,
        detail="TTS inference starts Phase 6; endpoint wired in Phase 7.",
    )


@app.post("/v1/voice/enroll")
def voice_enroll(req: EnrollRequest) -> dict[str, Any]:
    # Phase 7/8: consent-recorded upload -> speaker embedding (enrollment flow)
    raise HTTPException(status_code=503, detail="Voice enrollment starts Phase 7.")


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
