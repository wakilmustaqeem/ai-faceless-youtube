# Alternate Production Route B — No Local GPU Preflight Required

## Decision

If the production machine preflight is inconvenient or unavailable, do not stop the project.

Use a hybrid route:

**Reference Images → Free/available image-to-video service when credits/access permit → local FFmpeg compositing → local Remotion/assembly → QA**

## Primary principle

Do not depend on a single video-generation provider.

The story assets, shot prompts, continuity rules and teleport compositing remain provider-neutral.

## Route B-A — Free cloud generation

Use an actually available free web/space-based video workflow for short reference-driven clips.

Priority:
1. free access;
2. image-to-video;
3. reference support;
4. short clips;
5. export without forced paid upgrade.

If a service requires payment or credits, skip it rather than changing the story.

## Route B-B — Local compositing fallback

If no free generative video service is available:

- create approved still keyframes;
- animate camera movement with FFmpeg/Remotion;
- create the teleport light burst with local compositing;
- use masks/opacity for disappearance and materialization;
- add particles, glow and distortion locally;
- add natural sound locally;
- assemble all shots into the final vertical video.

This still produces the cinematic teleport sequence even without local AI video generation.

## Route B-C — Mixed workflow

For human motion:
- use any free short image-to-video generation that is available.

For teleport:
- generate the clean human/environment motion separately;
- build the light burst, disappearance and arrival locally.

This separates the hardest visual effect from the generative model.

## Why this route is valid

Wan 2.2 has a native ComfyUI image-to-video workflow, including a 5B TI2V workflow, and ComfyUI provides an official image-to-video blueprint. citeturn0search1turn0search9

The project therefore keeps Wan as a future local option, but it is no longer a blocker for production.

## Hard rules

- No paid credits.
- No subscription.
- No main-branch changes.
- No unapproved generated reference becoming canonical.
- No claim that a video rendered until an actual output exists.
- Keep all story prompts provider-neutral.
- Human approval remains the final gate.

## Immediate next action

Build the Episode 2 reference pack and a 3-second teleport compositing prototype using still images first.

Only introduce generative video after a free route is confirmed.
