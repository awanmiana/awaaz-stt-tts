"""Tiny YAML + override config utility (Phase 0).

Avoids PyYAML hard dependency for config parsing? — Actually we DO use PyYAML
(in requirements.txt). This wrapper adds dot-path overrides and CLI parsing.
"""

from __future__ import annotations

from typing import Any

import yaml

from shared.text_norm import normalize_transcript  # noqa: F401  (re-export convenience)


def load_yaml(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def parse_scalar(s: str) -> Any:
    s = s.strip()
    if s in ("", '""'):
        return ""
    if s == "null":
        return None
    if s.startswith("[") and s.endswith("]"):
        return [parse_scalar(x) for x in s[1:-1].split(",")]
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    if s.lower() in ("true", "false"):
        return s.lower() == "true"
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s


def set_path(cfg: dict[str, Any], dotted: str, value: Any) -> None:
    keys = dotted.split(".")
    cur = cfg
    for k in keys[:-1]:
        if k not in cur or not isinstance(cur[k], dict):
            cur[k] = {}
        cur = cur[k]
    cur[keys[-1]] = value


def apply_overrides(cfg: dict[str, Any], overrides: list[str]) -> dict[str, Any]:
    for ov in overrides or []:
        if "=" not in ov:
            continue
        key, val = ov.split("=", 1)
        set_path(cfg, key, parse_scalar(val))
    return cfg


def parse_args_overrides(overrides: list[str]) -> list[str]:
    return overrides or []


def load_config(path: str, overrides: list[str] | None = None) -> dict[str, Any]:
    cfg = load_yaml(path)
    return apply_overrides(cfg, overrides or [])


if __name__ == "__main__":  # pragma: no cover
    import sys

    print(load_config(sys.argv[1]) if len(sys.argv) > 1 else "usage: python config_util.py <yaml>")
