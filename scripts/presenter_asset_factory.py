#!/usr/bin/env python3
"""Prepare a verified full-body presenter asset for the local production pipeline.

This tool deliberately does not fake a human with PIL. It accepts a real generated
or photographed presenter image, validates dimensions and image content, and can
normalize it to PNG. Semantic human detection is outside this local dependency
scope, so this check is reported as image-content QA rather than human identity QA.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageFilter, ImageStat


def _has_image_content(image: Image.Image) -> bool:
    """Return whether the image contains meaningful non-uniform visual content."""
    grayscale = image.convert("L")
    stddev = ImageStat.Stat(grayscale).stddev[0]
    edges = grayscale.filter(ImageFilter.FIND_EDGES)
    edge_count = sum(1 for value in edges.getdata() if value >= 24)
    return stddev >= 5.0 and edge_count >= max(100, image.width * image.height // 5000)


def verify(source: Path, destination: Path) -> None:
    """Validate dimensions/content and save a normalized PNG without overwriting."""
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
        if not _has_image_content(image):
            raise ValueError(
                "Presenter image failed image-content QA: the image appears blank "
                "or nearly uniform. Semantic human detection is not available."
            )
        rgba = image.convert("RGBA")
        destination.parent.mkdir(parents=True, exist_ok=True)
        rgba.save(destination, "PNG")


def main() -> None:
    """Parse CLI arguments and run presenter image-content QA."""
    parser = argparse.ArgumentParser(description="Verify and normalize a full-body presenter asset.")
    parser.add_argument("--source", required=True)
    parser.add_argument("--destination", required=True)
    args = parser.parse_args()
    verify(Path(args.source), Path(args.destination))
    print(f"PASS: presenter image-content QA -> {args.destination}")


if __name__ == "__main__":
    main()
