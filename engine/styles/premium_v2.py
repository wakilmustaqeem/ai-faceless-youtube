"""Premium Tech Style v2 primitives.

The renderer is deliberately deterministic: visual state is derived from frame/time,
with no external image dependency. It targets a cinematic 16:9 YouTube master.
"""
from __future__ import annotations
import math
from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1920, 1080
CYAN = (0, 217, 255, 255)
WHITE = (242, 247, 250, 255)
MUTED = (145, 162, 177, 255)
GREEN = (90, 230, 150, 255)
PANEL = (12, 20, 30, 225)

@dataclass(frozen=True)
class Style:
    font: str = "Inter"
    mono: str = "JetBrains Mono"
    accent: tuple = CYAN


def _font(size: int, mono: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf" if mono else "/usr/share/fonts/truetype/inter/Inter-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf" if mono else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in candidates:
        if Path(p).exists(): return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def ease(t: float) -> float:
    t=max(0.0,min(1.0,t)); return t*t*(3-2*t)


def cinematic_background(t: float, seed: int = 7) -> Image.Image:
    # Keep the background expressive but cheap enough for a CI render.
    im=Image.new("RGBA",(W,H),(5,10,17,255))
    haze=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(haze)
    cx=W*(.20+.08*math.sin(t*.18+seed)); cy=H*(.36+.10*math.cos(t*.22))
    d.ellipse((cx-420,cy-420,cx+420,cy+420),fill=(0,217,255,38))
    cx2=W*(.78+.06*math.cos(t*.15)); cy2=H*(.68+.08*math.sin(t*.19))
    d.ellipse((cx2-300,cy2-300,cx2+300,cy2+300),fill=(55,90,255,20))
    haze=haze.filter(ImageFilter.GaussianBlur(95))
    im=Image.alpha_composite(im,haze)
    # Soft diagonal light bands create camera/sweep depth without a flat card.
    sweep=Image.new("RGBA",(W,H),(0,0,0,0)); sd=ImageDraw.Draw(sweep)
    offset=int((t*90)%500)-250
    sd.polygon([(offset,0),(offset+240,0),(offset+1050,H),(offset+810,H)],fill=(0,217,255,8))
    sweep=sweep.filter(ImageFilter.GaussianBlur(24))
    im=Image.alpha_composite(im,sweep)
    # Depth particles.
    p=Image.new("RGBA",(W,H),(0,0,0,0)); pd=ImageDraw.Draw(p)
    for i in range(70):
        x=(i*137 + int(t*18*(i%5+1)))%W
        y=(i*71 + int(t*11*(i%7+1)))%H
        a=18+(i%5)*7; r=1+(i%3)
        pd.ellipse((x-r,y-r,x+r,y+r),fill=(150,210,225,a))
    return Image.alpha_composite(im,p)


def glass_panel(base: Image.Image, box, radius=24, alpha=215, outline=0):
    x1,y1,x2,y2=box
    layer=Image.new("RGBA",base.size,(0,0,0,0)); d=ImageDraw.Draw(layer)
    d.rounded_rectangle(box,radius=radius,fill=(12,20,30,alpha),outline=(*CYAN[:3],outline) if outline else None,width=2)
    layer=layer.filter(ImageFilter.GaussianBlur(.35))
    base.alpha_composite(layer)


def glow_line(base, points, width=3, color=CYAN):
    glow=Image.new("RGBA",base.size,(0,0,0,0)); gd=ImageDraw.Draw(glow)
    gd.line(points,fill=(*color[:3],80),width=width*7,joint="curve")
    glow=glow.filter(ImageFilter.GaussianBlur(12)); base.alpha_composite(glow)
    ImageDraw.Draw(base).line(points,fill=color,width=width,joint="curve")


def text_fit(draw, xy, text, max_width, size, mono=False, fill=WHITE):
    f=_font(size,mono); 
    while draw.textbbox(xy,text,font=f)[2]-xy[0] > max_width and size>18:
        size-=2; f=_font(size,mono)
    draw.text(xy,text,font=f,fill=fill)
    return f
