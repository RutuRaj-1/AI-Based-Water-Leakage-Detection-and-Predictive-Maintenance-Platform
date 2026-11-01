"""
Async SQLAlchemy engine, session factory, and connection pool configuration.

This module provides the core database connectivity infrastructure:
- AsyncEngine: Async connection to PostgreSQL with asyncpg driver
- AsyncSessionLocal: Session factory for creating async sessions
- Connection pool: Configured for concurrent async operations

Usage:
    from app.db.engine import engine, AsyncSessionLocal
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(...)
"""

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

# Create async engine with asyncpg driver
engine: AsyncEngine = create_async_engine(
    settings.database_url,
    echo=settings.environment == "development",  # Log SQL in dev
    echo_pool=settings.environment == "development",  # Log pool events in dev
    pool_size=10,  # Number of connections to maintain in the pool
    max_overflow=20,  # Additional connections when pool is exhausted
    pool_pre_ping=True,  # Test connections before using (prevents stale connections)
    pool_recycle=3600,  # Recycle connections after 1 hour
)

# Session factory for creating async sessions
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit (safe for async)
    autoflush=False,  # Manual flush control (best practice for async)
)


async def get_session() -> AsyncSession:
    """
    Dependency injection helper for FastAPI endpoints.
    Yields an async session for use in a route handler.
    
    Usage in FastAPI:
        @app.get("/networks")
        async def list_networks(session: AsyncSession = Depends(get_session)):
            result = await session.execute(...)
    """
    async with AsyncSessionLocal() as session:
        yield session
