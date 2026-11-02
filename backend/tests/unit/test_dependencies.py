"""
Unit tests for database dependencies.

Verifies that all required database packages are installed and importable.
"""

import pytest


def test_sqlalchemy_import():
    """Verify SQLAlchemy is installed."""
    import sqlalchemy
    assert hasattr(sqlalchemy, '__version__')
    assert tuple(map(int, sqlalchemy.__version__.split('.')[:2])) >= (2, 0)


def test_asyncpg_or_psycopg_import():
    """Verify either asyncpg or psycopg (async PostgreSQL driver) is installed."""
    try:
        import psycopg
        assert hasattr(psycopg, '__version__')
    except ImportError:
        import asyncpg
        assert hasattr(asyncpg, '__version__')


def test_alembic_import():
    """Verify Alembic is installed."""
    import alembic
    assert hasattr(alembic, '__version__')


def test_geoalchemy2_import():
    """Verify GeoAlchemy2 is installed for PostGIS support."""
    import geoalchemy2
    assert hasattr(geoalchemy2, '__version__')


def test_models_import():
    """Verify all ORM models can be imported."""
    from app.db import (
        Network, Node, Pipe, Sensor, Observation,
        Anomaly, HealthAssessment, RiskPrediction,
        MaintenanceRecommendation, SimulationRun,
        Base
    )
    assert Network is not None
    assert Node is not None
    assert Pipe is not None
    assert Sensor is not None
    assert Observation is not None
    assert Anomaly is not None
    assert HealthAssessment is not None
    assert RiskPrediction is not None
    assert MaintenanceRecommendation is not None
    assert SimulationRun is not None
    assert Base is not None


def test_enums_import():
    """Verify all enum types can be imported."""
    from app.db import (
        NodeType, SensorType, AnomalySeverity,
        SimulationStatus, MaintenanceStatus
    )
    assert NodeType.JUNCTION is not None
    assert SensorType.PRESSURE is not None
    assert AnomalySeverity.HIGH is not None
    assert SimulationStatus.COMPLETED is not None
    assert MaintenanceStatus.OPEN is not None


def test_metadata_tables():
    """Verify all 10 tables are registered in Base metadata."""
    from app.db import Base
    expected_tables = {
        'networks',
        'nodes',
        'pipes',
        'sensors',
        'observations',
        'anomalies',
        'health_assessments',
        'risk_predictions',
        'maintenance_recommendations',
        'simulation_runs',
    }
    actual_tables = set(Base.metadata.tables.keys())
    assert expected_tables == actual_tables, f"Expected {expected_tables}, got {actual_tables}"
