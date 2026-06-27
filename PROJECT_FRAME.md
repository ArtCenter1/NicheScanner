# PROJECT_FRAME.md — 项目框架

状态：`已完成`
用户已确认：`是`（基于 PRD.md 和 ARCHITECTURE.md）

## 1. 项目类型

| 项目 | 内容 |
|---|---|
| 产品形态 | Web 单页应用（SPA 式多步交互） |
| 是否有前端界面 | 是 |
| 是否需要后端 | 是 |
| 是否需要数据库 | 是 |
| 是否需要登录 / 权限 | 否（v0 纯公开，无认证） |
| 是否需要外部服务 | 是（Reddit API, Product Hunt API, Google Trends scraping + Hermes CLI） |

## 2. 技术栈

所有不可逆选择均以 PRD.md 为基准。

| 层 | 选择 | 为什么 | 用户已确认 |
|---|---|---|---|
| 后端语言 | Python 3.13 | 已有 pyproject.toml 配置，Hermes CLI 原生支持，生态适合数据处理 | ✅ |
| 后端框架 | **FastAPI** | 异步原生，适合 httpx 并行抓取；已有 docker-compose 基础 | ✅ |
| ASGI 服务器 | **Uvicorn** | FastAPI 默认，开发热重载 | ✅ |
| 数据库 (prod) | **PostgreSQL 16** | 已有 docker-compose.yml 配置 | ✅ |
| 数据库 (dev/test) | **SQLite (aiosqlite)** | 零配置，单元测试无需 Docker | ✅ |
| ORM | **SQLAlchemy 2.0 + asyncpg** | 项目已有 alembic 迁移基础，支持 async | ✅ |
| 前端框架 | **Next.js 14 (App Router)** | 已有完整脚手架（来自 Polsia fork） | ✅ |
| 样式方案 | **Tailwind CSS 3** | 已有配置 | ✅ |
| UI 组件 | **Radix UI + lucide-react + recharts** | 已有依赖，评分可视化需要 recharts | ✅ |
| 状态管理 | **zustand** | 已有依赖，轻量 | ✅ |
| HTTP 客户端 | **httpx (AsyncClient)** | 异步并行抓取 | ✅ |
| PDF 渲染 | **WeasyPrint** | HTML→PDF，Python 原生 | ❓（需验证 Docker 兼容性） |
| LLM 接口 | **Hermes CLI subprocess** | 项目核心决策，非 Claude Code | ✅ |
| 任务队列 | **无（MVP）** | MVP 用 FastAPI BackgroundTasks + asyncio.create_task 即可，Celery/Redis 留 v2 | ✅ |
| 容器化 | **Docker Compose** | 已有配置，MVP 精简为 postgres + backend + frontend | ✅ |
| 测试框架 | **pytest + httpx_mock** | 已有 pytest 配置 | ✅ |
| Lint | **ruff + mypy** | 已有 pyproject.toml 配置 | ✅ |

## 3. 目录结构

```
D:/My_Projects/Niche Scanner/
├── backend/                          ← 新建（当前为空）
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   ← FastAPI app 入口
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── analyze.py        ← POST /analyze
│   │   │       └── report.py         ← GET /report/{id}
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py             ← 配置（env vars）
│   │   │   └── database.py           ← 数据库引擎 + session
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── analysis.py           ← Analysis ORM 模型
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── scraper.py            ← asyncio httpx scrapers
│   │       ├── scorer.py             ← rule-based scoring
│   │       ├── hermes_llm.py         ← Hermes CLI wrapper
│   │       └── report_pdf.py         ← WeasyPrint PDF 生成
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py               ← Fixtures: mock_hermes, async_db_session, api_client
│   │   ├── test_scorer.py
│   │   ├── test_scraper.py
│   │   └── test_analyze_api.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                         ← 已有（需清理 Polsia 遗留页面）
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx            ← 修改为 Niche Scanner 布局
│   │   │   ├── page.tsx              ← 主页面：输入 + 结果
│   │   │   └── globals.css
│   │   ├── components/
│   │   │   ├── IdeaInput.tsx         ← 想法输入区
│   │   │   ├── ResultsList.tsx       ← 排名列表
│   │   │   ├── IdeaCard.tsx          ← 单个想法卡片（含评分 bar chart）
│   │   │   └── ReportDownload.tsx    ← PDF 下载按钮
│   │   └── lib/
│   │       └── api.ts                ← API 客户端（POST /analyze, GET /report/{id}）
│   └── package.json
├── docker-compose.yml                ← 精简（移除 redis/celery/nginx/chroma）
├── pyproject.toml                    ← 已有
├── Makefile                          ← 已有
├── AGENTS.md                         ← 框架入口（已建）
├── PRD.md                            ← 产品需求（已建）
├── ARCHITECTURE.md                   ← 旧实现计划（参考用，以 PRD.md 为准）
├── DEVLOG.md                         ← 开发日志
└── .env.example                      ← 环境变量模板
```

### 待清理的 Polsia 遗留（v0 阶段不要动，但需要注意它们存在）

```
frontend/src/app/ads/                 ← Polsia 遗留
frontend/src/app/agents/              ← Polsia 遗留
frontend/src/app/dashboard/           ← Polsia 遗留
frontend/src/app/finance/             ← Polsia 遗留
frontend/src/app/memory/              ← Polsia 遗留
frontend/src/app/outreach/            ← Polsia 遗留
frontend/src/app/settings/            ← Polsia 遗留
frontend/src/app/social/              ← Polsia 遗留
frontend/src/app/tasks/               ← Polsia 遗留
tests/                                ← 多数 Polsia 遗留测试
celery_app/                           ← Polsia 遗留（MVP 不使用）
```

**清理策略**：v0 开发时不删除，只确保 Niche Scanner 新页面正常工作。v1 启动时一次性清理。

## 4. 模块边界

| 模块 | 负责什么 | 不负责什么 | 输入 | 输出 |
|---|---|---|---|---|
| **api/v1/analyze** | 接收想法、创建分析任务 | 实际的抓取和评分 | `{"ideas": [...], "analysis_id"}` | `{"analysis_id": "uuid"}` |
| **api/v1/report** | 返回分析结果和 PDF | 数据获取和计算 | `analysis_id` | 分析结果 JSON / PDF 二进制 |
| **services/scraper** | 并行抓取 3 个数据源 | 评分、数据持久化 | `keyword` + `analysis_id` | `{reddit: {...}, trends: {...}, producthunt: {...}}` |
| **services/scorer** | 规则引擎计算分数 | 数据抓取、LLM 调用 | scraper 输出 | `{total_score, dimensions: {...}}` |
| **services/hermes_llm** | 调用 Hermes CLI 生成建议 | 评分、数据抓取 | `{idea, scores}` | 行动建议文本 |
| **services/report_pdf** | HTML→PDF 渲染 | 数据获取 | `{analysis}` | PDF 文件路径 |
| **frontend/page** | 输入想法 → 显示进度 → 展示结果 → 下载 PDF | 后端逻辑、数据持久化 | 用户输入 | UI 渲染 |

## 5. 数据模型

### Analysis（核心表）

```python
class Analysis(Base):
    __tablename__ = "analyses"

    id: str = Column(String(36), primary_key=True, default=uuid4)  # UUID
    status: str = Column(String(20), default="pending")  # pending | scraping | scoring | complete | partial | failed
    ideas_raw: str = Column(Text)  # 原始输入 JSON
    created_at: datetime = Column(DateTime, default=func.now())
    completed_at: datetime = Column(DateTime, nullable=True)

    # JSON 存储结果
    results: dict = Column(JSON, nullable=True)  # 按 idea 索引的完整结果
    # {idea: {score: N, dimensions: {supply: N, demand: N, viability: N, timing: N},
    #         signals: {reddit: {...}, trends: {...}, producthunt: {...}},
    #         recommendation: "text"}}
    error_info: dict = Column(JSON, nullable=True)  # 各数据源错误记录
```

**无需额外表**：MVP 单表即可。v2 添加 users、saved_reports 等。

### 数据流

```text
用户输入 1-5 ideas
  │
  ▼
POST /analyze
  │ 创建 Analysis(status=pending)
  │ 返回 {analysis_id}
  │
  ▼
FastAPI BackgroundTask
  │ status = scraping
  │
  ├── httpx.AsyncClient.gather(
  │     scrape_reddit(keyword),
  │     scrape_trends(keyword),
  │     scrape_producthunt(keyword)
  │   )
  │   每源失败 → 记录到 error_info，继续
  │
  ▼
services/scorer.py
  │ status = scoring
  │ 规则引擎计算 4 维度分 × 总分
  │
  ▼
services/hermes_llm.py
  │ status = enriching
  │ Hermes CLI subprocess 生成行动建议
  │
  ▼
status = complete | partial
结果写入 Analysis.results JSON
  │
  ▼
前端轮询 GET /report/{id} ← 返回 results JSON
下载 → services/report_pdf.py → PDF
```

## 6. API / Mock 判断

| 问题 | 决策 |
|---|---|
| 前端是否先用 mock | 是。开发阶段前端用 mock API 响应，不依赖真实 scraper |
| 是否需要真实 API | 需要（Reddit API / Product Hunt API / Google Trends scraping）但在 SANDBOX_MODE=true 时自动 mock |
| API 契约写在哪里 | 内联到 `FRONTEND_HANDOFF.md` + OpenAPI schema（FastAPI 自动生成） |
| Mock 数据提供方式 | `HERMES_MOCK=true` + `SANDBOX_MODE=true` + `httpx_mock` fixture |

### API 端点（MVP）

```
POST /api/v1/analyze
  Body: {"ideas": ["AI tool for lawyers", "SaaS for plumbers"]}
  Response 202: {"analysis_id": "abc-123", "status": "pending"}

GET /api/v1/report/{analysis_id}
  Response 200 (in_progress): {"status": "scraping", "progress": 30}
  Response 200 (complete): {
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
        "recommendation": "Start with a Chrome extension...",
        "signals": {
          "reddit": {"post_count": 124, "avg_sentiment": 0.6},
          "trends": {"direction": "rising", "slope": 0.15},
          "producthunt": {"competitor_count": 3, "avg_rating": 3.2}
        }
      }
    ]
  }

GET /api/v1/report/{analysis_id}/pdf
  Response 200: application/pdf
```

## 7. 实现切片

每个切片可独立运行和验收。

| 切片 | 目标 | 交付物 | 验收方式 |
|---|---|---|---|
| **M0** | 项目脚手架 + 验收闸门 | FastAPI stub (`GET /health`)、`check.sh`、`GATES.md`、`conftest.py` | `bash check.sh` 退出码 0 |
| **M1** | 评分引擎 + 测试 | `scorer.py` + `test_scorer.py`，纯规则逻辑无外部依赖 | `pytest tests/test_scorer.py -v` 全通过 |
| **M2** | Scraper 层 + mock | `scraper.py` + `test_scraper.py`，httpx_mock 覆盖 3 数据源 | `pytest tests/test_scraper.py -v` 全通过 |
| **M3** | 完整 API 端点 | `POST /analyze` + `GET /report/{id}` + `GET /report/{id}/pdf`、Hermes CLI wrapper | `pytest backend/tests/ -v` 全通过 |
| **M4** | 前端页面 | `IdeaInput` + `ResultsList` + `IdeaCard` + `ReportDownload`，mock API 模式可用 | 手动：输入 3 想法 → 60s 内看到排名 |
| **M5** | Docker Compose 集成 | 精简 docker-compose.yml，后端 + 前端 + postgres 健康检查 | `docker-compose up` → `curl localhost` 返回界面 |
| **M6** | 验收闸门 + 文档 | `STATUS.md`、`CHANGELOG.md`、`ERRORS.md`、完整验收通过 | `bash check.sh` 退出码 0 |

## 8. 风险和取舍

| 风险 | 影响 | 当前取舍 | 何时重看 |
|---|---|---|---|
| Google Trends 非官方接口不稳定 | 数据缺失，评分不准 | 超时 fallback + "数据暂缺"标注 | M2 完成后 |
| Reddit API rate limit | 多想法并发时被限 | 指数退避 + 顺序执行（非并发） | 用户反馈部分数据常缺失时 |
| Hermes CLI 在 Docker 中不可用 | 无推荐建议 | Docker 内 `pip install hermes-cli` 或 `subprocess` 调用宿主机 | M3 测试 Docker 构建时 |
| WeasyPrint Docker 兼容 | PDF 不能生成 | 备选方案：pdfkit (wkhtmltopdf) 或 fpdf2 | M3 验证时 |
| Polsia 前端脚手架干扰 | 路由冲突，包冲突 | 保留不动，新页面在独立路由 `/` | v0 完成准备 v1 时 |

## 9. 给前端 AI 的技术边界

前端 AI 必须遵守：

- **可用框架**：Next.js 14 (App Router), Tailwind CSS 3, TypeScript 5
- **可用 UI 库**：Radix UI, lucide-react, recharts, tailwind-merge, clsx, class-variance-authority, zustand
- **是否允许新增依赖**：否（除非用户明确批准）
- **数据来源**：先在 mock API 模式下开发；真实 API 在 Docker Compose 完整集成后切换
- **禁止事项**：
  - 不新增 npm 包
  - 不修改 `page.tsx` 以外的路由文件（layout.tsx 可以改标题/meta）
  - 不删除任何 Polsia 遗留页面
  - 不改变现有的 tailwind.config.ts 主题变量

## 10. 确认记录

- 用户已确认项目框架：`是`（基于 PRD.md 中已确认的技术选型 + 已存在的项目脚手架）
- 确认时间：2026-06-27
- 备注：核心差异 — **MVP 无需 Celery/Redis**，用 FastAPI BackgroundTasks 简化架构
