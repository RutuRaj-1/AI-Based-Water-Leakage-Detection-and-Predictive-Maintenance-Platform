"""
Observation ORM Model.
Time-series pressure and flow readings from physical or simulated sensors.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, Float, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class Observation(Base):
    __tablename__ = "observations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sensor_id = Column(UUID(as_uuid=True), ForeignKey("sensors.id"), nullable=True)
    pipe_id = Column(UUID(as_uuid=True), ForeignKey("pipes.id"), nullable=True)
    simulation_run_id = Column(UUID(as_uuid=True), nullable=True)
    observed_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
    pressure_bar = Column(Float, nullable=True)
    pressure_kpa = Column(Float, nullable=True)
    flow_mld = Column(Float, nullable=True)
    flow_lps = Column(Float, nullable=True)
    quality_flag = Column(Integer, default=0)  # 0=ok, 1=suspect, 2=bad
