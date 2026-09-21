"""Build the Premium Tech Style v2 private review MP4.

This script only renders a local artifact. It never uploads or publishes to YouTube.
"""
from __future__ import annotations
import subprocess
from pathlib import Path
from engine.premium_v2 import render_frames, FPS, DURATION

ROOT=Path(__file__).resolve().parents[1]
FRAMES=ROOT/"output"/"premium_v2_frames"
OUT=ROOT/"output"/"review"/"test1_v2.mp4"

render_frames(str(FRAMES),FPS,DURATION)
OUT.parent.mkdir(parents=True,exist_ok=True)
subprocess.run([
 "ffmpeg","-y","-framerate",str(FPS),"-i",str(FRAMES/"frame_%05d.jpg"),
 "-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p",
 "-movflags","+faststart",str(OUT)
],check=True)
print(f"PRIVATE REVIEW READY: {OUT}")
