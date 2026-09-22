# RACING GAME — EPISODE 01 PRODUCTION WORKFLOW v1

## Objective
Turn the locked story, asset bible and shot prompts into a repeatable production pipeline.

## Current Production Chain
1. Generate reference assets.
2. Human/owner approval of references.
3. Generate shot keyframes from approved references.
4. Approve keyframes as shot anchors.
5. Animate one shot at a time.
6. Run continuity QA after every shot.
7. Assemble approved clips.
8. Run final episode QA.
9. Export master 9:16 episode.
10. Human review remains the publish gate.

## Reference Discipline
The same canonical reference set must be reused across shots. Current 2026 guidance consistently recommends reference-first/image-to-video workflows for multi-shot character continuity rather than rebuilding the character from text every time. citeturn0search0turn0search1turn0search6

For the presenter, use multiple views when the generator supports them: face/front, profile or three-quarter, and full-body. This reduces the model's need to invent unseen facial and body details. citeturn0search0turn0search3

## Keyframe Gate
A shot cannot enter video generation until its still keyframe passes:
- correct presenter/student identity;
- correct wardrobe;
- correct three-display geometry;
- correct master mobile where required;
- correct classroom geography;
- correct UI state;
- correct camera framing;
- no unwanted objects.

## Motion Gate
Generate short controlled clips rather than attempting the entire episode in one generation.
Each clip should have:
- one primary action;
- one motivated camera move;
- stable identity;
- stable room geometry;
- physically plausible hand/body movement.

## Episode Assembly
Target runtime: approximately 90–115 seconds.
Structure:
HOOK → CLASS → BUILD → FIRST TEST → BUG → DEBUG → RACE → MYSTERY → CLIFFHANGER.

## Audio
Keep dialogue natural and intelligible.
Preserve room ambience.
Use restrained UI/racing effects.
Do not let music or effects cover dialogue.
Mystery reveal should have a controlled audio drop rather than a horror sting.

## Final QA
Reject the episode if:
- any major character visibly changes identity;
- wardrobe changes without story reason;
- displays become floating or change count;
- presenter touches a screen despite remote-control canon;
- student permissions are bypassed;
- Legacy Core appears before its designated reveal;
- 2027 mystery is explained too early;
- any shot breaks physical continuity;
- generated audio becomes obviously synthetic or disconnected from the scene.

## Publish Gate
Final video remains in private/manual-review state until the human owner approves it. No automatic public publishing is enabled by this document.
