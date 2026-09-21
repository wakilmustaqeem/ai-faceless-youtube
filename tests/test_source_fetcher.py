from governance.source_fetcher import verify_evidence_in_source

def test_evidence_must_exist_in_fetched_source():
    assert verify_evidence_in_source("source evidence", "Intro source evidence conclusion")

def test_missing_evidence_blocks():
    assert not verify_evidence_in_source("not present", "Fetched source text")