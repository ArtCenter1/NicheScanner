# PRD.md — Niche Scanner 产品需求文档

状态：`已完成`
用户已确认：`是`（基于 wiki: pulsia-next-stage-shovel-opportunities）

## 0. 产品经理判断

- **用户真正想解决的问题是**：AI 创业者（solo founder / micro studio）能快速 launch 产品（via Polsia/Bolt/v0），但不知道**该建什么**——市场缺乏持续监控「需求旺盛但供给不足」微小利基的工具
- **当前最大不确定性是**：Scraper 数据源的可靠性和覆盖率（Reddit/Product Hunt/Google Trends 的 API 限制）
- **P0 先做**：输入 1–5 个想法 → 异步抓取 → 规则评分 → 排名输出 + PDF 报告
- **不建议这版做**：用户画像/登录系统、多语言、历史趋势追踪、API 开放给第三方

## 1. 一句话定位

**Niche Scanner** 是一个 AI 利基市场发现工具：输入 1–5 个商业想法，它通过 Reddit、Product Hunt、Google Trends 等公开数据源，在 60 秒内输出带评分的排名分析和 PDF 报告，帮你决定「先做哪个」。

## 2. 用户与场景

| 项目 | 内容 |
|---|---|
| 核心用户 | **AI 创业者 / solo founder / micro studio**（已用或正用 Polsia/Bolt/v0/Replit Agent 建产品的人） |
| 使用场景 | 手上有多个想法，需要数据决定优先级；或者完全空想阶段，需要市场信号启发方向 |
| 触发时机 | 每周做 1-2 次分析，测试新想法；Polsia 生态用户 launch 新公司前做验证 |
| 当前替代方案 | 手动搜索 Reddit、Product Hunt、Google Trends 再自己判断 — 耗时 30min-2h/次 |
| 当前痛点 | 创业者花大量时间调研但缺乏结构化对比；感觉型判断易出错 |
| 使用频率 | 低频高价值：一个用户每月用 2-5 次，每次 $79 |

## 3. 问题定义

### 必须解决的问题

- 输入 1–5 个商业想法，输出可按评分排序的排名结果
- 从 Reddit 抓取讨论热度和情绪
- 从 Google Trends 抓取搜索趋势斜率
- 从 Product Hunt 抓取竞品供给密度
- 规则引擎计算 Niche Score（0–100）
- Hermes CLI 生成每个想法的"第一行动建议"
- 提供 PDF 报告下载
- 部分数据源失败时，仍用可用信号继续并提示

### 明确不解决的问题

- 不提供持续监控（每日/每周自动扫描）——此为 v2
- 不提供用户账户/登录系统——v0 就是公开页面
- 不提供历史趋势对比——v0 只做单次 snapshot
- 不提供评分权重自定义——v0 固定权重

## 4. 范围

### P0：必须交付

1. **输入界面**：textarea 输入 1–5 个想法，逗号或换行分隔
2. **异步分析**：POST /analyze 立即返回 analysis_id，后台并行抓取 + 评分
3. **实时轮询**：前端每 3 秒轮询 GET /report/{id}，显示分析进度
4. **评分结果**：4 维度打分（Supply Quality / Demand Heat / Viability / Timing），总分 0–100
5. **排名列表**：按总分降序排列，每个想法显示维度分解 bar chart
6. **推荐建议**：每个想法有 Hermes LLM 生成的"第一行动建议"文本
7. **PDF 报告**：WeasyPrint 渲染，含排名、评分分解、推荐建议
8. **部分数据容错**：某个 scraper 失败时，用剩余信号评分并标注"XX 数据暂缺"

### P1：后续增强

- 数据源扩展（Twitter/X, G2, App Store 评论）
- 历史分析保存和对比
- 评分权重可调
- 用户账户系统
- 报告分享链接

### 不做什么

- 不做登录/认证系统（v0 纯公开）
- 不做持续监控/定期推送
- 不做多语言支持
- 不做 API 开放
- 不做订阅制商业模式

## 5. 成功标准

产品做成后，用户应该能：

- 打开页面 → 粘贴 1–5 个想法 → 点击 Analyze → 60 秒内看到评分排名
- 每个想法看到分数、维度分解、一条 AI 行动建议
- 一键下载 PDF 报告，内容与页面上一致
- 即使某个数据源挂了，仍然能看到部分评分 + 缺失标注
- 移动端和桌面端都正常可用

## 6. 验收标准

- [ ] `POST /analyze` 接受 `{"ideas": ["idea1", "idea2"]}`，返回 `{"analysis_id": "uuid"}`
- [ ] 前端提交 3 个想法后，60 秒内显示完整排名结果
- [ ] 每个想法展示总分 + 4 维度分数（可视化 bar chart）
- [ ] 每个想法有 AI 生成的行动建议文本（非空）
- [ ] "Download PDF" 按钮产出含完整内容的 PDF
- [ ] 断开网络后提交一个 scraper 目标，提示"部分数据不可用"但仍显示评分
- [ ] 移动端（390px 宽）布局正常，无文字溢出或错位
- [ ] `bash check.sh` 退出码 0
- [ ] `make test` 全部通过
- [ ] 没有硬编码密钥或 token 在源码中

## 7. 约束

| 类型 | 内容 |
|---|---|
| 时间 | MVP 工期 2 周（单人开发者） |
| 平台 | Web 优先（Next.js 14 + FastAPI），移动端响应式 |
| 数据 | Reddit API / Product Hunt API / Google Trends（非官方） — 需处理 rate limit 和 API 不稳定 |
| 成本 | 零外部服务成本（除 Hermes CLI 免费额度外）；WeasyPrint 免费；托管在既有 Docker 环境 |
| LLM | 仅 Hermes CLI 子进程，不用 Claude Code、OpenAI 等外部 LLM API |

## 8. 假设与风险

| 类型 | 内容 | 如何验证 |
|---|---|---|
| 假设 | Reddit / Product Hunt / Google Trends 提供足够区分度的信号 | MVP 后用 50 个想法测试评分与人工判断的相关性 |
| 风险 | Reddit API rate limit 导致部分请求失败 | 实现指数退避 + 部分数据模式 |
| 风险 | Google Trends 非官方接口不稳定 | 异步 + 超时 + fallback 到 "数据暂缺" |
| 风险 | Hermes CLI 在 Docker 容器内不可用 | 捆 local hermes binary 或 fallback 到 mock |
| 风险 | 评分算法太简单，结果没有实际价值 | 先上线，收集反馈后迭代 v2 |

## 9. 待确认问题

- **评分权重**：已确认 MVP 固定权重（Supply 35% / Demand 30% / Viability 20% / Timing 15%）
- **目标受众**：已确认 — AI 创业者 / solo founder / micro studio（非初次编程学习者）
- **数据源优先级**：MVP 只做 Reddit + Product Hunt + Google Trends；G2/App Store/ Twitter 留到 v2

## 10. 确认记录

- 确认来源：wiki `star up ideas/pulsia-next-stage-shovel-opportunities.md` + ARCHITECTURE.md + README.md
- 确认时间：2026-06-27
- 备注：Niche Scanner 定位为 Wave 1 "AI 增长引擎"的第一款工具 — 利基市场发现器
