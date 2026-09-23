"""Fail-closed pre-publication compliance checks; no publishing or API calls."""
from pathlib import Path
import json, re, sys

ROOT=Path(__file__).resolve().parents[1]
ep=ROOT/"documentary/episode.json"
assets=ROOT/"documentary/assets.json"
policy=ROOT/"documentary/compliance-policy.json"
out=ROOT/"output/documentary"
out.mkdir(parents=True,exist_ok=True)

if not ep.exists():
    print("No episode supplied; compliance gate remains pending.")
    raise SystemExit(0)

e=json.loads(ep.read_text(encoding="utf-8"))
p=json.loads(policy.read_text(encoding="utf-8"))
fail=[]; notes=[]

# Originality / anti-mass-production
texts=[e.get("hook","")]+[a.get("text","") for a in e.get("acts",[])]
joined=" ".join(texts).strip()
if len(joined.split()) < 2250: fail.append("originality_gate: documentary narration is below the 15-minute minimum")
if len(e.get("acts",[])) < 6: fail.append("originality_gate: fewer than 6 acts")
if len({a.get("name","").strip().lower() for a in e.get("acts",[])}) != len(e.get("acts",[])): fail.append("originality_gate: duplicate act names")
if "REPLACE WITH" in joined.upper(): fail.append("originality_gate: placeholder text remains")
notes.append("originality gate is structural; it does not claim external plagiarism detection")

# Sources / reused content
for i,s in enumerate(e.get("sources",[]),1):
    if s.get("verification_status")!="verified": fail.append(f"source_gate: source {i} is not verified")

# Asset provenance
if not assets.exists():
    fail.append("rights_gate: documentary/assets.json is required")
else:
    a=json.loads(assets.read_text(encoding="utf-8"))
    for i,x in enumerate(a.get("assets",[]),1):
        if x.get("rights_status") in {"unknown","permission_required"}: fail.append(f"rights_gate: asset {i} has unresolved rights")
        if x.get("commercial_use_allowed") is not True: fail.append(f"rights_gate: asset {i} lacks confirmed commercial-use permission")
        if x.get("attribution_required") and not x.get("attribution"): fail.append(f"rights_gate: asset {i} requires attribution but attribution is missing")

# AI disclosure
ai=e.get("ai_disclosure_required")
if ai not in {True,False}: fail.append("ai_disclosure_gate: episode must explicitly set ai_disclosure_required true/false")
if ai is True and e.get("ai_disclosure_reason") in {None,""}: notes.append("AI disclosure is required; final upload must carry the applicable YouTube altered/synthetic-content disclosure")

# Safety / advertiser pre-check: deterministic metadata flags only; human review remains authoritative
risk_terms=r"\b(graphic gore|explicit sexual|sexual nudity|instructions to harm|targeted harassment)\b"
if re.search(risk_terms, joined, re.I): fail.append("safety_gate: potentially restricted content requires human review/remediation")
notes.append("community-guidelines and advertiser-suitability checks remain human editorial gates; this script does not make a policy determination")

# Metadata
meta=e.get("metadata",{})
for k in ("title","description","thumbnail_concept"):
    if not meta.get(k): fail.append(f"metadata_gate: missing {k}")
if len(meta.get("title","")) > 100: fail.append("metadata_gate: title exceeds 100 characters")

status="BLOCKED" if fail else "REVIEW_REQUIRED"
manifest={
 "status":status,"public_youtube_publish_allowed":False,"human_review_required":True,
 "gates":{
   "originality":"blocked" if any(x.startswith("originality_gate") for x in fail) else "passed",
   "reused_content":"review_required",
   "asset_rights":"blocked" if any(x.startswith("rights_gate") for x in fail) else "passed",
   "ai_disclosure":"blocked" if any(x.startswith("ai_disclosure_gate") for x in fail) else "passed",
   "community_guidelines":"human_review_required",
   "advertiser_suitability":"human_review_required",
   "metadata":"blocked" if any(x.startswith("metadata_gate") for x in fail) else "passed"
 },
 "failures":fail,"notes":notes
}
(out/"compliance-manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps(manifest,indent=2,ensure_ascii=False))
if fail: raise SystemExit(1)
