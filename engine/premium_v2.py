"""Render the 60s Premium Tech Style v2 test video as deterministic PNG frames.

FFmpeg is intentionally invoked by the caller/workflow, keeping this module testable.
No publish/upload action exists in this engine.
"""
from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw
from engine.styles.premium_v2 import W,H,WHITE,CYAN,MUTED, GREEN, cinematic_background, _font, text_fit
from engine.components.agent_workflow import draw_agent_workflow
from engine.components.code_window import draw_code_window
from engine.components.terminal_window import draw_terminal_window

FPS=24; DURATION=60

def draw_center_title(im,title,subtitle="",progress=0.0):
    d=ImageDraw.Draw(im); f=_font(68,False); box=d.textbbox((0,0),title,font=f); x=(W-(box[2]-box[0]))/2
    d.text((x,330),title,font=f,fill=WHITE)
    if subtitle: text_fit(d,(360,430),subtitle,1200,30,False,MUTED)

def render_frame(t: float, frame_index: int) -> Image.Image:
    im=cinematic_background(t,seed=11)
    # scene transitions every 12s; each scene has continuous motion
    if t<8:
        draw_center_title(im,"AI AGENTS ARE CHANGING", "HOW DEVELOPERS WORK", min(t/2,1))
        d=ImageDraw.Draw(im); text_fit(d,(550,540),"AUTOMATE  •  REASON  •  SHIP",820,34,True,CYAN)
    elif t<20:
        draw_agent_workflow(im,t-8,active=min(4,int((t-8)/2.4)))
        d=ImageDraw.Draw(im); text_fit(d,(520,120),"FROM INTENT → WORKING SOFTWARE",880,42,False,WHITE)
    elif t<35:
        draw_code_window(im,t-20)
    elif t<50:
        draw_terminal_window(im,t-35)
    elif t<56:
        draw_agent_workflow(im,t-50,active=4)
        d=ImageDraw.Draw(im); text_fit(d,(650,150),"DEPLOY WITH CONFIDENCE",650,54,False,WHITE)
        text_fit(d,(730,760),"BUILD  •  TEST  •  DEPLOY",500,28,True,CYAN)
    else:
        draw_center_title(im,"BUILD FASTER. THINK BIGGER.","AI & IT FUTURE TECH",1)
        d=ImageDraw.Draw(im); text_fit(d,(690,620),"SUBSCRIBE FOR THE NEXT SHIFT",560,30,False,CYAN)
    # subtle cinematic vignette
    vign=Image.new("RGBA",(W,H),(0,0,0,0)); vd=ImageDraw.Draw(vign)
    vd.rectangle((0,0,W,H),outline=(0,0,0,130),width=80); im.alpha_composite(vign)
    return im

def render_frames(out_dir: str, fps: int=FPS, duration: int=DURATION):
    out=Path(out_dir); out.mkdir(parents=True,exist_ok=True)
    for i in range(fps*duration):
        render_frame(i/fps,i).convert("RGB").save(out/f"frame_{i:05d}.jpg",quality=92)

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("out"); p.add_argument("--fps",type=int,default=FPS); p.add_argument("--duration",type=int,default=DURATION)
    a=p.parse_args(); render_frames(a.out,a.fps,a.duration)
