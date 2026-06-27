"""Rule-based niche scoring engine.

Computes a Niche Score (0–100) from scraped signals across four dimensions:

- Supply Quality   (35%) — How bad are existing solutions?
- Demand Heat      (30%) — How strong is the search / discussion volume?
- Business Viability (20%) — Can you charge for it?
- Timing           (15%) — Is now the right time?

The scoring is *rule-based* and deterministic — no LLM calls here.
Partial data is handled gracefully: missing signals are scored 0 and
flagged for the frontend to display as "data unavailable".
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ScoredIdea:
    name: str
    total_score: float
    supply_quality: float
    demand_heat: float
    business_viability: float
    timing: float
    recommendation: str = ""
    signals: dict = field(default_factory=dict)


def score_supply_quality(reddit_data: dict | None, producthunt_data: dict | None) -> float:
    """Score supply quality (0–100). Higher = existing solutions are bad → opportunity."""
    score = 50.0  # neutral baseline

    if reddit_data:
        sentiment = reddit_data.get("avg_sentiment", 0.5)
        # Negative sentiment toward existing tools → good (high score)
        score += (0.5 - sentiment) * 40  # -20 to +20

    if producthunt_data:
        avg_rating = producthunt_data.get("avg_rating", 3.0)
        # Low ratings → existing solutions are bad → opportunity
        score += (3.0 - avg_rating) * 10  # -10 to +20

    return max(0.0, min(100.0, score))


def score_demand_heat(reddit_data: dict | None, trends_data: dict | None) -> float:
    """Score demand heat (0–100). Higher = more people are looking for this."""
    score = 30.0  # conservative baseline

    if reddit_data:
        post_count = reddit_data.get("post_count", 0)
        # Scale: 0 posts = 0, 200+ posts = max contribution
        score += min(post_count / 2, 40)

    if trends_data:
        slope = trends_data.get("slope", 0.0)
        # Rising trend = bonus
        score += max(0, slope) * 50  # 0 to +15
        if trends_data.get("direction") == "rising":
            score += 10

    return max(0.0, min(100.0, score))


def score_business_viability(producthunt_data: dict | None, trends_data: dict | None) -> float:
    """Score business viability (0–100). Higher = easier to monetise."""
    score = 40.0

    if producthunt_data:
        competitors = producthunt_data.get("competitor_count", 0)
        # Few competitors but existing ones have high ratings = viable market
        # Many competitors with low ratings = crowded but opportunity
        if competitors <= 3:
            score += 20
        elif competitors <= 10:
            score += 10
        else:
            score -= 10

        upvotes = producthunt_data.get("avg_upvotes", 0)
        score += min(upvotes / 10, 15)

    if trends_data:
        volume = trends_data.get("volume", 0)
        score += min(volume / 50, 15)

    return max(0.0, min(100.0, score))


def score_timing(producthunt_data: dict | None, trends_data: dict | None) -> float:
    """Score timing (0–100). Higher = now is the right time to enter."""
    score = 40.0

    if trends_data:
        slope = trends_data.get("slope", 0.0)
        score += max(0, slope) * 60  # 0 to +25
        if trends_data.get("direction") == "rising":
            score += 15

    if producthunt_data:
        new_entrants = producthunt_data.get("competitor_count", 0)
        # Some new entrants = validated category; too many = late
        if 1 <= new_entrants <= 5:
            score += 15
        elif new_entrants > 10:
            score -= 10

    return max(0.0, min(100.0, score))


def compute_score(
    name: str,
    reddit_data: dict | None = None,
    trends_data: dict | None = None,
    producthunt_data: dict | None = None,
) -> ScoredIdea:
    """Compute the full Niche Score for one idea."""
    supply = score_supply_quality(reddit_data, producthunt_data)
    demand = score_demand_heat(reddit_data, trends_data)
    viability = score_business_viability(producthunt_data, trends_data)
    timing = score_timing(producthunt_data, trends_data)

    total = supply * 0.35 + demand * 0.30 + viability * 0.20 + timing * 0.15

    return ScoredIdea(
        name=name,
        total_score=round(total, 1),
        supply_quality=round(supply, 1),
        demand_heat=round(demand, 1),
        business_viability=round(viability, 1),
        timing=round(timing, 1),
        signals={
            "reddit": reddit_data or {"available": False},
            "trends": trends_data or {"available": False},
            "producthunt": producthunt_data or {"available": False},
        },
    )
