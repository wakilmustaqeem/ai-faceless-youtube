# Episode 01 — Shot 04: First Car / First Test — Local Production Lock v1

## Purpose
Turn the build interface into the first tangible playable racing-car test.

## Duration
Target 8–14 seconds.

## Action
1. Build interface finishes loading.
2. Right display brings the first 3D racing car onto the test track.
3. Presenter watches the car, then gives the command: “Run the first lap.”
4. Center display switches to live race view.
5. Left display shows steering/input telemetry.
6. The car accelerates smoothly from the starting line.
7. Students react with restrained, believable excitement.
8. Camera follows the car briefly while retaining classroom context.

## Dialogue
Presenter: “Run the first lap.”

## Continuity
- Same 2040 classroom and student group.
- Same presenter identity and wardrobe.
- Exactly three fixed physical displays.
- Same master mobile control console.
- No floating screens or fantasy technology.
- Car design and UI remain consistent with the previous build-mode shot.

## Human motion
Presenter: natural breathing, blinking, eye tracking, subtle weight shift and hand movement.
Students: small posture changes, natural eye tracking toward the race, believable reactions; no synchronized cheering or exaggerated gestures.

## Camera
Start medium-wide on presenter and displays; transition into a controlled short tracking move toward the right display/car simulation. Keep the physical classroom geography readable.

## Visual prompt
“Photorealistic cinematic 2040 technology classroom, same established full-body human male teacher and students, three fixed wall-mounted LCD displays, teacher holding master mobile control console, live racing-game build has completed its first playable car, teacher calmly commands the first test lap, center display becomes a live racing view, left display shows steering input telemetry, right display shows a realistic compact electric racing car accelerating from a marked starting line on a clean test circuit, students naturally lean forward and watch, subtle authentic excitement, realistic anatomy, blinking, breathing, natural eye focus, believable physics, premium classroom lighting, restrained futuristic UI, cinematic live-action camera movement, realistic reflections, consistent identity and room geometry.”

## Negative prompt
“cartoon, anime, avatar, plastic skin, mannequin, frozen students, synchronized cheering, exaggerated reaction, deformed hands, extra limbs, identity drift, floating displays, impossible screen placement, fantasy UFO, random UI, excessive neon, camera shake, motion smear, broken car geometry, unrealistic acceleration, watermark, text artifacts.”

## Local generation
Use reference-first image-to-video when possible. Wan2.2 TI2V-5B is the preferred documented local backend after hardware approval; its official configuration is 24 FPS with 121 frames, and published documentation lists 720P TI2V support. citeturn0search0turn0search1

## Hardware gate
Rendering is blocked until the production-machine preflight is reviewed. No claim of local GPU readiness without actual output from `scripts/check_local_video_env.py`.

## Acceptance gate
PASS only if:
- First car appears consistently with the established game UI.
- Car movement is physically believable.
- Presenter remains photorealistic and identity-stable.
- Student reactions are individual and natural.
- Three displays remain physically fixed.
- Camera movement is controlled.
- No slideshow/static-image feel.
- Shot matches Shots 1–3 in lighting, geography, and visual identity.
- Human owner approves before promotion to final assembly.
