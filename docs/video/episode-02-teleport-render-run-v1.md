# Episode 2 — Teleport Prototype Render Run v1

## Precondition
Run only on the production machine after the local environment gate passes and the three approved reference images are present.

## Commands

From repository root:

```bash
python scripts/check_local_video_env.py
python scripts/build_teleport_prototype.py
python scripts/verify_teleport_prototype.py
```

## Expected asset paths

```
assets/video/teleport/presenter_departure.png
assets/video/teleport/destination_2027.png
assets/video/teleport/presenter_arrival.png
```

## Expected output

```
artifacts/video/teleport-prototype-v1.mp4
```

## Result states

- PREFLIGHT BLOCKED — environment is not ready.
- ASSET BLOCKED — approved references are missing.
- RENDER FAILED — FFmpeg returned an error.
- MEDIA VERIFIED — ffprobe can inspect the produced MP4.
- HUMAN QA REQUIRED — technical verification is not visual approval.

## Evidence

Record the command output and actual file metadata before claiming a successful render.

FFmpeg officially supports building video from image inputs and processing streams through simple or complex filtergraphs. This makes the still-keyframe prototype a valid local execution route.