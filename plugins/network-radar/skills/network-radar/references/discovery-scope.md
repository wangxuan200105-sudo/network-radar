# Discovery scope and recall

Use this reference for every new contact scan. Optimize for relevant coverage first, then apply the admission gates in [eligibility-gates.md](eligibility-gates.md) before verification depth and prioritization.

## Constraint model

Translate the request into four separate sets:

1. **Hard constraints**: facts every included candidate must satisfy, such as current company and target role family.
2. **Soft preferences**: ranking signals such as alumni, mutual contacts, seniority, city proximity, or similar background.
3. **Exclusions**: roles, companies, locations, or relationship types the user explicitly does not want.
4. **Scope**: quick preview, standard scan, deep scan, or a user-specified result limit.

Never combine soft preferences into hard eligibility. Rank after the eligible pool is collected.
Never treat raw search recall as eligible-pool recall. Broad discovery is allowed; broad admission is not.

Example interpretation:

> PDD在职运营人脉，校友优先、资历深优先；招商和其他岗位方向不看。

- Hard constraints: current PDD employment; operations role family.
- Soft preferences: same school; greater visible seniority.
- Exclusions:招商 and clearly non-operations job families.
- Default scope: standard scan.

## Scope modes

- **Quick preview**: use only when the user says `先看看`, `快速`, `样例`, or gives a small limit. Aim for roughly 20–40 unique eligible candidates.
- **Standard scan**: default for `抓取人脉`, `建立人脉池`, or an unspecified count. A broad target often yields roughly 60–150 unique eligible candidates when the platform has enough relevant supply, but this is a warning range rather than a quota.
- **Deep scan**: use when the user asks for `尽量全`, `全面`, `深挖`, or continued expansion. Search until role-family and company-variant lanes saturate or the platform blocks further access.

Never add irrelevant candidates just to reach a number. Result count diagnoses possible under-search; it does not decide completion by itself. Decide completion from coverage of material search lanes, marginal eligible additions, and platform limits.

## Query expansion

Build query lanes instead of one narrow intersection:

1. Company aliases and business-unit variants.
2. Core target-role term.
3. Adjacent synonyms that remain inside the requested job family.
4. Seniority/title variants as a separate preference lane.
5. School or relationship clues as a separate preference lane.
6. Exclusion-aware queries when a high-noise adjacent role dominates results.

Do not put the school and seniority preference into every query. Broad queries build the pool; preference queries improve ranking and evidence.

For a standard scan, keep a lightweight coverage ledger. Mark each material company-alias and role-family lane as `not searched`, `active`, `saturated`, or `blocked`, and record the batches inspected plus new eligible contacts. Do not infer lane coverage merely from the overall candidate count.

## Stopping rules

Evaluate stopping per material lane, then for the scan as a whole. Continue discovery until one of these conditions is met:

- All material role-family and company-variant lanes have been searched, and each remaining active lane has two consecutive result batches that add fewer than 5 new eligible contacts or less than 10% new unique contacts.
- The user-specified result limit is reached.
- The platform has no more results.
- Login, CAPTCHA, rate limits, or access restrictions block safe continuation.

Do not stop because the first page or verified shortlist contains 20–30 people.

## Small-pool expansion review

If a standard scan has fewer than 40 eligible contacts, treat that as a warning and complete one deliberate expansion review before deciding to stop:

1. Recheck whether any soft preference was accidentally applied as a hard constraint.
2. Add missed company aliases, business-unit names, and current-employer variants.
3. Add genuine role-family synonyms and adjacent titles that remain inside the user's target function.
4. Review exclusions for false positives, especially ambiguous adjacent roles.
5. Inspect whether important lanes stopped on the first page or before two low-yield batches.

After this review, the scan may finish below 40 when material lanes are covered and marginal additions remain low. Explain the smaller pool using observed search coverage or platform limits. Do not keep expanding merely to cross the warning line.

## Candidate pool versus verified shortlist

Maintain four logical layers:

- **Raw discovery**: every deduplicated search result worth evaluating.
- **Eligible pool**: every candidate with decisive evidence for all hard constraints.
- **Review and exclusion log**: ambiguous rows marked `待核验` and decisive mismatches marked `排除`.
- **Verified priority segment**: candidates whose detail pages were inspected first because preference clues or role relevance suggested higher priority.

The main output is the eligible pool. A shortlist, filtered view, or `高优先级` sheet is secondary. Pending or excluded rows do not receive priority. Selective verification controls evidence depth inside the eligible pool; hard admission controls whether a candidate is allowed into it.

## Coverage report

Always record:

- scope mode;
- query families and important synonyms used;
- pages or batches inspected;
- raw results, unique candidates, eligible candidates, pending-review candidates, verified profiles, and excluded candidates;
- top exclusion reasons;
- stopping condition and any platform limitation.
- whether the small-pool expansion review was triggered and what it changed.

If the final eligible pool is below 40 in a standard scan, explicitly report the expansion review and explain why the scan ended. Do not silently present a small pool as complete.
