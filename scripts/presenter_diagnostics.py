#!/usr/bin/env python3
"""Local presenter studio diagnostics.

Checks only local prerequisites; it never downloads models, calls paid APIs, or
writes/overwrites assets.
"""
from __future__ import annotations

import argparse
import importlib
import os
from pathlib import Path


def check_module(name: str):
    """Import a dependency and return its module, or None when initialization fails."""
    try:
        return importlib.import_module(name)
    except Exception:
        return None


def main() -> int:
    """Run dependency/model checks and return a nonzero code when not ready."""
    parser = argparse.ArgumentParser(description="Diagnose local presenter generation prerequisites.")
    parser.add_argument("--model", default=os.getenv("PRESENTER_MODEL_PATH", ""))
    args = parser.parse_args()

    ok = True
    print("LOCAL PRESENTER DIAGNOSTICS")
    print("=" * 30)

    modules = {}
    for name in ("torch", "diffusers"):
        module = check_module(name)
        modules[name] = module
        print(f"{name}: {'READY' if module is not None else 'BROKEN/MISSING'}")
        ok &= module is not None

    model = Path(args.model).expanduser() if args.model else None
    if model:
        print(f"model path: {model}")
        print(f"model exists: {'READY' if model.exists() else 'MISSING'}")
        ok &= model.exists()
    else:
        print("model path: MISSING (set PRESENTER_MODEL_PATH or pass --model)")
        ok = False

    torch = modules.get("torch")
    if torch is not None:
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
