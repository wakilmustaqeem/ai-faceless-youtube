"""Claim verification against fetched source content."""
from __future__ import annotations

from governance.source_fetcher import fetch_source, verify_evidence_in_source

def verify_claims_against_sources(claims: list[dict] | None = None) -> dict:
    claims = claims or []
    if not claims:
        return {"passed": False, "reason": "claims_required", "claims": []}
    results = []
    for index, claim in enumerate(claims, 1):
        item = dict(claim)
        item["claim_id"] = str(claim.get("claim_id") or f"claim-{index}")
        url = str(claim.get("source_url", "")).strip()
        evidence = str(claim.get("evidence", "")).strip()
        if not url or not evidence:
            item["status"] = "blocked"
            item["verification_reason"] = "source_url_and_evidence_required"
            results.append(item)
            continue
        source = fetch_source(url)
        if not source.get("passed"):
            item["status"] = "blocked"
            item["verification_reason"] = source.get("reason", "source_fetch_failed")
            results.append(item)
            continue
        matched = verify_evidence_in_source(evidence, source["text"])
        item["status"] = "verified" if matched else "blocked"
        item["verification_reason"] = "evidence_found_in_source" if matched else "evidence_not_found_in_source"
        item["verified_source_url"] = source["url"]
        item["source_content_sha256"] = source["content_sha256"]
        item["source_content_type"] = source.get("content_type", "")
        results.append(item)
    passed = all(item["status"] == "verified" for item in results)
    return {"passed": passed, "reason": "all_claims_source_verified" if passed else "claim_source_verification_failed", "claims": results}