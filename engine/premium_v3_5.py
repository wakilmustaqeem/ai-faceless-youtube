"""V3.5 quality-first renderer for Test Video #1."""
from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw
from engine.styles.premium_v2 import W,H,_font,cinematic_background
from engine.styles.premium_v3_5 import desk,shift,architecture,code_demo,feedback,evidence,judgment,takeaway

FPS=24
DURATION=60

def render_frame(t: float, frame_index: int) -> Image.Image:
    im=cinematic_background(t,seed=31)
    if t<5: desk(im,t)
    elif t<12: shift(im,t-5)
    elif t<22: architecture(im,t-12)
    elif t<32: code_demo(im,t-22)
    elif t<41: feedback(im,t-32)
    elif t<49: evidence(im,t-41)
    elif t<56: judgment(im,t-49)
    else: takeaway(im,t-56)
    d=ImageDraw.Draw(im)
    d.text((76,46),"AI & IT / FUTURE TECH",font=_font(18,True),fill=(145,162,177,255))
    d.text((W-250,46),f"V3.5 • {frame_index:04d}",font=_font(18,True),fill=(145,162,177,255))
    return im

def render_frames(out_dir: str, fps: int=FPS, duration: int=DURATION):
    out=Path(out_dir); out.mkdir(parents=True,exist_ok=True)
    for i in range(fps*duration):
        render_frame(i/fps,i).convert("RGB").save(out/f"frame_{i:05d}.jpg",quality=94)
