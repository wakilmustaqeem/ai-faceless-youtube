# Episode 2 — Teleport Reference Assets Intake v1

## Required files

Place only approved canonical assets in:

assets/video/teleport/

Required:
- presenter_departure.png
- destination_2027.png
- presenter_arrival.png

Optional:
- teleport_audio.wav

## Intake rules

- Assets must be approved before rendering.
- Departure and arrival presenter references must preserve the same identity and wardrobe.
- The destination plate must visibly represent 2027/Past.
- Do not use generated output as a canonical reference.
- Do not create fake placeholder images to satisfy the gate.
- Missing assets must keep the render BLOCKED.

## Render command

python scripts/build_teleport_prototype.py

## Verification command

python scripts/verify_teleport_prototype.py

A successful script run is not visual approval. Human visual QA remains mandatory.

## Free-first rule

No paid generation or subscription is required for this local prototype. FFmpeg can read image inputs and use filtergraphs/zoompan/concat for local compositing.
