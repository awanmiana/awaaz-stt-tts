"""shared/manifest tests."""

import tempfile
from pathlib import Path

from shared.manifest import ManifestEntry, load_manifest, save_manifest


def test_roundtrip():
    e = ManifestEntry(audio_path="/a/b.wav", text="ہیلو", speaker_id="spk-01")
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "m.jsonl"
        save_manifest([e], p)
        loaded = load_manifest(p)
    assert loaded[0].text == "ہیلو"
    assert loaded[0].language == "ur"
    assert loaded[0].split == "train"


def test_normalizes_on_entry():
    e = ManifestEntry(audio_path="/a/b.wav", text="۲۰۲۶۔", speaker_id="spk-01")
    assert e.text == "2026"
