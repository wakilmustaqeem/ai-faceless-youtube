"""V3.5 originality / quality gate for private renders.

The gate blocks rendering when the approved story blueprint, research evidence,
verified demo, or publication lock is missing. It never publishes to YouTube.
"""
from __future__ import annotations
from pathlib import Path
import json
import re
import yaml

ROOT = Path(__file__).resolve().parents[2]
MAP = ROOT / "docs" / "visual_purpose_map_v1.md"
SOURCES = ROOT / "config" / "research_sources.yaml"
DEMO = ROOT / "output" / "review" / "test1_v3_5_demo.json"
PUBLISH = ROOT / "config" / "publish.yaml"

REQUIRED_SCENES = [
    "Cold Open", "The Shift", "Mechanism", "Real Demo",
    "Failure → Feedback", "Evidence", "Human Judgment", "Original Takeaway",
]

def fail(msg: str):
    raise SystemExit(f"V3.5 QUALITY GATE FAILED: {msg}")

def main():
    if not MAP.exists():
        fail("Visual Purpose Map is missing.")
    text = MAP.read_text(encoding="utf-8")
    missing = [s for s in REQUIRED_SCENES if s not in text]
    if missing:
        fail("Missing scene purpose(s): " + ", ".join(missing))
    if "Static panels <= 20%" not in text or "Purposeful motion >= 80%" not in text:
        fail("Locked motion/static rules are missing.")

    if not SOURCES.exists():
        fail("No research source manifest.")
    data = yaml.safe_load(SOURCES.read_text(encoding="utf-8")) or {}
    sources = data.get("sources", [])
    valid_sources = [s for s in sources if s.get("url") and s.get("title")]
    if not valid_sources:
        fail("At least one named source-backed claim is required.")

    if not DEMO.exists():
        fail("Verified cause→action→result demo artifact is missing.")
    demo = json.loads(DEMO.read_text(encoding="utf-8"))
    if not all(demo.get(k) for k in ("cause", "action", "result")):
        fail("Demo must contain cause, action, and result.")
    if demo.get("verified") is not True:
        fail("Demo verification is not GREEN.")

    if not PUBLISH.exists():
        fail("Publish lock is missing.")
    pub = yaml.safe_load(PUBLISH.read_text(encoding="utf-8")) or {}
    if pub.get("publish_enabled") is not False:
        fail("Public publishing must remain disabled.")

    print("V3.5 QUALITY GATE: GREEN")
    print(f"Sources: {len(valid_sources)}")
    print("Demo: VERIFIED")
    print("Publish: OFF")
    print("AI disclosure: REVIEW_REQUIRED_IF_REALISTIC_SYNTHETIC")

if __name__ == "__main__":
    main()
