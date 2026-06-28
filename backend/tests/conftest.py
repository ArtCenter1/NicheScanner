"""Backend test fixtures and configuration.

Provides:
- ``mock_hermes`` (autouse): sets HERMES_MOCK=true so no real Hermes CLI calls.
- ``db_engine``: in-memory SQLite engine with tables created; patches
  ``app.core.database.async_session_factory`` so all layers (endpoints via
  dependency injection, background tasks via module reference) see the same
  test database.
- ``api_client``: HTTPX AsyncClient wired to the FastAPI app.
"""

from __future__ import annotations

import os
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Force mock mode for all tests
os.environ.setdefault("HERMES_MOCK", "true")
os.environ.setdefault("SANDBOX_MODE", "true")

# Import FastAPI app and database module separately to avoid naming collision.
# We alias them so the variable names below are unambiguous.
from app.main import app as fastapi_app  # noqa: N817
from app.core import database as db_mod  # noqa: E402
from app.core.database import Base  # noqa: E402

# Import the analyzer module so its module-level copy of ``database``
# gets patched too (it holds a reference via ``from app.core import database``).
import app.services.analyzer  # noqa: F401  # noqa: E402


@pytest.fixture(autouse=True)
def _mock_hermes():
    os.environ["HERMES_MOCK"] = "true"
    os.environ["SANDBOX_MODE"] = "true"
    yield


@pytest_asyncio.fixture
async def db_engine():
    """Create an in-memory SQLite engine with all tables, then patch
    the global ``async_session_factory`` so every layer uses it."""
    engine = create_async_engine("sqlite+aiosqlite://", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    test_factory = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    # Patch both references: the core module AND analyzer's cached module object
    db_mod.async_session_factory = test_factory

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture
async def api_client(db_engine) -> AsyncGenerator[AsyncClient, None]:
    """HTTPX AsyncClient pointed at the FastAPI app (no server needed).

    Depends on ``db_engine`` to ensure the in-memory DB with tables
    is live before any request hits the API.
    """
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client