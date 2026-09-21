"""Build an independent English AI & IT Future Tech review video."""
from pathlib import Path
from datetime import datetime, timezone
import os, subprocess
from PIL import Image, ImageDraw
from scripts.generate_voice import synthesize
from scripts.generate_presenter_asset import main as generate_presenter_asset
from governance.voice_quality_gate import check_voice
from governance.visual_quality_gate import check_video
from governance.captions_quality_gate import check_captions
from scripts.generate_captions import generate_captions

OUT=Path("output"); OUT.mkdir(exist_ok=True)
W,H,FPS=1080,1920,30
SCENE_SECONDS=8.05; XFADE_SECONDS=0.55; DURATION=30
DURATION_TOLERANCE=0.10
BRAND="AI & IT Future Tech"
TOPIC="How AI Agents Are Changing Software Workflows"
SCENES=[
    "AI agents can now handle multi-step software tasks.\nBut what actually changes for developers?",
    "Agents can research, draft code, run checks, and iterate.\nThe workflow becomes more automated, not fully autonomous.",
    "The key is verification: tests, review gates, and human approval still matter.\nAutomation should stop when evidence is missing.",
    "AI & IT Future Tech\nAI, IT & the Future of Technology",
]
VOICE_TEXT=("Welcome to AI and IT Future Tech. Today we are exploring how AI agents are changing software workflows. "
"AI agents can handle multi-step tasks such as research, drafting code, running checks, and iterating. "
"The important change is workflow automation, not removing every human decision. "
"Verification still matters: tests, review gates, and human approval should stop the pipeline when evidence is missing. "
"This is AI and IT Future Tech, bringing practical explainers on AI, IT, and the future of technology.")
SCRIPT=f"# {TOPIC}\n\n{VOICE_TEXT}\n\nReview note: verify current product capabilities and source claims before publication.\n"
metadata=(f"brand: {BRAND}\ntopic: {TOPIC}\ncreated_utc: {datetime.now(timezone.utc).isoformat()}\n"
f"source_language: en\nduration_target_seconds: {DURATION}\nduration_tolerance_seconds: {DURATION_TOLERANCE}\nformat: YouTube Shorts 9:16\nresolution: {W}x{H}\nframe_rate: {FPS}\n"
f"voice: Microsoft Edge Neural English ({os.getenv('TTS_VOICE','en-US-GuyNeural')})\nvideo_codec: H.264\naudio_codec: AAC-LC\nstatus: REVIEW_REQUIRED\n")
(OUT/"script.md").write_text(SCRIPT,encoding="utf-8"); (OUT/"metadata.txt").write_text(metadata,encoding="utf-8")

def make_background(path:Path, index:int, presenter:Path)->None:
    # Composite one consistent full-body presenter/LCD anchor across all scenes.
    presenter_img=Image.open(presenter).convert("RGB").resize((W,H),Image.Resampling.LANCZOS)
    base=Image.new("RGB",(W,H))
    px=base.load()
    for y in range(H):
        t=y/(H-1)
        for x in range(W):
            glow=max(0,1-abs(x-W/2)/(W*.72))
            px[x,y]=(int(6+7*t+4*glow),int(10+14*t+6*glow),int(20+24*t+10*glow))
    base=Image.blend(base,presenter_img,0.82)
    d=ImageDraw.Draw(base,"RGBA")
    d.rectangle((24,24,W-24,H-24),outline=(110,200,255,170),width=3)
    d.rounded_rectangle((74,260,W-74,1680),radius=54,outline=(90,180,240,125),width=3)
    d.rounded_rectangle((320,500,760,1560),radius=90,outline=(130,210,255,55),width=2)
    for yy in (430,1610):
        d.line((112,yy,968,yy),fill=(110,200,255,80),width=2)
    d.text((W//2,185),BRAND,anchor="mm",fill=(220,240,255,235))
    d.text((W//2,215),"PREMIUM TECH • V3",anchor="mm",fill=(140,205,240,180))
    base.save(path,format="PNG")

def run_renderer(title,body,footer,out):
    subprocess.run(["python","scripts/render_text.py",title,body,footer,str(out)],check=True)

def run_cta_renderer(out):
    subprocess.run(["python","scripts/render_text.py","--cta",str(out)],check=True)

def make_motion_scene(background:Path,output:Path,direction:int)->None:
    zoom="min(zoom+0.00075,1.12)"
    x="iw/2-(iw/zoom/2)+sin(on/70)*18" if direction%2 else "iw/2-(iw/zoom/2)-sin(on/70)*18"
    vf="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=contrast=1.03:saturation=1.02:brightness=-0.02,format=yuv420p"
    subprocess.run(["ffmpeg","-y","-loop","1","-i",str(background),"-vf",vf,"-t",str(SCENE_SECONDS),"-r",str(FPS),"-an","-c:v","libx264","-profile:v","baseline","-level","4.0","-pix_fmt","yuv420p","-movflags","+faststart",str(output)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)

scene_videos=[]
presenter_asset=OUT/"presenter_anchor.png"
generate_presenter_asset()
for i,text in enumerate(SCENES,1):
    bg=OUT/f"scene_{i}_background.png"; overlay=OUT/f"scene_{i}_text.png"; motion=OUT/f"scene_{i}_motion.mp4"; scene=OUT/f"scene_{i}.mp4"
    make_background(bg,i,presenter_asset); run_renderer(TOPIC,text,f"{BRAND} • Scene {i}",overlay); make_motion_scene(bg,motion,i)
    subprocess.run(["ffmpeg","-y","-i",str(motion),"-loop","1","-i",str(overlay),"-filter_complex","[0:v][1:v]overlay=0:0:format=auto,format=yuv420p,setsar=1","-t",str(SCENE_SECONDS),"-r",str(FPS),"-c:v","libx264","-profile:v","baseline","-level","4.0","-pix_fmt","yuv420p","-an",str(scene)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
    motion.unlink(missing_ok=True); scene_videos.append(scene)

inputs=sum((["-i",str(s)] for s in scene_videos),[])
filters=[f"[{i}:v]fps={FPS},format=yuv420p,setsar=1[v{i}]" for i in range(len(scene_videos))]
current="v0"; current_duration=SCENE_SECONDS
for i in range(1,len(scene_videos)):
    out=f"xf{i}"; offset=current_duration-XFADE_SECONDS
    filters.append(f"[{current}][v{i}]xfade=transition=fade:duration={XFADE_SECONDS}:offset={offset:.2f}[{out}]"); current=out; current_duration+=SCENE_SECONDS-XFADE_SECONDS
silent=OUT/"silent.mp4"
subprocess.run(["ffmpeg","-y",*inputs,"-filter_complex",";".join(filters),"-map",f"[{current}]","-t",str(DURATION),"-c:v","libx264","-profile:v","baseline","-level","4.0","-pix_fmt","yuv420p","-r",str(FPS),"-fps_mode","cfr","-preset","medium","-movflags","+faststart",str(silent)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
cta=OUT/"subscribe_cta.png"; run_cta_renderer(cta); start=(len(SCENES)-1)*(SCENE_SECONDS-XFADE_SECONDS); with_cta=OUT/"silent_with_cta.mp4"
subprocess.run(["ffmpeg","-y","-i",str(silent),"-loop","1","-i",str(cta),"-filter_complex",f"[0:v][1:v]overlay=0:0:format=auto:enable='between(t,{start:.2f},{DURATION})'[v]","-map","[v]","-t",str(DURATION),"-c:v","libx264","-profile:v","baseline","-level","4.0","-pix_fmt","yuv420p","-r",str(FPS),"-fps_mode","cfr","-preset","medium","-movflags","+faststart",str(with_cta)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
voice=OUT/"voice.mp3"; synthesize(VOICE_TEXT,str(voice))
voice_qa=check_voice(str(voice))
if not voice_qa["passed"]: raise SystemExit(f"Voice QA blocked: {voice_qa}")
captions=OUT/"captions.srt"
generate_captions(VOICE_TEXT, DURATION, str(captions))
captions_qa=check_captions(str(captions), expected_duration=DURATION)
if not captions_qa["passed"]: raise SystemExit(f"Captions QA blocked: {captions_qa}")
video=OUT/"video.mp4"
subprocess.run(["ffmpeg","-y","-i",str(with_cta),"-i",str(voice),"-map","0:v:0","-map","1:a:0","-t",str(DURATION),"-c:v","libx264","-profile:v","baseline","-level","4.0","-pix_fmt","yuv420p","-r",str(FPS),"-fps_mode","cfr","-c:a","aac","-profile:a","aac_low","-ar","44100","-ac","2","-b:a","128k","-af",f"apad=pad_dur={DURATION}","-movflags","+faststart",str(video)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
probe=subprocess.run(["ffprobe","-v","error","-show_entries","format=format_name,duration:stream=index,codec_type,codec_name,pix_fmt,width,height","-of","default=noprint_wrappers=1",str(video)],check=True,capture_output=True,text=True)
required=["codec_type=video","codec_name=h264","pix_fmt=yuv420p","codec_type=audio","codec_name=aac",f"width={W}",f"height={H}"]
if any(x not in probe.stdout for x in required): raise SystemExit("Generated MP4 failed stream/resolution checks")
if "format_name=mov,mp4,m4a,3gp,3g2,mj2" not in probe.stdout: raise SystemExit("Generated file is not a standard MP4 container")
duration_line=next((line for line in probe.stdout.splitlines() if line.startswith("duration=")), "")
actual_duration=float(duration_line.split("=",1)[1]) if duration_line else -1.0
if abs(actual_duration-DURATION) > DURATION_TOLERANCE: raise SystemExit(f"Generated MP4 duration {actual_duration:.3f}s is outside {DURATION}±{DURATION_TOLERANCE}s")
visual_qa=check_video(str(video))
if not visual_qa["passed"]: raise SystemExit(f"Visual QA blocked: {visual_qa}")
subprocess.run(["ffmpeg","-v","error","-i",str(video),"-f","null","-"],check=True)
for p in scene_videos: p.unlink(missing_ok=True)
for p in OUT.glob("scene_*_background.png"): p.unlink(missing_ok=True)
for p in OUT.glob("scene_*_text.png"): p.unlink(missing_ok=True)
for p in [silent,with_cta,cta,presenter_asset]: p.unlink(missing_ok=True)
print(f"Verified independent English 1080x1920 H.264/AAC MP4 for {BRAND}: {video} ({actual_duration:.3f}s)")
