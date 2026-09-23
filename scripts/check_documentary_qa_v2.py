"""Fail-closed Documentary QA v2: evidence chain, multimedia verification and provenance."""
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[1]
EP=ROOT/"documentary/episode.json"
ASSETS=ROOT/"documentary/assets.json"
QA=ROOT/"documentary/qa-manifest.json"
fail=[]; flags=[]

if not EP.exists():
    print("No documentary/episode.json supplied; QA v2 remains pending.")
    raise SystemExit(0)

e=json.loads(EP.read_text(encoding="utf-8"))
claims=e.get("claims") or e.get("evidence_chain") or []
if not claims:
    fail.append("evidence_chain: claim-level chain is required")

sources={f"source-{i+1}" for i,_ in enumerate(e.get("sources",[]))}
acts={f"act-{i+1}" for i,_ in enumerate(e.get("acts",[]))}
for i,c in enumerate(claims,1):
    if not c.get("claim_id") or not c.get("claim"): fail.append(f"evidence_chain: claim {i} missing claim_id/claim")
    if not set(c.get("source_ids",[])).issubset(sources): fail.append(f"evidence_chain: claim {i} references unknown source")
    if not c.get("evidence"): fail.append(f"evidence_chain: claim {i} missing evidence")
    if not c.get("script_refs"): fail.append(f"evidence_chain: claim {i} missing script refs")
    if not c.get("voice_refs"): fail.append(f"evidence_chain: claim {i} missing voice refs")
    if not c.get("visual_refs"): fail.append(f"evidence_chain: claim {i} missing visual refs")
    if not c.get("timestamp_refs"): fail.append(f"evidence_chain: claim {i} missing timestamp refs")

if not ASSETS.exists():
    fail.append("multimedia: documentary/assets.json is required")
else:
    a=json.loads(ASSETS.read_text(encoding="utf-8"))
    for i,x in enumerate(a.get("assets",[]),1):
        required=("asset_id","source_type","generation_method","reference","timestamp","verification_status")
        if any(not x.get(k) for k in required): fail.append(f"provenance: asset {i} missing required provenance field")
        for k in ("origin","authenticity","context","temporal_geographic_consistency","manipulation_signals"):
            if k not in x: fail.append(f"multimedia: asset {i} missing {k}")
        if x.get("verification_status") != "verified":
            fail.append(f"multimedia: asset {i} is not verified")
        ai=x.get("ai_detection") or {}
        if ai.get("status") in {"flagged","inconclusive"}:
            flags.append(f"asset {i}: AI detector result is {ai.get('status')}; human review remains required")

disclosure=e.get("ai_disclosure_required")
if disclosure is not True:
    fail.append("disclosure: AI disclosure must be explicitly enabled for documentary production")
if e.get("ai_disclosure_reason") in {None,""}:
    fail.append("disclosure: ai_disclosure_reason is required")

approval=e.get("human_approval_status","pending")
if approval != "approved":
    flags.append("publication authority: human approval is not granted")

manifest={
 "schema_version":"2.0","status":"BLOCKED" if fail else "REVIEW_REQUIRED",
 "evidence_chain":"blocked" if any(x.startswith("evidence_chain") for x in fail) else "passed",
 "multimedia_verification":"blocked" if any(x.startswith("multimedia") for x in fail) else "passed",
 "synthetic_asset_provenance":"blocked" if any(x.startswith("provenance") for x in fail) else "passed",
 "ai_detection":"assistive_only",
 "disclosure":"blocked" if any(x.startswith("disclosure") for x in fail) else "passed",
 "human_approval":"approved" if approval=="approved" else "pending",
 "flags":flags,"failures":fail,
 "public_youtube_publish_allowed":False,"human_review_required":True,"fail_closed":True
}
QA.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps(manifest,indent=2,ensure_ascii=False))
if fail: raise SystemExit(1)
