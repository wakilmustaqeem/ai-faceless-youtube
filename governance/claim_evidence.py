"""Claim-level evidence contract for source-backed research."""
from __future__ import annotations

import hashlib
from urllib.parse import urlparse

def _valid_url(url: str) -> bool:
    parsed = urlparse(url.strip())
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)

def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def verify_claims(claims: list[dict] | None = None) -> dict:
    claims = claims or []
    if not claims:
        return {"passed": False, "reason": "claims_required", "claims": []}
    results = []
    for index, claim in enumerate(claims, 1):
        text = str(claim.get("claim", "")).strip()
        url = str(claim.get("source_url", "")).strip()
        title = str(claim.get("source_title", "")).strip()
        evidence = str(claim.get("evidence", "")).strip()
        supported = claim.get("supported") is True
        valid = bool(text and title and evidence and _valid_url(url) and supported)
        item = {"claim_id": str(claim.get("claim_id") or f"claim-{index}"), "claim": text, "source_url": url, "source_title": title, "evidence": evidence, "evidence_sha256": _hash(evidence) if evidence else "", "supported": supported, "status": "verified" if valid else "blocked"}
        results.append(item)
    passed = all(item["status"] == "verified" for item in results)
    return {"passed": passed, "reason": "all_claims_verified" if passed else "claim_evidence_missing_or_unsupported", "claims": results}