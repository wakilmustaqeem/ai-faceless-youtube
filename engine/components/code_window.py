from __future__ import annotations
from PIL import Image, ImageDraw
from engine.styles.premium_v2 import glass_panel, CYAN, WHITE, MUTED, GREEN, _font

LINES=["agent = Planner(model='future-1')","plan = agent.create_plan(task)","result = agent.execute(plan)","assert result.tests_passed","deploy(result.artifact)"]

def draw_code_window(base: Image.Image, t: float):
    glass_panel(base,(210,190,1710,900),radius=26,alpha=238)
    d=ImageDraw.Draw(base)
    d.rectangle((210,190,1710,245),fill=(20,31,43,235))
    for i in range(3): d.ellipse((240+i*26,216,252+i*26,228),fill=((255,90,100) if i==0 else (245,190,70) if i==1 else GREEN))
    d.text((330,207),"agent_pipeline.py",font=_font(22,True),fill=MUTED)
    visible=min(len(LINES),max(1,int(t*2.2)+1)); char_count=int(max(0,t*2.8)%90)
    y=285
    for i,line in enumerate(LINES[:visible]):
        d.text((255,y),f"{i+1:02}",font=_font(24,True),fill=(80,105,120,255))
        shown=line if i<visible-1 else line[:min(len(line),char_count)]
        d.text((330,y),shown,font=_font(28,True),fill=WHITE)
        if i==visible-1: 
            bbox=d.textbbox((330,y),shown,font=_font(28,True)); d.rectangle((bbox[2]+2,y,bbox[2]+4,y+30),fill=CYAN)
        y+=78
    d.text((255,760),"MONOKAI PRO  •  LIVE EDIT",font=_font(20,True),fill=CYAN)
