#!/usr/bin/env python3
"""Local asset library manager + deterministic cinematic motion presets.

Downloads only explicitly supplied direct asset URLs into assets/library/.
Motion presets generate FFmpeg filter fragments for local assets.
Existing files are never overwritten.
"""
from __future__ import annotations
import argparse, hashlib, mimetypes, subprocess
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "assets" / "library"
ALLOWED = {".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov", ".webm"}

MOTIONS = {
    "slow-zoom": "scale=2400:-2,zoompan=z='min(zoom+0.0007,1.12)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30",
    "slow-push": "scale=2400:-2,zoompan=z='min(zoom+0.0010,1.18)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30",
    "pan-left": "scale=2400:-2,zoompan=z='1.08':d=1:x='min(iw-iw/zoom,iw*0.35)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30",
    "pan-right": "scale=2400:-2,zoompan=z='1.08':d=1:x='max(0,iw-iw/zoom-iw*0.35)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30",
    "static": "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
}

def download(url: str, name: str | None):
    LIB.mkdir(parents=True, exist_ok=True)
    req = Request(url, headers={"User-Agent": "FM-Local-Asset-Library/1.0"})
    with urlopen(req, timeout=30) as r:
        data = r.read()
        ctype = (r.headers.get_content_type() or "").lower()
    suffix = Path(name or "").suffix.lower()
    if suffix not in ALLOWED:
        suffix = mimetypes.guess_extension(ctype) or ".bin"
    if suffix not in ALLOWED:
        raise SystemExit(f"REFUSED: unsupported asset type {ctype}")
    digest = hashlib.sha256(data).hexdigest()[:12]
    filename = name or f"asset-{digest}{suffix}"
    path = LIB / Path(filename).name
    if path.exists():
        raise SystemExit(f"REFUSED: {path} already exists")
    path.write_bytes(data)
    print(f"PASS: downloaded asset -> {path}")
    print(f"SHA256: {hashlib.sha256(data).hexdigest()}")

def motion(name: str):
    print(MOTIONS[name])

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Local asset library + motion presets")
    sub = ap.add_subparsers(dest="cmd", required=True)
    dl = sub.add_parser("download")
    dl.add_argument("url", help="Direct public asset URL")
    dl.add_argument("--name")
    mo = sub.add_parser("motion")
    mo.add_argument("preset", choices=sorted(MOTIONS))
    args = ap.parse_args()
    if args.cmd == "download":
        download(args.url, args.name)
    else:
        motion(args.preset)
