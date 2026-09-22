# Teleport Compositing Recipe + Local Preflight Gate v1

## Teleport compositing

The teleport effect is assembled as a short controlled sequence rather than relying on a single generated take.

### Departure
1. Start with the approved full-body traveler plate.
2. Add a brief white/golden exposure bloom around the body.
3. Build the glow rapidly over a few frames.
4. Add restrained particles and subtle spatial distortion.
5. Add motion blur only during the peak transition.
6. At peak brightness, hide/remove the traveler with a clean plate or controlled mask.
7. Cut the energy down immediately after disappearance.

### Transition
- Keep the transition brief.
- Preserve the original camera direction and scene geometry.
- Do not use a giant fantasy portal.
- Do not obscure the actor for the entire shot.
- Maintain readable cause → effect: year selection causes the light event.

### Arrival
1. Begin with the approved destination environment plate.
2. Place the traveler at the approved arrival position.
3. Start a matching white/golden light burst.
4. Contract the light toward the body.
5. Reveal the traveler progressively.
6. Restore natural footing, clothing motion and breathing.
7. Remove excess particles as the light contracts.
8. Immediately establish destination ambience.

### UI synchronization
Departure:
DESTINATION LOCKED
YEAR: [selected year]
ERA: [PAST / PRESENT / FUTURE]

Arrival:
NEW WORLD
YEAR: [actual year]
ERA: [actual era]
LOCATION: [optional location]

The screen update must happen as part of the same cinematic event, not as an unrelated overlay.

## Sound synchronization

Departure:
- short rising electronic energy;
- brief pulse;
- clean whoosh at disappearance.

Arrival:
- matching reverse energy movement;
- short impact;
- immediate environmental ambience.

No horror sting, alarm, explosion or fantasy magic sound.

## Local preflight gate

Before any local generative render, run:

python scripts/check_local_video_env.py

The preflight must report:
- Python version;
- FFmpeg version;
- Git version;
- PyTorch availability;
- PyTorch version;
- CUDA availability;
- GPU name;
- GPU VRAM where available.

### Render policy

If the machine is not confirmed suitable:
- do not download a large checkpoint;
- do not claim local generation is ready;
- use approved stills plus FFmpeg/Remotion assembly where practical;
- keep generation blocked until hardware is reviewed.

If hardware is suitable:
- install/use only the approved local stack;
- test one tiny sample first;
- validate memory/VRAM;
- then proceed shot-by-shot.

## Acceptance gate

PASS only when:
- departure and arrival match visually;
- light burst is clearly visible;
- traveler identity remains stable;
- materialization has correct footing;
- UI year/era matches the destination;
- NEW WORLD is used correctly;
- sound is synchronized;
- no fantasy/horror aesthetic appears;
- local renderer has passed preflight;
- human owner approves the test shot before scaling production.

## Cost rule

No paid generation is required by this production lock. Existing free/local routes remain preferred.
