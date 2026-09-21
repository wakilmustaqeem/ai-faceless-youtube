"""Deterministic SRT captions quality gate."""

from __future__ import annotations

import re
from pathlib import Path

TIMESTAMP = re.compile(r"^(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})$")


def _seconds(value: str) -> float:
    match = TIMESTAMP.match(value.strip())
    if not match:
        raise ValueError("invalid_timestamp")
    h1, m1, s1, ms1, h2, m2, s2, ms2 = map(int, match.groups())
    return h1 * 3600 + m1 * 60 + s1 + ms1 / 1000, h2 * 3600 + m2 * 60 + s2 + ms2 / 1000


def check_captions(
    path: str,
    *,
    expected_duration: float | None = None,
    max_cue_seconds: float = 8.0,
    max_gap_seconds: float = 3.0,
) -> dict:
    captions = Path(path)
    if not captions.exists() or captions.stat().st_size == 0:
        return {"passed": False, "reason": "captions_missing_or_empty"}

    try:
        lines = captions.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
        cues = []
        index = 0
        while index < len(lines):
            if not lines[index].strip():
                index += 1
                continue
            if not lines[index].strip().isdigit():
                return {"passed": False, "reason": "invalid_cue_index"}
            index += 1
            if index >= len(lines):
                return {"passed": False, "reason": "missing_timestamp"}
            start, end = _seconds(lines[index])
            index += 1
            text_lines = []
            while index < len(lines) and lines[index].strip():
                text_lines.append(lines[index].strip())
                index += 1
            text = " ".join(text_lines).strip()
            if not text:
                return {"passed": False, "reason": "empty_caption_text"}
            if end <= start:
                return {"passed": False, "reason": "invalid_cue_duration"}
            cues.append((start, end, text))

        if not cues:
            return {"passed": False, "reason": "no_caption_cues"}

        previous_end = 0.0
        for start, end, _ in cues:
            if start < previous_end:
                return {"passed": False, "reason": "caption_overlap"}
            if end - start > max_cue_seconds:
                return {"passed": False, "reason": "caption_cue_too_long", "duration_seconds": end - start}
            if start - previous_end > max_gap_seconds and previous_end > 0:
                return {"passed": False, "reason": "caption_gap_too_long", "gap_seconds": start - previous_end}
            previous_end = end

        if expected_duration is not None:
            if abs(cues[-1][1] - expected_duration) > 1.0:
                return {"passed": False, "reason": "caption_duration_mismatch", "last_end": cues[-1][1], "expected_duration": expected_duration}

        return {
            "passed": True,
            "reason": "captions_quality_passed",
            "cue_count": len(cues),
            "caption_end_seconds": cues[-1][1],
        }
    except (OSError, ValueError):
        return {"passed": False, "reason": "caption_parse_failed"}
