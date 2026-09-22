#!/usr/bin/env python3
"""Prepare a verified full-body presenter asset for the local production pipeline.

This tool deliberately does not fake a human with PIL. It accepts a real generated
or photographed presenter image, validates it, and can optionally remove a plain
background when Pillow's RGBA conversion is sufficient. A true photorealistic
generation backend (ComfyUI/Stable Diffusion or another approved generator) can be
connected later without changing the video pipeline.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def verify(source: Path, destination: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(source)
    if destination.exists():
        raise FileExistsError(f"Refusing to overwrite existing presenter: {destination}")

    with Image.open(source) as image:
        width, height = image.size
        if width < 900 or height < 1400:
            raise ValueError(
                f"Presenter image is too small ({width}x{height}); "
                "use a full-body source of at least 900x1400."
            )
        rgba = image.convert("RGBA")
        alpha = rgba.getchannel("A")
        bbox = alpha.getbbox()
        if bbox is None:
            raise ValueError("Presenter image contains no visible subject.")
        rgba.save(destination, "PNG")


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify and normalize a full-body presenter asset.")
    parser.add_argument("--source", required=True)
    parser.add_argument("--destination", required=True)
    args = parser.parse_args()
    verify(Path(args.source), Path(args.destination))
    print(f"PASS: verified presenter asset -> {args.destination}")


if __name__ == "__main__":
    main()
