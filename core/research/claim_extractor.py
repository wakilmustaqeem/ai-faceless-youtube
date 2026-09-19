from __future__ import annotations
import re
from collections import Counter
from core.contracts.research import Claim, Source
SENT_SPLIT=re.compile(r"(?<=[.!?])\\s+")

def _sentences_for(source: Source):
    return [s.strip() for s in SENT_SPLIT.split(source.text or "") if len(s.strip())>=40]

def _tokens(text): return set(re.findall(r"[\\w-]{4,}",text.lower()))

def extract_claims(topic: str, sources: list[Source])->list[Claim]:
    claims=[]
    for source in sources[:6]:
        for sent in _sentences_for(source)[:8]:
            claims.append(Claim(id=f"C{len(claims)+1}",text=sent,source_ids=[source.id],corroborated=False,confidence=min(.9,source.credibility)))
    for claim in claims:
        a=_tokens(claim.text)
        refs={c.source_ids[0] for c in claims if c.id!=claim.id and a and len(a & _tokens(c.text))/max(1,len(a|_tokens(c.text)))>=.35}
        if refs: claim.source_ids=sorted(set(claim.source_ids)|refs); claim.corroborated=len(claim.source_ids)>=2
    return claims
