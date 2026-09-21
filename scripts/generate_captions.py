"""Generate deterministic sentence-level SRT captions for the production review video."""

from __future__ import annotations

import re
from pathlib import Path


def _timestamp(seconds: float) -> str:
    milliseconds = int(round(seconds * 1000))
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    seconds_int, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds_int:02d},{milliseconds:03d}"


def generate_captions(text: str, duration: float, output_path: str) -> None:
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text.strip()) if part.strip()]
    if not sentences or duration <= 0:
        raise ValueError("captions_require_text_and_positive_duration")

    weights = [max(1, len(sentence.split())) for sentence in sentences]
    total_weight = sum(weights)
    current = 0.0
    blocks = []

    for index, (sentence, weight) in enumerate(zip(sentences, weights), 1):
        end = duration if index == len(sentences) else current + duration * weight / total_weight
        blocks.append(
            f"{index}\n{_timestamp(current)} --> {_timestamp(end)}\n{sentence}\n"
        )
        current = end

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(blocks), encoding="utf-8")
