# Niche Scanner — AI Niche Market Discovery Tool

**Find the best business idea to build — in under 60 seconds.**

Niche Scanner takes 1–5 business ideas and produces a data-backed, ranked analysis
with scores across 4 dimensions, action recommendations, and a downloadable PDF report.

```
Input:  "AI tool for lawyers", "SaaS for plumbers", "Pet-sitting marketplace"
           ↓
    Scrapes: Reddit discussion volume, Google Trends trajectory, Product Hunt supply gap
           ↓
    Scores: Supply quality (35%) · Demand heat (30%) · Business viability (20%) · Timing (15%)
           ↓
Output:  Ranked list + detailed cards + PDF report
```

## Business Model

| Dimension | Detail |
|-----------|--------|
| **Pricing** | One-time $79/report (not subscription) |
| **Rationale** | User finds their niche → has the info → churns → subscription doesn't fit |
| **Positioning** | Entry tool for the Polsia AI-agent ecosystem |

## Architecture

```
┌──────────────┐     POST /analyze      ┌──────────────────┐
│  Next.js 14  │ ─────────────────────→  │   FastAPI (Python)│
│  (frontend)  │ ←── polling GET /report─│                  │
└──────────────┘                         │  ┌────────────┐  │
                                         │  │ Scrapers   │  │
                                         │  │ (httpx)    │  │
                                         │  ├────────────┤  │
                                         │  │ Scorer     │  │
                                         │  │ (rule-based)│  │
                                         │  ├────────────┤  │
                                         │  │ Hermes CLI │  │
                                         │  │ (LLM enrich)│  │
                                         │  ├────────────┤  │
                                         │  │ PDF Render │  │
                                         │  └────────────┘  │
                                         │                  │
                                         │  ┌────────────┐  │
                                         │  │ PostgreSQL │  │
                                         │  └────────────┘  │
                                         └──────────────────┘
```

## Quick Start

```bash
# Clone and configure
git clone <repo>
cd niche-scanner
cp .env.example .env

# Start with Docker
make up

# Or run backend locally
make backend

# Run tests
make test
```

## Scoring Dimensions

| Dimension | Weight | Core Question | Data Source |
|-----------|--------|---------------|-------------|
| **Supply Quality** | 35% | How bad are existing solutions? | G2/App Store ratings, complaint density |
| **Demand Heat** | 30% | Is the demand real? | Reddit discussion volume, Google Trends |
| **Business Viability** | 20% | Can you charge for it? | Pricing range, B2B/B2C signals |
| **Timing** | 15% | Is now the right time? | Trend direction, new entrants velocity |

## License

Forked from [Polsia](https://github.com/PolsiaAI/Polsia) (BSD-3-Clause).
Niche Scanner additions are available under the same license.
