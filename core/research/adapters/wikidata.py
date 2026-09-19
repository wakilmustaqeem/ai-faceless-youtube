from __future__ import annotations
import json, urllib.parse, urllib.request
from core.contracts.research import Source


def fetch(topic: str, language: str) -> list[Source]:
    params=urllib.parse.urlencode({"action":"wbsearchentities","search":topic,"language":language if language in {"en","ur","hi","ar"} else "en","format":"json","limit":3})
    url=f"https://www.wikidata.org/w/api.php?{params}"
    req=urllib.request.Request(url,headers={"User-Agent":"ai-faceless-youtube/1.0 research-bot"})
    with urllib.request.urlopen(req,timeout=10) as response: data=json.load(response)
    out=[]
    for item in data.get("search",[]):
        qid=item.get("id")
        if not qid: continue
        label=item.get("label") or qid
        desc=item.get("description") or ""
        out.append(Source(id="",url=f"https://www.wikidata.org/wiki/{qid}",title=label,publisher="Wikidata",language="en",source_type="encyclopedia",credibility=0.75,text=f"{label}. {desc}"))
    return out
