# Incremental update and audit

Use this workflow only when the user supplies an earlier table, requests an update, or asks whether a segment was missed.

## Merge rules

1. Read the old and fresh contact tables.
2. Match by platform user ID extracted from the profile URL, then canonical profile URL, then normalized `platform + name + company + role`.
3. Preserve user-managed fields from the old table when non-empty:
   - `建联状态`
   - `推荐开场白` unless the user explicitly requests regeneration
   - User-written parts of `备注/证据`
4. Prefer newly verified factual fields over old unverified values.
5. Never replace confirmed evidence with a weaker search snippet.
6. Keep unmatched old rows; mark them in the change log as `本次未发现`, not deleted.
7. Add unmatched fresh rows as `新增`.

Use `scripts/merge_contacts.py OLD.csv FRESH.csv OUTPUT.csv --changes CHANGES.csv` for deterministic CSV merging. Review the generated changes before workbook export.

## Targeted audit

For a request such as `重新检查校友`:

1. Select rows without the target relationship label, prioritizing candidates whose role already fits the user's goal.
2. Open detail pages and apply the strict section-isolation rule.
3. Update only rows with decisive evidence.
4. Record false positives separately, such as `同济出现在旁栏推荐，不属于本人教育经历`.
5. Report how many rows were checked, corrected, left pending, and inaccessible.

## Change types

Use concise values:

- `新增`
- `字段修正`
- `关系标签补充`
- `优先级调整`
- `本次未发现`
- `待核验`

Do not force every unchanged row into the change log.
