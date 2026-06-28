"""Application configuration via environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Settings:
    """App-wide settings, loaded from environment variables with sensible defaults."""

    # Database
    database_url: str = field(
        default_factory=lambda: os.getenv(
            "DATABASE_URL",
            "sqlite+aiosqlite:///./niche_scanner.db",
        )
    )

    # Mock / sandbox flags
    hermes_mock: bool = field(
        default_factory=lambda: os.getenv("HERMES_MOCK", "true").lower() == "true"
    )
    sandbox_mode: bool = field(
        default_factory=lambda: os.getenv("SANDBOX_MODE", "true").lower() == "true"
    )

    # Paths
    reports_dir: Path = field(
        default_factory=lambda: Path(
            os.getenv("REPORTS_DIR", str(Path.cwd() / "reports"))
        )
    )

    # Scraper timeouts (seconds)
    scraper_timeout: int = int(os.getenv("SCRAPER_TIMEOUT", "15"))

    # Hermes CLI
    hermes_cli: str = os.getenv("HERMES_CLI", "hermes")

    def __post_init__(self) -> None:
        self.reports_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()
