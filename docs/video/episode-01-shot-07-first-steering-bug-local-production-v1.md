# Episode 01 — Shot 07: First Steering Attempt → Bug — Local Production Lock v1

## Purpose
Deliver the first real gameplay payoff: Student 07 drives, the steering fails, and the class discovers its first bug.

## Duration
Target 9–15 seconds.

## Action
1. Student 07 starts the assigned racing car.
2. Right display shows the car accelerating along the test track.
3. Student makes a natural steering input.
4. The car fails to turn correctly and continues toward the wrong line.
5. Student reacts with focused surprise, not panic.
6. Nearby students react individually and look toward the presenter.
7. Presenter immediately observes the steering telemetry on the left display.
8. Presenter says: “That’s not a failure. That’s our first bug.”
9. Cut toward the duplicated-input visualization that will begin Shot 8.

## Dialogue
Presenter: “That’s not a failure. That’s our first bug.”

## Game behavior
- Steering input is visibly received.
- Telemetry shows the same steering command being processed twice.
- Car behavior is consistent with the bug: delayed/incorrect turn rather than random movement.
- Do not make the car crash violently; the failure should feel like a teachable software bug.

## Human performance
- Student 07 maintains both hands on the device and makes one clear steering action.
- Natural eye tracking between device and right display.
- Presenter watches the student first, then checks telemetry.
- Students have different subtle reactions.
- Natural blinking, breathing, posture changes and weight shifts.
- No exaggerated cheering, panic, or synchronized reactions.

## Camera
Begin close enough to read Student 07's focused action and the right display. Use a controlled tracking move with a brief cut to the left telemetry display as the steering problem appears. Finish on presenter + telemetry.

## Continuity
- Same 2040 classroom and lighting.
- Same presenter and students.
- Exactly three fixed physical LCDs.
- Same car, track and UI established in Shots 4–6.
- Same teacher mobile remains visible/available.
- No floating displays or holograms.
- No unexplained UI redesign.

## Visual prompt
“Photorealistic cinematic live-action 2040 technology classroom, same established full-body male teacher, same students and same three fixed wall-mounted LCD displays, Student 07 actively controls the assigned realistic electric racing car, car accelerates on the test track, student makes a clear natural steering input, telemetry on the left display shows the steering command being processed twice, right display shows the car failing to turn correctly and drifting toward the wrong racing line without a violent crash, student reacts with focused surprise, nearby students respond naturally and individually, teacher studies the telemetry and calmly says ‘That’s not a failure. That’s our first bug’, realistic human anatomy, natural blinking and breathing, believable physics, premium restrained future classroom lighting, realistic reflections, cinematic controlled camera movement, photorealistic live-action look.”

## Negative prompt
“cartoon, anime, avatar, mannequin, plastic skin, frozen faces, exaggerated panic, synchronized reactions, violent crash, explosion, damaged car, impossible physics, deformed hands, extra fingers, identity drift, floating displays, holographic classroom, excessive neon, random telemetry, random UI changes, camera shake, extreme zoom, slideshow aesthetic, watermark, text artifacts.”

## Local generation
Reference-first image-to-video remains preferred. Wan2.2 TI2V-5B supports 720P at 24 FPS and both text-to-video/image-to-video workflows; the official model documentation confirms the 5B TI2V route. citeturn0search6turn0search10

## Hardware gate
Rendering remains blocked until `scripts/check_local_video_env.py` is actually run on the production machine and reviewed. Published Wan2.2 TI2V-5B documentation gives a 24GB VRAM class consumer-GPU route for 720P with offload. citeturn0search2

## Acceptance gate
PASS only if:
- Student steering action visibly causes the incorrect turn.
- Telemetry visibly supports the duplicated-input diagnosis.
- Presenter delivers the line naturally.
- Student and presenter identities remain stable.
- Three displays remain physically fixed.
- No violent crash or horror tone.
- Bug reads as a software/debugging problem.
- Shot matches Shots 1–6 in classroom geography, lighting, UI and car continuity.
- Human owner approves before promotion to final assembly.
