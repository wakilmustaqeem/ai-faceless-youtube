#!/usr/bin/env python3
"""Build review-ready distribution packages for social and WordPress publishing.

This tool prepares platform-specific metadata and copies no media. It never
publishes, never stores credentials, and refuses to overwrite an existing
package. Actual API publishing remains behind explicit human approval.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

PLATFORMS = ("facebook", "instagram", "tiktok", "wordpress")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, help="Rendered video path")
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--platform", action="append", choices=PLATFORMS, required=True)
    parser.add_argument("--output", required=True, help="New JSON package path")
    args = parser.parse_args()

    video = Path(args.video)
    output = Path(args.output)

    if not video.is_file() or video.stat().st_size == 0:
        raise SystemExit("REFUSED: rendered video is missing or empty.")
    if output.exists():
        raise SystemExit(f"REFUSED: output already exists: {output}")

    payload = {
        "publishing": False,
        "human_approval_required": True,
        "video": str(video),
        "title": args.title,
        "description": args.description,
        "platforms": {
            platform: {
                "enabled": True,
                "mode": "manual_or_api",
                "status": "READY_FOR_REVIEW",
            }
            for platform in dict.fromkeys(args.platform)
        },
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"PASS: distribution package created → {output}")


if __name__ == "__main__":
    main()
