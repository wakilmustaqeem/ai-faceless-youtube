from governance.script_originality_gate import check_script

def test_originality_blocks_without_verified_claims():
    result = check_script("A sufficiently long script " * 8, {"status": "approved", "claims": [], "sources": []})
    assert result["passed"] is False
    assert result["reason"] == "verified_claims_required"

def test_originality_blocks_unverified_claim():
    research = {"status": "approved", "claims": [{"status": "blocked", "source_title": "Example", "source_url": "https://example.com", "evidence": "evidence"}], "sources": []}
    result = check_script("A sufficiently long script " * 8, research)
    assert result["passed"] is False
    assert result["reason"] == "unverified_claim_in_research"