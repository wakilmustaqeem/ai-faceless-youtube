"""Build an independent cinematic Urdu YouTube Short with automatic motion and validation."""
from pathlib import Path
from datetime import datetime, timezone
import os, subprocess
from PIL import Image, ImageDraw
from scripts.generate_voice import synthesize

OUT=Path("output"); OUT.mkdir(exist_ok=True)
W,H,FPS=1080,1920,30
SCENE_SECONDS=7.5; XFADE_SECONDS=0.55; DURATION=30
TOPIC="روزانہ مختصر اسلامی یاددہانی"
SCENES=[
"السلام علیکم ورحمۃ اللہ وبرکاتہ۔\nآج کی مختصر یاددہانی۔",
"نماز اللہ سے تعلق مضبوط کرنے کا ذریعہ ہے۔\nاپنی نماز کی حفاظت کریں۔",
"دل کا سکون اللہ کی یاد میں ہے۔\nروزانہ اپنے رب کو یاد کریں۔",
"آئیے نیکی کے سفر کو جاری رکھیں۔\nLike • Share • Subscribe",
]
VOICE_TEXT="السلام علیکم ورحمۃ اللہ وبرکاتہ۔ آج کی مختصر یاددہانی پیش خدمت ہے۔ نماز اللہ سے تعلق مضبوط کرنے کا ذریعہ ہے۔ اپنی نماز کی حفاظت کریں۔ دل کا سکون اللہ کی یاد میں ہے۔ روزانہ اپنے رب کو یاد کریں۔ آئیے نیکی کے سفر کو جاری رکھیں۔"
SCRIPT=f"# {TOPIC}\n\n{VOICE_TEXT}\n\nنوٹ: قرآن و حدیث کے اصل حوالہ جات اشاعت سے پہلے مستند ذریعے سے انسانی طور پر verify کیے جائیں۔\n"
metadata=(f"topic: {TOPIC}\ncreated_utc: {datetime.now(timezone.utc).isoformat()}\n"
f"duration_target_seconds: {DURATION}\nformat: YouTube Shorts 9:16\nresolution: {W}x{H}\nframe_rate: {FPS}\n"
f"voice: Microsoft Edge Neural Urdu ({os.getenv('TTS_VOICE','ur-PK-AsadNeural')})\nvideo_codec: H.264\naudio_codec: AAC-LC\nstatus: REVIEW_REQUIRED\n")
(OUT/"script.md").write_text(SCRIPT,encoding="utf-8"); (OUT/"metadata.txt").write_text(metadata,encoding="utf-8")

def make_background(path:Path, index:int)->None:
    img=Image.new("RGB",(W,H)); px=img.load()
    for y in range(H):
        t=y/(H-1)
        for x in range(W):
            glow=max(0,1-abs(x-W/2)/(W*.72))
            px[x,y]=(int(10+16*t+8*glow),int(16+14*t+7*glow),int(30+22*t+10*glow))
    d=ImageDraw.Draw(img,"RGBA")
    d.rectangle((28,28,W-28,H-28),outline=(190,155,70,190),width=4)
    d.rounded_rectangle((58,430,W-58,1490),radius=52,fill=(5,8,16,126),outline=(190,155,70,205),width=3)
    d.rounded_rectangle((98,468,W-98,510),radius=18,fill=(190,155,70,220))
    img.save(path,format="PNG")

def run_renderer(title,body,footer,out):
    subprocess.run(["python","scripts/render_text.py",title,body,footer,str(out)],check=True)

def run_cta_renderer(out):
    subprocess.run(["python","scripts/render_text.py","--cta",str(out)],check=True)

def make_motion_scene(background:Path,output:Path,direction:int)->None:
    zoom="min(zoom+0.00075,1.12)"
    x="iw/2-(iw/zoom/2)+sin(on/70)*18" if direction%2 else "iw/2-(iw/zoom/2)-sin(on/70)*18"
    vf=f"scale=1220:2170:force_original_aspect_ratio=increase,crop=1220:2170,zoompan=z='{zoom}':x='{x}':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,eq=contrast=1.03:saturation=0.92:brightness=-0.02,format=yuv420p"
    subprocess.run(["ffmpeg","-y","-loop","1","-i",str(background),"-vf",vf,"-t",str(SCENE_SECONDS),"-r",str(FPS),"-an","-c:v","libx264","-profile:v","baseline","-level","4.0","-pix_fmt","yuv420p",str(output)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)

scene_videos=[]
for i,text in enumerate(SCENES,1):
    bg=OUT/f"scene_{i}_background.png"; overlay=OUT/f"scene_{i}_text.png"; motion=OUT/f"scene_{i}_motion.mp4"; scene=OUT/f"scene_{i}.mp4"
    make_background(bg,i); run_renderer(TOPIC,text,f"INDEPENDENT • منظر {i}",overlay); make_motion_scene(bg,motion,i)
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
voice=OUT/"voice.mp3"; synthesize(VOICE_TEXT,str(voice)); video=OUT/"video.mp4"
subprocess.run(["ffmpeg","-y","-i",str(with_cta),"-i",str(voice),"-map","0:v:0","-map","1:a:0","-t",str(DURATION),"-c:v","libx264","-profile:v","baseline","-level","4.0","-pix_fmt","yuv420p","-r",str(FPS),"-fps_mode","cfr","-c:a","aac","-profile:a","aac_low","-ar","44100","-ac","2","-b:a","128k","-af",f"apad=pad_dur={DURATION}","-movflags","+faststart",str(video)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
probe=subprocess.run(["ffprobe","-v","error","-show_entries","format=format_name,duration:stream=index,codec_type,codec_name,pix_fmt,width,height","-of","default=noprint_wrappers=1",str(video)],check=True,capture_output=True,text=True)
required=["codec_type=video","codec_name=h264","pix_fmt=yuv420p","codec_type=audio","codec_name=aac",f"width={W}",f"height={H}"]
if any(x not in probe.stdout for x in required): raise SystemExit("Generated MP4 failed stream/resolution checks")
if "format_name=mov,mp4,m4a,3gp,3g2,mj2" not in probe.stdout: raise SystemExit("Generated file is not a standard MP4 container")
subprocess.run(["ffmpeg","-v","error","-i",str(video),"-f","null","-"],check=True)
for p in scene_videos: p.unlink(missing_ok=True)
for p in OUT.glob("scene_*_background.png"): p.unlink(missing_ok=True)
for p in OUT.glob("scene_*_text.png"): p.unlink(missing_ok=True)
for p in [silent,with_cta,cta]: p.unlink(missing_ok=True)
print(f"Verified independent cinematic 1080x1920 H.264/AAC MP4 with automatic motion: {video}")
