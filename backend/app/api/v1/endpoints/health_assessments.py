"""
Pipeline Health Assessment Endpoints.
"""

from typing import Any, Dict, Optional
from fastapi import APIRouter, Query
from app.repositories import pipe_repo
from app.ml.health_scorer import HealthScorer

router = APIRouter(prefix="/health-assessments", tags=["Health Assessments"])


@router.get("", summary="List pipeline health assessments")
async def list_health_assessments(
    pipe_id: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
) -> Dict[str, Any]:
    pipes_res = pipe_repo.list_pipes(page=page, page_size=page_size)
    pipes = pipes_res["items"]
    if pipe_id:
        pipes = [p for p in pipes if p["id"] == pipe_id or p.get("code") == pipe_id]

    items = []
    for p in pipes:
        score_data = HealthScorer.calculate_health_score(
            pipe_dict=p,
            active_anomalies_count=p.get("active_anomalies_count", 0),
        )
        items.append(
            {
                "id": f"ha-{p['id']}",
                "pipe_id": p["id"],
                "pipe_label": p.get("label", p["id"]),
                "health_score": score_data["health_score"],
                "condition": score_data["condition"],
                "material_risk": score_data["material_risk"],
                "age_factor": score_data["age_factor"],
                "pressure_stress": score_data["pressure_stress"],
                "anomaly_penalty": score_data["anomaly_penalty"],
                "component_scores": score_data["component_scores"],
            }
        )

    return {
        "items": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": len(items),
            "total_pages": 1,
        },
    }
