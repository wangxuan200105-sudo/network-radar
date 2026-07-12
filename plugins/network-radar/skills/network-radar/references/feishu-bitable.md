# Feishu Bitable output

Use this route only when the user requests a Feishu multidimensional table or provides an existing Feishu Bitable destination.

## Choose the write path

Prefer the lowest-setup path that the user has authorized:

1. **Authenticated Feishu UI**: generate and verify the Excel/CSV first, then import it into Bitable through the user's logged-in browser session. Use this when no Feishu app credentials or connector are available.
2. **Authorized connector or OpenAPI**: create fields and batch-write records only when the required Feishu authorization is already available or the user explicitly completes it.

Do not request app credentials if browser import can satisfy the task. Never expose access tokens in output, logs, files, or Git.

## Destination confirmation

Before writing, confirm the target workspace/folder or existing Bitable link and whether to:

- create a new Bitable;
- add a new table to an existing Bitable; or
- update an existing contact table.

Do not overwrite an existing table without explicit confirmation. For updates, preserve user-maintained status, notes, views, and formulas when possible.

## UI import workflow

1. Finish and validate the standard `.xlsx` or UTF-8 BOM `.csv`.
2. Open Feishu in the authenticated browser task space.
3. Create a Bitable or open the confirmed destination.
4. Use Feishu's file-import flow to import the verified file as a multidimensional table.
5. After import, set or verify field types using the mapping below.
6. Verify the total row count, all 15 field names, the first row, one high-priority row, and one evidence-heavy row.
7. Return the Feishu link together with the Excel fallback.

For rich Feishu editors, use screenshot-guided interaction first. Perform a small probe before substantial edits and verify each meaningful change visually.

## Field mapping

| Field | Recommended Feishu type |
|---|---|
| 姓名/昵称 | Text |
| 平台 | Single select |
| 主页链接 | URL |
| 公司 | Text or single select |
| 岗位/简介 | Multiline text |
| 城市/地区 | Single select |
| 方向标签 | Multiple select |
| 角色类型 | Single select |
| 关系钩子 | Multiple select |
| 核验状态 | Single select |
| 优先级 | Single select |
| 优先级理由 | Multiline text |
| 建联状态 | Single select |
| 推荐开场白 | Multiline text |
| 备注/证据 | Multiline text |

Create useful views only when requested. A common optional view is `高优先级待建联`, filtered to `优先级 = 高` and `建联状态 = 未联系`.

## OpenAPI path

Feishu OpenAPI supports creating a Bitable, creating fields, and adding records. Creating or writing records requires an access token with the relevant Bitable permissions and edit access to the destination.

Use current official Feishu Open Platform documentation before implementing an API call:

- Create Bitable: `https://open.feishu.cn/document/server-docs/docs/bitable-v1/app/create`
- Bitable overview and authorization: `https://open.feishu.cn/document/server-docs/docs/bitable-v1/bitable-overview`
- Batch-create records: `https://open.feishu.cn/document/server-docs/docs/bitable-v1/app-table-record/batch_create`

Prefer batch writes within the current documented limit and serialize writes to a single Bitable. After writing, query or read back records and reconcile the returned count with the verified source dataset.

## Failure handling

- On missing login or authorization, hand control to the user and resume only after confirmation.
- On field-type mismatch, stop the import/update and correct the schema before writing more rows.
- On partial UI import, preserve the verified Excel and report exactly which rows or fields remain incomplete.
- Never claim Feishu delivery succeeded until the destination link and representative records have been verified.

