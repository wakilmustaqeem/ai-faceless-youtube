"""Import-safe human approval gate."""

def decision(reviewed: bool, approved: bool) -> dict:
    if not reviewed:
        return {"status": "BLOCKED", "reason": "human_review_required"}
    if not approved:
        return {"status": "REJECTED"}
    return {"status": "APPROVED"}
