from __future__ import annotations
import json
from pathlib import Path
from core.config import flags
from core.contracts.research import ResearchBundle
from core.research.engine import run_research

def stage_research(run_id: str, topic: str, language: str = "en", **kwargs) -> ResearchBundle | None:
    if not flags.ENABLE_RESEARCH:
        return None
    bundle=run_research(run_id,topic,language,**kwargs)
    run_dir=Path("runs")/run_id; run_dir.mkdir(parents=True,exist_ok=True)
    (run_dir/"research.json").write_text(bundle.model_dump_json(indent=2),encoding="utf-8")
    if any(w.startswith("only_") for w in bundle.warnings):
        return None
    return bundle
