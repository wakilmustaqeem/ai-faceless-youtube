"""Visual asset stage. Asset provenance must be retained in the audit record."""

def run(script: str) -> dict:
    return {"stage": "visuals", "status": "queued", "asset_sources": []}
