"""
Observation Time-Series Endpoints.
"""

from typing import Any, Dict, Optional
from fastapi import APIRouter, Query
from app.repositories import observation_repo

router = APIRouter(prefix="/observations", tags=["Observations"])


@router.get("", summary="Query sensor pressure and flow observations")
async def list_observations(
    pipe_id: Optional[str] = Query(default=None),
    from_time: Optional[str] = Query(default=None, alias="from"),
    to_time: Optional[str] = Query(default=None, alias="to"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
) -> Dict[str, Any]:
    return observation_repo.list_observations(
        pipe_id=pipe_id,
        from_time=from_time,
        to_time=to_time,
        page=page,
        page_size=page_size,
    )
