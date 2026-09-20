from agents.researcher import run as research
from agents.scriptwriter import run as script


def test_research_requires_sources():
    result = research("AI agents")
    assert result["status"] == "needs_sources"


def test_approved_research_produces_script():
    result = research(
        "AI agents",
        [{"title": "Example source", "url": "https://example.com", "summary": "A factual summary."}],
    )
    assert result["status"] == "approved"
    draft = script(result)
    assert draft["status"] == "draft"
    assert "A factual summary." in draft["script"]
