from agents import researcher

def test_research_uses_real_source_verification(monkeypatch):
    monkeypatch.setattr(researcher, "verify_claims_against_sources", lambda claims: {"passed": True, "reason": "all_claims_source_verified", "claims": [{"claim_id": "claim-1", "status": "verified", "source_url": "https://example.com", "source_title": "Example", "evidence": "verified evidence"}]})
    result = researcher.run("Topic", [{"url": "https://example.com", "title": "Example", "summary": "Summary"}], [{"claim": "Fact", "source_url": "https://example.com", "source_title": "Example", "evidence": "verified evidence"}])
    assert result["status"] == "approved"
    assert result["claims"][0]["status"] == "verified"

def test_research_blocks_when_source_verification_fails(monkeypatch):
    monkeypatch.setattr(researcher, "verify_claims_against_sources", lambda claims: {"passed": False, "reason": "claim_source_verification_failed", "claims": [{"claim_id": "claim-1", "status": "blocked"}]})
    result = researcher.run("Topic", [{"url": "https://example.com", "title": "Example", "summary": "Summary"}], [{"claim": "Fact", "source_url": "https://example.com", "evidence": "missing"}])
    assert result["status"] == "needs_evidence"