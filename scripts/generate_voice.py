"""Generate English-first narration for the independent AI & IT Future Tech channel."""
import asyncio
import os
from pathlib import Path
import edge_tts

VOICE = os.getenv("TTS_VOICE", "en-US-GuyNeural")
RATE = os.getenv("TTS_RATE", "-5%")
PITCH = os.getenv("TTS_PITCH", "+0Hz")
VOLUME = os.getenv("TTS_VOLUME", "+0%")

async def generate_voice(text: str, output_path: str, voice: str = VOICE) -> None:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    communicate = edge_tts.Communicate(text, voice=voice, rate=RATE, pitch=PITCH, volume=VOLUME)
    await communicate.save(str(output))
    if not output.exists() or output.stat().st_size == 0:
        raise RuntimeError(f"Edge-TTS produced no audio: {output}")

def synthesize(text: str, output_path: str, voice: str = VOICE) -> None:
    asyncio.run(generate_voice(text, output_path, voice))

if __name__ == "__main__":
    synthesize(
        "Welcome to AI and IT Future Tech. Today we are exploring how AI agents are changing software workflows.",
        "output/voice-test.mp3",
    )
