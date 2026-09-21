"""Manual research intake for human-entered sources and claim evidence."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from agents.researcher import run

def main() -> int:
    parser = argparse.ArgumentParser(description="Verify manually entered research sources and claims.")
    parser.add_argument("--input", required=True, help="Path to manual research JSON")
    parser.add_argument("--output", default="output/research_result.json")
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = run(data["topic"], data.get("sources"), data.get("claims"))
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": result.get("status"), "reason": result.get("evidence_reason", "")}, ensure_ascii=False))
    return 0 if result.get("status") == "approved" else 1

if __name__ == "__main__":
    raise SystemExit(main())