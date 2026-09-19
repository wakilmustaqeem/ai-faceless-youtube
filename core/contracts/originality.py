from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field

class Match(BaseModel):
    kind: Literal["exact_ngram", "semantic", "internal_history", "source_overlap"]
    reference: str
    score: float = Field(ge=0.0, le=1.0)
    snippet: str | None = None

class OriginalityReport(BaseModel):
    run_id: str
    verdict: Literal["PASS", "REWRITE", "FAIL"]
    max_similarity: float = Field(ge=0.0, le=1.0)
    ngram_score: float = Field(ge=0.0, le=1.0)
    semantic_score: float = Field(ge=0.0, le=1.0)
    internal_score: float = Field(ge=0.0, le=1.0)
    matches: list[Match] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
