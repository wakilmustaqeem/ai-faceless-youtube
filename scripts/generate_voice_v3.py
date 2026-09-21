"""Generate V3.5 private-review narration. No upload/publish action."""
from __future__ import annotations
import asyncio
from pathlib import Path
import edge_tts

VOICE="en-US-GuyNeural"; RATE="+8%"; PITCH="+1Hz"
TEXT="""Shipping faster is broken.
Developers still move through a chain of tasks: coding, testing, reviewing, debugging, and shipping.
AI agents are changing that loop by connecting intent to planning, tool use, code, and verification.
In this example, the workflow is visible: a test fails, the agent reads the traceback, the calculation is corrected, and the test turns green.
That failure-and-feedback loop matters more than a flashy demo because it shows cause, action, and result.
There is also evidence behind the broader shift.
Anthropic's 2026 State of AI Agents report says organizations reported time gains of 58 percent for planning and ideation, and 59 percent for code generation, research and documentation, and code review and testing.
Those figures describe reported organizational experience, not a guarantee for every developer.
The practical lesson is simple: let the agent execute repetitive steps, but keep human judgment at the decision layer.
AI does not remove the loop. It moves the human up the loop.
This is AI and IT Future Tech."""

async def main():
    out=Path("output/review/test1_v3_voice.mp3"); out.parent.mkdir(parents=True,exist_ok=True)
    await edge_tts.Communicate(TEXT,VOICE,rate=RATE,pitch=PITCH).save(str(out))
    print(f"VOICE READY: {out}")

if __name__=="__main__": asyncio.run(main())
