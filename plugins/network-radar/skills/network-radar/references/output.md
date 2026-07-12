# Output specification

## Main contact table

Use these columns in this order:

1. `姓名/昵称`
2. `平台`
3. `主页链接`
4. `公司`
5. `岗位/简介`
6. `城市/地区`
7. `方向标签`
8. `角色类型`
9. `关系钩子`
10. `核验状态`
11. `优先级`
12. `优先级理由`
13. `建联状态`
14. `推荐开场白`
15. `备注/证据`

Use semicolons for multiple tags inside one cell. Leave unknown factual fields blank instead of guessing. Default `建联状态` to `未联系` for new rows.

For Maimai rows, `主页链接` must follow `maimai-links.md`: prefer the current per-candidate full detail link with `dstu + trackable_token + search-source context`; otherwise use the encoded site-search fallback. Put the stable ID and fallback search URL in `备注/证据`. Never place a naked `profile/detail?dstu=...` link in the final workbook.

For a standard new scan, include every deduplicated candidate that satisfies the hard constraints. Do not limit the main table to `高` priority or `已核验` rows. Use `核验状态` to distinguish evidence depth, and let filters or optional views expose a high-priority shortlist.

## Workbook structure

For a new scan, create:

- `联系人池`: the main table.
- `高优先级`: an optional filtered view or derived sheet, not a replacement for the main pool.
- `说明`: search scope, generation time, evidence standard, and limitations.

For an update or targeted audit, also create:

- `本次更新`: change type, stable ID or profile link, person, changed fields, old value, new value, evidence, and action.

Keep internal stable IDs in processing data or the update log when needed; do not add them to the approved main-table columns.

## Formatting

Use a warm-social but professional workbook style:

- Freeze the header row and enable filters.
- Use a soft theme-aware accent for headers.
- Wrap role, reason, opening, and evidence columns.
- Keep links clickable.
- Highlight `高` priority and `待核验` status without overwhelming color.
- Size columns for readable scanning; cap overly wide evidence and message columns.

Export a verified `.xlsx` by default and a UTF-8 BOM `.csv` when practical. Visually render all workbook sheets before delivery and fix clipping or broken wrapping.

When the user requests Feishu Bitable, first finish and verify the same standard dataset, then follow [feishu-bitable.md](feishu-bitable.md). Treat the Excel file and Feishu table as two views of one schema; do not silently change labels, priority, or evidence between them.

## Evidence quality checks

- Every `高` row must have a non-empty `优先级理由`.
- Every confirmed relationship hook should have supporting text in `备注/证据` or be identified as an explicit platform label.
- `已核验` must not rely only on a search snippet.
- Each Maimai full detail link must use the token attached to the same candidate ID in the current search response.
- A Maimai token must not be reused across different candidate IDs.
- Every Maimai detail link must have a site-search fallback in `备注/证据`.
- Do not include match or accessibility scores.
