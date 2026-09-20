"""Build Premium Tech Style v3 private review MP4 with voice + procedural music.
No upload or public publishing action exists in this script.
"""
from __future__ import annotations
import subprocess
from pathlib import Path
from engine.premium_v3 import render_frames, FPS, DURATION

ROOT = Path(__file__).resolve().parents[1]
FRAMES = ROOT / "output" / "premium_v3_frames"
OUT = ROOT / "output" / "review" / "test1_v3.mp4"
VOICE = ROOT / "output" / "review" / "test1_v3_voice.mp3"
MUSIC = ROOT / "output" / "review" / "test1_v3_music.wav"

render_frames(str(FRAMES), FPS, DURATION)
OUT.parent.mkdir(parents=True, exist_ok=True)

subprocess.run(["python", "scripts/generate_voice_v3.py"], cwd=ROOT, check=True)
subprocess.run(["python", "scripts/generate_music_v3.py"], cwd=ROOT, check=True)

subprocess.run([
    "ffmpeg", "-y",
    "-framerate", str(FPS), "-i", str(FRAMES / "frame_%05d.jpg"),
    "-i", str(VOICE), "-i", str(MUSIC),
    "-filter_complex",
    "[1:a]atrim=0:60,asetpts=N/SR/TB,volume=1.0[voice];"
    "[2:a]atrim=0:60,asetpts=N/SR/TB,volume=0.07[music];"
    "[voice][music]amix=inputs=2:duration=longest:dropout_transition=2,"
    "loudnorm=I=-16:TP=-1.5:LRA=11[a]",
    "-map", "0:v", "-map", "[a]",
    "-t", str(DURATION),
    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
    "-movflags", "+faststart", str(OUT)
], cwd=ROOT, check=True)
print(f"PRIVATE V3 REVIEW READY: {OUT}")
