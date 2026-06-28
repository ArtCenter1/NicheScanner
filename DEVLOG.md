# Niche Scanner — Development Log

> Timestamped log of decisions, progress, and blockers.

---

## 2026-06-27 — Project Bootstrap & Repo Cleanup

**Status:** 🚧 Scaffolding

### Done
- Forked from `ArtCenter1/NicheScanner` (origin `PolsiaAI/Polsia`)
- Removed `.gitmodules` file from Polsia fork
- Rewrote `CLAUDE.md` for Niche Scanner identity → so AI agents stop confusing this with Polsia
- Rewrote `README.md` — Niche Scanner branding, not Polsia
- Updated frontend branding: layout title, sidebar heading, npm package names
- Updated infrastructure defaults: docker-compose DB names, alembic URL, Celery app name
- Updated test references: activity channel key, Polsia agent references
- Cleaned up `ARCHITECTURE.md` — removed Polsia refs
- Created `DEVLOG.md` — this file
- Updated MyWiki `entities/niche-scanner.md` — fixed repo path, marked active development

### Decisions
- **Niche Scanner != Polsia.** The 9-agent crew pattern, Claude Code CLI, ChromaDB, and
  Redis pub/sub are NOT part of this project. Hermes CLI replaces Claude Code for LLM tasks.
- **All Polsia branding removed from public-facing files.** The infra skeleton (Docker, nginx,
  CI patterns) stays but is now Niche Scanner branded.
- **Remaining Polsia test files** (`tests/unit/test_base_agent.py`) reference
  `BasePolsiaAgent` which doesn't exist in this repo — they'll be replaced when we
  build our own backend.

### Next Up
- Build the actual Niche Scanner backend (FastAPI, scrapers, scoring engine)
- See `ARCHITECTURE.md` for the full implementation plan
