# Local Presenter Diagnostics

Run from the repository root:

    python scripts/presenter_diagnostics.py

The diagnostic checks:

- torch availability
- diffusers availability
- an already-installed local model path from PRESENTER_MODEL_PATH or --model
- CUDA availability when PyTorch is installed

It never downloads a model, calls a paid API, or overwrites assets.

A successful diagnostic means the environment is ready to attempt local photorealistic presenter generation. Generation itself remains a separate runtime gate and is not claimed successful until the generated PNG passes the existing presenter verification step.
