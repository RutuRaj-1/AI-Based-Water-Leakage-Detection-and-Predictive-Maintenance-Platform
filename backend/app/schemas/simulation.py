"""
Simulation Pydantic Schemas.
"""

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class SimulationRunRequest(BaseModel):
    network_id: Optional[UUID] = None
    scenario_type: str = Field(
        default="normal",
        description="normal, pipe_burst, slow_leak, demand_surge, blockage",
    )
    duration_hours: int = Field(default=24, ge=1, le=72)
    time_step_minutes: int = Field(default=15, ge=5, le=60)


class SimulationRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    scenario_type: str
    duration_hours: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    status: str
    summary_metrics: Dict[str, Any] = {}



class SimulationTelemetry(BaseModel):
    scenarioName: str
    timeStep: str
    engineStatus: str
    meanPressureBar: float
    totalFlowMld: float
    estimatedLossPct: float
    activeLeaksCount: int
    totalMonitoredPipes: int
    totalNodes: int
    networkHealthScore: float
