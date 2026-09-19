"""Import-safe originality gate placeholder."""

def check(script: str, threshold: float = 0.8) -> dict:
    if not script.strip():
        return {"passed": False, "reason": "empty_script"}
    return {"passed": False, "reason": "originality_engine_not_configured", "threshold": threshold}
