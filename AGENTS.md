# AGENTS.md — Niche Scanner 线性执行入口

本文件是默认唯一入口。目标：让 AI 按固定流程推进项目，同时避免每次对话读取全部文档。

## 1. 当前项目状态

| 字段 | 当前值 |
|---|---|
| 当前步骤 | `7_验收闸门`（M0–M3 验收通过；M4 前端 + M5 Docker 待完成） |
| 当前目标 | 前端组件实现 (M4) → Docker 集成验证 (M5) → bash check.sh 最终验收 |
| PRD | `已完成 ✅` |
| 项目框架 | `已完成 ✅` |
| 交互逻辑 | `已完成 ✅` |
| 前端交接包 | `已完成 ✅` |
| 前端代码 | `进行中` — M4 待实现（IdeaInput / ResultsList / IdeaCard / ReportDownload） |
| 当前版本 | `0.1.0-dev` |
| 历史报错 | `已记录` ✅ — 见 ERRORS.md |
| 验收闸门 | `已配置 ✅` — M0–M3 验收通过；M4/M5 后执行最终 check.sh |

**项目背景：** Niche Scanner 已从 Polsia fork 完成品牌替换，Infrastructure 脚手架（Docker Compose、Next.js 14、nginx、Makefile）已就位。ARCHITECTURE.md 有完整实现计划。下一步是真正的业务代码。

允许的步骤：

1. `1_PRD规划`
2. `2_项目框架`
3. `3_交互逻辑`
4. `4_前端交接包`
5. `5_前端生成代码`
6. `6_项目记录`
7. `7_验收闸门`

## 2. 核心流程

```text
1_PRD规划
  -> 2_项目框架
  -> 3_交互逻辑
  -> 4_前端交接包
  -> 5_前端生成代码
  -> 6_项目记录
  -> 7_验收闸门
```

说明：

- 主流程是线性的，优先按顺序推进。
- 如果用户明确要求修 bug、查版本、跑验收，可以跳到对应步骤。
- 每一步完成后，更新本文件状态块。
- 不要因为"保险起见"读取全部文档。

**发现约束冲突时的规则：**

如果在推进过程中发现当前步骤与前序决策冲突（例如技术可行性影响产品范围、交互设计超出技术边界），必须：

1. 停止推进当前步骤。
2. 明确标注冲突点：哪个决策 vs 哪个约束。
3. 退回冲突涉及的最早步骤，等待用户确认修订后再继续。
4. 不允许在冲突未解决时绕过约束自行决定。

## 3. 项目身份（固定契约）

以下内容不可更改，除非用户明确要求：

### What this project IS

**Niche Scanner** 是一个 AI 驱动的利基市场发现工具。输入 1–5 个商业想法，输出带有分数的排名分析和数据支持的建议（PDF 报告）。

- **商业模式：** 情报产品 — 一次性付款（$79/报告），不做订阅
- **定位：** Polsia 生态的入口工具（但独立可用）
- **架构：** FastAPI 后端 + Next.js 14 前端 + PostgreSQL
- **评分：** 基于规则（rule-based），不依赖 LLM
- **LLM 使用：** 仅用于推荐文字生成，通过 Hermes CLI 子进程调用

### What this project IS NOT

- 不是 Polsia（9-agent 业务流程自动化）
- 不使用 `BasePolsiaAgent`、Claude Code CLI、ChromaDB、Redis pub/sub
- 不使用 `CLAUDE_CLI_MOCK` — 使用 `HERMES_MOCK`
- 没有 9-agent crew 模式

### 关键环境变量

| 变量 | 描述 |
|---|---|
| `HERMES_MOCK=true` | 测试中跳過真实 Hermes CLI 子进程 |
| `SANDBOX_MODE=true` | 防止真实外部 API 调用 |
| `DATABASE_URL` | PostgreSQL 连接字符串 |

### 常见陷阱

- **不要在单元测试中调用真实 scraper** — 使用 `respx` 或 `httpx_mock`
- **scoring 是 rule-based，不是 LLM-based** — LLM 仅用于推荐文本
- **部分数据是可接受的** — 如果某个 scraper 失败，记录日志并用可用信号继续

## 4. 文件路由表

| 当前任务 | 只读取这些文件 | 默认不读 |
|---|---|---|
| PRD 规划 | `PRD.md` | 其他全部 |
| 项目框架 / 技术方案 | `PRD.md`、`PROJECT_FRAME.md`、必要时 `GATES.md` | `FLOWS.md`、`FRONTEND_HANDOFF.md`、历史记录 |
| 交互逻辑 | `PRD.md`、`PROJECT_FRAME.md`、`FLOWS.md` | 版本和报错记录 |
| 生成前端交接包 | `PRD.md`、`PROJECT_FRAME.md`、`FLOWS.md`、`FRONTEND_HANDOFF.md`、必要时 `GATES.md` | 历史报错（除非影响交接） |
| 前端 AI 生成代码 | `FRONTEND_HANDOFF.md`、相关源码、必要时 `check.sh` | 完整 PRD / 完整历史记录 |
| 记录当前状态 | `STATUS.md`、`CHANGELOG.md`、必要时 `ERRORS.md` | 产品和交互文档 |
| 记录历史报错 | `ERRORS.md`、`STATUS.md`、相关报错输出 | 完整产品文档 |
| 验收闸门 | `GATES.md`、`check.sh`、必要时 `PRD.md` 验收标准 | 其他规划文档 |
| 理解这套框架 | `README.md`、必要时 `WORKFLOW.md` | 项目业务文档 |
| **接续已有项目** | `STATUS.md`、本文件状态块；若 `ERRORS.md` 有记录则同时读取 | 完整产品文档、完整历史记录 |
| **后端 / API 设计** | `PRD.md`、`PROJECT_FRAME.md` 第 6 节 API/Mock 判断 | `FLOWS.md`（除非 API 形状直接影响页面行为） |

## 5. 各阶段视角

每个阶段进入时，以对应视角工作，不要在阶段内切换角色。

| 阶段 | 视角 | 核心判断标准 |
|---|---|---|
| `1_PRD规划` | 资深产品经理 | 用户问题清楚、P0 可交付、验收可观察 |
| `2_项目框架` | 技术架构师 | 技术选型有理由、模块边界清楚、不可逆决定已确认 |
| `3_交互逻辑` | 交互设计师 | 每个动作的触发 / 反馈 / 异常路径清楚 |
| `4_前端交接包` | 技术负责人（写规格） | 接收方 AI 无需问任何问题就能开工 |
| `5_前端生成代码` | 前端工程师（执行规格） | 严格按交接包实现，不自行扩展范围 |
| `6_项目记录` | 项目经理 | 下次对话无需翻聊天记录也能接续 |
| `7_验收闸门` | QA 工程师 | 用脚本和验收标准说话，不靠 AI 自我报告 |

### PRD 阶段额外规则（最容易出问题的阶段）

- 先判断用户真实想解决什么问题，再决定问什么。
- 每轮最多问 3 个关键问题，避免一口气抛长问卷。
- 主动指出范围过大、目标不清、验收不可测的地方。
- 把 P0 压到可以交付、可以验收、可以交给前端 AI 的最小版本。
- 明确区分事实、假设、用户确认、待确认。
- 用户没有确认定位、P0、验收标准前，不进入下一步。

## 6. 硬门

- 用户没有明确说"开始写代码"之前，不写功能代码。
- 不擅自选择或更改核心技术栈、框架、存储方案、付费服务。
- 不引入未经用户确认的新依赖。
- 不硬编码密钥、密码、token。
- 所有外部输入必须校验。
- 不删除或覆盖用户数据，除非用户明确批准。
- 没有通过 `bash check.sh` 且没有满足相关验收标准，不许声称完成。

## 7. 文档更新规则

| 发生了什么 | 更新哪里 |
|---|---|
| 产品定位、用户、范围、验收变化 | `PRD.md` |
| 技术栈、目录结构、模块、数据模型变化 | `PROJECT_FRAME.md` |
| 页面、流程、状态、交互、异常变化 | `FLOWS.md` |
| 给前端 AI 的交接内容变化 | `FRONTEND_HANDOFF.md` |
| 当前版本、当前进度、下一步变化 | `STATUS.md` |
| 发布或完成一个版本 | `CHANGELOG.md` |
| 出现报错、失败、踩坑 | `ERRORS.md` |
| 验收命令、质量标准变化 | `GATES.md`、`check.sh` |
| 当前步骤变化 | 本文件状态块 |

## 8. 回复结尾格式

每次较完整的回复结尾都汇报：

1. 完成了什么。
2. 下一步是什么。
3. 有没有卡点或需要用户确认。

## 参考

- 框架来源：https://github.com/liuethanyes-spec/vibecoding-linear-framework
- 项目 Wiki：`entities/niche-scanner.md`、`concepts/current-focus.md`
