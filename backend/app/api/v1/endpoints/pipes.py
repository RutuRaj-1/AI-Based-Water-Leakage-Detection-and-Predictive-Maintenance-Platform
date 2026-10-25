"""
Pipeline Asset Management Endpoints.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.repositories import pipe_repo, observation_repo
from app.ml.health_scorer import HealthScorer

router = APIRouter(prefix="/pipes", tags=["Pipelines"])


@router.get("", summary="List pipeline inventory")
async def list_pipes(
    zone: Optional[str] = Query(default=None),
    condition: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
) -> Dict[str, Any]:
    return pipe_repo.list_pipes(zone=zone, condition=condition, page=page, page_size=page_size)


@router.get("/{pipe_id}", summary="Get specific pipe details and health assessment")
async def get_pipe(pipe_id: str) -> Dict[str, Any]:
    pipe = pipe_repo.get_pipe(pipe_id)
    if not pipe:
        raise HTTPException(status_code=404, detail="Pipeline asset not found")
    return pipe


@router.get("/{pipe_id}/observations", summary="Get pressure and flow time-series observations")
async def get_pipe_observations(
    pipe_id: str,
    limit: int = Query(default=96, ge=1, le=500),
) -> List[Dict[str, Any]]:
    pipe = pipe_repo.get_pipe(pipe_id)
    if not pipe:
        raise HTTPException(status_code=404, detail="Pipeline asset not found")
    return observation_repo.get_pipe_observations(pipe_id=pipe_id, limit=limit)


@router.get("/{pipe_id}/health", summary="Get composite health breakdown for pipe")
async def get_pipe_health(pipe_id: str) -> Dict[str, Any]:
    pipe = pipe_repo.get_pipe(pipe_id)
    if not pipe:
        raise HTTPException(status_code=404, detail="Pipeline asset not found")
    health_breakdown = HealthScorer.calculate_health_score(
        pipe_dict=pipe,
        active_anomalies_count=pipe.get("active_anomalies_count", 0),
    )
    return {
        "pipe_id": pipe_id,
        "pipe_label": pipe.get("label"),
        "health_score": health_breakdown["health_score"],
        "condition": health_breakdown["condition"],
        "breakdown": health_breakdown["component_scores"],
        "deductions": {
            "material_risk": health_breakdown["material_risk"],
            "age_factor": health_breakdown["age_factor"],
            "pressure_stress": health_breakdown["pressure_stress"],
            "anomaly_penalty": health_breakdown["anomaly_penalty"],
        },
    }
