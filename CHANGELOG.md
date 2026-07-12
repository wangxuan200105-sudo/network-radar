# Changelog

## 0.1.3 - 2026-07-12

- Replaced hard result-count completion logic with lane coverage and diminishing eligible additions.
- Kept result-count ranges as under-search warnings rather than quotas.
- Added a mandatory one-pass expansion review when a standard scan yields fewer than 40 eligible contacts.
- Added per-lane coverage states and batch-level new-contact tracking.
- Allowed a scan to finish below 40 after expansion review when material lanes are covered and marginal additions remain low.

## 0.1.2 - 2026-07-12

- Added `兜底搜索入口` as the fourth main-table field, immediately after `主页链接`.
- Expanded the standard contact schema from 15 to 16 fields and updated Feishu field mapping.
- Made missing or malformed Maimai fallback-search links a validation error and added fallback-field coverage reporting.
- Added automatic migration of fallback URLs from legacy 15-column evidence notes during incremental merges.
- Preserved `dstu`-based identity matching while independently refreshing both detail and fallback links.

## 0.1.1 - 2026-07-12

- Fixed Maimai profile links by separating stable `dstu` identity from session-aware navigation URLs.
- Added per-candidate `trackable_token` recovery from authenticated search responses and prohibited token reuse across contacts.
- Added targeted search recovery for candidates whose token is missing from the initial result batch.
- Added a site-search fallback in the existing evidence/notes field without changing the 15-column output schema.
- Added link coverage, token consistency, fallback, and expiry-aware validation before export.
- Added incremental link refresh rules so token changes do not create duplicate contact records.

## 0.1.0 - 2026-07-12

- Initial public release.
- Added natural-language onboarding and warm-social interaction guidance.
- Added Maimai discovery and strict profile-section verification rules.
- Added explainable priority labels without abstract scores.
- Added contact-table validation and incremental merge scripts.
- Added verified Excel output by default and optional Feishu Bitable delivery.
- Added recall-oriented standard scans, role-family expansion, preference-versus-constraint parsing, and explicit saturation rules.
