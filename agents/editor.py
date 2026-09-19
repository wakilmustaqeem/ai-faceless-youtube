"""Edit stage. FFmpeg is the baseline local renderer."""

def run(voice: str, visuals: list) -> dict:
    return {"stage": "edit", "status": "queued", "renderer": "ffmpeg"}
