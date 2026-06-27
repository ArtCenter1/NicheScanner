# FRONTEND_HANDOFF.md — 前端 AI 交接包（Niche Scanner MVP）

状态：`已完成`
用户已确认可交接：`是`

## 0. 给前端 AI 的角色与执行规则

**你的角色：** 你是 Niche Scanner 项目的前端实现工程师。你没有参与过产品规划、架构设计和交互设计——这些决策已经完成并写在本文件中。你的唯一职责是按本文件的规格实现前端代码。

**执行规则：**

- 你只负责前端实现，不擅自改产品范围。
- 交互行为以本文件为准，不自行脑补。
- 技术边界以本文件为准，不新增未经允许的依赖。
- 缺信息时先提问，不绕过约束。
- 完成后说明如何运行、如何验证。

## 1. 产品摘要

- **产品一句话：** Niche Scanner 是一个 AI 利基市场发现工具：用户输入 1–5 个商业想法，后端异步抓取 Reddit/Product Hunt/Google Trends 数据，规则引擎评分，60 秒内返回排名结果 + AI 建议，可下载 PDF 报告。
- **核心用户：** AI 创业者 / solo founder / micro studio（已用或正用 Polsia/Bolt/v0 建产品的人）
- **P0 目标：** 单页应用 — 输入想法 → 显示进度 → 展示排名结果 → 下载 PDF。无用户认证。无多页面路由。
- **不做什么：** 用户登录/注册、历史记录、多语言、评分权重自定义、持续监控

## 2. 技术边界

| 项目 | 决策 |
|---|---|
| 前端框架 | **Next.js 14 (App Router)** — 已有完整脚手架 |
| 样式方案 | **Tailwind CSS 3** — 已有配置 |
| UI 组件库 | **Radix UI** (dialog, dropdown-menu, select, slot, tabs, toast) |
| 图标 | **lucide-react** |
| 图表 | **recharts** (用于 rating bar chart) |
| 状态管理 | **zustand** |
| CSS 工具 | tailwind-merge, clsx, class-variance-authority |
| 数据来源 | **初期 mock API**，后期对接真实 FastAPI 后端 |
| 是否允许新增依赖 | **否** — 使用 `package.json` 中已有依赖 |
| 运行命令 | `cd frontend && npm run dev` |
| 构建命令 | `cd frontend && npm run build` |

## 3. 页面和模块

Niche Scanner MVP 是 **单页应用**，只有一个页面 (`/`)，所有交互在同一视口完成。

| 页面 / 模块 | 作用 | 主要组件 | 数据来源 |
|---|---|---|---|
| **首页 (/) 输入区** | Hero + textarea + Analyze 按钮 | `IdeaInput` | — |
| **首页 (/) 进度区** | 显示分析进度（scraping → scoring → enriching） | 内嵌在 `page.tsx` 或 `AnalysisProgress` | POST /analyze -> GET /report/{id} |
| **首页 (/) 结果区** | 排名卡片列表 + 下载按钮 | `ResultsList`, `IdeaCard`, `ReportDownload` | GET /report/{id} |
| **Polsia 遗留页面** | (/agents, /dashboard, /finance 等) | **不要修改** | — |

## 4. 交互契约

### 交互 A：输入想法

- **用户动作：** 在 textarea 输入文字（逗号、换行或分号分隔），点击 "Analyze" 按钮
- **即时反馈：** 按钮变为 "Analyzing..." + spinner 图标，输入区变只读
- **成功结果：** 输入区恢复正常，结果显示在下方区域
- **失败结果：** 错误横幅显示在页面顶部，输入区恢复正常
- **禁用条件：** 输入为空时按钮置灰；分析进行中按钮禁用

### 交互 B：查看进度

- **用户动作：** 无（自动显示）
- **即时反馈：** 分析启动后，输入区下方出现进度卡片，显示当前阶段名称
- **成功结果：** 进度卡片被结果区域替换
- **失败结果：** 进度卡片被错误横幅 + 重试按钮替换

### 交互 C：查看评分结果

- **用户动作：** 无（自动显示）
- **即时反馈：** 结果区域以淡入动画出现
- **成功结果：** 排名卡片列表 — 每个卡片包含：想法名称、总分（大数字）、4 维度 bar chart、行动建议文本、数据来源标注
- **失败结果：** 单个卡片内的失败维度显示 "数据暂缺"

### 交互 D：下载 PDF

- **用户动作：** 点击 "Download PDF" 按钮
- **即时反馈：** 按钮变为 "Generating PDF..." + spinner
- **成功结果：** 浏览器下载 PDF 文件
- **失败结果：** Toast "PDF 生成失败，请重试"
- **禁用条件：** 正在生成时按钮禁用

### 交互 E：重新分析

- **用户动作：** 修改 textarea 内容，再次点击 "Analyze"
- **即时反馈：** 同交互 A
- **成功结果：** 旧结果被新结果替换（不保留历史）
- **失败结果：** 同交互 A 失败

## 5. 状态要求

| 页面 / 模块 | 加载中 | 空状态 | 错误态 | 成功态 |
|---|---|---|---|---|
| **输入区** | textarea 只读 + 按钮 "Analyzing..." + spinner | textarea placeholder + 按钮置灰 | textarea 恢复正常 + 顶部错误横幅 | textarea 恢复正常 |
| **进度卡片** | 显示阶段文字 + 自定义进度动画（非骨架屏） | 隐藏（display:none） | 隐藏，替换为错误横幅 | 隐藏，替换为结果区域 |
| **结果区域** | Skeleton loading cards（灰色占位块 × 输入数量） | 隐藏 | 隐藏（错误在顶部横幅显示） | IdeaCard 列表（淡入动画） |
| **Download PDF** | "Generating PDF..." + spinner | 隐藏 | Toast 提示 | 按钮可用 |
| **排名卡片** | 灰色 skeleton 块（约 200px 高） | — | 灰底 + 维度标注 "数据暂缺" | 完整内容 |

## 6. 视觉要求

- **整体风格：** 干净、专业、数据驱动。类似 Stripe/Linear 风格——大量留白，无复杂装饰
- **颜色：**
  - 主色：深蓝 (`#1e3a5f`) — Hero 背景 + 按钮
  - 强调色：翠绿 (`#10b981`) — 高分；琥珀 (`#f59e0b`) — 中分；玫瑰 (`#ef4444`) — 低分
  - 底色：白 (`#ffffff`) — 卡片背景；灰 (`#f8fafc`) — 页面背景
  - 文字：`#1a1a2e` — 标题；`#64748b` — 副文
- **字体：** 系统默认（-apple-system, Inter, sans-serif），无自定义字体加载
- **间距：** `gap-6`（卡片间），`p-8`（内边距），`max-w-4xl`（内容宽度）
- **圆角：** `rounded-xl`（卡片），`rounded-lg`（按钮），`rounded-md`（输入区）
- **动效：** 结果卡片列表 `animate-fadeIn`（0.3s ease）；进度动画为简洁脉冲点或进度条；过渡使用 `transition-all duration-200`
- **响应式：** 桌面端（>768px）两列卡片网格；移动端（<768px）单列全宽
- **无障碍：** 所有按钮有 aria-label；状态变化用 role="status" 或 aria-live；颜色对比度符合 WCAG AA

## 7. Mock / API

### POST /api/v1/analyze

```json
// Request
{
  "ideas": ["AI tool for lawyers", "SaaS for plumbers", "Pet-sitting marketplace"]
}

// Response (202)
{
  "analysis_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "pending"
}
```

### GET /api/v1/report/{analysis_id} (polling)

```json
// In progress (status = "scraping" | "scoring" | "enriching")
{
  "status": "scraping",
  "progress": "Scraping Reddit, Product Hunt, and Google Trends..."
}

// Complete
{
  "status": "complete",
  "ideas": [
    {
      "name": "AI tool for lawyers",
      "total_score": 78,
      "dimensions": {
        "supply_quality": 82,
        "demand_heat": 74,
        "business_viability": 65,
        "timing": 88
      },
      "recommendation": "Start with a Chrome extension that summarizes legal documents. Law firms are actively seeking AI tools — the signal is strongest in demand heat and timing.",
      "signals": {
        "reddit": {"available": true, "post_count": 124, "avg_sentiment": 0.6},
        "trends": {"available": true, "direction": "rising", "slope": 0.15},
        "producthunt": {"available": true, "competitor_count": 3, "avg_rating": 3.2}
      }
    },
    {
      "name": "SaaS for plumbers",
      "total_score": 52,
      "dimensions": {
        "supply_quality": 45,
        "demand_heat": 60,
        "business_viability": 70,
        "timing": 35
      },
      "recommendation": "The market is less crowded but demand signals are weaker. Consider niche focus on scheduling + invoicing for independent plumbers.",
      "signals": {
        "reddit": {"available": true, "post_count": 38, "avg_sentiment": 0.3},
        "trends": {"available": false, "error": "Rate limited"},
        "producthunt": {"available": true, "competitor_count": 1, "avg_rating": 4.5}
      }
    }
  ]
}

// Error
{
  "status": "failed",
  "error": "All data sources failed",
  "ideas": []
}
```

### GET /api/v1/report/{analysis_id}/pdf

Returns `application/pdf` binary.

**开发期间 mock 数据：** 在前端建立 mock 模式，当无后端运行时，Analyze 按钮触发 `setTimeout` 3 秒后返回上方示例 JSON。用 `.env.local` 中 `NEXT_PUBLIC_MOCK_API=true` 控制。

## 8. 禁止事项

- 不要改 PRD 范围（不做登录、不做历史记录、不新增页面路由）
- 不要改交互逻辑（输入→进度→结果→PDF 的线性流程）
- 不要引入未确认依赖（只使用 `package.json` 中已有依赖）
- 不要硬编码密钥（API 地址从 `.env.local` 读取）
- 不要把 mock URL、API URL 散落在组件里（集中到 `lib/api.ts`）
- 不要删除或修改 Polsia 遗留页面（不在 `/` 路由覆盖范围内的页面）
- 不要往 layout.tsx 中新增服务端组件/数据加载逻辑

## 9. 验收标准

- [ ] P0 主流程可用：打开页面 → 输入 3 想法 → 点击 Analyze → 看到进度 → 看到排名 → 下载 PDF
- [ ] 交互行为符合第 4 节的 5 个交互契约
- [ ] 四类状态（加载/空/错误/成功）符合第 5 节
- [ ] UI 符合第 6 节视觉要求（颜色、间距、响应式、动效）
- [ ] 移动端 390px 宽度下所有内容正常
- [ ] 没有控制台明显报错
- [ ] 可以按 `npm run dev` 启动并看到页面
- [ ] 当数据源部分失败时，对应维度显示 "数据暂缺" 而非空白

## 10. 交接确认

- 用户已确认可交给前端 AI：`是`
- 确认时间：2026-06-27
- 备注：后端 API 尚不存在时，用 `NEXT_PUBLIC_MOCK_API=true` 模式开发
