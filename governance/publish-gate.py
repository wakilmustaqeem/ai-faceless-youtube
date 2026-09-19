"""Final publishing gate: explicit human approval plus independent channel configuration."""

def can_publish(human_approved: bool, channel_configured: bool, qa_passed: bool) -> dict:
    if not human_approved:
        return {"allowed": False, "reason": "human_approval_required"}
    if not channel_configured:
        return {"allowed": False, "reason": "independent_channel_not_configured"}
    if not qa_passed:
        return {"allowed": False, "reason": "qa_failed"}
    return {"allowed": False, "reason": "publishing_disabled_by_default"}
