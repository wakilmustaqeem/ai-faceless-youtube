#!/usr/bin/env python3
"""Build a short free/local teleport prototype from approved stills.

No AI API, paid service, or model download is used.
"""

from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "assets/video/teleport"
OUT = ROOT / "artifacts/video/teleport-prototype-v1.mp4"

INPUTS = [
    ASSET / "presenter_departure.png",
    ASSET / "destination_2027.png",
    ASSET / "presenter_arrival.png",
]


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> int:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print("BLOCKED: ffmpeg is not installed.")
        return 2

    missing = [str(p) for p in INPUTS if not p.exists()]
    if missing:
        print("BLOCKED: approved teleport references are missing:")
        print("\n".join(missing))
        return 3

    OUT.parent.mkdir(parents=True, exist_ok=True)
    filters = (
        "[0:v]scale=720:1280:force_original_aspect_ratio=decrease,"
        "pad=720:1280:(ow-iw)/2:(oh-ih)/2,zoompan=z='min(zoom+0.0008,1.04)':"
        "d=17:s=720x1280:fps=24,fade=t=in:st=0:d=0.15,fade=t=out:st=0.55:d=0.15[a];"
        "[1:v]scale=720:1280:force_original_aspect_ratio=decrease,"
        "pad=720:1280:(ow-iw)/2:(oh-ih)/2,zoompan=z='min(zoom+0.0005,1.02)':"
        "d=12:s=720x1280:fps=24,fade=t=in:st=0:d=0.12,fade=t=out:st=0.28:d=0.12[b];"
        "[2:v]scale=720:1280:force_original_aspect_ratio=decrease,"
        "pad=720:1280:(ow-iw)/2:(oh-ih)/2,zoompan=z='min(zoom+0.0008,1.04)':"
        "d=17:s=720x1280:fps=24,fade=t=in:st=0:d=0.15,fade=t=out:st=0.55:d=0.15[c];"
        "[a][b][c]concat=n=3:v=1:a=0,format=yuv420p[v]"
    )
    run([
        ffmpeg, "-y",
        "-loop", "1", "-t", "0.708", "-i", str(INPUTS[0]),
        "-loop", "1", "-t", "0.500", "-i", str(INPUTS[1]),
        "-loop", "1", "-t", "0.708", "-i", str(INPUTS[2]),
        "-filter_complex", filters,
        "-map", "[v]",
        "-r", "24",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "20",
        "-movflags", "+faststart",
        str(OUT),
    ])
    print(f"CREATED: {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
