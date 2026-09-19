from __future__ import annotations
import re
from core.contracts.research import ResearchBundle, Source
from core.research.adapters import wikipedia,wikidata,duckduckgo
from core.research.credibility import score_source
from core.research.dedupe import dedupe_sources
from core.research.claim_extractor import extract_claims

MIN_SOURCES=3; MIN_CREDIBLE=2

def _entities(sources):
    words=[]
    for s in sources:
        for token in re.findall(r"\b[A-Z][A-Za-z0-9&.-]{2,}\b",s.text or s.title):
            if token not in words: words.append(token)
    return words[:20]

def _keywords(topic,sources):
    text=" ".join([topic]+[s.title for s in sources]); counts={}
    for word in re.findall(r"[A-Za-z][A-Za-z0-9-]{3,}",text.lower()): counts[word]=counts.get(word,0)+1
    return [w for w,_ in sorted(counts.items(),key=lambda x:(-x[1],x[0]))[:15]]

def _outline(topic,claims):
    lines=[f"What is {topic}?","Key facts and context"]
    lines.extend(c.text for c in claims if c.corroborated) ; return lines[:8]

def _confidence(bundle):
    source_factor=min(1,len(bundle.sources)/MIN_SOURCES); credible_factor=min(1,len([s for s in bundle.sources if s.credibility>=.6])/MIN_CREDIBLE)
    corroborated=sum(c.corroborated for c in bundle.claims)/max(1,len(bundle.claims))
    return round(.4*source_factor+.3*credible_factor+.3*corroborated,2)

def run_research(run_id,topic,language="en",content_type="ai_it_future_tech",target_duration_sec=300):
    bundle=ResearchBundle(run_id=run_id,topic=topic,language=language,content_type=content_type,target_duration_sec=target_duration_sec)
    raw=[]
    for adapter in (wikipedia,wikidata,duckduckgo):
        try: raw.extend(adapter.fetch(topic,language))
        except Exception as exc: bundle.warnings.append(f"adapter_error:{adapter.__name__}:{type(exc).__name__}")
    raw=dedupe_sources(raw)
    raw.sort(key=score_source,reverse=True)
    for i,s in enumerate(raw,1): s.id=f"S{i}"; s.credibility=score_source(s)
    bundle.sources=raw
    bundle.claims=extract_claims(topic,raw)
    bundle.entities=_entities(raw); bundle.keywords=_keywords(topic,raw); bundle.outline=_outline(topic,bundle.claims)
    if len(bundle.sources)<MIN_SOURCES: bundle.warnings.append(f"only_{len(bundle.sources)}_sources")
    credible=[s for s in bundle.sources if s.credibility>=.6]
    if len(credible)<MIN_CREDIBLE: bundle.warnings.append(f"only_{len(credible)}_credible_sources")
    if not bundle.claims: bundle.warnings.append("no_claims_extracted")
    bundle.confidence=_confidence(bundle)
    return bundle
