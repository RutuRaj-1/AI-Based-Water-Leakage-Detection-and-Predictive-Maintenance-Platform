"""
Maintenance Work Order Management Endpoints.
"""

from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, Query
from app.repositories import maintenance_repo
from app.schemas.maintenance import MaintenanceUpdate

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])


@router.get("", summary="List prioritised maintenance work orders")
@router.get("/recommendations", summary="List prioritised maintenance recommendations")
async def list_maintenance(
    status: Optional[str] = Query(default=None),
    priority: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
) -> Dict[str, Any]:
    return maintenance_repo.list_recommendations(
        status=status,
        priority=priority,
        page=page,
        page_size=page_size,
    )


@router.get("/{work_order_id}", summary="Get specific maintenance work order detail")
async def get_maintenance(work_order_id: str) -> Dict[str, Any]:
    wo = maintenance_repo.get_recommendation(work_order_id)
    if not wo:
        raise HTTPException(status_code=404, detail="Maintenance work order not found")
    return wo


@router.patch("/{work_order_id}", summary="Update maintenance work order status or assignment")
async def update_maintenance(
    work_order_id: str,
    payload: MaintenanceUpdate,
) -> Dict[str, Any]:
    update_data = payload.model_dump(exclude_unset=True)
    updated = maintenance_repo.update_recommendation(work_order_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Maintenance work order not found")
    return updated
