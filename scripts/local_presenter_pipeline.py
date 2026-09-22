"""Local cinematic presenter compositor.

Assembles a supplied presenter asset, LCD artwork and local narration with FFmpeg.
It never overwrites an existing output artifact.
"""
from __future__ import annotations
import argparse, shutil, subprocess
from pathlib import Path

W, H, FPS = 1920, 1080, 30

def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)

def require_binary(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"Required local binary not found: {name}")

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--presenter", required=True)
    p.add_argument("--voice", required=True)
    p.add_argument("--output", default="output/local-presenter-review.mp4")
    p.add_argument("--lcd", default="")
    args = p.parse_args()

    require_binary("ffmpeg")
    require_binary("ffprobe")
    presenter, voice, output = Path(args.presenter), Path(args.voice), Path(args.output)
    if not presenter.is_file():
        raise SystemExit(f"Presenter asset missing: {presenter}")
    if not voice.is_file():
        raise SystemExit(f"Voice asset missing: {voice}")
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise SystemExit(f"Refusing to overwrite existing artifact: {output}")

    bg = output.parent / ".local_stage.png"
    stage = output.parent / ".local_stage.mp4"
    try:
        run(["ffmpeg","-y","-f","lavfi","-i","color=c=#070b14:s=1920x1080:r=30",
             "-t","1","-frames:v","1",str(bg)])

        if args.lcd and Path(args.lcd).is_file():
            lcd = Path(args.lcd)
            filt = ("[1:v]scale=1050:590:force_original_aspect_ratio=decrease,"
                    "pad=1050:590:(ow-iw)/2:(oh-ih)/2:color=#02050a,setsar=1[lcd];"
                    "[2:v]scale=620:930:force_original_aspect_ratio=decrease,format=rgba[p];"
                    "[0:v][lcd]overlay=790:125[s];[s][p]overlay=105:110:format=auto[v]")
            inputs=["-loop","1","-i",str(bg),"-loop","1","-i",str(lcd),
                    "-loop","1","-i",str(presenter)]
        else:
            filt=("[1:v]scale=620:930:force_original_aspect_ratio=decrease,"
                  "format=rgba[p];[0:v][p]overlay=105:110:format=auto[v]")
            inputs=["-loop","1","-i",str(bg),"-loop","1","-i",str(presenter)]

        run(["ffmpeg","-y",*inputs,"-filter_complex",filt,"-map","[v]","-t","30",
             "-r",str(FPS),"-c:v","libx264","-pix_fmt","yuv420p","-an",str(stage)])

        run(["ffmpeg","-y","-i",str(stage),"-i",str(voice),"-map","0:v:0","-map","1:a:0",
             "-shortest","-c:v","libx264","-profile:v","high","-pix_fmt","yuv420p",
             "-c:a","aac","-b:a","192k","-ar","48000","-movflags","+faststart",str(output)])

        probe=subprocess.run(["ffprobe","-v","error","-show_entries",
                              "stream=codec_type,codec_name,width,height,pix_fmt",
                              "-of","default=noprint_wrappers=1",str(output)],
                             check=True,capture_output=True,text=True)
        required=("codec_name=h264","codec_name=aac","width=1920","height=1080","pix_fmt=yuv420p")
        missing=[x for x in required if x not in probe.stdout]
        if missing:
            output.unlink(missing_ok=True)
            raise SystemExit("Local presenter QA failed: "+", ".join(missing))
        print(f"PASS: local cinematic presenter review video -> {output}")
    finally:
        bg.unlink(missing_ok=True)
        stage.unlink(missing_ok=True)

if __name__ == "__main__":
    main()
