#!/usr/bin/env python3
"""Verify the local teleport prototype when a rendered MP4 exists."""

from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
VIDEO = ROOT / "artifacts/video/teleport-prototype-v1.mp4"


def main() -> int:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        print("BLOCKED: ffprobe is not installed.")
        return 2
    if not VIDEO.exists():
        print(f"BLOCKED: rendered prototype not found: {VIDEO}")
        print("Run scripts/build_teleport_prototype.py after approved references are installed.")
        return 3

    cmd = [
        ffprobe, "-v", "error",
        "-show_entries",
        "format=duration:stream=codec_name,width,height,r_frame_rate",
        "-of", "default=noprint_wrappers=1",
        str(VIDEO),
    ]
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode:
        print(result.stderr.strip())
        return result.returncode

    print("PROTOTYPE MEDIA INSPECTION")
    print(result.stdout.strip())
    print("VERIFY visually before marking PASS.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
