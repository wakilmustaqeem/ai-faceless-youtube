from core.contracts.research import Source, ResearchBundle
from core.research.dedupe import dedupe_sources
from core.research.credibility import score_source

def test_dedupe_removes_same_url():
    a=Source(id="",url="https://wikipedia.org/wiki/A",title="A")
    b=Source(id="",url="https://wikipedia.org/wiki/A",title="Other")
    assert len(dedupe_sources([a,b]))==1

def test_credibility_whitelist_domains():
    s=Source(id="",url="https://www.nasa.gov/test",title="NASA")
    assert score_source(s)==0.9

def test_bundle_json_roundtrip():
    b=ResearchBundle(run_id="r1",topic="AI",language="en")
    restored=ResearchBundle.model_validate_json(b.model_dump_json())
    assert restored.run_id=="r1"
