#!/usr/bin/env python3
"""Local Cinematic Graphic Studio — create/edit safe graphics offline.

Uses PIL only. It can build a Letust Gadget LCD graphic, cinematic room plate,
title card, lower-third, and thumbnail. Existing files are never overwritten.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

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
    path=Path(path)
    if path.exists(): raise SystemExit(f"REFUSED: {path} already exists")
    path.parent.mkdir(parents=True,exist_ok=True)
    img.convert("RGB").save(path,quality=95)

def base():
    im=Image.new("RGB",(W,H),(6,10,22))
    d=ImageDraw.Draw(im)
    for i in range(0,W,80):
        d.line((i,0,i,H),fill=(10,24,42),width=1)
    for i in range(0,H,80):
        d.line((0,i,W,i),fill=(10,24,42),width=1)
    return im

def lcd(path):
    im=base(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((28,28,W-28,H-28),radius=34,outline=(90,190,255),width=5)
    d.rounded_rectangle((70,70,W-70,H-70),radius=20,fill=(9,20,38),outline=(40,100,150),width=2)
    d.text((W//2,150),"LETUST GADGET",font=font(72,True),anchor="mm",fill=(225,245,255))
    d.text((W//2,235),"AI ASSISTANCE • FUTURE TECH",font=font(32),anchor="mm",fill=(135,210,255))
    d.rounded_rectangle((190,330,1410,690),radius=30,outline=(80,160,230),width=3)
    d.text((800,410),"LIVE ASSIST",font=font(42,True),anchor="mm",fill=(180,225,255))
    d.text((800,515),"Research  •  Explain  •  Verify  •  Create",font=font(38),anchor="mm",fill=(225,235,245))
    d.text((800,610),"Human approval remains in control.",font=font(34),anchor="mm",fill=(150,210,240))
    safe_save(im,path)

def room(path):
    im=base(); d=ImageDraw.Draw(im)
    d.rectangle((0,H-190,W,H),fill=(3,7,15))
    d.rectangle((0,H-195,W,H-190),fill=(35,90,125))
    d.text((70,90),"AI & IT FUTURE TECH",font=font(46,True),fill=(220,240,255))
    d.text((70,145),"AI, IT & the Future of Technology",font=font(27),fill=(130,190,230))
    d.rounded_rectangle((930,180,1510,520),radius=24,outline=(60,140,190),width=3)
    d.text((1220,350),"LETUST",font=font(64,True),anchor="mm",fill=(160,220,255))
    safe_save(im,path)

def title(path,title,subtitle="AI, IT & the Future of Technology"):
    im=base(); d=ImageDraw.Draw(im)
    d.text((800,360),title,font=font(74,True),anchor="mm",fill=(235,245,255),align="center")
    d.text((800,475),subtitle,font=font(32),anchor="mm",fill=(140,205,240),align="center")
    d.text((70,820),"AI & IT FUTURE TECH  •  LETUST GADGET",font=font(24,True),fill=(150,200,225))
    safe_save(im,path)

def lower_third(path,name="LETUST GADGET",role="AI & IT FUTURE TECH"):
    im=Image.new("RGB",(W,H),(0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((70,700,760,835),radius=22,fill=(8,18,34),outline=(70,170,220),width=3)
    d.text((105,735),name,font=font(38,True),fill=(235,245,255))
    d.text((105,790),role,font=font(24),fill=(135,205,240))
    safe_save(im,path)

def thumbnail(source,path,title_text):
    src=Image.open(source).convert("RGB").resize((W,H))
    src=ImageEnhance.Contrast(src).enhance(1.12).filter(ImageFilter.GaussianBlur(0.15))
    d=ImageDraw.Draw(src)
    d.rectangle((0,0,W,H),fill=(0,0,0),outline=(0,0,0),width=0)
    d.rectangle((55,55,W-55,H-55),outline=(120,200,245),width=4)
    d.rounded_rectangle((90,610,1510,810),radius=28,fill=(5,12,24))
    d.text((800,675),title_text,font=font(58,True),anchor="mm",fill=(240,248,255),align="center")
    d.text((800,755),"AI & IT FUTURE TECH",font=font(27,True),anchor="mm",fill=(145,210,240))
    safe_save(src,path)

if __name__=="__main__":
    ap=argparse.ArgumentParser(description="Offline graphic studio")
    ap.add_argument("mode",choices=["lcd","room","title","lower-third","thumbnail"])
    ap.add_argument("--output",required=True)
    ap.add_argument("--title",default="THE FUTURE OF AI")
    ap.add_argument("--subtitle",default="AI, IT & the Future of Technology")
    ap.add_argument("--name",default="LETUST GADGET")
    ap.add_argument("--role",default="AI & IT FUTURE TECH")
    ap.add_argument("--source")
    a=ap.parse_args()
    out=Path(a.output)
    if a.mode=="lcd": lcd(out)
    elif a.mode=="room": room(out)
    elif a.mode=="title": title(out,a.title,a.subtitle)
    elif a.mode=="lower-third": lower_third(out,a.name,a.role)
    elif a.mode=="thumbnail":
        if not a.source: raise SystemExit("--source is required for thumbnail mode")
        thumbnail(a.source,out,a.title)
    print(f"PASS: graphic created -> {out}")
