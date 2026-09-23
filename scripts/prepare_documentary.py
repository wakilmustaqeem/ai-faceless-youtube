"""Build a long-form documentary production package from a verified episode JSON."""
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "documentary/documentary-spec.json"
VOICES = ROOT / "documentary/voice-profiles.json"
EPISODE = ROOT / "documentary/episode.json"
OUT = ROOT / "output/documentary"
OUT.mkdir(parents=True, exist_ok=True)

spec = json.loads(SPEC.read_text(encoding="utf-8"))
voices = json.loads(VOICES.read_text(encoding="utf-8"))
episode = json.loads(EPISODE.read_text(encoding="utf-8")) if EPISODE.exists() else None

required = ["title", "hook", "acts", "sources"]
if not episode or any(k not in episode for k in required):
    raise SystemExit("Documentary blocked: documentary/episode.json with title, hook, acts and sources is required.")
if not episode["sources"]:
    raise SystemExit("Documentary blocked: at least one verified source is required.")
if not isinstance(episode["acts"], list) or len(episode["acts"]) < 6:
    raise SystemExit("Documentary blocked: provide at least 6 narrative acts.")
if any(not a.get("text") or not a.get("voice") for a in episode["acts"]):
    raise SystemExit("Documentary blocked: every act needs text and an approved voice profile.")
if any(a["voice"] not in {"girl", "boy"} for a in episode["acts"]):
    raise SystemExit("Documentary blocked: only configured girl/boy voices are allowed.")

word_count = sum(len(re.findall(r"\b\w+[’'-]?\w*\b", a["text"])) for a in episode["acts"])
minutes_at_150wpm = word_count / 150
lo, hi = spec["acceptable_minutes"]
if not (lo <= minutes_at_150wpm <= hi):
    raise SystemExit(f"Documentary blocked: estimated narration is {minutes_at_150wpm:.1f} min; target is {lo}-{hi} min.")

for src in episode["sources"]:
    if not src.get("url") or src.get("verification_status") != "verified":
        raise SystemExit("Documentary blocked: every source must have a URL and verification_status=verified.")

script_lines = [f"# {episode['title']}", "", episode["hook"], ""]
for i, act in enumerate(episode["acts"], 1):
    voice = voices["voices"][act["voice"]]
    script_lines += [f"## Act {i} — {act.get('name','')}", f"Voice: {voice['voice']}", "", act["text"], ""]
script_lines += ["## Sources", ""]
for src in episode["sources"]:
    script_lines.append(f"- {src['name']}: {src['url']}")
(OUT / "documentary-script.md").write_text("\n".join(script_lines), encoding="utf-8")

manifest = {
    "status": "REVIEW_REQUIRED",
    "brand": spec["brand"],
    "title": episode["title"],
    "master_language": "en",
    "estimated_minutes": round(minutes_at_150wpm, 2),
    "word_count": word_count,
    "voices": sorted(set(a["voice"] for a in episode["acts"])),
    "source_count": len(episode["sources"]),
    "source_verification": "passed",
    "public_youtube_publish_allowed": False,
    "human_review_required": True
}
(OUT / "documentary-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(json.dumps(manifest, indent=2))
