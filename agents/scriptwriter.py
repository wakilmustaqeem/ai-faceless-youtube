"""Script stage: converts verified, source-backed research into a draft."""

from __future__ import annotations


def run(research: dict) -> dict:
    if research.get("status") != "approved":
        return {"stage": "script", "status": "blocked", "reason": "research_not_approved"}

    topic = str(research.get("topic", "")).strip()
    sources = research.get("sources") or []
    claims = research.get("claims") or []

    if not topic or not sources:
        return {"stage": "script", "status": "blocked", "reason": "missing_topic_or_sources"}

    verified_claims = []
    for claim in claims:
        if (
            claim.get("status") != "verified"
            or not str(claim.get("source_url", "")).strip()
            or not str(claim.get("source_title", "")).strip()
            or not str(claim.get("evidence", "")).strip()
            or not str(claim.get("verified_source_url", claim.get("source_url", ""))).strip()
            or not str(claim.get("source_content_sha256", "")).strip()
        ):
            return {
                "stage": "script",
                "status": "blocked",
                "reason": "claim_evidence_not_verified",
                "claims": claims,
            }
        verified_claims.append(claim)

    if not verified_claims:
        return {
            "stage": "script",
            "status": "blocked",
            "reason": "claim_evidence_not_verified",
            "claims": claims,
        }

    evidence = "\n".join(
        f"- {item['source_title']}: {item['evidence']} ({item['source_url']})"
        for item in verified_claims
    )
    script = (
        f"{topic}\n\n"
        "What the verified evidence shows\n"
        f"{evidence}\n\n"
        "Originality note\n"
        "This draft uses verified evidence but requires original explanation, context, and synthesis before publication. Do not present source wording as original reporting.\n"
    )
    return {
        "stage": "script",
        "status": "draft",
        "script": script,
        "sources": sources,
        "claims": verified_claims,
    }
