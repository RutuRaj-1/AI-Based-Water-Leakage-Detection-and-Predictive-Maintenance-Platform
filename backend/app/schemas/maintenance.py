"""
Maintenance Work Order Pydantic Schemas.
Matches both backend ORM and frontend MaintenanceTask types.
"""

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class MaintenanceBase(BaseModel):
    work_order_number: str
    title: str
    target_asset: str
    priority: str = "medium"  # urgent, high, medium, routine
    priority_score: float = 50.0
    recommended_action: str = "inspect"
    estimated_cost_inr: float = 25000.0
    assigned_team: str = "PMC Quick Response Team"
    status: str = "open"  # open, in_progress, completed, deferred
    due_date: Optional[datetime] = None


class MaintenanceCreate(MaintenanceBase):
    pipe_id: Optional[UUID] = None
    details: Optional[Dict[str, Any]] = None


class MaintenanceUpdate(BaseModel):
    status: Optional[str] = None
    assigned_team: Optional[str] = None
    priority: Optional[str] = None
    recommended_action: Optional[str] = None


class MaintenanceResponse(MaintenanceBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    pipe_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    details: Optional[Dict[str, Any]] = None



class MaintenanceTaskFrontend(BaseModel):
    id: str
    workOrderNumber: str
    title: str
    targetAsset: str
    priority: str
    priorityScore: float
    assignedTeam: str
    dueDate: str
