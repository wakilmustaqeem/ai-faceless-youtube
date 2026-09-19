def dedupe_sources(sources):
    seen_urls=set(); seen_titles=set(); out=[]
    for source in sources:
        url=str(source.url).rstrip("/").lower(); title=source.title.strip().lower()
        if url in seen_urls or title in seen_titles: continue
        seen_urls.add(url); seen_titles.add(title); out.append(source)
    return out
