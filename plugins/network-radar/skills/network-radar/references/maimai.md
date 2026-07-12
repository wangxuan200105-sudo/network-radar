# Maimai workflow

## Browser setup

Use the authenticated browser session. Prefer ego-browser when available. Create one task space for the user's networking goal and reuse it across discovery, verification, and correction rounds.

If login, CAPTCHA, user control, or an inactive task space blocks work, follow the browser handoff rules. Never work around the block through an unrelated session or unauthenticated endpoint.

## Discovery

Build an adaptive search matrix from the user's hard constraints and role-family vocabulary. A standard scan commonly needs 8–20 focused searches; use fewer only for an explicitly quick preview. Typical combinations include:

- Company + function
- Company + specialty
- Company + school
- Specialty + city
- Company + seniority or program name

Expand the target function into genuine role-family synonyms before searching. For an operations request, consider titles such as `运营`, `用户运营`, `商家运营`, `平台运营`, `类目运营`, `活动运营`, `内容运营`, `产品运营`, `增长运营`, `策略运营`, `业务运营`, `行业运营`, `供给运营`, `生态运营`, and `电商运营`. Adapt this list to the user's exclusions and the platform's actual vocabulary.

Search preference clues such as school or seniority in separate lanes. Do not require them in every query. Otherwise `校友优先` becomes an accidental alumni-only filter and damages recall.

Collect only data visibly attached to each search result: displayed name, profile link or user ID, company, role, city, direction clues, platform relationship tags, and the result-specific navigation token when the page exposes it.

Apply exclusions after collecting enough context to distinguish adjacent roles. `招商不看` excludes招商/商务拓展/招商运营 when that is the actual function, but it must not automatically exclude `商家运营`. Exclude clearly non-target functions such as product, engineering, HR, finance, legal, design, or sales only when the user said other job families are out of scope.

Prefer semantic page inspection. Use direct DOM extraction only when it is simpler and returns data already visible in the authenticated page. Do not encode brittle selectors into permanent skill logic without verifying them in the current session.

## Stable identity

For Maimai profile URLs, use `dstu` as the stable internal ID when present. A stable identity and a working navigation URL are different artifacts: `dstu` supports deduplication, while the current result-specific `trackable_token` supports navigation. Store the full working profile URL in the table and deduplicate by `dstu`, not the full query string. Read `maimai-links.md` before exporting.

## Detail-page verification

Open high-potential or ambiguous candidates. Capture the person's main profile content and identify explicit section boundaries before extracting facts.

For education, require evidence inside the person's own `教育经历` section. A school name found in recommended contacts, common-connection cards, or sidebar modules is a false positive.

For employment, distinguish current role from previous experience. Do not treat a former employer as the current company merely because it appears first in a search snippet.

Record concise evidence in `备注/证据`, for example:

`本人教育经历：同济大学，工业设计，硕士，2019–2022；本人工作经历：拼多多，AI产品经理。`

## Scope and cleanup

Do not claim to have found every relevant Maimai user. State search terms and the number of results/pages inspected. Stop or slow down if the platform shows access limits.

Do not stop merely because the verified high-priority segment is small. Keep the broader eligible pool and apply the saturation rules in `references/discovery-scope.md`.

When finished, close the ego-browser task space unless the user explicitly needs the live page, login handoff, or visible result preserved.
