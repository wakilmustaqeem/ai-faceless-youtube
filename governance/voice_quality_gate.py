"""Measurable audio QA gate for generated narration."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


def check_voice(path: str, *, min_duration: float = 1.0, max_silence_ratio: float = 0.65, max_peak_db: float = -0.1) -> dict:
    audio = Path(path)
    if not audio.exists() or audio.stat().st_size == 0:
        return {"passed": False, "reason": "audio_missing_or_empty"}

    try:
        duration_probe = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(audio),
            ],
            check=True, capture_output=True, text=True,
        )
        duration = float(duration_probe.stdout.strip())

        analysis = subprocess.run(
            [
                "ffmpeg", "-hide_banner", "-i", str(audio),
                "-af", "silencedetect=noise=-45dB:d=0.25,volumedetect",
                "-f", "null", "-",
            ],
            check=False, capture_output=True, text=True,
        )
        stderr = analysis.stderr
        if analysis.returncode != 0:
            return {"passed": False, "reason": "audio_analysis_failed"}

        silence_duration = sum(float(value) for value in re.findall(r"silence_duration: ([0-9.]+)", stderr))
        peak_match = re.search(r"max_volume:\s*([+-]?[0-9.]+) dB", stderr)
        peak_db = float(peak_match.group(1)) if peak_match else None
        silence_ratio = silence_duration / duration if duration > 0 else 1.0

        if duration < min_duration:
            return {"passed": False, "reason": "audio_too_short", "duration_seconds": duration}
        if silence_ratio > max_silence_ratio:
            return {"passed": False, "reason": "excessive_silence", "silence_ratio": silence_ratio}
        if peak_db is not None and peak_db > max_peak_db:
            return {"passed": False, "reason": "possible_clipping", "peak_db": peak_db}

        return {
            "passed": True,
            "reason": "voice_quality_passed",
            "duration_seconds": duration,
            "silence_ratio": silence_ratio,
            "peak_db": peak_db,
        }
    except (OSError, ValueError):
        return {"passed": False, "reason": "audio_probe_failed"}
