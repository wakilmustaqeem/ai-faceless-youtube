"""Script stage: converts approved research into an original draft."""

def run(research: dict) -> dict:
    if research.get("status") != "approved":
        return {"stage": "script", "status": "blocked", "reason": "research_not_approved"}
    return {"stage": "script", "status": "draft", "script": ""}
