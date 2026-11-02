"""
Database module: async SQLAlchemy setup, ORM models, and utilities.

Exports:
- engine: Async SQLAlchemy engine
- AsyncSessionLocal: Async session factory
- get_session: Dependency for FastAPI endpoints
- Base: Declarative base for all models
- AuditMixin, TimestampMixin: Audit column mixins
- All ORM model classes (Network, Node, Pipe, Sensor, Observation, Anomaly, etc.)
- Enums: NodeType, SensorType, AnomalySeverity, SimulationStatus, MaintenanceStatus
"""

from app.db.base import AuditMixin, Base, TimestampMixin
from app.db.engine import AsyncSessionLocal, engine, get_session
from app.db.models import (
    Anomaly,
    AnomalySeverity,
    HealthAssessment,
    MaintenanceRecommendation,
    MaintenanceStatus,
    Node,
    NodeType,
    Observation,
    Pipe,
    RiskPrediction,
    Sensor,
    SensorType,
    SimulationRun,
    SimulationStatus,
    Network,
)

__all__ = [
    # Engine and session
    "engine",
    "AsyncSessionLocal",
    "get_session",
    # Base and mixins
    "Base",
    "AuditMixin",
    "TimestampMixin",
    # Models
    "Network",
    "Node",
    "Pipe",
    "Sensor",
    "Observation",
    "Anomaly",
    "HealthAssessment",
    "RiskPrediction",
    "MaintenanceRecommendation",
    "SimulationRun",
    # Enums
    "NodeType",
    "SensorType",
    "AnomalySeverity",
    "SimulationStatus",
    "MaintenanceStatus",
]
