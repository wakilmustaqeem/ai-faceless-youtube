"""Research stage: produces a source-backed research package."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from core.research.engine import run_research


def run(topic: str, run_id: str = "research-cli") -> dict:
    if not topic.strip():
        raise ValueError("topic is required")
    bundle = run_research(run_id=run_id, topic=topic)
    return bundle.model_dump(mode="json")


if __name__ == "__main__":
    topic = " ".join(sys.argv[1:]).strip() or "demo-topic"
    result = run(topic)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if any(w.startswith("only_") or w == "no_claims_extracted" for w in result["warnings"]):
        raise SystemExit(1)
