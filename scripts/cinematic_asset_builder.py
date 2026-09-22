#!/usr/bin/env python3
"""Build local cinematic support assets for the presenter studio.

Creates a 72-inch LCD-style Letust Gadget screen graphic and a cinematic
background plate with PIL. No network, API key, or overwrite is used.
A realistic human presenter remains an external/local input asset.
"""
from pathlib import Path
import argparse
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"assets"
W,H=1600,900

def font(size,bold=False):
    candidates=[
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for p in candidates:
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default()

def safe_save(img,path):
    if path.exists(): raise SystemExit(f"REFUSED: {path} already exists")
    path.parent.mkdir(parents=True,exist_ok=True); img.save(path,quality=95)

def lcd(path):
    im=Image.new("RGB",(W,H),(7,12,24)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((28,28,W-28,H-28),radius=34,outline=(90,190,255),width=5)
    d.rectangle((70,70,W-70,H-70),fill=(10,20,38))
    d.text((W//2,150),"LETUST GADGET",font=font(72,True),anchor="mm",fill=(225,245,255))
    d.text((W//2,235),"AI ASSISTANCE • FUTURE TECH",font=font(32),anchor="mm",fill=(135,210,255))
    d.rounded_rectangle((190,330,1410,690),radius=30,outline=(80,160,230),width=3)
    d.text((800,410),"LIVE ASSIST",font=font(42,True),anchor="mm",fill=(180,225,255))
    d.text((800,515),"Research  •  Explain  •  Verify  •  Create",font=font(38),anchor="mm",fill=(225,235,245))
    d.text((800,610),"Human approval remains in control.",font=font(34),anchor="mm",fill=(150,210,240))
    safe_save(im,path)

def plate(path):
    im=Image.new("RGB",(W,H)); px=im.load()
    for y in range(H):
        for x in range(W):
            g=max(0,1-abs(x-W*.55)/(W*.7))
            t=y/H
            px[x,y]=(int(5+10*t+4*g),int(9+17*t+6*g),int(20+30*t+12*g))
    d=ImageDraw.Draw(im)
    d.rectangle((0,H-190,W,H),fill=(3,7,15))
    d.text((70,90),"AI & IT FUTURE TECH",font=font(46,True),fill=(220,240,255))
    d.text((70,145),"AI, IT & the Future of Technology",font=font(27),fill=(130,190,230))
    safe_save(im,path)

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--lcd",default=str(OUT/"letust-gadget-lcd.png")); ap.add_argument("--background",default=str(OUT/"cinematic-room-bg.png"))
    a=ap.parse_args(); lcd(Path(a.lcd)); plate(Path(a.background)); print("PASS: local cinematic support assets created")
