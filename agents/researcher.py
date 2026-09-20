"""Source-backed research stage for the independent channel.

Research is deliberately deterministic: it accepts a topic plus explicit source
records and refuses to approve a package without usable evidence.
"""

from __future__ import annotations


def run(topic: str, sources: list[dict] | None = None) -> dict:
    topic = topic.strip()
    if not topic:
        raise ValueError("topic is required")

    normalized = []
    for source in sources or []:
        url = str(source.get("url", "")).strip()
        title = str(source.get("title", "")).strip()
        summary = str(source.get("summary", "")).strip()
        if url and title and summary:
            normalized.append({"title": title, "url": url, "summary": summary})

    if not normalized:
        return {
            "stage": "research",
            "topic": topic,
            "sources": [],
            "status": "needs_sources",
        }

    return {
        "stage": "research",
        "topic": topic,
        "sources": normalized,
        "status": "approved",
    }


if __name__ == "__main__":
    import json
    import sys

    topic = " ".join(sys.argv[1:]).strip() or "demo-topic"
    print(json.dumps(run(topic), ensure_ascii=False, indent=2))
