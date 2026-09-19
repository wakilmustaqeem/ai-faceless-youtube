"""Research stage: produces a source-backed research package."""

def run(topic: str) -> dict:
    if not topic.strip():
        raise ValueError("topic is required")
    return {"stage": "research", "topic": topic, "sources": [], "status": "needs_sources"}

if __name__ == "__main__":
    import sys
    print(run(" ".join(sys.argv[1:]) or "demo-topic"))
