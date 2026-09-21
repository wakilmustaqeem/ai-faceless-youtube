"""Script originality gate bound to verified research evidence."""
from __future__ import annotations
from governance.originality_gate import check

def check_script(script: str, research: dict, threshold: float = 0.82) -> dict:
    if research.get("status") != "approved":
        return {"passed": False, "reason": "research_not_approved"}
    claims = research.get("claims") or []
    if not claims:
        return {"passed": False, "reason": "verified_claims_required"}
    sources = research.get("sources") or []
    evidence_sources = []
    for claim in claims:
        if claim.get("status") != "verified":
            return {"passed": False, "reason": "unverified_claim_in_research"}
        evidence_sources.append({"title": claim.get("source_title", ""), "url": claim.get("source_url", ""), "evidence": claim.get("evidence", "")})
    return check(script, evidence_sources, threshold=threshold)