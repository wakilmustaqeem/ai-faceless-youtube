# Multi-Language Localization

## Source of truth
Every episode is authored as an English master first.

Flow:
English research -> English script -> originality/QA -> English production -> approved master -> translation -> locale QA -> localized package

## Translation scope
The system is designed for all languages supported by the active translation provider. It is not hard-coded to a small language list.

Initial locale registry:
en, ur, ar, hi, bn, tr, id, es, fr, de, pt, it, ja, ko, zh, ru

The registry can be extended without changing the English master.

## Translation rules
- Translate meaning, not word-for-word text.
- Preserve technical names, product names, company names, URLs and code identifiers.
- Preserve the brand name AI & IT Future Tech unless brand policy later says otherwise.
- Do not alter factual numbers without source verification.
- Run locale QA after translation.
- Human review remains required for publishable output.

## Independence
Localization uses this repository's own content package and credentials. It does not read, write or link to HidayatTube content, branding, credentials, history or storage.

## State
Brand and localization architecture are implemented. Actual translation-provider execution is a separate integration and must be verified before production-ready status.
