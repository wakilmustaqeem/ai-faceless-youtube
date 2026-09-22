# Episode 2 — Free Teleport Prototype Execution v1

## Execution route
Approved still keyframes + local FFmpeg/Remotion compositing.

## Required inputs
1. presenter departure reference
2. 2027 destination plate
3. presenter arrival reference
4. optional local sound effect

Do not substitute missing references with placeholders.

## Timing
- 0.0–0.7s stable presenter
- 0.7–1.4s controlled white/golden glow
- 1.4–1.8s peak burst and disappearance
- 1.8–2.3s destination transition
- 2.3–3.0s arrival burst and materialization

## Composite layers
Base plate → camera motion → glow → particles → disappearance mask → destination UI → arrival glow → reveal/mask → sound sync.

## Output
Native vertical 9:16 prototype, short duration, H.264 preview suitable for visual QA.

## QA gate
PASS requires:
- presenter identity remains consistent
- departure and arrival positions match
- no floating displays
- no fantasy portal
- destination year is readable
- light burst is brief and controlled
- materialization has believable footing
- no horror treatment

## Safety
This is a local prototype specification only. It must not claim a rendered video exists until FFmpeg/Remotion actually produces and verifies the output.
