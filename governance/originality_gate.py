"""Deterministic source-overlap originality gate."""
from __future__ import annotations

import re
from collections import Counter
from math import sqrt

DEFAULT_THRESHOLD = 0.82
MIN_TOKEN_COUNT = 20
NGRAM_SIZE = 5


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _ngrams(tokens: list[str], size: int = NGRAM_SIZE) -> list[tuple[str, ...]]:
    return [tuple(tokens[i:i + size]) for i in range(max(0, len(tokens) - size + 1))]


def _cosine(left: Counter, right: Counter) -> float:
    common = set(left) & set(right)
    dot = sum(left[k] * right[k] for k in common)
    ln = sqrt(sum(v * v for v in left.values()))
    rn = sqrt(sum(v * v for v in right.values()))
    return dot / (ln * rn) if ln and rn else 0.0


def _source_text(source: dict) -> str:
    return " ".join(
        str(source.get(k, "")).strip()
        for k in ("title", "summary", "excerpt", "evidence")
        if source.get(k)
    ).strip()


def _longest_shared_run(left: list[str], right: list[str]) -> int:
    """Return the longest contiguous token sequence shared by both texts."""
    if not left or not right:
        return 0
    right_positions: dict[str, list[int]] = {}
    for index, token in enumerate(right):
        right_positions.setdefault(token, []).append(index)
    best = 0
    for left_index, token in enumerate(left):
        for right_index in right_positions.get(token, []):
            run = 0
            while (
                left_index + run < len(left)
                and right_index + run < len(right)
                and left[left_index + run] == right[right_index + run]
            ):
                run += 1
            best = max(best, run)
    return best


def check(script: str, sources=None, threshold: float = DEFAULT_THRESHOLD) -> dict:
    if not script.strip():
        return {"passed": False, "reason": "empty_script"}

    tokens = _tokens(script)
    if len(tokens) < MIN_TOKEN_COUNT:
        return {
            "passed": False,
            "reason": "script_too_short_for_originality_check",
            "token_count": len(tokens),
        }

    usable = [s for s in list(sources or []) if _source_text(s)]
    if not usable:
        return {"passed": False, "reason": "source_evidence_required", "threshold": threshold}

    script_ngrams = Counter(_ngrams(tokens))
    matches = []
    for source in usable:
        source_tokens = _tokens(_source_text(source))
        overlap = script_ngrams & Counter(_ngrams(source_tokens))
        similarity = _cosine(Counter(tokens), Counter(source_tokens))
        matches.append(
            {
                "title": source.get("title", ""),
                "url": source.get("url", ""),
                "cosine_similarity": round(similarity, 4),
                "shared_ngrams": sum(overlap.values()),
                "longest_shared_ngram": _longest_shared_run(tokens, source_tokens),
            }
        )

    if not matches:
        return {"passed": False, "reason": "no_comparable_source_evidence"}

    highest = max(matches, key=lambda x: x["cosine_similarity"])
    passed = (
        highest["cosine_similarity"] < threshold
        and highest["longest_shared_ngram"] < 12
    )
    return {
        "passed": passed,
        "reason": "originality_check_passed" if passed else "source_overlap_too_high",
        "threshold": threshold,
        "highest_similarity": highest["cosine_similarity"],
        "matches": matches,
    }
