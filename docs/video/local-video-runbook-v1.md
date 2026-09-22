# Local Video Runbook v1

## Purpose
Run the local video preflight on the user's own machine before downloading large models or attempting a render.

## Preflight
From the repository root:

python scripts/check_local_video_env.py

The check reports Python, FFmpeg, Git, PyTorch, CUDA availability, GPU name and visible VRAM. It is discovery-only: it does not download models and does not render.

## Next step
Send the complete output back after the command finishes. The production branch can then select the appropriate Wan/ComfyUI tier without guessing the machine's hardware.

## Cost rule
Do not purchase OpenArt credits for this route. The local route is being prepared around open-source Wan/ComfyUI tooling.

## Safety
- Never change main for this experiment.
- Keep the existing restore branch.
- Do not download a large checkpoint until the hardware tier is known.
- Do not replace an approved reference with a generated drifted frame.
