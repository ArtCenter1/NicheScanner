"""Tests for the rule-based scoring engine (scorer.py).

Scoring is fully deterministic — no mocks needed for these tests.
"""

from app.services.scorer import compute_score


def test_score_all_signals_present():
    """When all three data sources return data, scores should be well-formed."""
    result = compute_score(
        name="AI for lawyers",
        reddit_data={"post_count": 80, "avg_sentiment": 0.4},
        trends_data={"volume": 60, "slope": 0.15, "direction": "rising"},
        producthunt_data={
            "competitor_count": 3,
            "avg_rating": 3.2,
            "avg_upvotes": 45,
        },
    )

    assert result.name == "AI for lawyers"
    assert 0 <= result.total_score <= 100
    assert 0 <= result.supply_quality <= 100
    assert 0 <= result.demand_heat <= 100
    assert 0 <= result.business_viability <= 100
    assert 0 <= result.timing <= 100


def test_score_no_signals():
    """With zero signals, score defaults to a low baseline."""
    result = compute_score(name="Empty idea")

    assert result.name == "Empty idea"
    # All dimensions should have their baseline values
    assert result.supply_quality == 50.0
    assert result.business_viability == 40.0
    assert result.total_score > 0


def test_score_negative_sentiment_boosts_supply():
    """Worse existing-solution sentiment → higher supply quality score."""
    bad = compute_score(
        name="Bad sentiment",
        reddit_data={"post_count": 100, "avg_sentiment": 0.2},
        producthunt_data={"competitor_count": 2, "avg_rating": 2.0, "avg_upvotes": 30},
    )
    good = compute_score(
        name="Good sentiment",
        reddit_data={"post_count": 100, "avg_sentiment": 0.8},
        producthunt_data={"competitor_count": 2, "avg_rating": 4.5, "avg_upvotes": 30},
    )

    assert bad.supply_quality > good.supply_quality


def test_score_rising_trend_boosts_demand_and_timing():
    """A rising trend direction should increase demand heat and timing scores."""
    rising = compute_score(
        name="Rising",
        trends_data={"volume": 50, "slope": 0.2, "direction": "rising"},
    )
    flat = compute_score(name="Flat", trends_data={"volume": 50, "slope": 0.0, "direction": "stable"})

    assert rising.demand_heat > flat.demand_heat
    assert rising.timing > flat.timing


def test_score_high_post_count_demand():
    """Higher Reddit post count → higher demand heat."""
    high = compute_score(
        name="Popular",
        reddit_data={"post_count": 200, "avg_sentiment": 0.5},
    )
    low = compute_score(
        name="Unpopular",
        reddit_data={"post_count": 5, "avg_sentiment": 0.5},
    )

    assert high.demand_heat > low.demand_heat


def test_score_sorting():
    """Multiple ideas should sort by total_score descending."""
    a = compute_score(
        name="A",
        reddit_data={"post_count": 150, "avg_sentiment": 0.3},
        trends_data={"volume": 80, "slope": 0.2, "direction": "rising"},
        producthunt_data={"competitor_count": 1, "avg_rating": 2.5, "avg_upvotes": 60},
    )
    b = compute_score(
        name="B",
        reddit_data={"post_count": 10, "avg_sentiment": 0.7},
        trends_data={"volume": 10, "slope": -0.1, "direction": "falling"},
        producthunt_data={"competitor_count": 15, "avg_rating": 4.8, "avg_upvotes": 10},
    )

    assert a.total_score > b.total_score


def test_score_signals_metadata():
    """The result should carry signal metadata for the frontend."""
    result = compute_score(
        name="Test",
        reddit_data={"post_count": 50, "avg_sentiment": 0.5},
    )

    assert "signals" in result.__dict__
    assert result.signals["reddit"]["post_count"] == 50
    assert result.signals["producthunt"]["available"] is False
