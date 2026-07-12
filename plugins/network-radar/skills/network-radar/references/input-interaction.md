# Input and warm-social interaction

## Natural-language input

Require only three ideas:

- Who the user is.
- Whom the user wants to meet.
- Why the user wants to connect.

Use this prompt when guidance is needed:

> 我是【你的身份或背景】，想认识【什么样的人】，主要希望【解决什么问题或达成什么目的】。如果有偏好，也可以补充【优先或排除条件】。

Example:

> 我是同济管科应届生，即将入职拼多多做产品，想认识公司里从事AI产品的校友，主要想请教方向选择和岗位双选，优先入职1—3年的人。

Do not require the user to repeat information already present in the conversation, attached files, or an explicitly reusable user profile. Ask at most one missing question at a time.

Parse constraint language conservatively:

- `优先校友`, `资历深的人优先`, `尽量有共同好友` are soft ranking preferences.
- `必须是校友`, `只看总监以上`, `仅限上海` are hard constraints.
- `招商不看`, `排除HR`, `不要销售` are hard exclusions.

Do not turn multiple soft preferences into an intersection filter. For example, `校友优先、资历深优先` means rank alumni and senior contacts higher; it does not mean every returned contact must be both an alumnus and senior.

When the input contains an obvious but consequential typo, restate the likely interpretation and isolate its effect. Example: `20206届` can be treated as likely `2026届` for discovery, but confirm it before drafting outreach. Do not block a broad scan on an uncertainty that does not change the target pool.

## Confirmation card

Before a new scan, show:

- `你的背景`
- `目标人群`
- `建联目的`
- `优先/排除条件` only when present
- `扫描范围`: quick preview, standard scan, or deep scan

Use a warm, socially approachable tone. Avoid corporate dashboard language and scoring language.

If interactive visualization is available, provide a compact confirmation surface with one primary `开始扫描` action and one low-emphasis `修改` action. Use warm-social styling: soft theme-aware accents, restrained rounded forms, clear spacing, and friendly wording.

## Progress motion

When interactive visualization materially helps, transition through these states:

1. `理解需求`
2. `搜索候选人`
3. `核验关系`
4. `判断优先级`
5. `生成表格`

Animate state changes only. Do not loop motion, simulate fake precision, or leave a progress indicator running when browser work is blocked. Honor reduced-motion settings. If visualization is unavailable, provide short commentary updates instead.

## Result interaction

When useful, let the user locally filter the result summary by `高优先级`, relationship hooks, or direction tags. Keep the exported table as the source of record. A visualization must not contain independent facts that are absent from the verified dataset.
