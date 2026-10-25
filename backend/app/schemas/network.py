"""
Network Pydantic Schemas.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class NetworkBase(BaseModel):
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    srid: int = 4326


class NetworkResponse(NetworkBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime

