"""
Observation Pydantic Schemas.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class ObservationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    pipe_id: Optional[UUID] = None
    sensor_id: Optional[UUID] = None
    observed_at: datetime
    pressure_bar: Optional[float] = None
    pressure_kpa: Optional[float] = None
    flow_mld: Optional[float] = None
    flow_lps: Optional[float] = None
    quality_flag: int = 0



class TimeSeriesPoint(BaseModel):
    timestamp: str
    pressure_bar: float
    flow_mld: float
    expected_pressure_bar: Optional[float] = None
    is_anomaly: bool = False
