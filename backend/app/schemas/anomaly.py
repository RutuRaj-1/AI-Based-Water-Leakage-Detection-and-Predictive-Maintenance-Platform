"""
Anomaly Pydantic Schemas.
Matches both backend ORM and frontend LeakAlert / LeakMarker types.
"""

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class AnomalyBase(BaseModel):
    title: str
    location: str
    pipe_code: Optional[str] = None
    anomaly_type: str = "leak"
    severity: str = "moderate"  # critical, high, moderate, low, normal
    confidence: float = 0.85
    estimated_loss: Optional[str] = None
    status: str = "active"


class AnomalyCreate(AnomalyBase):
    pipe_id: Optional[UUID] = None
    details: Optional[Dict[str, Any]] = None


class AnomalyResponse(AnomalyBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    pipe_id: Optional[UUID] = None
    detected_at: datetime
    details: Optional[Dict[str, Any]] = None



class LeakAlert(BaseModel):
    id: str
    title: str
    location: str
    pipelineId: str
    estimatedLoss: str
    severity: str
    timestamp: str
    status: str
