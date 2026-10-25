"""
Anomaly ORM Model.
Detected leakage events, pressure drops, and bursts.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base, TimestampMixin


class Anomaly(Base, TimestampMixin):
    __tablename__ = "anomalies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pipe_id = Column(UUID(as_uuid=True), ForeignKey("pipes.id"), nullable=True)
    pipe_code = Column(String(50), nullable=True)
    title = Column(String(200), nullable=False)
    location = Column(String(200), nullable=False)
    anomaly_type = Column(String(50), default="leak")  # leak, burst, pressure_drop, demand_surge
    severity = Column(String(20), nullable=False, default="moderate")  # critical, high, moderate, low, normal
    confidence = Column(Float, nullable=False, default=0.85)
    estimated_loss = Column(String(50), nullable=True)  # e.g., "42 kL/h"
    status = Column(String(30), default="active")  # active, investigating, resolved
    detected_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    details = Column(JSON, default=dict)
