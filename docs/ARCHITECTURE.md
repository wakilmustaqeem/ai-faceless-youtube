# Architecture

## Control flow
Research → Script → Originality Gate → Voice → Visuals → Edit → QA → Private Upload → Human Review → Publish/Reject

## Failure rule
Any failed or unverifiable gate stops downstream execution.

## Provider rule
Providers are adapters, not shared project state. Credentials are runtime-only.

## Publishing rule
Public publishing is OFF by default and remains blocked until the independent channel is configured and a human approval decision exists.
