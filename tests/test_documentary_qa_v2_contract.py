import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_qa_v2_policy_locks_human_authority():
    policy = json.loads((ROOT / "documentary/qa-policy-v2.json").read_text(encoding="utf-8"))
    assert policy["ai_detection"]["authority"] == "assistive_only"
    assert policy["ai_detection"]["final_authority"] == "human"
    assert policy["public_publish_allowed"] is False
    assert policy["human_review_required"] is True
    assert policy["fail_closed"] is True

def test_evidence_chain_schema_contains_full_trace():
    schema = json.loads((ROOT / "documentary/evidence-chain.schema.json").read_text(encoding="utf-8"))
    required = set(schema["properties"]["claims"]["items"]["required"])
    assert {"claim_id","claim","source_ids","evidence","script_refs","voice_refs","visual_refs","timestamp_refs"} <= required

def test_multimedia_schema_requires_verification_layers():
    schema = json.loads((ROOT / "documentary/multimedia-verification.schema.json").read_text(encoding="utf-8"))
    required = set(schema["properties"]["assets"]["items"]["required"])
    assert {"origin","authenticity","context","temporal_geographic_consistency","manipulation_signals","verification_status","human_approval_required"} <= required

def test_provenance_schema_requires_synthetic_asset_fields():
    schema = json.loads((ROOT / "documentary/asset-provenance.schema.json").read_text(encoding="utf-8"))
    required = set(schema["properties"]["assets"]["items"]["required"])
    assert {"asset_id","source_type","generation_method","reference","timestamp","verification_status"} <= required
