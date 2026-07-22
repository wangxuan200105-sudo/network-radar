# Eligibility gates

Use this reference for every new scan and every audit where the user names a target company, current-employment requirement, target job family, or exclusion.

## Separate discovery from admission

Maintain three layers:

1. `raw discovery`: every deduplicated search result worth evaluating.
2. `eligible pool`: candidates with decisive evidence for every hard constraint and no decisive exclusion.
3. `review or exclusion log`: ambiguous candidates marked `待核验` and decisive mismatches marked `排除`.

Search broadly, but never copy the raw discovery set directly into the eligible pool. Only the eligible pool may receive `高 / 中 / 低` priority or outreach drafts.

## Current-employer gate

When current employment is a hard constraint:

- Build an explicit allowlist of the target company's official names, known legal entities, brands, and business units relevant to the request.
- Test the person's current-employer field or current work-experience section against that allowlist.
- Treat a company name in search queries, biographies, former roles, project descriptions, client lists, product/platform names, or negative statements as a search clue only.
- Do not interpret a platform flag such as `former=0` as proof that the person currently works for the target company. It describes the returned position, not why the target keyword matched.
- Mark an unrecognized or conflicting current employer as `待核验`; exclude a decisively different current employer.

Do not use loose substring matching when a brand name is also a marketplace or product used by outside sellers, agencies, vendors, or service providers. Prefer exact normalized aliases and verified current-employment sections.

## Target-role gate

Model the user's target as a job family, not a bag of keywords. Build:

- positive current-title anchors;
- explicit adjacent-role exclusions;
- ambiguous titles that require profile verification.

Use functional meaning and title boundaries. For a product-manager-only request:

- Positive anchors can include `产品经理`, `产品专家`, `产品负责人`, `产品总监`, `策略产品`, `增长产品`, `商业产品`, `数据产品`, or an equivalent current title.
- `产品运营`, `策略运营`, `增长运营`, `招商运营`, `平台治理`, design, engineering, algorithm, sales, procurement, and marketing are not product-manager roles merely because nearby text contains `产品`, `策略`, or `AI`.
- A domain word does not override a valid function: `供应链产品经理` is a product role, while `供应链经理` is not.
- Tool names and object phrases do not establish function: `AI产品精修`, `AI绘图`, or `使用AI软件` do not mean `AI产品经理`.

For an operations-only request, invert the family deliberately: include genuine operations titles and exclude product, engineering, HR, finance, design, sales, and the user's named exclusions. Never reuse one role family's allowlist for another.

When the current title and platform career line conflict, use `待核验` unless the current title is decisive and comes from a stronger evidence level.

## Decision order

Apply gates in this order for every candidate:

1. Resolve stable identity and current-position fields.
2. Apply current-employer gate.
3. Apply target-role gate.
4. Apply the user's explicit exclusions.
5. Assign one admission state:
   - `合格`: every hard constraint is decisively satisfied.
   - `待核验`: evidence is missing, ambiguous, or conflicting.
   - `排除`: a hard constraint decisively fails or an exclusion decisively applies.
6. Deduplicate the eligible pool.
7. Only then decide priority and draft outreach.

Never rescue an excluded candidate because of alumni status, mutual contacts, influence, seniority, or another soft preference. Never downgrade an excluded candidate to `低` and leave them in the main pool; put them in the exclusion log.

## Auditing and export

For a new scan, report raw, unique, eligible, pending-review, and excluded counts. List the top exclusion reasons.

For an existing-table audit:

- Preserve the source table or workbook as a rollback copy.
- Produce an eligible table, a pending-review table, and an exclusion/change log.
- Preserve user-managed contact status, outreach drafts, and notes when a candidate remains eligible.
- Do not delete ambiguous rows silently.
- Verify that no `排除` or `待核验` row appears in a high-priority view.

Use `scripts/audit_eligibility.py` when the source is CSV and the hard gates can be expressed as a small JSON config. Review the generated reasons before importing or replacing any live table.
