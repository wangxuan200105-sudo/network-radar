# Maimai link handling

Use this reference whenever Maimai contacts will be exported to Excel, CSV, Feishu, or another clickable table.

## Separate identity from navigation

Maimai exposes two different concepts:

- `dstu` or result `id`: stable identity used for deduplication and incremental updates.
- `trackable_token` plus search-source parameters: result-specific navigation context used to open the profile from a search flow.

Do not confuse them. A naked URL such as `https://maimai.cn/profile/detail?dstu=123` is an identity-derived guess, not a reliable clickable profile link.

## Link priority

Use this order for `主页链接`:

1. The exact full detail URL exposed by the current authenticated search result for that candidate.
2. A full detail URL constructed only from the `dstu/id` and `trackable_token` found on the same current result record, with the search-source parameters used by that result.
3. If the current token cannot be recovered, the encoded site-search fallback for `name + company + role`.

Never use a naked `dstu` detail link as the final primary link. Never copy a token from another card, another candidate, or an earlier scan.

A typical current full link has this shape:

```text
https://maimai.cn/profile/detail?dstu=<candidate-id>&trackable_token=<same-record-token>&from=pc_web_search&outofrel=false&is_node=1
```

Treat this as a current navigation link, not a permanent URL. Maimai may bind it to time, account, session, source, or risk-control context.

## Recover per-candidate tokens

1. Open the normal Maimai people-search page in the authenticated browser task space.
2. Let the page load the visible result cards normally.
3. Inspect the page's own search response used for those visible cards. At the time of writing this is commonly a `/search/contacts?...jsononly=1` request, but discover the actual current request instead of assuming a fixed endpoint forever.
4. Read the response through the same authenticated browser context. Do not call it from an unrelated server session or use it to bypass access controls.
5. Map each response record by `dstu/id`. Extract that record's own `trackable_token`, city, and visible card metadata.
6. Join tokens to candidates by ID, never by result-card position or array order.
7. If a candidate is missing because ranking changed, run a targeted search using `name + company + role` and repeat the same ID-based join.

Only collect records represented in the user's authorized search results. Stop on login, CAPTCHA, access denial, or rate limiting.

## Search fallback

Build a stable, URL-encoded fallback from the most discriminating visible terms:

```text
https://maimai.cn/web/search_center?type=contact&query=<encoded name company role>&highlight=true
```

Put the fallback in the dedicated `兜底搜索入口` field immediately after `主页链接`, even when the full detail link is available. Keep only the stable ID, link source, and expiry note in `备注/证据`, for example:

```text
稳定ID：dstu=223214413；链接来源：本轮站内搜索响应；详情直链可能随会话或时间失效。
```

If no current token is available, use the search fallback as `主页链接` and note `当前未取得完整跳转 token，先从搜索结果卡片进入主页`.

## Pre-export checks

Before writing the final workbook:

1. Reconcile every detail URL's `dstu` with the candidate's stable ID.
2. Confirm every full detail URL has a non-empty `trackable_token` from the same record.
3. Reject any token mapped to more than one distinct candidate ID.
4. Record the count and percentage of full-token links and populated `兜底搜索入口` fields.
5. Run targeted searches for missing-token rows before accepting fallback-only output.
6. Open a small representative sample through the authenticated search context and verify that the expected profile is reached without 403.
7. Run `scripts/validate_contacts.py` on the exported CSV.

Do not claim links are permanent. Report the retrieval time, full-token coverage, fallback coverage, and any rows that still require a fresh search.

## Incremental refresh

On a later scan, retain `dstu` as the contact key and refresh the full navigation URL from the new search response. A token change is link maintenance, not a new person and not a meaningful profile-field change.

Do not commit exported URLs containing real candidate tokens to a public repository. Keep them only in the user's private output files.
