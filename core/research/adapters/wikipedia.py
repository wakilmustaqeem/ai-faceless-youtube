from __future__ import annotations
import json
import urllib.parse
import urllib.request
from core.contracts.research import Source


def fetch(topic: str, language: str) -> list[Source]:
    lang = {"ur":"ur","en":"en","hi":"hi","ar":"ar"}.get(language, "en")
    params = urllib.parse.urlencode({"action":"query","format":"json","list":"search","srsearch":topic,"srlimit":3})
    url = f"https://{lang}.wikipedia.org/w/api.php?{params}"
    req = urllib.request.Request(url, headers={"User-Agent":"ai-faceless-youtube/1.0 research-bot"})
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.load(response)
    out=[]
    for item in data.get("query",{}).get("search",[]):
        title=item["title"]
        page_params=urllib.parse.urlencode({"action":"query","format":"json","prop":"extracts|info","exintro":"1","explaintext":"1","inprop":"url","titles":title})
        page_url=f"https://{lang}.wikipedia.org/w/api.php?{page_params}"
        page_req=urllib.request.Request(page_url,headers={"User-Agent":"ai-faceless-youtube/1.0 research-bot"})
        try:
            with urllib.request.urlopen(page_req,timeout=10) as response: page_data=json.load(response)
            pages=page_data.get("query",{}).get("pages",{})
            page=next(iter(pages.values()),{})
            canonical=page.get("fullurl") or f"https://{lang}.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ','_'))}"
            extract=page.get("extract","")
        except Exception:
            canonical=f"https://{lang}.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ','_'))}"; extract=""
        out.append(Source(id="",url=canonical,title=title,publisher="Wikipedia",language=lang,source_type="encyclopedia",credibility=0.75,text=extract))
    return out
