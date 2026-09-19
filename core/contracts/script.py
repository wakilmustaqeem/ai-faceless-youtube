from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field
from .research import Language

class Scene(BaseModel):
    scene_id: str
    narration: str
    visual_prompt: str
    broll_keywords: list[str] = Field(default_factory=list)
    text_overlay: str | None = None
    duration_sec: float = Field(gt=0)
    citation_ids: list[str] = Field(default_factory=list)

class ScriptPackage(BaseModel):
    run_id: str
    language: Language
    title_options: list[str] = Field(min_length=1)
    hook: str
    structure: Literal["listicle", "explainer", "narrative", "comparison", "news", "story"] = "explainer"
    scenes: list[Scene] = Field(min_length=1)
    total_duration_sec: float = Field(gt=0)
    word_count: int = Field(ge=0)
    citations: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
