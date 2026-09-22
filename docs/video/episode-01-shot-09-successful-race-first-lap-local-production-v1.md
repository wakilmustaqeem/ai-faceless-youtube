# Episode 01 — Shot 09: Successful Race / First Lap — Local Production Lock v1

## Purpose
Pay off the debugging sequence: Student 07 successfully controls the car after the duplicated steering input is fixed.

## Duration
Target 10–16 seconds.

## Action
1. Presenter finishes the debug correction and gives Student 07 the go-ahead.
2. Student 07 makes a clean steering input.
3. Right LCD shows the car responding immediately and naturally.
4. The car enters the corner smoothly.
5. Center display shows the live race progressing.
6. Left LCD shows one clean steering signal with stable telemetry.
7. Student 07 realizes the fix worked and smiles naturally.
8. Nearby students react with believable excitement and attention.
9. Presenter watches the successful corner, then gives a subtle satisfied nod.
10. Car completes the first clean section of the lap.
11. Hold briefly on the successful race state before the next story beat.

## Dialogue
No required dialogue during the main movement.
Optional natural reaction from students should remain subtle and unscripted.

## Gameplay continuity
Before Shot 9:
- Duplicate steering processing has been disabled.
- Student 07 remains the authorized active driver.
- Master mobile remains under teacher control.

During Shot 9:
- One steering input produces one steering response.
- Car follows the intended racing line.
- No teleporting, sudden acceleration, impossible turns or random physics.
- Telemetry remains consistent with the visible car behavior.

## Human performance
- Student 07 uses a natural two-handed controller posture.
- Eyes alternate naturally between controller and race display.
- Smile/reaction occurs only after seeing the successful turn.
- Other students respond individually; no synchronized cheering.
- Presenter remains calm and confident.
- Natural blinking, breathing, posture shifts and eye tracking.
- No avatar-like or mannequin behavior.

## Camera
Start on Student 07's steering action, smoothly track toward the right LCD as the car enters the corner, then widen enough to include the classroom reaction and presenter. End with the successful car movement clearly readable.

## Visual prompt
“Photorealistic cinematic live-action 2040 international technology classroom, exact same established presenter, Student 07 and student group, same three physically fixed wall-mounted LCD displays, Student 07 actively driving the same realistic electric racing car after a successful software fix, one clean steering input shown on the left telemetry display, the car responds immediately and smoothly on the right racing track display, clean racing line through a corner, center display shows the live race progressing, student realizes the fix worked and smiles naturally, nearby students show restrained believable excitement, teacher watches with a subtle satisfied nod, realistic human anatomy, natural blinking breathing and eye movement, believable vehicle physics, premium restrained future classroom lighting, cinematic controlled tracking camera, photorealistic live-action quality.”

## Negative prompt
“cartoon, anime, avatar, mannequin, plastic skin, frozen faces, synchronized cheering, exaggerated celebration, deformed hands, extra fingers, identity drift, floating displays, holographic screens, random UI changes, duplicate steering signals, broken telemetry, teleporting car, impossible physics, sudden speed jumps, violent crash, explosion, excessive neon, horror, camera shake, slideshow aesthetic, watermark, text artifacts.”

## Local generation
Reference-first image-to-video is preferred so the approved classroom, presenter, Student 07, car and displays remain stable. Wan2.2 TI2V-5B is the planned local backend after hardware approval; its official configuration specifies 24 FPS and 121 frames, while the documented TI2V-5B workflow supports 720P generation. citeturn0search0turn0search1

## Hardware gate
Do not claim render readiness until `scripts/check_local_video_env.py` has been run on the actual production machine and reviewed. The documented single-GPU 720P TI2V-5B example uses a 24GB-class GPU with offloading. citeturn0search1

## Acceptance gate
PASS only if:
- Car visibly responds correctly to the steering input.
- Left telemetry shows one clean steering signal.
- Right display and center display agree with the car's motion.
- Student 07 remains the active authorized driver.
- Student reactions are natural and unsynchronized.
- Presenter identity and classroom geography remain stable.
- Exactly three fixed displays remain in place.
- No violent crash, horror tone or cartoon/AI-avatar appearance.
- The shot clearly reads as the payoff to the Shot 8 debugging fix.
- Human owner approves before final assembly.
