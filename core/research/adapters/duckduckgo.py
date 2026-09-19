from __future__ import annotations
import json, urllib.parse, urllib.request
from core.contracts.research import Source


def fetch(topic: str, language: str, max_results: int = 8) -> list[Source]:
    params=urllib.parse.urlencode({"q":topic,"format":"json","no_html":"1","no_redirect":"1"})
    url=f"https://api.duckduckgo.com/?{params}"
    req=urllib.request.Request(url,headers={"User-Agent":"ai-faceless-youtube/1.0 research-bot"})
    with urllib.request.urlopen(req,timeout=10) as response: data=json.load(response)
    candidates=[]
    if data.get("AbstractURL"):
        candidates.append((data.get("Heading") or topic,data["AbstractURL"],data.get("AbstractText") or ""))
    def walk(items):
        for item in items or []:
            if item.get("FirstURL"): yield item.get("Text") or topic,item["FirstURL"],item.get("Text") or ""
            yield from walk(item.get("Topics"))
    candidates.extend(walk(data.get("RelatedTopics")))
    out=[]
    seen=set()
    for title,url,text in candidates:
        if url in seen: continue
        seen.add(url)
        out.append(Source(id="",url=url,title=title,publisher="DuckDuckGo",language="en",source_type="other",credibility=0.5,text=text))
        if len(out)>=max_results: break
    return out
