"""
FastAPI dependencies for API-key authentication and DB sessions.
"""
from collections.abc import AsyncIterator

from fastapi import Header, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings


def require_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> None:
    """Require a configured API key for protected endpoints."""
    if not settings.api_key:
        raise HTTPException(
            status_code=503,
            detail="API authentication is not configured",
        )
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    """Yield an async database session from the application factory."""
    factory = request.app.state.session_factory
    async with factory() as session:
        yield session
