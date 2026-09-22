#!/usr/bin/env python3
"""Optional local photorealistic presenter generator.

Uses a diffusion model that is already installed locally. It never downloads a
model and never overwrites an existing asset. If diffusers/torch or a local
model is missing, the command fails clearly instead of creating a fake placeholder.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path


def generate(prompt: str, output: Path, model_path: Path) -> None:
    """Generate a presenter image from an already-installed local diffusion model."""
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite existing presenter: {output}")
    if not model_path.exists():
        raise FileNotFoundError(
            f"Local diffusion model not found: {model_path}. "
            "Install/download an approved model separately, then point PRESENTER_MODEL_PATH to it."
        )

    try:
        import torch
        from diffusers import DiffusionPipeline
    except ImportError as exc:
        raise RuntimeError(
            "Local presenter generation needs torch and diffusers. "
            "The GUI still supports supplied assets and ElevenLabs/Edge-TTS without them."
        ) from exc

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32
    pipe = DiffusionPipeline.from_pretrained(
        str(model_path), torch_dtype=dtype, local_files_only=True
    ).to(device)
    image = pipe(
        prompt=prompt, height=1536, width=1024,
        num_inference_steps=30, guidance_scale=6.5,
    ).images[0]

    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, "PNG")
    if output.stat().st_size == 0:
        raise RuntimeError("Presenter generation produced an empty file.")
    print(f"PASS: generated local presenter -> {output}")


def main() -> None:
    """Parse CLI arguments and run local presenter generation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", default=os.getenv(
        "PRESENTER_PROMPT",
        "photorealistic full-body adult technology presenter, standing naturally, "
        "professional modern outfit, realistic proportions, natural skin texture, "
        "friendly confident expression, cinematic studio lighting, feet visible, "
        "clean professional technology studio, no text, no logo"
    ))
    parser.add_argument("--model", default=os.getenv("PRESENTER_MODEL_PATH", ""))
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if not args.model:
        raise SystemExit("Set PRESENTER_MODEL_PATH to an already-installed local diffusion model.")
    generate(args.prompt, Path(args.output), Path(args.model))


if __name__ == "__main__":
    main()
