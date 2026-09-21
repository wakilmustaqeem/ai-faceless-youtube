""""Measurable visual QA gate for generated video."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


BLACK_PIXEL_THRESHOLD = 0.05


def check_video(path: str, *, max_black_seconds: float = 0.75, max_freeze_seconds: float = 1.5) -> dict:
    video = Path(path)
    if not video.exists() or video.stat().st_size == 0:
        return {"passed": False, "reason": "video_missing_or_empty"}
    try:
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,pix_fmt",
             "-of", "default=noprint_wrappers=1", str(video)],
            check=True, capture_output=True, text=True,
        )
        if "codec_type=video" not in probe.stdout:
            return {"passed": False, "reason": "video_stream_missing"}
        analysis = subprocess.run(
            ["ffmpeg", "-hide_banner", "-i", str(video),
             "-vf", f"blackdetect=d=0.25:pix_th={BLACK_PIXEL_THRESHOLD},freezedetect=n=-60dB:d=0.5",
             "-an", "-f", "null", "-"],
            check=False, capture_output=True, text=True,
        )
        if analysis.returncode != 0:
            return {"passed": False, "reason": "visual_analysis_failed"}
        stderr = analysis.stderr
        black = max((float(x) for x in re.findall(r"black_duration:([0-9.]+)", stderr)), default=0.0)
        freeze = max((float(x) for x in re.findall(r"freeze_duration:([0-9.]+)", stderr)), default=0.0)
        if black > max_black_seconds:
            return {"passed": False, "reason": "extended_black_frame", "black_seconds": black}
        if freeze > max_freeze_seconds:
            return {"passed": False, "reason": "extended_frozen_frame", "freeze_seconds": freeze}
        return {"passed": True, "reason": "visual_quality_passed", "max_black_seconds": black, "max_freeze_seconds": freeze}
    except (OSError, ValueError):
        return {"passed": False, "reason": "visual_probe_failed"}
"