"""
Node ORM Model.
Represents junctions, reservoirs, tanks, and pumps in the Pune hydraulic network.
"""

import uuid
from sqlalchemy import Column, String, Float, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base, TimestampMixin


class Node(Base, TimestampMixin):
    __tablename__ = "nodes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    network_id = Column(UUID(as_uuid=True), ForeignKey("networks.id"), nullable=True)
    label = Column(String(100), nullable=False)
    node_type = Column(String(50), default="junction", nullable=False)  # reservoir, pump, junction, treatment_plant
    elevation_m = Column(Float, nullable=False, default=560.0)
    base_demand_lps = Column(Float, default=0.0)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    zone = Column(String(100), nullable=True)
    attributes = Column(JSON, default=dict)
