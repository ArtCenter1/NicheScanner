"""GET /api/v1/report/{id} — poll analysis results and download PDF."""

from __future__ import annotations

from typing import Annotated

from app.core.config import settings
from app.core.database import get_session
from app.models.analysis import Analysis
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["report"])


@router.get("/report/{analysis_id}")
async def get_report(
    analysis_id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Return the current status and (if complete) the analysis results."""
    result = await session.execute(
        select(Analysis).where(Analysis.id == analysis_id)
    )
    analysis = result.scalar_one_or_none()

    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")

    if analysis.status in ("pending", "scraping", "scoring", "enriching"):
        return {
            "status": analysis.status,
            "progress": f"Analysis in progress: {analysis.status}",
        }

    if analysis.status == "failed":
        return {"status": "failed", "error": analysis.error_info, "ideas": []}

    # complete or partial
    return {
        "status": analysis.status,
        "ideas": analysis.results,
    }


@router.get("/report/{analysis_id}/pdf")
async def download_pdf(analysis_id: str):
    """Download the analysis report as a PDF."""
    pdf_path = settings.reports_dir / f"{analysis_id}.pdf"

    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="PDF not yet generated")

    return FileResponse(
        str(pdf_path),
        media_type="application/pdf",
        filename=f"niche-scanner-report-{analysis_id[:8]}.pdf",
    )
