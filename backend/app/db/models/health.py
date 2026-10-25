"""
Health Assessment ORM Model.
Composite health scores (0-100) and risk factors for pipes.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, Float, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class HealthAssessment(Base):
    __tablename__ = "health_assessments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pipe_id = Column(UUID(as_uuid=True), ForeignKey("pipes.id"), nullable=False)
    assessed_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    health_score = Column(Float, nullable=False)  # 0 to 100
    material_risk = Column(Float, default=0.0)
    age_factor = Column(Float, default=0.0)
    pressure_stress = Column(Float, default=0.0)
    anomaly_penalty = Column(Float, default=0.0)
    component_scores = Column(JSON, default=dict)
