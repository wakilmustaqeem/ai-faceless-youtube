"""Voice stage. Provider credentials are read only from the runtime environment."""

def run(script: str) -> dict:
    if not script.strip():
        raise ValueError("script is required")
    return {"stage": "voice", "status": "queued", "provider": "edge-tts"}
