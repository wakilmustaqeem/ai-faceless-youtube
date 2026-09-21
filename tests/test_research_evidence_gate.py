from agents.researcher import run

def test_research_requires_claim_evidence():
    result = run("topic", [{"url": "https://example.com", "title": "Example", "summary": "Summary"}], claims=[] )
    assert result["status"] == "needs_evidence"

def test_research_approves_verified_claim():
    result = run("topic", [{"url": "https://example.com", "title": "Example", "summary": "Summary"}], claims=[{"claim": "A fact", "source_url": "https://example.com", "source_title": "Example", "evidence": "The source states the fact.", "supported": True}])
    assert result["status"] == "approved"