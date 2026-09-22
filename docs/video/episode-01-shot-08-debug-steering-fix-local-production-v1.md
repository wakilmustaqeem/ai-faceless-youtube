# Episode 01 — Shot 08: Debugging / Steering Fix — Local Production Lock v1

## Purpose
Show the class solving the first bug together and make the debugging process visually understandable.

## Duration
Target 10–17 seconds.

## Action
1. Presenter steps toward the center display while keeping the master mobile in hand.
2. Center display switches from race view to a clean live debugging layout.
3. Left LCD isolates the steering input pipeline.
4. A duplicated steering signal is highlighted at the processing stage.
5. Presenter points to the duplicated path and says: “There. The input is being processed twice.”
6. Student 07 watches the diagnostic view and keeps the controller ready.
7. Presenter uses the mobile to disable the duplicate processing path.
8. The duplicated signal disappears.
9. Left LCD shows one clean steering signal.
10. Right LCD returns to the car and track, ready for another test.
11. Presenter says: “Try it again.”
12. Transition directly into the successful race shot.

## Dialogue
Presenter: “There. The input is being processed twice.”
Presenter: “Try it again.”

## Debugging logic
Before fix:
Student input → steering signal → processing path A + processing path B → incorrect steering behavior.

After fix:
Student input → single steering signal → single processing path → correct steering behavior.

The visualization should communicate cause and correction without requiring technical expertise.

## Human performance
- Presenter naturally leans/steps toward the display.
- Pointing gesture must align with the actual duplicated signal.
- Mobile interaction must look physically plausible.
- Student 07 watches the highlighted diagnostic path, then returns attention to the controller.
- Other students remain engaged but restrained.
- Natural blinking, breathing, eye tracking, weight shifts and hand movement.
- No robotic or avatar-like motion.

## Camera
Controlled medium-wide shot establishing presenter, Student 07 and all three displays. Brief close insert on the duplicated signal and mobile approval/fix action. Return to medium framing for “Try it again.”

## Continuity
- Same 2040 classroom.
- Same presenter, Student 07 and student group.
- Exactly three fixed physical LCDs.
- Same racing car, track and UI language from Shots 4–7.
- Same master mobile control console.
- No floating displays.
- No holograms in this shot.
- Preserve established lighting and room geography.

## Visual prompt
“Photorealistic cinematic live-action 2040 international technology classroom, same established full-body male teacher and students, three physically fixed wall-mounted LCD displays, teacher holding the same master mobile control console, center display switches to a clean live debugging interface, left display clearly visualizes one student steering input splitting into two duplicated processing paths, duplicated signal highlighted at the processing stage, teacher naturally points to the duplicated path and explains the problem, student watches attentively with controller ready, teacher uses the mobile to disable the duplicate path, one clean steering signal remains, right display shows the same racing car and track ready for another test, teacher says ‘Try it again’, realistic human anatomy, natural blinking and breathing, believable gestures, premium restrained future classroom lighting, realistic reflections, cinematic controlled camera movement, photorealistic live-action look.”

## Negative prompt
“cartoon, anime, avatar, mannequin, plastic skin, frozen faces, robotic gestures, exaggerated acting, deformed hands, extra fingers, identity drift, floating displays, holographic screens, random code, unreadable UI, random signal paths, duplicated cars, excessive neon, horror, explosion, violent crash, camera shake, extreme zoom, slideshow aesthetic, watermark, text artifacts.”

## Local generation
Preferred: reference-first image-to-video with the approved classroom, presenter, student and game references.
Wan2.2 TI2V-5B remains the documented local backend after hardware approval; use the established portrait 720P-class workflow and preserve shot continuity.

## Hardware gate
Rendering readiness remains blocked until `scripts/check_local_video_env.py` is run on the production machine and its output is reviewed. Do not claim GPU/model readiness from repository documentation alone.

## Acceptance gate
PASS only if:
- The duplicated input is visually understandable.
- The presenter’s pointing gesture matches the highlighted signal.
- Mobile action visibly causes removal of the duplicate path.
- One clean input path remains after the fix.
- Student 07 remains the active tester.
- Three displays stay physically fixed.
- Presenter/student identities remain stable.
- No avatar or slideshow aesthetic.
- Shot matches Shots 1–7 in geography, lighting, car and UI continuity.
- Human owner approves before promotion to final assembly.
