# Local Hardware Preflight — Operator Gate v1

## Current status

Preflight is prepared but NOT yet executed on the production machine.

Run from the repository root:

python scripts/check_local_video_env.py

## Required evidence

Return the complete terminal output. Do not summarize it manually.

The gate needs:
- Python version;
- FFmpeg version;
- Git version;
- PyTorch installed/version;
- CUDA available;
- GPU model;
- GPU VRAM;
- any error text.

## Decision matrix

### 24GB+ VRAM
Candidate for the planned Wan 2.2 TI2V-5B 720p-class route, subject to actual preflight and successful test render.

### 8–23GB VRAM
Use a low-memory/offload route where supported. Start with a short low-resolution image-to-video test. Do not assume 720p production is available.

### 6–7GB VRAM
Use a quantized/offload workflow only if the exact machine passes testing. Expect slower, lower-resolution test generation.

### Below 6GB VRAM or no compatible GPU
Do not attempt a large local video checkpoint. Use approved stills plus local FFmpeg/Remotion assembly and keep generative rendering blocked.

## Important evidence note

Published 2026 guidance is not fully consistent on exact VRAM thresholds. Some current ComfyUI/Wan guides report the 5B route can operate around 8GB with native offloading, while official-style Wan guidance cited elsewhere places the 5B 720p route around 24GB with offload. Therefore this project will use the actual machine preflight and a tiny test render as the final authority, rather than trusting a generic VRAM table.

## First test

Do NOT start with the teleport shot.

First test:
- 2–3 seconds;
- low resolution;
- approved static classroom reference;
- one simple natural camera movement;
- no complex particles;
- no audio generation.

If this passes:
1. test presenter motion;
2. test 2027 creator motion;
3. test teleport composite;
4. only then scale to Episode 2 shots.

## Cost policy

- No paid API.
- No OpenArt credit spending required.
- No large model download until hardware suitability is confirmed.
- Prefer open/local/free tooling.

## Safety

Never report “local video generation ready” until the actual preflight and first test both pass.
