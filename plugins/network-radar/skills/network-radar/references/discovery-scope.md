# Discovery scope and recall

Use this reference for every new contact scan. Optimize for relevant coverage first, then verification depth and prioritization.

## Constraint model

Translate the request into four separate sets:

1. **Hard constraints**: facts every included candidate must satisfy, such as current company and target role family.
2. **Soft preferences**: ranking signals such as alumni, mutual contacts, seniority, city proximity, or similar background.
3. **Exclusions**: roles, companies, locations, or relationship types the user explicitly does not want.
4. **Scope**: quick preview, standard scan, deep scan, or a user-specified result limit.

Never combine soft preferences into hard eligibility. Rank after the eligible pool is collected.

Example interpretation:

> PDD在职运营人脉，校友优先、资历深优先；招商和其他岗位方向不看。

- Hard constraints: current PDD employment; operations role family.
- Soft preferences: same school; greater visible seniority.
- Exclusions:招商 and clearly non-operations job families.
- Default scope: standard scan.

## Scope modes

- **Quick preview**: use only when the user says `先看看`, `快速`, `样例`, or gives a small limit. Aim for roughly 20–40 unique eligible candidates.
- **Standard scan**: default for `抓取人脉`, `建立人脉池`, or an unspecified count. Aim for roughly 60–150 unique eligible candidates when the platform has enough relevant supply.
- **Deep scan**: use when the user asks for `尽量全`, `全面`, `深挖`, or continued expansion. Search until role-family and company-variant lanes saturate or the platform blocks further access.

These ranges are coverage guides, not quotas. Never add irrelevant candidates just to reach a number. If the platform exposes fewer eligible people, report the evidence and search coverage that explains the smaller pool.

## Query expansion

Build query lanes instead of one narrow intersection:

1. Company aliases and business-unit variants.
2. Core target-role term.
3. Adjacent synonyms that remain inside the requested job family.
4. Seniority/title variants as a separate preference lane.
5. School or relationship clues as a separate preference lane.
6. Exclusion-aware queries when a high-noise adjacent role dominates results.

Do not put the school and seniority preference into every query. Broad queries build the pool; preference queries improve ranking and evidence.

## Stopping rules

Continue discovery until one of these conditions is met:

- All material role-family and company-variant lanes have been searched, and two consecutive result batches add fewer than 5 new eligible contacts or less than 10% new unique contacts.
- The user-specified result limit is reached.
- The platform has no more results.
- Login, CAPTCHA, rate limits, or access restrictions block safe continuation.

Do not stop because the first page or verified shortlist contains 20–30 people.

## Candidate pool versus verified shortlist

Maintain two logical layers:

- **Eligible pool**: every deduplicated candidate satisfying hard constraints, including `待核验` rows.
- **Verified priority segment**: candidates whose detail pages were inspected first because preference clues or role relevance suggested higher priority.

The main output is the eligible pool. A shortlist, filtered view, or `高优先级` sheet is secondary. Selective verification controls evidence depth, not whether a relevant candidate is allowed into the main table.

## Coverage report

Always record:

- scope mode;
- query families and important synonyms used;
- pages or batches inspected;
- raw results, unique candidates, eligible candidates, verified profiles, and excluded candidates;
- top exclusion reasons;
- stopping condition and any platform limitation.

If the final eligible pool is below 40 in a standard scan, explicitly explain why. Do not silently present a small pool as complete.

