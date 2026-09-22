# Episode 01 — Shot 03: Build Mode — Local Production Lock v1

## Purpose
Bridge the presenter entry into the first live game-building action.

## Duration
Target 8–16 seconds.

## Format
Native vertical 9:16 composition. Preserve the canonical 2040 classroom geography.

## Continuity
- Same realistic full-body male presenter as Shots 1–2.
- Same student group, seating, lighting, props, and classroom.
- Exactly three physical fixed displays: large center wall display plus fixed left/right LCDs angled inward.
- No floating screens or holographic displays in this shot.
- Presenter holds the master mobile control console.
- Students remain natural: breathing, blinking, small posture shifts, realistic eye tracking.

## Action
1. Presenter settles near the center teaching position.
2. He looks at the displays, then at the students.
3. He gives the voice command: “Start build mode.”
4. His mobile confirms the command.
5. A restrained hand gesture accompanies the command.
6. Center display transitions into a live racing-game build interface.
7. Left display shows steering/input logic and signal flow.
8. Right display shows a 3D car and empty test track beginning simulation.
9. Students lean forward naturally; two students interact with laptops/tablets without exaggerated reactions.

## Dialogue
Presenter: “Start build mode.”

## Visual target
Premium cinematic future classroom, believable 2040 technology, realistic skin and anatomy, physically grounded displays, subtle UI glow, natural classroom lighting, realistic reflections, shallow depth of field where appropriate, controlled camera movement.

## Motion requirements
- Real human gait and weight transfer.
- Natural hand/finger motion around the mobile.
- Natural eye focus between students, mobile, and displays.
- No rubber limbs, frozen faces, sliding feet, identity drift, or impossible hand-to-device contact.
- UI changes must visibly follow the command rather than appearing randomly.

## Camera
Medium-wide three-quarter classroom angle that keeps presenter, students, and all three displays readable. Slow controlled push-in; no aggressive zoom.

## Local generation strategy
Preferred: reference-first image-to-video using the approved classroom/presenter references.
Preferred local backend: Wan2.2 TI2V-5B when local hardware passes preflight. Wan2.2 TI2V-5B officially targets 720P at 24 FPS and supports text+image-to-video; the official configuration uses 24 FPS and 121 frames. 
For 9:16, use the portrait orientation supported by the model (704*1280 at the 720P-class size), then crop/encode only if required by the final assembly pipeline.

## Hardware gate
Do not claim rendering readiness until `scripts/check_local_video_env.py` has been run on the production machine and its output reviewed.
The published Wan2.2 TI2V-5B single-GPU 720P route uses a 24GB VRAM example (RTX 4090); lower-memory machines should use an approved lower-resolution/offload path or stills + FFmpeg/Remotion assembly rather than pretending full local video generation is available.

## Prompt
“Cinematic realistic 2040 international technology classroom, same established male human teacher and same student group, teacher standing naturally at the center teaching position holding a modern master mobile control console, three physically fixed wall-mounted displays exactly matching continuity, teacher calmly says ‘Start build mode’, subtle natural hand gesture, mobile command visibly triggers the classroom system, center display changes into a live racing game development interface, left display shows steering input and logic flow, right display shows a realistic 3D racing car beginning an empty test-track simulation, students naturally lean forward and interact with laptops, realistic human anatomy, natural blinking and breathing, believable weight and foot placement, premium cinematic lighting, realistic reflections, restrained UI glow, cinematic depth, controlled camera push-in, grounded physical technology, international high-end future classroom, photorealistic live-action look.”

## Negative prompt
“cartoon, anime, CGI-looking human, plastic skin, avatar, mannequin, frozen face, exaggerated expressions, deformed hands, extra fingers, missing fingers, fused fingers, rubber limbs, floating displays, impossible screen geometry, duplicate people, identity drift, sliding feet, broken anatomy, random UI changes, unreadable clutter, excessive neon, horror, sci-fi fantasy, flying objects, camera shake, extreme zoom, low detail, watermark, text artifacts.”

## Acceptance gate
PASS only if:
- Presenter identity remains stable.
- All three displays remain physically fixed and correctly placed.
- Mobile interaction is physically believable.
- UI transition clearly follows “Start build mode.”
- Students move naturally.
- No avatar/slideshow aesthetic.
- The shot matches Shots 1–2 in classroom geography and lighting.
- Human owner approves before animation/assembly is promoted.
