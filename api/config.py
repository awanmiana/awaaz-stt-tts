"""App config loader (Phase 0; richer on-disk overrides in Phase 7)."""

from __future__ import annotations

from typing import Any

from shared.config_util import load_config

CONFIG: dict[str, Any] = load_config("configs/tts/default.yaml")
