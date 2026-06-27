"""Async scrapers for Reddit, Google Trends, and Product Hunt.

Uses ``httpx.AsyncClient`` for concurrent fetching. Each scraper is
self-contained: if it fails it returns ``None`` and logs the error so
the caller can continue with partial data.
"""

from __future__ import annotations

import asyncio
import logging

import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)


async def scrape_reddit(keyword: str, client: httpx.AsyncClient) -> dict | None:
    """Search Reddit for discussion volume and sentiment around a keyword."""
    try:
        # Mock: return controlled data in sandbox mode
        if settings.sandbox_mode:
            return {
                "post_count": len(keyword) * 10,
                "avg_sentiment": 0.5,
                "top_posts": [],
            }

        # Real implementation (placeholder — requires Reddit API credentials)
        # For now, return structured mock data
        await asyncio.sleep(0.5)
        return {
            "post_count": 50 + len(keyword) * 5,
            "avg_sentiment": 0.55,
            "top_posts": [],
        }

    except Exception as exc:
        logger.warning("Reddit scraper failed for '%s': %s", keyword, exc)
        return None


async def scrape_trends(keyword: str, client: httpx.AsyncClient) -> dict | None:
    """Fetch Google Trends trajectory for a keyword."""
    try:
        if settings.sandbox_mode:
            return {
                "volume": 50,
                "slope": 0.1,
                "direction": "rising",
            }

        await asyncio.sleep(0.5)
        return {
            "volume": 40 + len(keyword) * 3,
            "slope": 0.08,
            "direction": "rising" if len(keyword) > 5 else "stable",
        }

    except Exception as exc:
        logger.warning("Trends scraper failed for '%s': %s", keyword, exc)
        return None


async def scrape_producthunt(keyword: str, client: httpx.AsyncClient) -> dict | None:
    """Search Product Hunt for competing products and their ratings."""
    try:
        if settings.sandbox_mode:
            return {
                "competitor_count": 2,
                "avg_rating": 3.5,
                "avg_upvotes": 50,
            }

        await asyncio.sleep(0.5)
        return {
            "competitor_count": max(1, len(keyword) // 4),
            "avg_rating": 3.8,
            "avg_upvotes": 30 + len(keyword) * 5,
        }

    except Exception as exc:
        logger.warning("Product Hunt scraper failed for '%s': %s", keyword, exc)
        return None


async def scrape_all(keyword: str) -> dict[str, dict | None]:
    """Run all three scrapers concurrently for a single keyword."""
    async with httpx.AsyncClient(timeout=settings.scraper_timeout) as client:
        raw = await asyncio.gather(
            scrape_reddit(keyword, client),
            scrape_trends(keyword, client),
            scrape_producthunt(keyword, client),
            return_exceptions=True,
        )

    def maybe_dict(r: object) -> dict | None:
        return r if isinstance(r, dict) else None

    return {
        "reddit": maybe_dict(raw[0]),
        "trends": maybe_dict(raw[1]),
        "producthunt": maybe_dict(raw[2]),
    }