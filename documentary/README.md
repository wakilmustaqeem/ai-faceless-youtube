# Long-Form Documentary Engine

The AI & IT Future Tech channel now has a dedicated long-form documentary format.

## Target

- 15–30 minutes per documentary; default target: 20 minutes.
- English is the master language.
- Narrative style: energetic, curious and natural without sensational claims.
- Two natural adult English voices:
  - Female: `en-US-JennyNeural`
  - Male: `en-US-GuyNeural`
- Voice changes happen at act/evidence boundaries so the conversation feels natural rather than mechanical.

## Story architecture

Cold open → central question → context → evidence reveals → turning point → implications → uncertainty → what happens next → closing question.

Every factual claim must remain traceable to the research/evidence package. The engine never grants publishing authority.

## Production gates

Research → source verification → documentary script → originality gate → dual-voice narration → visuals → captions → QA → private review → human approval → publish.

Public YouTube publishing remains OFF by default.

## Documentary QA v2

The documentary engine now uses a claim-level evidence chain:

**Claim → Source → Evidence → Script → Voice → Visual → Timestamp**

Important multimedia assets must record origin, authenticity, context, temporal/geographic consistency, manipulation signals, and verification status. Generated or reconstructed assets additionally require explicit provenance: **asset_id, source_type, generation_method, reference, timestamp, verification_status**.

AI/automated detection is assistive only. Detector outputs may flag or recommend investigation; they do not establish authenticity or publication authority. Human review remains the final authority.

AI-generated or reconstructed media must be clearly disclosed where applicable. Provenance and watermarking are treated as authenticity-supporting layers, not substitutes for editorial verification.

Locked rule:

> Source establishes fact. Evidence supports claim. AI assists verification. Automation flags problems. Human approval establishes publication authority.
