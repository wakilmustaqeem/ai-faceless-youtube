"""Source-backed research stage with real source verification."""

from __future__ import annotations

from governance.evidence_verifier import verify_claims_against_sources

def run(topic: str, sources: list[dict] | None = None, claims: list[dict] | None = None) -> dict:
    topic = topic.strip()
    if not topic:
        raise ValueError("topic is required")
    normalized = []
    for source in sources or []:
        url = str(source.get("url", "")).strip()
        title = str(source.get("title", "")).strip()
        summary = str(source.get("summary", "")).strip()
        if url and title and summary:
            normalized.append({"title": title, "url": url, "summary": summary})
    if not normalized:
        return {"stage": "research", "topic": topic, "sources": [], "status": "needs_sources"}
    evidence_result = verify_claims_against_sources(claims)
    if not evidence_result["passed"]:
        return {"stage": "research", "topic": topic, "sources": normalized, "claims": evidence_result["claims"], "status": "needs_evidence", "evidence_reason": evidence_result["reason"]}
    return {"stage": "research", "topic": topic, "sources": normalized, "claims": evidence_result["claims"], "status": "approved"}