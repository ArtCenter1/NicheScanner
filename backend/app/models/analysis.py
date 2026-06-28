"""Analysis ORM model — single table for the MVP."""

from __future__ import annotations

from datetime import datetime

from app.core.database import Base
from sqlalchemy import JSON, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    status: Mapped[str] = mapped_column(
        String(20), default="pending", index=True
    )  # pending | scraping | scoring | enriching | complete | partial | failed
    ideas_raw: Mapped[list] = mapped_column(JSON, default=list)
    results: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error_info: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
