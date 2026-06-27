# ERRORS.md — Known Issues and Resolutions

Do NOT read this file by default. Search by keyword, error message, or tag when debugging.

## Tags

- `#session-patching` — test infrastructure / DI
- `#ruff` — linting / formatting
- `#fastapi` — FastAPI-specific patterns
- `#sqlalchemy` — ORM / async session

## Error Log

### 2026-06-27 — B008: `Depends` in argument default values

**Tags:** `#ruff` `#fastapi`

- **Trigger:** `ruff check app/` flagged `session: AsyncSession = Depends(get_session)` as B008
- **Root cause:** Ruff B008 flags all `=` defaults that call `Depends()` — but this is the standard FastAPI pattern
- **Fix:** Changed to `Annotated[AsyncSession, Depends(get_session)]` — equivalent semantics, ruff-compliant
- **Files:** `app/api/v1/analyze.py`, `app/api/v1/report.py`
- **Verified:** ruff clean after fix ✅

### 2026-06-27 — `no such table: analyses` in API tests

**Tags:** `#sqlalchemy` `#session-patching`

- **Trigger:** All API tests failed with `sqlite3.OperationalError: no such table: analyses`
- **Root cause:** The `api_client` fixture used a separate in-memory DB, while the FastAPI endpoints used the globally imported `async_session_factory` pointing to the file-based SQLite (`niche_scanner.db`). Even the patched `async_session_factory` was a new reference; the endpoints held module-level references created at import time.
- **Fix:** Two-layer patch:
  1. Patched `db_mod.async_session_factory` so analyzer background tasks (which import `from app.core import database`) see the test DB
  2. Pre-imported `app.services.analyzer` at module level in `conftest.py` so the module's cached reference is also patched
  3. Dropped FastAPI `dependency_overrides` (unnecessary when factory patching works)
- **Files:** `backend/tests/conftest.py`, `backend/app/services/analyzer.py`
- **Verified:** All 15 tests pass ✅

### 2026-06-27 — UnboundLocalError: `app` name shadowed in conftest fixture

**Tags:** `#session-patching`

- **Trigger:** `from app.services import analyzer` inside `db_engine` fixture body created a local variable `app`, shadowing the FastAPI `app` from the import above
- **Fix:** Moved `import app.services.analyzer` to module level with a `# noqa: F811` marker
- **Files:** `backend/tests/conftest.py`
- **Verified:** All 15 tests pass ✅

### 2026-06-27 — Module name collision: `app` vs `app.main.app`

**Tags:** `#session-patching` `#fastapi`

- **Trigger:** `from app.main import app` combined with `import app.services.analyzer` caused Python to create local `app` references in the `db_engine` fixture that shadowed the FastAPI app
- **Fix:** Renamed import alias: `from app.main import app as fastapi_app`
- **Files:** `backend/tests/conftest.py`
- **Verified:** All 15 tests pass ✅