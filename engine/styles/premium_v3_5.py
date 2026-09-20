"""Premium V3.5 visual primitives: cinematic motion + purposeful technical storytelling."""
from __future__ import annotations
import math
from PIL import Image, ImageDraw, ImageFilter
from engine.styles.premium_v2 import W,H,WHITE,CYAN,MUTED,GREEN,PANEL,_font,text_fit,cinematic_background,glow_line

def desk(im,t):
    d=ImageDraw.Draw(im)
    # layered desk / monitor silhouettes create depth instead of a flat card
    d.rounded_rectangle((120,170,1800,910),radius=38,fill=(7,13,22,210),outline=(70,110,125,120),width=2)
    d.rectangle((220,250,1690,760),fill=(4,9,16,235))
    d.polygon([(0,1080),(1920,1080),(1690,760),(230,760)],fill=(9,17,27,255))
    for x in range(260,1680,140):
        d.line((x,780,x-80,1080),fill=(40,65,78,80),width=2)
    glow_line(im,[(300,730),(850,730),(1100,650),(1600,650)],width=2)
    p=min(1.0,t/1.2)
    text_fit(d,(170+int((1-p)*100),365),"SHIPPING FASTER",1100,100,False,WHITE)
    text_fit(d,(170+int((1-p)*100),480),"IS BROKEN?",900,100,True,CYAN)
    text_fit(d,(175,650),"THE AGENTIC LOOP CHANGES THE WORKFLOW",1100,30,True,MUTED)

def shift(im,t):
    d=ImageDraw.Draw(im)
    left=(260,420); right=(1510,420); mid=(960,420)
    for i in range(5):
        y=220+i*120
        x=250+int(80*math.sin(t*2+i))
        d.rounded_rectangle((x,y,x+330,y+72),18,fill=(12,24,36,230),outline=(80,120,135,150),width=2)
        d.text((x+28,y+20),("CODE","TEST","REVIEW","DEBUG","SHIP")[i],font=_font(24,True),fill=WHITE)
    d.ellipse((820,300,1100,580),fill=(8,22,34,245),outline=CYAN,width=4)
    d.text((875,390),"AGENT",font=_font(38,True),fill=CYAN)
    for i in range(5):
        y=255+i*120
        glow_line(im,[(580,y+36),(820,y+36)],width=3)
        glow_line(im,[(1100,y+36),(1430,y+36)],width=3)
    d.text((240,140),"HUMAN TASKS",font=_font(26,True),fill=MUTED)
    d.text((1430,140),"ORCHESTRATED LOOP",font=_font(26,True),fill=MUTED)

def architecture(im,t):
    d=ImageDraw.Draw(im)
    nodes=[("INTENT",180),("PLAN",500),("TOOLS",820),("CODE",1140),("TEST",1460)]
    y=520
    for label,x in nodes:
        pulse=5*math.sin(t*4+x/200)
        r=62+int(pulse)
        d.ellipse((x-r,y-r,x+r,y+r),fill=(7,18,29,245),outline=CYAN,width=3)
        text_fit(d,(x-48,y-14),label,110,21,True,CYAN)
    for i in range(len(nodes)-1):
        glow_line(im,[(nodes[i][1]+65,y),(nodes[i+1][1]-65,y)],width=5)
    d.text((180,180),"FROM INTENT TO VERIFIED SOFTWARE",font=_font(46,True),fill=WHITE)
    d.text((180,245),"Plan → tools → code → tests → feedback",font=_font(27),fill=MUTED)

def code_demo(im,t):
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((150,150,1770,930),28,fill=(7,12,20,245),outline=(65,95,110,170),width=2)
    d.rectangle((150,150,1770,215),fill=(17,27,38,255))
    d.text((205,174),"VS CODE  •  agent_demo.py",font=_font(24,True),fill=MUTED)
    d.text((230,255),"def total(items):",font=_font(28,True),fill=CYAN)
    d.text((290,305),"return sum(items) - 10",font=_font(28,True),fill=WHITE)
    d.text((230,385),"items = [50, 30, 40]",font=_font(28,True),fill=WHITE)
    d.text((230,435),"assert total(items) == 120",font=_font(28,True),fill=WHITE)
    d.text((230,535),"EXPECTED   120",font=_font(26,True),fill=MUTED)
    d.text((230,585),"OBSERVED   110",font=_font(26,True),fill=(255,100,110,255))
    d.text((230,690),"LIVE DIFF",font=_font(24,True),fill=CYAN)
    d.text((230,740),"- return sum(items) - 10",font=_font(27,True),fill=(255,110,120,255))
    d.text((230,790),"+ return sum(items)",font=_font(27,True),fill=GREEN)
    d.text((1320,255),"FUNCTIONAL DEMO",font=_font(22,True),fill=GREEN)
    d.text((1320,300),"verified in CI",font=_font(22,True),fill=MUTED)

def feedback(im,t):
    d=ImageDraw.Draw(im)
    phase=t/9.0
    if phase<.34:
        label="TEST FAILED"; color=(255,90,105,255); detail="AssertionError: expected 120, got 110"
    elif phase<.67:
        label="AGENT READS TRACEBACK"; color=CYAN; detail="locate cause → edit calculation"
    else:
        label="TEST PASSED"; color=GREEN; detail="1 passed  •  expected 120  •  received 120"
    d.rounded_rectangle((190,230,1730,830),28,fill=(7,13,22,245),outline=color,width=3)
    d.text((260,315),label,font=_font(62,True),fill=color)
    d.text((260,430),detail,font=_font(30,True),fill=WHITE)
    glow_line(im,[(300,600),(800,600),(1120,520),(1580,520)],width=5,color=color)
    d.text((260,690),"CAUSE  →  ACTION  →  RESULT",font=_font(28,True),fill=MUTED)

def evidence(im,t):
    d=ImageDraw.Draw(im)
    d.text((180,150),"WHERE AGENTS OPEN UP TIME",font=_font(44,True),fill=WHITE)
    vals=[("Planning",58),("Code generation",59),("Research/docs",59),("Review/testing",59)]
    base=700
    for i,(name,val) in enumerate(vals):
        y=290+i*105
        d.text((210,y),name,font=_font(25),fill=MUTED)
        d.rounded_rectangle((610,y+4,1510,y+42),18,fill=(20,34,46,255))
        width=int(900*val/65)
        d.rounded_rectangle((610,y+4,610+width,y+42),18,fill=CYAN)
        d.text((1540,y),f"{val}%",font=_font(25,True),fill=WHITE)
    d.text((180,860),"Source: Anthropic — The 2026 State of AI Agents Report",font=_font(18,True),fill=MUTED)

def judgment(im,t):
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((180,180,1740,880),30,fill=(7,13,22,235),outline=(75,105,120,140),width=2)
    d.text((260,280),"AGENT OUTPUT",font=_font(28,True),fill=MUTED)
    d.text((260,345),"proposal ready for review",font=_font(42,True),fill=WHITE)
    d.rounded_rectangle((260,500,760,610),18,fill=(14,30,40,255),outline=GREEN,width=2)
    d.text((350,535),"APPROVE",font=_font(30,True),fill=GREEN)
    d.rounded_rectangle((850,500,1410,610),18,fill=(35,22,30,255),outline=(255,150,120,220),width=2)
    d.text((925,535),"REQUEST CHANGE",font=_font(30,True),fill=(255,170,135,255))
    d.text((260,720),"THE AGENT EXECUTES. THE HUMAN DECIDES.",font=_font(34,True),fill=CYAN)

def takeaway(im,t):
    d=ImageDraw.Draw(im)
    d.text((180,260),"AI DOESN’T REMOVE THE LOOP.",font=_font(66,True),fill=WHITE)
    d.text((180,370),"IT MOVES THE HUMAN UP THE LOOP.",font=_font(66,True),fill=CYAN)
    d.text((185,560),"AI & IT FUTURE TECH",font=_font(30,True),fill=MUTED)
    d.text((185,610),"ORIGINAL ANALYSIS • PRIVATE REVIEW",font=_font(20,True),fill=MUTED)
