# Episode 02 — Teleport Test Shot v1

## Purpose

The first local test must validate the project's hardest continuity effect without spending paid credits.

## Test

Duration: 2–3 seconds.

Input:
- one approved full-body presenter reference;
- one approved neutral destination environment;
- no dialogue;
- no complex UI;
- no audio generation.

### Sequence

0.0–0.7 sec
Presenter stands naturally and remains stable.

0.7–1.4 sec
White/golden light builds rapidly around the full body.

1.4–1.8 sec
Peak flash; controlled particles and subtle distortion; presenter disappears.

1.8–2.3 sec
Destination plate remains clean.

2.3–3.0 sec
Optional matching arrival burst and partial materialization test.

## Pass criteria

- Face/body identity remains stable.
- Natural posture and proportions.
- Light burst is clearly visible.
- No fantasy portal.
- No cartoon/avatar look.
- No excessive particles.
- No camera jump.
- No unwanted object movement.
- Departure remains readable at 9:16.
- If arrival is tested, footing and body geometry remain believable.

## Local execution gate

Before this test:
python scripts/check_local_video_env.py

The repository does not yet have the actual machine output, so this test is a specification only. It must not be represented as rendered.

## Model strategy

ComfyUI has native Wan 2.2 support and a 5B TI2V workflow, with later memory optimizations improving the 5B path. Current ComfyUI also has newer dynamic-VRAM tooling, but hardware behavior must be validated on the actual machine rather than inferred from generic thresholds. citeturn0search0turn0search1turn0search3

## Fallback

If local video generation is not viable:
- keep approved stills;
- create the light burst and disappearance locally with FFmpeg/compositing;
- assemble the sequence in the local editing pipeline;
- do not purchase generation credits.

## Approval

Human owner approves the test before Episode 2 generation scales beyond the test shot.
