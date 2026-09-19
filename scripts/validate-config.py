"""Basic repository configuration validation."""

from pathlib import Path

REQUIRED = [Path("config.yaml"), Path("config/content-policy.yaml"), Path("governance/originality-gate.py"), Path("governance/human-review.py"), Path("governance/audit-log.py")]
missing = [str(p) for p in REQUIRED if not p.exists()]
if missing:
    raise SystemExit("Missing required files: " + ", ".join(missing))
print("Configuration structure OK")
