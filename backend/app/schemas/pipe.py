"""
Pipeline Pydantic Schemas.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class PipeBase(BaseModel):
    label: str
    code: Optional[str] = None
    zone: Optional[str] = None
    length_m: float
    diameter_mm: float
    material: str
    roughness: Optional[float] = 130.0
    installation_year: int
    current_health_score: float = 100.0
    condition: str = "healthy"
    pressure_bar: float = 3.5
    flow_rate_mld: float = 10.0


class PipeCreate(PipeBase):
    network_id: Optional[UUID] = None
    coordinates: Optional[List[List[float]]] = None


class PipeResponse(PipeBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    network_id: Optional[UUID] = None
    start_node_id: Optional[UUID] = None
    end_node_id: Optional[UUID] = None
    coordinates: Optional[List[List[float]]] = None
    attributes: Optional[Dict[str, Any]] = None



class PipeDetailResponse(PipeResponse):
    age_years: int
    failure_probability: float = 0.05
    criticality: str = "medium"
    active_anomalies_count: int = 0
