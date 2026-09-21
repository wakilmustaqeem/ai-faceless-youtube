from governance import evidence_verifier

def test_claim_verification_fetches_and_matches_source(monkeypatch):
    monkeypatch.setattr(evidence_verifier, "fetch_source", lambda url: {"passed": True, "url": url, "content_type": "text/html", "text": "The source states the fact.", "content_sha256": "a" * 64})
    monkeypatch.setattr(evidence_verifier, "verify_evidence_in_source", lambda evidence, text: evidence in text)
    result = evidence_verifier.verify_claims_against_sources([{"claim": "A fact", "source_url": "https://example.com", "source_title": "Example", "evidence": "The source states the fact."}])
    assert result["passed"] is True
    assert result["claims"][0]["status"] == "verified"
    assert result["claims"][0]["source_content_sha256"] == "a" * 64

def test_claim_verification_blocks_missing_source_evidence():
    result = evidence_verifier.verify_claims_against_sources([{"claim": "A fact", "source_url": "", "evidence": ""}])
    assert result["passed"] is False
    assert result["claims"][0]["status"] == "blocked"