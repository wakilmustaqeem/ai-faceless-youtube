from agents.scriptwriter import run

def test_scriptwriter_blocks_without_verified_claims():
    research = {"status": "approved", "topic": "topic", "sources": [{"title": "Example", "url": "https://example.com", "summary": "Summary"}], "claims": []}
    result = run(research)
    assert result["status"] == "blocked"
    assert result["reason"] == "claim_evidence_not_verified"

def test_scriptwriter_uses_verified_claim_evidence():
    research = {"status": "approved", "topic": "topic", "sources": [{"title": "Example", "url": "https://example.com", "summary": "Summary"}], "claims": [{"claim": "A fact", "source_url": "https://example.com", "source_title": "Example", "evidence": "The source states the fact.", "supported": True}]}
    result = run(research)
    assert result["status"] == "draft"
    assert "The source states the fact." in result["script"]