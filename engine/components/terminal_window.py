from __future__ import annotations
from PIL import Image, ImageDraw
from engine.styles.premium_v2 import glass_panel, CYAN, WHITE, MUTED, GREEN, _font

LOGS=["$ python -m pytest tests/test_pipeline.py","collecting ...","test_agent_plan ................. PASS","test_source_gate ................ PASS","test_render_contract ............ PASS","BUILD  ████████████████████  100%","✓ READY FOR DEPLOYMENT"]

def draw_terminal_window(base: Image.Image, t: float):
    glass_panel(base,(250,220,1670,860),radius=24,alpha=242)
    d=ImageDraw.Draw(base)
    d.text((300,255),"TERMINAL / CI",font=_font(24,True),fill=CYAN)
    count=min(len(LOGS),max(1,int(t*2.1)+1)); y=325
    for i,line in enumerate(LOGS[:count]):
        fill=GREEN if ("PASS" in line or "READY" in line or "100%" in line) else WHITE
        d.text((300,y),line,font=_font(27,True),fill=fill); y+=70
    d.text((300,790),"AUTOMATED QA • HUMAN REVIEW REQUIRED",font=_font(20,True),fill=MUTED)
