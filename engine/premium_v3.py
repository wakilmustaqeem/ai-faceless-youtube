"""Premium Tech Style v3 renderer: stronger motion, HUD depth, and visual storytelling."""
from __future__ import annotations
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
from engine.premium_v2 import render_frame as render_v2_frame, FPS, DURATION
from engine.styles.premium_v2 import W, H, CYAN, WHITE, MUTED, GREEN, _font, text_fit

def _hud(im, t):
    d = ImageDraw.Draw(im)
    # fine circuit/grid texture
    for x in range(-80, W + 80, 120):
        d.line((x, 0, x + 260, H), fill=(70, 120, 140, 22), width=1)
    for y in range(90, H, 110):
        d.line((0, y, W, y), fill=(70, 120, 140, 15), width=1)
    # animated scan line
    sy = int((t * 180) % H)
    d.line((0, sy, W, sy), fill=(*CYAN[:3], 28), width=2)
    d.text((74, 48), "AI & IT / FUTURE TECH", font=_font(20, True), fill=MUTED)
    d.text((W - 310, 48), f"ENGINE 03  •  {int(t*24):04d}", font=_font(18, True), fill=MUTED)

def _zoom(im, scale):
    if abs(scale - 1.0) < 0.001:
        return im
    nw, nh = int(W * scale), int(H * scale)
    z = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left, top = (nw-W)//2, (nh-H)//2
    return z.crop((left, top, left+W, top+H))

def _kinetic_hook(im, t):
    d = ImageDraw.Draw(im)
    p = min(1.0, max(0.0, t / 1.4))
    slide = int((1-p) * 90)
    d.text((155-slide, 270), "AI AGENTS", font=_font(112, True), fill=WHITE)
    d.text((155-slide, 405), "ARE CHANGING", font=_font(82, True), fill=CYAN)
    d.text((155-slide, 515), "HOW DEVELOPERS WORK", font=_font(62, False), fill=WHITE)
    d.text((160, 650), "AUTOMATE  •  REASON  •  SHIP", font=_font(30, True), fill=MUTED)
    # live status chips
    for i, label in enumerate(("PLAN", "CODE", "TEST", "SHIP")):
        x = 1250 + i*135
        active = (int(t*2) % 4) == i
        d.rounded_rectangle((x, 820, x+112, 862), radius=12,
                            outline=CYAN if active else (80,105,120,180), width=2)
        d.text((x+22, 830), label, font=_font(17, True),
               fill=CYAN if active else MUTED)

def _story_overlay(im, t, scene):
    d = ImageDraw.Draw(im)
    labels = {
        1: ("AGENT LOOP", "intent → plan → execute"),
        2: ("GENERATE", "code appears as the agent works"),
        3: ("VERIFY", "tests become a feedback signal"),
        4: ("SHIP", "deployment follows proof"),
    }
    if scene in labels:
        a, b = labels[scene]
        d.text((90, 925), a, font=_font(22, True), fill=CYAN)
        d.text((250, 928), b, font=_font(20, False), fill=MUTED)
        d.text((W-300, 925), "PRIVATE TEST", font=_font(18, True), fill=GREEN)

def render_frame(t: float, frame_index: int) -> Image.Image:
    if t < 8:
        im = render_v2_frame(t, frame_index)
        # Replace the centered slide-like hook with kinetic composition.
        im = _zoom(im, 1.015 + 0.008*math.sin(t*.8))
        _kinetic_hook(im, t)
        _hud(im, t)
        return im
    im = render_v2_frame(t, frame_index)
    scene = 1 if t < 20 else 2 if t < 35 else 3 if t < 50 else 4
    # subtle camera breathing makes panels feel less static
    im = _zoom(im, 1.0 + 0.012*math.sin(t*.55))
    _hud(im, t)
    _story_overlay(im, t, scene)
    # animated focus ring
    if 8 <= t < 20:
        d = ImageDraw.Draw(im)
        cx = 960 + int(130*math.sin(t*.9))
        cy = 560 + int(55*math.cos(t*.7))
        r = 150 + int(10*math.sin(t*2.0))
        d.ellipse((cx-r, cy-r, cx+r, cy+r), outline=(*CYAN[:3], 38), width=2)
    return im

def render_frames(out_dir: str, fps: int=FPS, duration: int=DURATION):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    for i in range(fps * duration):
        render_frame(i/fps, i).convert("RGB").save(out/f"frame_{i:05d}.jpg", quality=92)
