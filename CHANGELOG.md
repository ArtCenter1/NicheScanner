# CHANGELOG.md — Version History

Default only read when checking history, recording a release, or running acceptance.
Latest version goes at the top.

| Version | Date | Type | Change Summary | Milestone |
|---|---|---|---|---|
| `0.1.0-dev` | 2026-06-27 | feat | MVP backend scaffold — FastAPI app, scorer, scraper, API endpoints, all tests passing | MVP v0.1 |

## Version Rules

- `0.x.x` — development / pre-release versions.
- `x.y.z` — semantic versioning: feature bump on `y`, patch bump on `z`, breaking change bumps `x`.
- Each completed milestone that produces a runnable / testable version gets a row here.

## Milestone Notes

### 0.1.0-dev

- Backend structure: `app/api/v1/analyze.py`, `app/api/v1/report.py`, `app/services/`
- Scoring: 4-dimension rule-based engine with 8 passing unit tests
- API: `POST /api/v1/analyze` → `GET /api/v1/report/{id}` → `GET /api/v1/report/{id}/pdf`
- Tests: 15/15 passing, ruff clean
- `docker-compose.yml` stripped of redis/celery/chroma/nginx — lean 3-service stack