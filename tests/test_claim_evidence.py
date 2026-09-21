from governance.claim_evidence import verify_claims

def test_claims_require_evidence():
    result = verify_claims([{"claim": "A fact", "source_url": "https://example.com", "source_title": "Example", "evidence": "", "supported": True}])
    assert result["passed"] is False
    assert result["claims"][0]["status"] == "blocked"

def test_verified_claim_has_evidence_hash():
    result = verify_claims([{"claim_id": "c1", "claim": "A fact", "source_url": "https://example.com", "source_title": "Example", "evidence": "The source states the fact.", "supported": True}])
    assert result["passed"] is True
    assert result["claims"][0]["status"] == "verified"
    assert len(result["claims"][0]["evidence_sha256"]) == 64

def test_unsupported_claim_blocks():
    result = verify_claims([{"claim": "A fact", "source_url": "https://example.com", "source_title": "Example", "evidence": "Some text.", "supported": False}])
    assert result["passed"] is False