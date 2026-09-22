# Production State — 2026-09-22

## Saved state

Project: RACING GAME — TIME-TRAVEL UNIVERSE

Active branch:
production/local-video-v1

Main:
Untouched.

## Locked

- Episode 1 local-production shot plan: Shots 1–11.
- Episode 1 teleport/cliffhanger continuity.
- Permanent cinematic teleportation signature.
- Episode 2 — THE FIRST CONTACT production lock.
- 2040 classroom continuity.
- Three fixed physical LCD displays.
- Master mobile + voice + hand-gesture control.
- Realistic full-body human presenter.
- Natural student movement.
- Friendly time bridge.
- No casual history rewriting.
- NEW WORLD → YEAR / ERA / LOCATION destination UI.
- Manual human approval before publication.

## Production rule

Reference-first workflow is the default for important shots. Current 2026 workflow guidance also supports using an approved still/reference as the visual anchor and asking the video model primarily for controlled motion; this is useful for character and scene continuity.

## Local-render status

Local rendering is NOT declared ready until the production-machine preflight is actually run and reviewed.

Preflight command:
python scripts/check_local_video_env.py

No large checkpoint download or paid generation is authorized by this state file.

## Next work

1. Build Episode 2 shot prompts 01–10 using the locked production plan.
2. Create/verify reference requirements for 2027 first-contact environment and characters.
3. Prepare teleport departure/arrival compositing recipe.
4. Run local hardware preflight when the production machine is available.
5. Generate only after the reference gate passes.
6. Assemble and QA before any human publication review.

## Restore point

The branch backup/production-local-video-v1-base remains the restore point for this local-video workstream.

## Safety

Do not merge to main without explicit owner authorization.
Do not claim rendered video exists until an actual renderer produces it.
Do not spend paid credits.
