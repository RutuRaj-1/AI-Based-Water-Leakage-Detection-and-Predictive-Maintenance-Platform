"""
Pipe ORM Model.
Represents pipeline segments connecting nodes with physical, material,
and spatial attributes in the Pune water distribution network.
"""

import uuid
from sqlalchemy import Column, String, Float, Integer, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base, TimestampMixin


class Pipe(Base, TimestampMixin):
    __tablename__ = "pipes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    network_id = Column(UUID(as_uuid=True), ForeignKey("networks.id"), nullable=True)
    label = Column(String(100), nullable=False)          # e.g., "Katraj Feeder Main (P-104)"
    code = Column(String(50), nullable=True)             # e.g., "P-104"
    zone = Column(String(100), nullable=True)            # e.g., "Zone 4 — Katraj"
    start_node_id = Column(UUID(as_uuid=True), ForeignKey("nodes.id"), nullable=True)
    end_node_id = Column(UUID(as_uuid=True), ForeignKey("nodes.id"), nullable=True)
    length_m = Column(Float, nullable=False, default=1000.0)
    diameter_mm = Column(Float, nullable=False, default=300.0)
    material = Column(String(50), nullable=False, default="DI")  # CI, DI, PVC, HDPE
    roughness = Column(Float, default=130.0)             # Hazen-Williams coefficient
    installation_year = Column(Integer, nullable=False, default=2005)
    current_health_score = Column(Float, default=100.0)  # 0 to 100
    condition = Column(String(20), default="healthy")    # healthy, monitor, attention, critical
    pressure_bar = Column(Float, default=3.5)
    flow_rate_mld = Column(Float, default=10.0)
    coordinates = Column(JSON, default=list)             # Array of [lng, lat] coordinate pairs
    attributes = Column(JSON, default=dict)
