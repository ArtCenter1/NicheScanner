"""PDF report generation via WeasyPrint.

Converts analysis results into a clean single-page PDF report.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from app.core.config import settings


def generate_pdf(analysis_id: str, results: list[dict]) -> Path | None:
    """Generate a PDF report for completed analysis.

    Args:
        analysis_id: UUID of the analysis.
        results: List of scored idea dicts from the analysis.

    Returns:
        Path to the generated PDF, or None if generation failed or WeasyPrint unavailable.
    """
    try:
        from weasyprint import HTML

        ideas_html = ""
        for i, idea in enumerate(results, 1):
            dims = idea.get("dimensions", {})
            ideas_html += f"""
            <div class="idea-card">
                <div class="rank">#{i}</div>
                <h2>{idea.get('name', 'Unknown')}</h2>
                <div class="total-score">{idea.get('total_score', 0)}</div>
                <div class="dimensions">
                    <div>Supply Quality: {dims.get('supply_quality', 'N/A')}</div>
                    <div>Demand Heat: {dims.get('demand_heat', 'N/A')}</div>
                    <div>Business Viability: {dims.get('business_viability', 'N/A')}</div>
                    <div>Timing: {dims.get('timing', 'N/A')}</div>
                </div>
                <p class="recommendation">{idea.get('recommendation', '')}</p>
            </div>
            """

        html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8">
<style>
  body {{ font-family: -apple-system, sans-serif; max-width: 800px; margin: 0 auto; padding: 40px 20px; color: #1a1a2e; }}
  h1 {{ font-size: 24px; margin-bottom: 4px; }}
  .date {{ color: #64748b; font-size: 14px; margin-bottom: 24px; }}
  .idea-card {{ border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; margin-bottom: 16px; }}
  .rank {{ font-size: 12px; color: #64748b; font-weight: 600; }}
  h2 {{ font-size: 18px; margin: 4px 0; }}
  .total-score {{ font-size: 32px; font-weight: 700; color: #1e3a5f; }}
  .dimensions {{ display: flex; gap: 16px; margin: 12px 0; font-size: 13px; color: #475569; }}
  .recommendation {{ background: #f8fafc; padding: 12px; border-radius: 8px; font-size: 14px; line-height: 1.5; color: #334155; }}
</style></head>
<body>
  <h1>Niche Scanner Report</h1>
  <div class="date">{datetime.now().strftime('%Y-%m-%d')}</div>
  {ideas_html}
</body></html>"""

        pdf_path = settings.reports_dir / f"{analysis_id}.pdf"
        HTML(string=html).write_pdf(str(pdf_path))
        return pdf_path

    except Exception as exc:
        import logging
        logging.getLogger(__name__).warning(
            "PDF generation failed for %s: %s", analysis_id, exc
        )
        return None
