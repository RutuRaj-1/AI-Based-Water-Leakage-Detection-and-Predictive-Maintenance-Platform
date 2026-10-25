"""
Sensor ORM Model.
Represents telemetry monitoring devices installed on network nodes or pipelines.
"""

import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base, TimestampMixin


class Sensor(Base, TimestampMixin):
    __tablename__ = "sensors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    label = Column(String(100), nullable=False)
    sensor_type = Column(String(50), nullable=False, default="pressure")  # pressure, flow, acoustic, quality
    pipe_id = Column(UUID(as_uuid=True), ForeignKey("pipes.id"), nullable=True)
    node_id = Column(UUID(as_uuid=True), ForeignKey("nodes.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    attributes = Column(JSON, default=dict)
