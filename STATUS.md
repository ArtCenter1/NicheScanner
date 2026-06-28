# STATUS.md — Current Project State

Default only read when resuming, recording progress, or running acceptance.
This records "where we are now" — not full history.

## Current Version

| Field | Value |
|---|---|
| Version | `0.1.0-dev` |
| Milestone | MVP — Niche Scanner Core |
| Current Step | `6_项目记录` → `7_验收闸门` (M4/M5 pending) |

## Progress

### Completed

- [x] `AGENTS.md` — Linear workflow entry point (replaces CLAUDE.md)
- [x] `PRD.md` — Full product spec (定位 / 用户 / P0 / 验收标准)
- [x] `PROJECT_FRAME.md` — Tech stack, dir structure, 6 slices (M0–M5)
- [x] `FLOWS.md` — Interaction logic (5 interactions + 4-state matrix)
- [x] `FRONTEND_HANDOFF.md` — Self-contained spec for frontend AI
- [x] `GATES.md` + `check.sh` — Acceptance gates (6 automated + manual checklist)
- [x] **M0** — Backend scaffold: FastAPI app, directory structure, conftest fixtures
- [x] **M1** — Rule-based scoring engine (4 dimensions, fully tested)
- [x] **M2** — Async scraper layer (Reddit / Trends / Product Hunt, sandbox-mocked)
- [x] **M3** — Full API: `POST /analyze`, `GET /report/{id}`, `GET /report/{id}/pdf`
  - Hermes CLI wrapper (mocked in tests)
  - WeasyPrint PDF generation
- [x] `docker-compose.yml` — Simplified: postgres + backend + frontend only
- [x] All tests pass (15/15), ruff clean, B008 fixed

### In Progress

- [ ] **M4** — Frontend components: `IdeaInput`, `ResultsList`, `IdeaCard`, `ReportDownload`

### Next

- **M4**: Implement frontend in `frontend/src/app/page.tsx` (mock API mode first)
- **M5**: Verify Docker Compose full-stack run, confirm PDF generation in container
- **M7**: Final acceptance — `bash check.sh` must exit 0

## Current Blocker

- None.

## Key Decisions Made

| Date | Decision | Impact |
|---|---|---|
| 2026-06-27 | MVP no Celery/Redis — use FastAPI BackgroundTasks | Simplified architecture, faster to ship |
| 2026-06-27 | DI via `get_session()` FastAPI dependency | Enables clean test DB patching |
| 2026-06-27 | Scoring weights fixed (not user-adjustable) | Simplifies MVP UI and explains to users |

## Resume Prompt

Start a new session by reading `AGENTS.md` first, then:
- If working on M4/M5 → read `FRONTEND_HANDOFF.md`
- If running acceptance → `bash check.sh`
- If resuming after failure → check `ERRORS.md`