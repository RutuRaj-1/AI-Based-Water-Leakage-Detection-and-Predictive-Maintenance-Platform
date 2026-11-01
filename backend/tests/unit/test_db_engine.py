"""
Unit tests for database engine and connection pool configuration.

Verifies async engine creation, session factory setup, and pool configuration.
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.pool import QueuePool

from app.db import engine, AsyncSessionLocal, Base


def test_engine_is_async_engine():
    """Verify that the engine is an AsyncEngine."""
    assert isinstance(engine, AsyncEngine)


def test_engine_url_configured():
    """Verify engine is configured with PostgreSQL URL."""
    url_str = str(engine.url)
    assert 'postgresql' in url_str or 'postgres' in url_str
    assert 'localhost' in url_str or '127.0.0.1' in url_str
    assert '5432' in url_str


def test_session_local_is_async_sessionmaker():
    """Verify AsyncSessionLocal is an async session factory."""
    assert AsyncSessionLocal is not None
    # Verify it's a session maker by checking for required attributes
    assert hasattr(AsyncSessionLocal, '__call__')


def test_base_metadata_exists():
    """Verify Base metadata is initialized."""
    assert Base is not None
    assert Base.metadata is not None
    assert len(Base.metadata.tables) == 10


def test_base_metadata_has_all_tables():
    """Verify all 10 tables are registered in metadata."""
    expected_tables = {
        'networks', 'nodes', 'pipes', 'sensors', 'observations',
        'anomalies', 'health_assessments', 'risk_predictions',
        'maintenance_recommendations', 'simulation_runs'
    }
    actual_tables = set(Base.metadata.tables.keys())
    assert expected_tables == actual_tables


def test_engine_pool_config():
    """Verify engine pool configuration for async performance."""
    # Pool configuration should exist
    pool = engine.pool
    assert pool is not None
    # Pool size should be configured (default 10)
    assert hasattr(pool, '_pool_size')
