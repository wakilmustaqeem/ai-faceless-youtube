"""Private-upload boundary. Public publishing is intentionally not implemented here."""

PUBLIC_PUBLISHING_ENABLED = False

def private_upload(video_path: str) -> dict:
    if not video_path.strip():
        return {"status": "BLOCKED", "reason": "video_required"}
    return {"status": "BLOCKED", "reason": "youtube_credentials_not_configured", "public": False}
