# Episode 2 — Exact Teleport Asset Request v1

The local render pipeline is ready, but the render remains BLOCKED until these three approved image assets are supplied on the production machine:

- assets/video/teleport/presenter_departure.png
- assets/video/teleport/destination_2027.png
- assets/video/teleport/presenter_arrival.png

Optional:
- assets/video/teleport/teleport_audio.wav

Do not invent, scrape, or promote unapproved images to canonical references.

Once the assets exist, run:

python scripts/build_teleport_prototype.py
python scripts/verify_teleport_prototype.py

Then perform human visual QA.

FFmpeg supports image inputs and filtergraphs for local media processing, so no paid AI generation is required for this prototype route.