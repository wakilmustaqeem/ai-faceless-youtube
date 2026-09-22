# Local Video Generation Gate v1

## Purpose
Free/local-first production path for cinematic Episode 1. Paid generation is not required.

## Current verified model route
Primary candidate: Wan 2.2 TI2V-5B through ComfyUI.

Wan 2.2 TI2V-5B supports text-to-video and image-to-video. ComfyUI provides a Wan 2.2 5B video workflow template.

## Hardware gate
Do not download large weights or start a production render until the local machine is checked.

Required checks:
- GPU vendor and model
- VRAM
- system RAM
- available disk
- CUDA/ROCm availability
- Python/PyTorch/ComfyUI availability
- FFmpeg availability

Reference implementations report different VRAM envelopes depending on quantization/offloading. The conservative official-style 720p path can require around 24 GB VRAM, while optimized/quantized ComfyUI configurations can operate on lower-VRAM consumer GPUs. Therefore this project treats hardware discovery as a hard gate rather than guessing.

## Episode 1 target
- Native vertical 9:16
- cinematic realistic classroom
- real human full-body presenter
- natural student movement
- fixed three-display geometry
- 3–6 second controlled shots
- reference-first continuity
- no avatar/slideshow aesthetic

## Production strategy
1. Generate/approve canonical still references.
2. Use image-to-video for controlled motion where possible.
3. Generate one shot at a time.
4. Keep the same reference assets across shots.
5. Assemble with FFmpeg.
6. Run continuity/technical QA.
7. Human review before any publication.

## Safety / cost rule
No paid provider or subscription is required for this route. OpenArt credits remain untouched unless a later human-approved exception is made.

## Current status
Repository preparation complete; actual local rendering remains blocked only on the local-machine hardware/software check.
