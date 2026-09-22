#!/usr/bin/env python3
"""Unified local production launcher.

Creates graphics, generates narration with the existing Edge-TTS module, then
assembles the presenter/LCD/background with FFmpeg. Existing outputs are never
overwritten. Publishing is deliberately outside this tool.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from scripts.generate_voice import synthesize
from scripts.cinematic_asset_builder import lcd as make_lcd, room as make_room
from scripts.local_presenter_pipeline import main as render_cli

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--script",required=True,help="Narration text")
    p.add_argument("--presenter",required=True)
    p.add_argument("--output",required=True)
    p.add_argument("--lcd",default=str(ROOT/"assets"/"library"/"letust-gadget-auto.png"))
    p.add_argument("--background",default=str(ROOT/"assets"/"library"/"cinematic-room-auto.png"))
    p.add_argument("--motion",choices=["static","slow-zoom","slow-push","pan-left","pan-right"],default="slow-push")
    p.add_argument("--voice",default=None)
    args=p.parse_args()

    for x in (args.output,args.lcd,args.background):
        if Path(x).exists():
            raise SystemExit(f"REFUSED: output already exists: {x}")

    Path(args.lcd).parent.mkdir(parents=True,exist_ok=True)
    Path(args.background).parent.mkdir(parents=True,exist_ok=True)
    make_lcd(Path(args.lcd))
    make_room(Path(args.background))

    voice=Path(args.output).with_suffix(".mp3")
    if voice.exists():
        raise SystemExit(f"REFUSED: voice already exists: {voice}")
    synthesize(args.script,str(voice),args.voice) if args.voice else synthesize(args.script,str(voice))

    # Reuse the tested CLI without duplicating FFmpeg logic.
    sys.argv=[
        "local_presenter_pipeline.py",
        "--presenter",args.presenter,
        "--voice",str(voice),
        "--lcd",args.lcd,
        "--background",args.background,
        "--motion",args.motion,
        "--output",args.output,
    ]
    render_cli()
    print("PASS: unified local production completed")
    
if __name__=="__main__":
    main()
