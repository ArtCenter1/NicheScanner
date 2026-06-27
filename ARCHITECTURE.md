# Niche Scanner MVP — Implementation Plan

**Goal:** Build an AI-powered niche market discovery tool that takes 1-5 business ideas as input and outputs scored, ranked analysis with data-backed recommendations in under 60 seconds.

**Architecture:** One-page web app — Next.js frontend + FastAPI backend. Data scraped asynchronously from Reddit, Google Trends, and Product Hunt. Scoring computed locally. AI enrichment via Hermes CLI subprocess (not Claude Code CLI). Single-payment model ($79 per report).

**Tech Stack:** Python 3.13 · FastAPI · Next.js 14 · SQLite (dev) / PostgreSQL (prod) · httpx + asyncio · Hermes CLI subprocess · WeasyPrint (PDF)

---

## Context

We are the first users. We already manually do this research in our wiki. The tool automates that workflow.

**MVP = 2-week sprint for one developer.**
We own the full stack. No teammates to coordinate. No CI pipeline yet.

---

## Phase 1: Project Bootstrap

### Task 1 — Setup project directory structure

```
D:/My_Projects/Niche Scanner/
├── backend/
│   ├── app/
│   │   ├── api/v1/           ← FastAPI routes
│   │   │   ├── analyze.py    ← POST /analyze
│   │   │   └── report.py     ← GET /report/{id}
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── analysis.py
│   │   │   └── idea.py
│   │   ├── services/
│   │   │   ├── scraper.py    ← asyncio httpx scrapers
│   │   │   ├── scorer.py     ← scoring logic
│   │   │   ├── hermes_llm.py ← Hermes CLI wrapper
│   │   │   └── report.py     ← PDF generation
│   │   └── main.py
│   ├── tests/
│   │   ├── unit/
│   │   │   ├── test_scorer.py
│   │   │   └── test_scraper.py
│   │   └── conftest.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx      ← Main analysis page
│   │   │   └── layout.tsx
│   │   ├── components/
│   │   │   ├── IdeaInput.tsx
│   │   │   ├── ResultsList.tsx
│   │   │   ├── IdeaCard.tsx
│   │   │   └── ReportDownload.tsx
│   │   └── lib/
│   │       └── api.ts
│   └── package.json
├── docker-compose.yml        ← Forked from Polsia (adapted)
├── Makefile                   ← Forked from Polsia (adapted)
└── .env.example
```

### Task 2 — Write a stub FastAPI app

Create `backend/app/main.py` with:
- `GET /health` → `{"status": "ok"}`
- `GET /` → `{"message": "Niche Scanner API"}`

Verify: `cd backend && uvicorn app.main:app --reload`

### Task 3 — Setup test infrastructure

Pattern from Polsia fork (`conftest.py`). Use `HERMES_MOCK=true` in tests (not `CLAUDE_CLI_MOCK`). SQLite in-memory for unit tests.

---

## Phase 2: Core Logic

### Task 4 — Write the scoring algorithm

**Files:** `backend/app/services/scorer.py`

**Scoring inputs per idea:**

| Signal | Source | Weight |
|--------|--------|--------|
| Discussion volume | Reddit search count | 30% |
| Trend direction | Google Trends (12mo slope) | 25% |
| Supply gap | Number of low-rated competitors | 25% |
| Business viability | Pricing data from G2/Product Hunt | 20% |

**Output:** `NicheScore(0-100)` with breakdown per signal.

Write tests first: `tests/unit/test_scorer.py`

### Task 5 — Write the scraper layer

**Files:** `backend/app/services/scraper.py`

Async scrapers for MVP:
- `scrape_reddit(keyword)` → `{count, sentiment, top_posts}`
- `scrape_trends(keyword)` → `{volume, slope}`
- `scrape_producthunt(keyword)` → `{count, avg_upvotes}`

Use `httpx.AsyncClient` with rate limiting. All scrapers return structured JSON. If a source fails, log and continue — partial data is OK.

Mock these in tests with `httpx_mock`.

### Task 6 — Wrap Hermes CLI as LLM caller

**Files:** `backend/app/services/hermes_llm.py`

```python
def call_hermes(prompt: str) -> str:
    result = subprocess.run(
        ["hermes", "chat", "-q", prompt, "--json"],
        capture_output=True, text=True, timeout=60
    )
    return json.loads(result.stdout)["content"]
```

Used for: generating the "first action recommendation" text per idea. The scoring itself is rule-based, not LLM.

Mock with `HERMES_MOCK=true` → returns sample recommendation text.

### Task 7 — Wire up the `/analyze` endpoint

**Files:** `backend/app/api/v1/analyze.py`

```
POST /analyze
Body: {"ideas": ["AI tool for lawyers", "..."]}
→ Task created in DB, returns {"analysis_id": "xxx"}
→ Scraper fires async
→ Scorer computes scores
→ Hermes adds recommendations
→ PDF generated
→ Stored in DB
```

Return immediately with `analysis_id`. Frontend polls `/report/{id}` every 3s.

### Task 8 — Write PDF report generator

**Files:** `backend/app/services/report.py`

Use `WeasyPrint` — convert HTML template to PDF. Template is a clean, single-page report with:
- Header: "Niche Scanner Report — [date]"
- Ranked list of ideas (1-5) with scores and breakdowns
- Action recommendations per idea

Store PDF on disk (`backend/reports/{analysis_id}.pdf`), serve via `/report/{id}`.

---

## Phase 3: Frontend

### Task 9 — Build the analysis page

**Files:** `frontend/src/app/page.tsx`

Layout:
1. Hero: "What should you build?" + 1-sentence description
2. Input: textarea for 1-5 ideas (comma or newline separated)
3. "Analyze" button → POST /analyze → poll /report/{id}
4. Results: ranked cards with scores
5. "Download Report" button

### Task 10 — Build results components

- `IdeaCard.tsx` — score badge (color-coded), breakdown bars, recommendation
- `ResultsList.tsx` — sortable by score (default) or any signal
- `ReportDownload.tsx` — triggers PDF download

### Task 11 — API client

Adapt from Polsia fork (`frontend/src/lib/api.ts`). Add `POST /analyze` and `GET /report/{id}` endpoints.

---

## Phase 4: DevOps

### Task 12 — Docker Compose

Modify `docker-compose.yml` (from Polsia fork):
- Remove: ChromaDB, celery, nginx
- Keep: PostgreSQL, backend, frontend
- Add health checks for backend + frontend

### Task 13 — Makefile

```
make up         # docker-compose up -d
make down       # docker-compose down
make backend    # cd backend && uvicorn app.main:app --reload
make test       # pytest backend/tests/ -v
make lint       # ruff check . && mypy app/
```

---

## Verification

After each task:
- Run `make test` — all green before next task
- Manual smoke test of `/analyze` endpoint with 3 ideas
- Open `http://localhost` — verify frontend loads and displays results

After Phase 4:
- Full end-to-end test: enter 5 ideas → wait 60s → download PDF
- PDF opens correctly in browser

---

## Risks & Open Questions

| Risk | Mitigation |
|------|-----------|
| Reddit API rate limits | Use `mcporter reddit.search` or implement exponential backoff |
| Hermes CLI not available in Docker | Mount local `hermes` binary into container, or use HTTP API |
| Scoring algorithm too simplistic | Start simple (rule-based), add LLM enrichment in v2 |
| PDF generation fails in Docker | Test WeasyPrint in Docker before Phase 4 |

### Open question for you

> Should the scoring algorithm weights (30/25/25/20) be exposed to users as adjustable settings, or fixed for MVP?

Fixing them makes the product simpler to explain. Exposing them makes the product smarter but adds UI complexity. My recommendation: fix for MVP, expose in v2.