from governance import originality_gate

def test_originality_requires_source_evidence():
    result = originality_gate.check(" ".join(["original"] * 25), sources=[])
    assert result["passed"] is False
    assert result["reason"] == "source_evidence_required"

def test_originality_blocks_close_source_wording():
    source = {"title": "Example", "url": "https://example.com", "excerpt": "artificial intelligence tools can automate repetitive business tasks and help teams analyze large amounts of information quickly"}
    script = "Artificial intelligence tools can automate repetitive business tasks and help teams analyze large amounts of information quickly. The practical lesson is to use these tools carefully and verify results."
    result = originality_gate.check(script, [source])
    assert result["passed"] is False
    assert result["reason"] == "source_overlap_too_high"

def test_originality_accepts_distinct_synthesis():
    source = {"title": "Example", "url": "https://example.com", "excerpt": "artificial intelligence tools can automate repetitive business tasks and help teams analyze large amounts of information quickly"}
    script = "A small business can save time by choosing one narrow workflow to improve. Start with a task that happens every day, measure the old process, then test an automation and compare the result before expanding it."
    result = originality_gate.check(script, [source])
    assert result["passed"] is True
    assert result["reason"] == "originality_check_passed"