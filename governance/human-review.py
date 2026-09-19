"""Human approval gate. Public publishing must never bypass this gate."""

def decision(reviewed: bool, approved: bool) -> dict:
    if not reviewed:
        return {"status": "BLOCKED", "reason": "human_review_required"}
    if not approved:
        return {"status": "REJECTED"}
    return {"status": "APPROVED"}
