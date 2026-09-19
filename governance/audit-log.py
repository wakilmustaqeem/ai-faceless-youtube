"""Append-only audit event schema."""

from datetime import datetime, timezone

def event(action: str, status: str, detail: str = "") -> dict:
    return {"timestamp": datetime.now(timezone.utc).isoformat(), "action": action, "status": status, "detail": detail}
