from urllib.parse import urlparse
from core.contracts.research import Source

WHITELIST={"wikipedia.org":0.75,"wikidata.org":0.75,"nature.com":0.9,"science.org":0.9,"arxiv.org":0.8,"openalex.org":0.85,"who.int":0.9,"nasa.gov":0.9,"ieee.org":0.85,"acm.org":0.85}

def score_source(source: Source)->float:
    host=(urlparse(str(source.url)).hostname or "").lower().removeprefix("www.")
    base=0.5
    for domain,value in WHITELIST.items():
        if host==domain or host.endswith("."+domain): base=value; break
    if source.source_type=="gov": base=max(base,0.85)
    if source.source_type=="academic": base=max(base,0.8)
    if source.source_type=="blog": base=min(base,0.4)
    return round(base,2)
