import os

def _flag(name: str, default: str) -> bool:
    return os.getenv(name, default).strip().lower() == "true"

ENABLE_RESEARCH = _flag("ENABLE_RESEARCH", "true")
ENABLE_AI_SCRIPTWRITER = _flag("ENABLE_AI_SCRIPTWRITER", "true")
ENABLE_ORIGINALITY_GATE = _flag("ENABLE_ORIGINALITY_GATE", "true")
ENABLE_YOUTUBE_PUBLISH = _flag("ENABLE_YOUTUBE_PUBLISH", "false")
ENABLE_HIDAYATTUBE = _flag("ENABLE_HIDAYATTUBE", "false")
REQUIRE_HUMAN_REVIEW = _flag("REQUIRE_HUMAN_REVIEW", "true")

if ENABLE_HIDAYATTUBE:
    raise RuntimeError("HIDAYATTUBE integration is permanently disabled for this independent project")
if ENABLE_YOUTUBE_PUBLISH:
    raise RuntimeError("Public YouTube publishing is disabled by default; explicit deployment configuration is required")
