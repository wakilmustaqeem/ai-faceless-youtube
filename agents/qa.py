"""QA gate for generated packages."""

def run(package: dict) -> dict:
    required = ("script", "voice", "visuals", "video")
    missing = [key for key in required if not package.get(key)]
    if missing:
        return {"stage": "qa", "status": "FAILED", "missing": missing}
    return {"stage": "qa", "status": "PASSED"}
