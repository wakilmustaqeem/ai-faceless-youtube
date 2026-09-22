#!/usr/bin/env python3
"""Check the local machine before enabling AI video generation.

This script performs discovery only. It never downloads models or starts a render.
"""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys


def command_version(command: str) -> str:
    path = shutil.which(command)
    if not path:
        return "missing"
    try:
        result = subprocess.run(
            [command, "-version"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        line = (result.stdout or result.stderr).splitlines()
        return line[0] if line else "installed"
    except Exception:
        return "installed"


def main() -> int:
    print("=== FM Local Video Hardware Gate ===")
    print(f"Python: {sys.version.split()[0]}")
    print(f"FFmpeg: {command_version('ffmpeg')}")
    print(f"Git: {command_version('git')}")

    torch_spec = importlib.util.find_spec("torch")
    print(f"PyTorch installed: {'yes' if torch_spec else 'no'}")

    if torch_spec:
        import torch  # type: ignore

        print(f"PyTorch: {torch.__version__}")
        cuda = bool(torch.cuda.is_available())
        print(f"CUDA available: {'yes' if cuda else 'no'}")
        if cuda:
            for i in range(torch.cuda.device_count()):
                name = torch.cuda.get_device_name(i)
                total = torch.cuda.get_device_properties(i).total_memory / (1024**3)
                print(f"GPU {i}: {name}")
                print(f"GPU {i} VRAM: {total:.1f} GiB")

    print("ComfyUI: check local installation separately")
    print("Result: discovery only; no model download/render was started.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
