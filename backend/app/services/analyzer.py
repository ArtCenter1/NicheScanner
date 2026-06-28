"""Orchestrator — ties scrapers, scorer, Hermes LLM, and PDF generation together.

Runs as a FastAPI BackgroundTask: scrape → score → enrich → persist.
"""

from __future__ import annotations

import logging
from datetime import UTC

from app.core import database
from app.models.analysis import Analysis
from app.services import scorer
from app.services.hermes_llm import generate_recommendation
from app.services.report_pdf import generate_pdf
from app.services.scraper import scrape_all
from sqlalchemy import select

logger = logging.getLogger(__name__)


async def run_analysis(analysis_id: str, ideas: list[str]) -> None:
    """Execute the full analysis pipeline for a set of ideas.

    Steps:
        1. Update status to ``scraping`` and scrape all data sources.
        2. Update status to ``scoring`` and compute rule-based scores.
        3. Update status to ``enriching`` and call Hermes CLI.
        4. Update status to ``complete`` or ``partial`` and persist results.
    """
    async with database.async_session_factory() as session:
        result = await session.execute(
            select(Analysis).where(Analysis.id == analysis_id)
        )
        analysis = result.scalar_one_or_none()
        if analysis is None:
            logger.error("Analysis %s not found — aborting pipeline", analysis_id)
            return

        try:
            # --- Step 1: Scrape ---
            analysis.status = "scraping"
            await session.commit()

            scraped_results = {}
            all_failed = True
            for idea in ideas:
                signals = await scrape_all(idea)
                scraped_results[idea] = signals
                if any(v is not None for v in signals.values()):
                    all_failed = False

            if all_failed:
                analysis.status = "failed"
                analysis.error_info = {"error": "All data sources failed for all ideas"}
                await session.commit()
                return

            # --- Step 2: Score ---
            analysis.status = "scoring"
            await session.commit()

            scored_ideas = []
            for idea in ideas:
                signals = scraped_results[idea]
                s = scorer.compute_score(
                    name=idea,
                    reddit_data=signals.get("reddit"),
                    trends_data=signals.get("trends"),
                    producthunt_data=signals.get("producthunt"),
                )
                scored_ideas.append(s)

            # --- Step 3: Enrich (Hermes) ---
            analysis.status = "enriching"
            await session.commit()

            for s in scored_ideas:
                scores_dict = {
                    "total_score": s.total_score,
                    "supply_quality": s.supply_quality,
                    "demand_heat": s.demand_heat,
                    "business_viability": s.business_viability,
                    "timing": s.timing,
                }
                s.recommendation = generate_recommendation(s.name, scores_dict)

            # --- Step 4: Persist ---
            results_list = []
            for s in scored_ideas:
                results_list.append(
                    {
                        "name": s.name,
                        "total_score": s.total_score,
                        "dimensions": {
                            "supply_quality": s.supply_quality,
                            "demand_heat": s.demand_heat,
                            "business_viability": s.business_viability,
                            "timing": s.timing,
                        },
                        "recommendation": s.recommendation,
                        "signals": s.signals,
                    }
                )

            # Sort by score descending
            results_list.sort(key=lambda x: x["total_score"], reverse=True)

            from datetime import datetime

            analysis.status = "complete" if not all_failed else "partial"
            analysis.results = results_list
            analysis.completed_at = datetime.utcnow()
            await session.commit()

            # --- Step 5: Generate PDF (fire-and-forget style) ---
            try:
                generate_pdf(analysis_id, results_list)
            except Exception as exc:
                logger.warning("PDF generation failed for %s: %s", analysis_id, exc)

        except Exception as exc:
            logger.exception("Analysis pipeline failed for %s", analysis_id)
            analysis.status = "failed"
            analysis.error_info = {"error": str(exc)}
            await session.commit()
