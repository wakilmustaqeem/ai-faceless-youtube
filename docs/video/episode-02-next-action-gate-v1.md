# Episode 2 — Next Action Gate v1

The production branch now contains the local prototype builder, verification script, asset-intake rules, render procedure, and QA checklist.

## Next executable action

Run the preflight and render on the actual production machine only after the approved reference assets are present.

1. python scripts/check_local_video_env.py
2. confirm FFmpeg/Python/GPU evidence
3. place approved teleport references in assets/video/teleport/
4. python scripts/build_teleport_prototype.py
5. python scripts/verify_teleport_prototype.py
6. visually inspect the MP4
7. record PASS or BLOCKED with evidence

Do not claim the prototype is rendered until step 5 produces real media metadata and step 6 is visually approved.

## Current state

- Branch: production/local-video-v1
- Main: untouched
- Paid generation: not required
- Canonical reference drift: prohibited
- Human approval: required
