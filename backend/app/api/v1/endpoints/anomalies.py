"""
Anomaly and Leak Detection Endpoints.
"""

from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.repositories import anomaly_repo

router = APIRouter(prefix="/anomalies", tags=["Anomalies"])


class AnomalyStatusUpdate(BaseModel):
    status: str  # active, investigating, resolved


@router.get("", summary="List detected anomaly events and leak alerts")
async def list_anomalies(
    active: Optional[bool] = Query(default=None),
    severity: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
) -> Dict[str, Any]:
    return anomaly_repo.list_anomalies(
        active=active,
        severity=severity,
        page=page,
        page_size=page_size,
    )


@router.get("/{anomaly_id}", summary="Get specific anomaly detail")
async def get_anomaly(anomaly_id: str) -> Dict[str, Any]:
    anomaly = anomaly_repo.get_anomaly(anomaly_id)
    if not anomaly:
        raise HTTPException(status_code=404, detail="Anomaly event not found")
    return anomaly


@router.patch("/{anomaly_id}", summary="Update anomaly status (e.g., investigating, resolved)")
async def update_anomaly_status(
    anomaly_id: str,
    payload: AnomalyStatusUpdate,
) -> Dict[str, Any]:
    updated = anomaly_repo.update_status(anomaly_id, payload.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Anomaly event not found")
    return updated
