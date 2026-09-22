#!/usr/bin/env python3
"""Render the new vertical cinematic Chinese-short-video style presenter production.

This is intentionally separate from scripts/prepare_content.py and its legacy
30-second slide test. It never overwrites an existing artifact.
"""
from __future__ import annotations
import argparse, shutil, subprocess
from pathlib import Path

W, H, FPS = 1080, 1920, 30
DURATION = 30

def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def need(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"Required binary missing: {name}")

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--presenter", required=True)
    ap.add_argument("--lcd", required=True)
    ap.add_argument("--background", required=True)
    ap.add_argument("--voice", required=True)
    ap.add_argument("--output", default="output/cinematic-short-v1/video.mp4")
    a = ap.parse_args()

    for name in ("ffmpeg", "ffprobe"):
        need(name)
    presenter, lcd, bg, voice, out = map(Path, (a.presenter, a.lcd, a.background, a.voice, a.output))
    for p in (presenter, lcd, bg, voice):
        if not p.is_file():
            raise SystemExit(f"Missing required asset: {p}")
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        raise SystemExit(f"REFUSED to overwrite existing artifact: {out}")

    stage = out.parent / ".cinematic-stage.mp4"
    try:
        # Vertical 9:16 composition: three-sided LCD wall + full-body presenter.
        # The side panels are angled to create a physical three-screen environment.
        filt = (
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,eq=contrast=1.06:saturation=1.05:brightness=-0.03,"
            "setsar=1[bg];"
            "[1:v]scale=700:394:force_original_aspect_ratio=decrease,"
            "pad=700:394:(ow-iw)/2:(oh-ih)/2:color=#02050a,"
            "setsar=1[lcd];"
            "[2:v]scale=560:930:force_original_aspect_ratio=decrease,"
            "format=rgba[p];"
            "[lcd]rotate=0.055:c=none:ow=rotw(0.055):oh=roth(0.055),"
            "scale=360:210[lp];"
            "[lcd]rotate=-0.055:c=none:ow=rotw(-0.055):oh=roth(-0.055),"
            "scale=360:210[rp];"
            "[bg][lcd]overlay=190:180[s1];"
            "[s1][lp]overlay=18:420[s2];"
            "[s2][rp]overlay=702:420[s3];"
            "[s3][p]overlay=260:760:format=auto,setsar=1[v]"
        )
        run([
            "ffmpeg","-y","-loop","1","-i",str(bg),"-loop","1","-i",str(lcd),
            "-loop","1","-i",str(presenter),"-filter_complex",filt,
            "-map","[v]","-t",str(DURATION),"-r",str(FPS),
            "-c:v","libx264","-pix_fmt","yuv420p","-profile:v","high",
            "-movflags","+faststart",str(stage)
        ])
        run([
            "ffmpeg","-y","-i",str(stage),"-i",str(voice),
            "-map","0:v:0","-map","1:a:0","-t",str(DURATION),
            "-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",
            "-ar","48000","-shortest","-movflags","+faststart",str(out)
        ])
        probe = subprocess.run([
            "ffprobe","-v","error","-show_entries",
            "stream=codec_type,codec_name,width,height,pix_fmt",
            "-of","default=noprint_wrappers=1",str(out)
        ], check=True, capture_output=True, text=True)
        required = ("codec_name=h264","codec_name=aac",f"width={W}",f"height={H}","pix_fmt=yuv420p")
        missing = [x for x in required if x not in probe.stdout]
        if missing:
            out.unlink(missing_ok=True)
            raise SystemExit("Cinematic production QA failed: " + ", ".join(missing))
        print(f"PASS: new cinematic short -> {out}")
    finally:
        stage.unlink(missing_ok=True)

if __name__ == "__main__":
    main()
