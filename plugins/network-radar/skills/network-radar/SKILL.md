---
name: network-radar
description: Discover, verify, prioritize, and organize professional contacts from authenticated web pages, search results, profile links, or existing contact spreadsheets. Use when a user wants to build or update a networking candidate pool, find alumni or target-role contacts, audit missed relationship labels, compare old and new contact data, export a structured Excel/CSV table, or draft evidence-based outreach messages. Supports Maimai first and can extend to other professional-network sources.
---

# Network Radar

Turn a user's natural-language networking goal into a verified, explainable contact table and optional outreach drafts. Keep the interaction lightweight, use evidence conservatively, and never contact people automatically.

## Route the request

Choose one route before acting:

- **New scan**: discover a candidate pool from search pages, profile links, or a named platform.
- **Single profile**: inspect one person, decide relevant labels and priority, and draft an opening.
- **Targeted audit**: re-check one relationship type or segment, such as alumni or AI product contacts.
- **Update**: merge fresh findings into an existing table and report additions, corrections, and missing records.

For Maimai work, read both [references/maimai.md](references/maimai.md) and [references/maimai-links.md](references/maimai-links.md). For update or audit work, also read [references/update.md](references/update.md).
For Feishu Bitable output, read [references/feishu-bitable.md](references/feishu-bitable.md).
For every new scan, read and apply [references/discovery-scope.md](references/discovery-scope.md).

## 1. Understand the request

Extract three required ideas from ordinary language:

1. `background`: who the user is and the background relevant to outreach.
2. `target`: whom the user wants to meet.
3. `purpose`: why the user wants to connect.

Separate the request into `hard constraints`, `soft preferences`, `exclusions`, and `output scope`. Words such as `优先`, `更想`, and `尽量` are ranking preferences unless the user also says `必须`, `仅限`, or `只要`. Words such as `不看`, `排除`, and `不要` are exclusions. Treat source links, old tables, output limits, and outreach-message requests as optional.

If any required idea is missing, show the one-sentence template in [references/input-interaction.md](references/input-interaction.md) and ask only the single most important missing question. Do not present a long form or require YAML.

For a new scan, restate the interpreted background, target, purpose, and optional preferences in a compact confirmation card. Use the warm-social interaction specified in [references/input-interaction.md](references/input-interaction.md). If interactive visualization is unavailable, use a concise text card. Continue after confirmation.

## 2. Select capabilities

- Use an authenticated browser capability for logged-in pages. Prefer ego-browser when available and follow its task-space, handoff, verification, and cleanup rules.
- Use the standalone spreadsheet capability for `.xlsx`, `.csv`, or `.tsv` authoring and visual verification when available. If it is unavailable, deliver a UTF-8 BOM CSV and clearly state the limitation.
- Generate a verified `.xlsx` as the default deliverable. When the user requests Feishu Bitable, import the same verified dataset through the user's authenticated Feishu session or an explicitly authorized Feishu API integration.
- Use interactive visualization only as an optional presentation layer. Never make core discovery or export depend on it.
- Never bypass login, CAPTCHA, access controls, site restrictions, or platform rate limits.

## 3. Discover broadly

Build an adaptive query plan from role families and company variants. Use the scope and stopping rules in [references/discovery-scope.md](references/discovery-scope.md). A standard new scan is coverage-first, not a 20-person shortlist. Treat result-count ranges as warnings, not quotas: finish from documented lane coverage and diminishing eligible additions. If a standard scan has fewer than 40 eligible contacts, complete one expansion review before deciding to stop.

Collect visible search-result data first. Create a stable internal identity using, in order: platform user ID, canonical profile URL, or normalized `platform + name + company + role`. Deduplicate before opening detail pages.

Treat search snippets and platform-provided relationship labels as discovery clues, not final evidence for profile facts. Keep every deduplicated candidate who satisfies the hard constraints. A missing detail-page verification changes `核验状态`; it does not remove an otherwise eligible candidate.

For Maimai, separate stable identity from clickable navigation. Deduplicate by `dstu/id`, then enrich each row with that candidate's current per-result `trackable_token` from the authenticated search response. Never use a naked `profile/detail?dstu=...` URL as the primary link and never reuse a token across candidates. Follow [references/maimai-links.md](references/maimai-links.md).

## 4. Verify selectively

Open detail pages for candidates who are likely to be high priority, whose key relationship evidence is missing, or whom the user explicitly asks to audit. Do not claim the result is exhaustive.

Verification depth and candidate inclusion are separate. Verify the highest-priority segment first, but retain the broader eligible pool as `部分核验` or `待核验`. Do not shrink the final table to only alumni, senior contacts, or fully verified profiles unless the user explicitly requests a shortlist.

Apply [references/evidence-priority.md](references/evidence-priority.md) exactly:

- Attribute evidence only to the person's own profile section.
- Exclude sidebar recommendations, similar people, comments, and unrelated cards.
- Mark uncertain facts as `待核验`; do not guess.
- Store concise evidence and its source in `备注/证据`.

Use the strict profile-section rule for alumni: a school name must appear inside the person's own education section. A nearby school name in a recommendation module is not alumni evidence.

## 5. Decide priority

Use only `高`, `中`, or `低`. Never produce match scores, accessibility scores, confidence percentages, or other pseudo-precision.

Judge priority relative to this user's current purpose. Always write a short natural-language reason, such as `同济校友 + AI产品 + 入职年限接近`. Priority is not a permanent judgment about the person.

Read [references/evidence-priority.md](references/evidence-priority.md) for the decision rubric and conflict handling.

## 6. Draft outreach

Draft a personalized message only from verified or user-provided facts. Keep it warm, specific, and low-pressure:

- Introduce the user's most relevant identity.
- State the real connection or observed role.
- Make one small, concrete request tied to the user's purpose.
- Avoid invented familiarity, exaggerated praise, urgency, or mass-message phrasing.
- Adapt address and tone only when the page or user provides enough evidence.

Generate tailored drafts for high-priority contacts first. A generic draft is acceptable for other rows unless the user requests full personalization. Never send, add, or message a contact without explicit user authorization for that action.

## 7. Export and verify

Follow [references/output.md](references/output.md). Keep the main table to the approved fields and put detailed provenance in `备注/证据` rather than adding speculative score columns.

For a new scan, produce a main contact sheet. For update/audit work, also produce a change-log sheet or CSV with additions, corrections, missing records, and preserved user fields. Default to Excel; additionally create or update a Feishu Bitable when the user selects that destination.

Before delivery:

1. Validate required columns and priority values with `scripts/validate_contacts.py` when a CSV is available.
2. Scan for duplicate stable identities, unsupported high-priority rows, and Maimai link-quality errors. Report full-token coverage and fallback-link coverage.
3. Inspect representative rows and all corrected relationship labels.
4. Visually render every workbook sheet and repair clipping, broken layout, or unreadable wrapping.
5. Preserve the source file; write a new output unless the user explicitly requests an in-place update.

## 8. Handle interruptions and limits

- On login or CAPTCHA, hand control to the user and resume only after confirmation.
- On access denial or rate limiting, save partial progress, mark affected rows `待核验`, and explain where to continue.
- Keep different users' profiles, contact pools, and notes separate.
- If a source is unavailable, distinguish `not found` from `not verified`.
- Report the search scope and known limitations without overstating completeness.
