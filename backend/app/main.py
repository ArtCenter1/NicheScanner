"""Niche Scanner — FastAPI application entry point."""

from app.api.v1 import analyze, report
from fastapi import FastAPI

app = FastAPI(
    title="Niche Scanner API",
    version="0.1.0",
    description="AI-powered niche market discovery tool. "
    "Input 1–5 business ideas, get scored rankings with data-backed recommendations.",
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
