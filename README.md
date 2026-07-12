# Network Radar · 人脉雷达

一个面向职业建联的 Codex Skill-only Plugin：从自然语言目标出发，发现、核验并整理值得联系的人，输出可解释的人脉表和自然的开场白。

## 它能做什么

- 从搜索页、个人主页链接或已有联系人表发现候选人
- 默认采用覆盖优先的标准扫描，区分硬约束、软偏好与排除项，避免把“校友优先”误做成“仅限校友”
- 严格区分本人主页证据与侧边栏、推荐卡片等误命中
- 为脉脉联系人恢复每人独立的完整主页跳转链接，并在紧邻的“兜底搜索入口”字段保留站内搜索链接
- 用“高 / 中 / 低 + 具体理由”判断本次建联优先级，不制造抽象评分
- 默认输出经过验证的 Excel/CSV 联系人池、核验证据和建联开场白
- 用户选择飞书时，可通过登录态导入或已授权 OpenAPI 生成飞书多维表格
- 按需进行增量更新、校友查漏和新旧版本对比
- 保留用户手工维护的建联状态、开场白和备注
- 在支持 Visualize 的环境中提供温暖社交风格的交互；不可用时自动降级为文字

## 安装

推荐作为 Skill-only Plugin 安装：

```bash
codex plugin marketplace add wangxuan200105-sudo/network-radar
codex plugin add network-radar@network-radar
```

安装完成后开启一个新任务。如果插件没有立即出现，重启 Codex。

仅用于本地实验时，也可以让 Skill Installer 直接从仓库中的 Skill 目录安装：

```text
$skill-installer install https://github.com/wangxuan200105-sudo/network-radar/tree/main/plugins/network-radar/skills/network-radar
```

## 使用

一句话即可开始：

> 我是【你的身份或背景】，想认识【什么样的人】，主要希望【解决什么问题或达成什么目的】。如果有偏好，也可以补充【优先或排除条件】。

例如：

> 我是同济管科应届生，即将入职一家互联网公司做产品，想认识公司里从事 AI 产品的校友，主要想请教方向选择和岗位双选，优先入职 1–3 年的人。

也可以直接提出专项任务：

- `重新检查这份表里有没有漏掉校友，并告诉我与上一版相比修正了谁。`
- `分析这个人的主页，判断是否值得优先建联，并写一条自然的开场白。`
- `把这次抓到的人合并进旧表，但保留我已经填写的联系状态和备注。`

默认的标准扫描会保留所有符合硬条件的候选人，并把校友、共同好友或资历更深者排到前面。未打开详情页的人会标记为 `待核验`，不会从主联系人池中被删除。搜索会按公司别名和岗位族记录覆盖路径，根据连续批次的新增合格人脉决定是否收敛。人数只是搜索过窄的预警，不是凑数目标；标准扫描少于 40 人时会自动完成一次扩展复查。只有用户明确要求“快速看看”或给出较小数量上限时，才收窄为小样本。

## 重要边界

- 不自动发送好友申请或消息。
- 不绕过登录、验证码、访问控制、平台限制或速率限制。
- 不把搜索摘要、侧边栏推荐或同名人物当成本人证据。
- 不承诺搜索结果穷尽平台上的所有相关用户。
- 仓库不包含任何真实联系人数据、登录凭据或浏览器会话。

## 运行能力

核心 Skill 不绑定单一工具。实际运行时可按当前环境使用：

- 已登录的浏览器能力，用于访问搜索页和个人主页
- Spreadsheet 能力，用于生成和验证 `.xlsx` / `.csv`
- 飞书登录态或已授权的飞书 OpenAPI（仅在输出到多维表格时需要）
- Visualize（可选），用于交互确认卡与进度状态

第一版重点适配脉脉，底层证据与表格规则可扩展到其他职业网络来源。脉脉中的 `dstu` 用于稳定识别联系人，完整跳转链接则使用当前搜索上下文里该候选人自己的 `trackable_token`。由于该 token 可能过期，16 列标准输出会在“主页链接”后紧接“兜底搜索入口”字段。

## 仓库结构

```text
.
├── .agents/plugins/marketplace.json
├── plugins/network-radar/
│   ├── .codex-plugin/plugin.json
│   └── skills/network-radar/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       ├── references/
│       └── scripts/
├── scripts/
├── .github/workflows/validate.yml
├── PRIVACY.md
└── LICENSE
```

## 本地校验

```bash
python3 scripts/validate_repository.py
```

发布前执行严格校验：

```bash
python3 scripts/validate_repository.py --release
```

## 一键发布到 GitHub

需要先安装 [GitHub CLI](https://cli.github.com/)；首次运行会引导完成 GitHub 登录。

```bash
./scripts/publish_github.sh public
```

脚本会自动读取 GitHub 用户名和插件 manifest 中的当前版本、回填仓库地址、执行严格校验、初始化 Git、创建或更新仓库、推送代码，并创建对应的标签和 GitHub Release。

## License

MIT
