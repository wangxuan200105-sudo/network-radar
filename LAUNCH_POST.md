# Launch post

## 中文版

我开源了一个 Codex Skill-only Plugin：**Network Radar（人脉雷达）**。

它可以把一句自然语言建联目标，转化成一套可执行的人脉发现流程：搜索候选人、核验个人主页证据、判断本次建联优先级、生成 Excel 或飞书多维表格，并为高优先级联系人准备自然的开场白。

这个项目特别关注两件事：

1. 不用抽象的“匹配度”和“可接近性”分数，而是给出 `高 / 中 / 低 + 具体理由`。
2. 严格区分本人主页信息与侧边栏推荐，避免把旁栏里的学校或公司误标到候选人身上。

项目地址：https://github.com/wangxuan200105-sudo/network-radar

欢迎试用、提 Issue，也欢迎一起扩展更多职业网络平台和输出方式。

## English

I open-sourced **Network Radar**, a Codex skill-only plugin that turns a natural-language networking goal into a verified contact pipeline.

It discovers candidates, verifies profile evidence, assigns explainable priorities, exports Excel or Feishu Bitable results, and drafts low-pressure outreach messages. It avoids pseudo-precise match scores and applies strict profile-section isolation to reduce false relationship labels.

Its default scan is coverage-first: preferences such as alumni or seniority affect ranking rather than accidentally narrowing the eligible pool.

Repository: https://github.com/wangxuan200105-sudo/network-radar
