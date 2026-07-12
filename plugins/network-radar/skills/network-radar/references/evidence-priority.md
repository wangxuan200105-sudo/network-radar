# Evidence and priority rules

## Evidence hierarchy

Use evidence in this order:

1. The person's own profile section: work experience, education, bio, verified platform fields.
2. Platform relationship labels explicitly attached to that person.
3. Search-result snippets attached to that result.
4. Inference from name, role wording, or nearby page context.

Levels 1–2 can support a confirmed label when unambiguous. Level 3 is a discovery clue and normally requires detail-page verification. Level 4 must never become a confirmed relationship label.

## Section isolation

Before assigning a profile fact, identify the section boundary containing it. Exclude:

- Recommended or similar people
- Sidebar cards
- Feed posts and comments
- Mutual-contact profiles
- Search suggestions
- Repeated navigation or footer content

For alumni, require the school in the person's own `教育经历` or equivalent section. Record a concise excerpt such as `本人教育经历：同济大学，工业设计，硕士，2019–2022`. If the school appears only in a sidebar, do not tag alumni.

## Verification status

- `已核验`: decisive evidence was read from the person's own profile or an explicit platform relationship field.
- `部分核验`: some relevant facts are verified but a decisive relationship or role detail remains unclear.
- `待核验`: only a search clue exists, the page is inaccessible, or evidence is absent.
- `冲突`: two sources materially disagree; describe both in `备注/证据`.

Do not interpret missing evidence as a negative fact. `未发现同济教育` means only that it was not verified in the inspected content.

## Priority rubric

Use relative, explainable judgment:

### 高

The person is an obvious first-contact candidate for this purpose. Common patterns include:

- Verified preferred relationship plus the target direction
- Mutual connection plus the target direction
- Current one-degree connection in the target direction
- Very close role or business match with a concrete learning or collaboration reason

### 中

The person is relevant but needs manual review. Common patterns include:

- Direction fits but the relationship hook is weak
- Relationship hook is strong but the role fit is imperfect
- Important page information is incomplete

### 低

The person is outside the current goal, clearly role-mismatched, or too weakly evidenced to prioritize now. Do not use `低` merely because a page is temporarily inaccessible; use `待核验` and usually `中` unless other evidence supports a different priority.

## Priority reason

Write 1–3 concrete factors separated by ` + `. Examples:

- `同济校友 + AI产品 + 入职年限接近`
- `共同好友 + 目标业务方向`
- `岗位相关，但关系线索较弱`
- `教育经历待核验 + 方向匹配`

Never output match scores, accessibility scores, confidence percentages, or rankings presented as objective truth.

