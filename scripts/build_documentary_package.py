"""Build a review-only documentary production package from a validated episode."""
from pathlib import Path
import json, re, sys

ROOT=Path(__file__).resolve().parents[1]
ep_path=ROOT/"documentary/episode.json"
out=ROOT/"output/documentary"
out.mkdir(parents=True,exist_ok=True)

if not ep_path.exists():
    print("No documentary/episode.json supplied; package not generated.")
    raise SystemExit(0)

ep=json.loads(ep_path.read_text(encoding="utf-8"))
if len(ep.get("acts",[])) < 6: raise SystemExit("Blocked: minimum 6 acts required.")
if any(a.get("voice") not in {"girl","boy"} for a in ep["acts"]): raise SystemExit("Blocked: invalid voice.")
if any(s.get("verification_status")!="verified" for s in ep.get("sources",[])): raise SystemExit("Blocked: every source must be verified.")

words=sum(len(re.findall(r"\b[\w’'-]+\b",a.get("text",""))) for a in ep["acts"])
minutes=words/150
if not 15 <= minutes <= 30: raise SystemExit(f"Blocked: estimated duration {minutes:.1f} min outside 15–30.")

lines=[
f"# {ep['title']}",
"",
"## Cold Open",
ep["hook"],"",
"## Documentary Acts"
]
for i,a in enumerate(ep["acts"],1):
    lines += [f"### {i}. {a['name']}", f"**Voice:** {a['voice']}", "", a["text"], "", f"**Visual direction:** {a['visual_direction']}"]
    refs=a.get("evidence_refs",[])
    if refs: lines += [f"**Evidence refs:** {', '.join(refs)}"]
    lines.append("")
lines += ["## Sources"]
for i,s in enumerate(ep["sources"],1):
    lines += [f"{i}. {s['name']} — {s['url']} — verification: {s['verification_status']}"]
lines += ["","## Editorial QA","- Source verification: REQUIRED","- Originality check: REQUIRED","- Voice QA: REQUIRED","- Caption QA: REQUIRED","- Visual QA: REQUIRED","- Human review: REQUIRED","- Public YouTube publish: DISABLED"]
(out/"documentary-script.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

manifest={
 "status":"REVIEW_REQUIRED","title":ep["title"],"master_language":"en",
 "format":"long_form_documentary","estimated_minutes":round(minutes,2),
 "word_count":words,"acts":len(ep["acts"]),
 "voice_plan":[{"act":i+1,"voice":a["voice"]} for i,a in enumerate(ep["acts"])],
 "visual_plan":[{"act":i+1,"direction":a["visual_direction"]} for i,a in enumerate(ep["acts"])],
 "sources":ep["sources"],"source_verification":"passed",
 "gates":{"originality_check":"required","voice_qa":"required","caption_qa":"required","visual_qa":"required","human_review":"required"},
 "public_youtube_publish":False,"fail_closed":True
}
(out/"documentary-manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps(manifest,indent=2,ensure_ascii=False))
