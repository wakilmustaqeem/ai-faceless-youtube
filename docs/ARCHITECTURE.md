# Architecture

## Control flow
Research -> English Script -> Originality Gate -> Voice -> Visuals -> Edit -> QA -> English Master -> Localization -> Locale QA -> Private Review -> Human Review -> Publish/Reject

## Brand
The independent working brand is AI & IT Future Tech. English is the canonical source language.

## Localization
The English master is translated into all languages supported by the active translation provider. Each locale receives its own package and locale QA.

## Failure rule
Any failed or unverifiable gate stops downstream execution.

## Provider rule
Providers are adapters, not shared project state. Credentials are runtime-only.

## Independence rule
No HidayatTube branding, content, credentials, channel identity, history, storage or deployment dependency is used.

## Publishing rule
Public publishing is OFF by default and remains blocked until the independent channel is configured and a human approval decision exists.
