#!/usr/bin/env python3
"""Local presenter studio diagnostics.

Checks only local prerequisites; it never downloads models, calls paid APIs, or
writes/overwrites assets.
"""
from __future__ import annotations

import argparse
import importlib.util
import os
from pathlib import Path


def check_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def main() -> int:
    parser = argparse.ArgumentParser(description="Diagnose local presenter generation prerequisites.")
    parser.add_argument("--model", default=os.getenv("PRESENTER_MODEL_PATH", ""))
    args = parser.parse_args()

    ok = True
    print("LOCAL PRESENTER DIAGNOSTICS")
    print("=" * 30)

    for name in ("torch", "diffusers"):
        present = check_module(name)
        print(f"{name}: {'READY' if present else 'MISSING'}")
        ok &= present

    model = Path(args.model).expanduser() if args.model else None
    if model:
        print(f"model path: {model}")
        print(f"model exists: {'READY' if model.exists() else 'MISSING'}")
        ok &= model.exists()
    else:
        print("model path: MISSING (set PRESENTER_MODEL_PATH or pass --model)")
        ok = False

    if check_module("torch"):
        import torch
        print(f"torch version: {torch.__version__}")
        print(f"CUDA: {'READY' if torch.cuda.is_available() else 'CPU ONLY'}")

    print("=" * 30)
    if ok:
        print("STATUS: READY for local presenter generation.")
        return 0
    print("STATUS: NOT READY — no model download was attempted.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
