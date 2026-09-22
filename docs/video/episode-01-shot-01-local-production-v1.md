# Episode 01 — Shot 01 Local Production Lock v1

## Goal
Produce the opening 3–4 second vertical cinematic hook for RACING GAME — THE FIRST LAP using the local/open-source route first.

## Locked frame
- Canvas: 9:16 vertical.
- Era: 2040.
- Premium international future classroom.
- Exactly three physical displays: huge center wall display, fixed left LCD angled inward, fixed right LCD angled inward.
- Real students with natural posture, blinking and small movements.
- No presenter in the first hook.
- Center display: CAN YOU BUILD A RACING GAME?
- Left display: steering/input visualization.
- Right display: empty racing track.
- Premium cinematic lighting with believable reflections and shadows.

## Motion
Controlled cinematic push-in; subtle student movement; center display wakes naturally. No floating screens, teleporting UI, plastic skin, cartoon look, avatar look, extra limbs, identity drift or slideshow motion.

## Generation strategy
1. Preferred: image-to-video from an approved canonical classroom reference.
2. Fallback: text-image-to-video with Wan 2.2 TI2V-5B.
3. Keep the shot short for the first hardware test.
4. Do not spend OpenArt credits for this test.

Wan 2.2 TI2V-5B supports text+image-to-video and 720p at 24 FPS; ComfyUI provides a 5B workflow requiring the TI2V-5B checkpoint and Wan 2.2 VAE.

## Hardware tiers
Planning tiers, not guarantees:
- 24 GB+: 704×1280-class vertical, 24 FPS, short clip.
- 16–23 GB: lower resolution plus aggressive offload.
- 8–15 GB: ComfyUI/offload experimental low-resolution test.
- <8 GB: skip Wan render; use approved stills plus FFmpeg/Remotion motion assembly.

The official Wan example documents a 24 GB-class GPU for its 720p TI2V-5B command with offloading. Community implementations document additional low-memory/offload approaches; the local machine must be checked before selecting the final tier.

## Prompt
Cinematic realistic 2040 international future classroom, three permanently wall-mounted digital displays, huge center display waking with the words CAN YOU BUILD A RACING GAME?, left display showing a clean steering input diagram, right display showing an empty futuristic racing track, diverse teenage students seated naturally at desks with laptops and tablets, subtle breathing and blinking, realistic classroom behavior, premium modern architecture, believable reflections, physically grounded objects, controlled cinematic camera push-in, natural lighting, photorealistic live-action film look, no presenter yet.

## Negative prompt
cartoon, anime, illustration, CGI-looking humans, plastic skin, AI avatar, floating displays, holographic screens, extra limbs, duplicate people, warped hands, deformed faces, identity drift, impossible physics, overreaction, frozen students, slideshow, text distortion, horror, dark sci-fi, war, weapons.

## Acceptance gate
Reject if any display floats or changes physical position, student anatomy/identity visibly drifts, classroom geometry changes, text becomes unreadable enough to break the hook, motion looks like a slideshow, lighting/shadows contradict the room, or the camera creates impossible perspective.

Human approval is required before this becomes a canonical reference or enters Episode 01 assembly.
