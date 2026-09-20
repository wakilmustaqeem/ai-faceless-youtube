"""Script stage: converts approved, source-backed research into an original draft."""

from __future__ import annotations


def run(research: dict) -> dict:
    if research.get("status") != "approved":
        return {
            "stage": "script",
            "status": "blocked",
            "reason": "research_not_approved",
        }

    topic = str(research.get("topic", "")).strip()
    sources = research.get("sources") or []
    if not topic or not sources:
        return {
            "stage": "script",
            "status": "blocked",
            "reason": "missing_topic_or_sources",
        }

    evidence = "\n".join(
        f"- {item['title']}: {item['summary']} ({item['url']})"
        for item in sources
    )
    script = (
        f"{topic}\n\n"
        "What the evidence shows\n"
        f"{evidence}\n\n"
        "Originality note\n"
        "This draft is based on the listed evidence and must add original "
        "explanation, context, and synthesis before publication. "
        "Do not present source wording as original reporting.\n"
    )
    return {
        "stage": "script",
        "status": "draft",
        "script": script,
        "sources": sources,
    }
