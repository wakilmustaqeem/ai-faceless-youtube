#!/usr/bin/env python3
"""Optional ElevenLabs TTS adapter with safe local fallback.

ElevenLabs is opt-in through ELEVENLABS_API_KEY. No key is stored in the repo.
If no key is configured, callers can use the existing Edge-TTS adapter instead.
"""
from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.elevenlabs.io/v1/text-to-speech"
DEFAULT_VOICE = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
DEFAULT_MODEL = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")


def synthesize(text: str, output_path: str, voice_id: str = DEFAULT_VOICE,
               model_id: str = DEFAULT_MODEL) -> None:
    key = os.getenv("ELEVENLABS_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "ELEVENLABS_API_KEY is not configured. "
            "Use Edge-TTS or configure the ElevenLabs key as an environment secret."
        )
    text = text.strip()
    if not text:
        raise ValueError("Narration text is empty.")

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite existing audio: {output}")

    url = f"{API}/{voice_id}?output_format=mp3_44100_128"
    payload = json.dumps({
        "text": text,
        "model_id": model_id,
    }).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "xi-api-key": key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            data = response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:1200]
        raise RuntimeError(f"ElevenLabs HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"ElevenLabs network error: {exc}") from exc

    if not data:
        raise RuntimeError("ElevenLabs returned an empty audio response.")
    output.write_bytes(data)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--voice-id", default=DEFAULT_VOICE)
    parser.add_argument("--model-id", default=DEFAULT_MODEL)
    args = parser.parse_args()
    synthesize(args.text, args.output, args.voice_id, args.model_id)
