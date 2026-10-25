"""
Health Assessment and Risk Prediction Pydantic Schemas.
"""

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class HealthAssessmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    pipe_id: UUID
    pipe_label: Optional[str] = None
    assessed_at: datetime
    health_score: float
    material_risk: float
    age_factor: float
    pressure_stress: float
    anomaly_penalty: float
    component_scores: Optional[Dict[str, Any]] = None



class RiskPredictionResponse(BaseModel):
    id: UUID
    pipe_id: UUID
    pipe_label: Optional[str] = None
    predicted_at: datetime
    horizon_days: int = 90
    failure_probability: float
    model_version: str = "v1.0-isolation-forest"
    criticality: str = "medium"
    recommended_action: str = "inspect"
