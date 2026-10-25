"""
Maintenance Recommendation & Work Order ORM Model.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base, TimestampMixin


class MaintenanceRecommendation(Base, TimestampMixin):
    __tablename__ = "maintenance_recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_order_number = Column(String(50), nullable=False, unique=True)
    pipe_id = Column(UUID(as_uuid=True), ForeignKey("pipes.id"), nullable=True)
    title = Column(String(200), nullable=False)
    target_asset = Column(String(100), nullable=False)
    priority = Column(String(20), nullable=False, default="medium")  # urgent, high, medium, routine
    priority_score = Column(Float, nullable=False, default=50.0)
    recommended_action = Column(String(100), default="inspect")  # inspect, repair, replace, acoustic_survey
    estimated_cost_inr = Column(Float, default=25000.0)
    assigned_team = Column(String(100), default="PMC Quick Response Team")
    status = Column(String(30), default="open")  # open, in_progress, completed, deferred
    due_date = Column(DateTime(timezone=True), nullable=True)
    details = Column(JSON, default=dict)
