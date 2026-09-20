"""Generate the private-review voice track with edge-tts only; no publish/upload action."""
from __future__ import annotations
import asyncio
from pathlib import Path
import edge_tts

VOICE = "en-US-GuyNeural"
RATE = "+12%"
PITCH = "+2Hz"
TEXT = """AI agents are changing how developers work.
Instead of starting from a blank editor, you can give an agent an intent, and watch it turn that intent into a plan.
Then it writes code, runs tests, reads the results, and iterates.
The important shift is not just faster code.
It is a new development loop: plan, build, verify, and ship.
A strong agent workflow still needs guardrails.
Source-backed research keeps the idea grounded.
Automated tests catch regressions.
And human review stays in control before anything goes public.
That combination is where AI-assisted development becomes practical.
The agent handles repetitive execution.
The developer keeps the judgment.
From intent to working software, the future looks less like replacing the developer, and more like giving the developer a powerful new teammate.
Build faster. Think bigger.
This is AI and IT Future Tech."""

async def main():
    out = Path("output/review/test1_v3_voice.mp3")
    out.parent.mkdir(parents=True, exist_ok=True)
    communicate = edge_tts.Communicate(TEXT, VOICE, rate=RATE, pitch=PITCH)
    await communicate.save(str(out))
    print(f"VOICE READY: {out}")

if __name__ == "__main__":
    asyncio.run(main())
