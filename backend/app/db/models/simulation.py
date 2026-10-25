"""
Simulation Run ORM Model.
Tracks hydraulic simulation runs and metadata.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class SimulationRun(Base):
    __tablename__ = "simulation_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    network_id = Column(UUID(as_uuid=True), nullable=True)
    scenario_type = Column(String(50), nullable=False, default="normal")  # normal, pipe_burst, slow_leak, demand_surge
    duration_hours = Column(Integer, default=24)
    time_step_minutes = Column(Integer, default=15)
    started_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    completed_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(30), default="running")  # running, completed, failed
    summary_metrics = Column(JSON, default=dict)
