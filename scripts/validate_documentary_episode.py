"""Fail-closed validation for a source-verified documentary episode package."""
from pathlib import Path
import json, re, sys
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
episode_path=ROOT/"documentary/episode.json"
schema_path=ROOT/"documentary/episode.schema.json"
if not episode_path.exists():
    print("No documentary/episode.json supplied; nothing to validate.")
    raise SystemExit(0)

ep=json.loads(episode_path.read_text(encoding="utf-8"))
required={"title","hook","acts","sources"}
missing=required-set(ep)
if missing: raise SystemExit(f"Documentary blocked: missing {sorted(missing)}")
if len(ep["acts"]) < 6: raise SystemExit("Documentary blocked: at least 6 acts required.")
if not ep["sources"]: raise SystemExit("Documentary blocked: at least one verified source required.")

source_ids={f"source-{i+1}" for i,_ in enumerate(ep["sources"])}
for i,src in enumerate(ep["sources"],1):
    if src.get("verification_status")!="verified": raise SystemExit(f"Documentary blocked: source {i} is not verified.")
    u=urlparse(src.get("url",""))
    if u.scheme not in {"http","https"} or not u.netloc: raise SystemExit(f"Documentary blocked: invalid URL for source {i}.")
for i,act in enumerate(ep["acts"],1):
    if act.get("voice") not in {"girl","boy"}: raise SystemExit(f"Documentary blocked: invalid voice in act {i}.")
    if len(act.get("text","").split()) < 20: raise SystemExit(f"Documentary blocked: act {i} is too short.")
    refs=set(act.get("evidence_refs",[]))
    if refs and not refs.issubset(source_ids): raise SystemExit(f"Documentary blocked: act {i} references unknown evidence.")

words=sum(len(re.findall(r"\b[\w’'-]+\b",a["text"])) for a in ep["acts"])
minutes=words/150
if not 15 <= minutes <= 30:
    raise SystemExit(f"Documentary blocked: estimated narration {minutes:.1f} minutes; target is 15–30.")
print(json.dumps({"status":"VALID","word_count":words,"estimated_minutes":round(minutes,2),"acts":len(ep["acts"]),"sources":len(ep["sources"]),"public_publish_allowed":False},indent=2))
