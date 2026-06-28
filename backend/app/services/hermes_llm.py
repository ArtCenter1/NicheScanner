"""Hermes CLI wrapper for LLM-generated recommendation text.

The scoring itself is rule-based (see ``scorer.py``). The LLM is only
used to generate the human-readable "first action recommendation" text
for each idea.

In test/sandbox mode (``HERMES_MOCK=true``) a canned response is returned
instead of invoking the Hermes CLI subprocess.
"""

from __future__ import annotations

import json
import logging
import subprocess

from app.core.config import settings

logger = logging.getLogger(__name__)

_MOCK_RECOMMENDATION = (
    "This niche shows strong demand signals with manageable competition. "
    "Consider validating with a landing page and targeted ads before building "
    "a full product. Focus on a specific sub-niche to differentiate early."
)


def generate_recommendation(idea_name: str, scores: dict) -> str:
    """Call Hermes CLI to generate an action recommendation.

    Args:
        idea_name: The business idea name.
        scores: Dict with ``total_score`` and dimension scores.

    Returns:
        A human-readable recommendation string.
    """
    if settings.hermes_mock:
        return _MOCK_RECOMMENDATION

    prompt = (
        f"You are a startup advisor. Given the business idea '{idea_name}' "
        f"with a niche score of {scores.get('total_score', 50)}/100 "
        f"(supply_quality={scores.get('supply_quality', 50)}, "
        f"demand_heat={scores.get('demand_heat', 50)}, "
        f"business_viability={scores.get('business_viability', 50)}, "
        f"timing={scores.get('timing', 50)}), "
        f"suggest ONE concrete first action the founder should take "
        f"(under 3 sentences). Be specific — name a channel, tool, or approach."
    )

    try:
        result = subprocess.run(
            [settings.hermes_cli, "chat", "-q", prompt, "--json"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        output = json.loads(result.stdout)
        return output.get("content", _MOCK_RECOMMENDATION)
    except Exception as exc:
        logger.warning("Hermes CLI call failed for '%s': %s", idea_name, exc)
        return _MOCK_RECOMMENDATION
