# Episode 01 — Shot 06: Permission Gate / Student Control — Local Production Lock v1

## Purpose
Show that the future classroom has a real teacher-controlled access system before a student can drive.

## Duration
Target 8–14 seconds.

## Action
1. Presenter looks toward the student and raises the master mobile.
2. The center display briefly shows **STUDENT CONTROL REQUEST — STUDENT 07**.
3. Presenter taps **Approve** on the mobile.
4. A restrained confirmation appears on the center display.
5. Left display changes from teacher telemetry to **Student 07 — Steering Input**.
6. Right display highlights the assigned racing car with a subtle control indicator.
7. Student places both hands naturally on the assigned device/controller.
8. Presenter says: “You’re live.”
9. Student prepares to steer; transition directly into the race-control action.

## Dialogue
Presenter: “You’re live.”

## System behavior
- Request originates from Student 07.
- Teacher approval is explicit.
- Approval affects only the assigned student session.
- Other students remain observers.
- No global control unlock.
- Master mobile remains the teacher's authoritative control.
- The permission UI must look like a functioning classroom system, not decorative HUD graphics.

## Human performance
- Presenter uses realistic thumb movement on the mobile.
- Presenter checks the student before approving.
- Student reacts with focused curiosity rather than exaggerated excitement.
- Nearby students watch naturally.
- Realistic blinking, breathing, eye tracking and posture changes.
- No synchronized reactions.

## Camera
Start on a medium two-shot of presenter and Student 07, then use a controlled insert of the mobile and center display before returning to the student preparing to drive. Keep the three-display geometry physically consistent.

## Continuity
- Same 2040 classroom, lighting, presenter, students and wardrobe.
- Exactly three fixed physical displays.
- Same racing car and track from Shot 04.
- Same mobile control console.
- No floating displays or holograms.
- No unexplained UI redesign.

## Visual prompt
“Photorealistic cinematic 2040 international technology classroom, same established full-body male teacher and student group, teacher holding a master mobile control console, one student has requested control of the racing simulation, center wall display shows a clean teacher approval interface reading STUDENT CONTROL REQUEST — STUDENT 07, teacher physically taps approve on the mobile, center display confirms the permission, left fixed LCD shows Student 07 steering input telemetry, right fixed LCD highlights the assigned realistic racing car on the test track, student calmly places hands on the assigned controller/device and prepares to drive, teacher says ‘You’re live’, natural eye contact, realistic human anatomy, breathing and blinking, restrained cinematic UI glow, premium believable future classroom, realistic reflections, live-action photorealism.”

## Negative prompt
“cartoon, anime, avatar, mannequin, plastic skin, frozen face, exaggerated excitement, synchronized students, deformed hands, extra fingers, identity drift, floating screens, holographic classroom, fantasy interface, excessive neon, unreadable UI, random permission changes, global unlock, broken controller, camera shake, extreme zoom, slideshow aesthetic, watermark, text artifacts.”

## Local generation
Reference-first image-to-video remains preferred. Wan2.2 TI2V-5B is the documented local backend after hardware approval; the official configuration specifies 24 FPS and 121 frames, and the model supports 720P TI2V. citeturn0search0turn0search3

## Hardware gate
Do not render or claim render readiness until `scripts/check_local_video_env.py` has been run on the production machine and reviewed. The documented 720P single-GPU example uses a 24GB VRAM class GPU; lower-memory systems require an approved offload/lower-resolution path. citeturn0search5

## Acceptance gate
PASS only if:
- Approval visibly originates from the teacher mobile.
- Only Student 07 becomes active.
- Other students remain observers.
- Three physical displays remain fixed.
- Presenter and student identities remain stable.
- UI changes are causally connected to the approval action.
- Human movement remains natural.
- No avatar/slideshow aesthetic.
- Shot matches Shots 1–5 in classroom geography, lighting and game continuity.
- Human owner approves before final assembly.
