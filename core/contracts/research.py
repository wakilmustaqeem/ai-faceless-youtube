from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field, HttpUrl

Language = Literal["ur", "en", "hi", "ar"]

class Source(BaseModel):
    id: str
    url: HttpUrl
    title: str
    publisher: str | None = None
    published_at: str | None = None
    language: Language = "en"
    source_type: Literal["encyclopedia", "news", "academic", "gov", "blog", "other"] = "other"
    credibility: float = Field(default=0.5, ge=0.0, le=1.0)
    text: str = ""

class Claim(BaseModel):
    id: str
    text: str
    source_ids: list[str] = Field(default_factory=list)
    corroborated: bool = False
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)

class ResearchBundle(BaseModel):
    run_id: str
    topic: str
    language: Language
    audience: str = "general"
    content_type: Literal["ai_it_future_tech", "science", "history", "other"] = "ai_it_future_tech"
    target_duration_sec: int = Field(default=300, gt=0)
    sources: list[Source] = Field(default_factory=list)
    claims: list[Claim] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    outline: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
