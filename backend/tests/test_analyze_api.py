"""Integration-style tests for the analyze and report API endpoints.

Uses SQLite in-memory DB and mock/sandbox mode — no real external calls.
"""

import pytest


@pytest.mark.asyncio
async def test_health_endpoint(api_client):
    """GET /health should return ok."""
    resp = await api_client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_root_endpoint(api_client):
    """GET / should return API metadata."""
    resp = await api_client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert "Niche Scanner API" in data["message"]
    assert data["version"] == "0.1.0"


@pytest.mark.asyncio
async def test_analyze_accepts_valid_request(api_client):
    """POST /api/v1/analyze with 1–5 ideas should return 202 + analysis_id."""
    resp = await api_client.post(
        "/api/v1/analyze",
        json={"ideas": ["AI for lawyers", "SaaS for plumbers"]},
    )
    assert resp.status_code == 202
    data = resp.json()
    assert data["status"] == "pending"
    assert len(data["analysis_id"]) > 0


@pytest.mark.asyncio
async def test_analyze_rejects_zero_ideas(api_client):
    """POST /api/v1/analyze with empty ideas should return 422."""
    resp = await api_client.post("/api/v1/analyze", json={"ideas": []})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_analyze_rejects_six_ideas(api_client):
    """POST /api/v1/analyze with 6 ideas should return 422."""
    resp = await api_client.post(
        "/api/v1/analyze",
        json={"ideas": [f"idea {i}" for i in range(6)]},
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_report_nonexistent_returns_404(api_client):
    """GET /api/v1/report/<bad-id> should return 404."""
    resp = await api_client.get("/api/v1/report/does-not-exist")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_report_pdf_nonexistent_returns_404(api_client):
    """GET /api/v1/report/<bad-id>/pdf should return 404."""
    resp = await api_client.get("/api/v1/report/does-not-exist/pdf")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_full_analyze_flow(api_client):
    """End-to-end: submit ideas → poll until complete → verify results."""
    resp = await api_client.post(
        "/api/v1/analyze",
        json={"ideas": ["AI for lawyers", "SaaS for plumbers"]},
    )
    assert resp.status_code == 202
    analysis_id = resp.json()["analysis_id"]

    # Poll until complete or timeout
    import asyncio

    for _ in range(30):
        await asyncio.sleep(0.5)
        resp = await api_client.get(f"/api/v1/report/{analysis_id}")
        data = resp.json()
        if data["status"] in ("complete", "partial", "failed"):
            break

    assert data["status"] in ("complete", "partial")

    # Verify result shape
    if data.get("ideas"):
        first = data["ideas"][0]
        assert "name" in first
        assert "total_score" in first
        assert "dimensions" in first
        assert "recommendation" in first
        assert len(first["recommendation"]) > 0
