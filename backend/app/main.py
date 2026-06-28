"""Niche Scanner — FastAPI application entry point."""

from contextlib import asynccontextmanager

from app.api.v1 import analyze, report
from app.core.database import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create DB tables on startup (dev-mode simplicity)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Niche Scanner API",
    version="0.1.0",
    description="AI-powered niche market discovery tool. "
    "Input 1–5 business ideas, get scored rankings with data-backed recommendations.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3333", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router, prefix="/api/v1")
app.include_router(report.router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/")
async def root():
    return {
        "message": "Niche Scanner API",
        "docs": "/docs",
        "version": "0.1.0",
    }
