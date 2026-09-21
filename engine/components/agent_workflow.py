from __future__ import annotations
import math
from PIL import Image, ImageDraw
from engine.styles.premium_v2 import CYAN, GREEN, WHITE, MUTED, glass_panel, glow_line, _font, ease

NODES=[("INPUT",270,620), ("AGENT",650,430), ("CODE",1040,650), ("TEST",1390,430), ("DEPLOY",1660,650)]

def draw_agent_workflow(base: Image.Image, t: float, active: int = 1):
    glass_panel(base,(150,260,1770,860),radius=30,alpha=185)
    d=ImageDraw.Draw(base)
    pts=[]
    for i,(label,x,y) in enumerate(NODES):
        pts.append((x,y))
        if i: glow_line(base,[pts[i-1],pts[i]],width=3)
        pulse=.5+.5*math.sin(t*3+i)
        r=34+int(5*pulse)
        fill=CYAN if i==active else (70,95,112,255)
        d.ellipse((x-r,y-r,x+r,y+r),fill=(8,18,27,255),outline=fill,width=4)
        if i==active:
            d.ellipse((x-r-10,y-r-10,x+r+10,y+r+10),outline=(*CYAN[:3],60),width=2)
        f=_font(25,True); tw=d.textbbox((0,0),label,font=f)[2]
        d.text((x-tw/2,y+58),label,font=f,fill=WHITE if i==active else MUTED)
    # moving packet along the chain
    seg=min(int(t*1.5),len(pts)-2); local=(t*1.5)%1; local=ease(local)
    x1,y1=pts[seg]; x2,y2=pts[seg+1]; x=x1+(x2-x1)*local; y=y1+(y2-y1)*local
    d.ellipse((x-9,y-9,x+9,y+9),fill=GREEN)
