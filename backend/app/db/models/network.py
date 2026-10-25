"""
Network ORM Model.
Represents a water distribution zone or district metering area (DMA) in Pune.
"""

import uuid
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base, TimestampMixin


class Network(Base, TimestampMixin):
    __tablename__ = "networks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    code = Column(String(50), nullable=True, unique=True)
    description = Column(Text, nullable=True)
    srid = Column(Integer, default=4326, nullable=False)
