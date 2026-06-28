from __future__ import annotations

from typing import Annotated

from app.core.database import get_session
from app.models.analysis import Analysis
from app.services.analyzer import run_analysis
from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["analyze"])


class AnalyzeRequest(BaseModel):
    ideas: list[str] = Field(..., min_length=1, max_length=5)


class AnalyzeResponse(BaseModel):
    analysis_id: str
    status: str


@router.post("/analyze", status_code=202, response_model=AnalyzeResponse)
async def create_analysis(
    body: AnalyzeRequest,
    background_tasks: BackgroundTasks,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Submit 1–5 business ideas for niche analysis.

    Returns immediately with an ``analysis_id``.
    The frontend polls ``GET /report/{analysis_id}`` for completion.
    """
    from uuid import uuid4

    analysis_id = str(uuid4())

    analysis = Analysis(id=analysis_id, status="pending", ideas_raw=body.ideas)
    session.add(analysis)
    await session.commit()

    background_tasks.add_task(run_analysis, analysis_id, body.ideas)

    return AnalyzeResponse(analysis_id=analysis_id, status="pending")
