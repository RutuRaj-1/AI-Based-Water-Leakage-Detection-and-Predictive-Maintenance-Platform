"""
Failure Risk Predictions Endpoints.
"""

from typing import Any, Dict, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Query
from app.repositories import pipe_repo
from app.ml.risk_predictor import RiskPredictor

router = APIRouter(prefix="/predictions", tags=["Predictions"])


@router.get("", summary="List pipeline failure risk predictions")
async def list_predictions(
    pipe_id: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
) -> Dict[str, Any]:
    pipes_res = pipe_repo.list_pipes(page=page, page_size=page_size)
    pipes = pipes_res["items"]
    if pipe_id:
        pipes = [p for p in pipes if p["id"] == pipe_id or p.get("code") == pipe_id]

    items = []
    now = datetime.now(timezone.utc).isoformat()
    for p in pipes:
        health_score = p.get("current_health_score", 100.0)
        diameter = p.get("diameter_mm", 200.0)
        fail_prob = RiskPredictor.calculate_failure_probability(health_score)
        crit_mult = RiskPredictor.get_criticality_multiplier(diameter)
        crit = "urgent" if crit_mult >= 1.4 else ("high" if crit_mult >= 1.1 else "medium")

        items.append(
            {
                "id": f"pred-{p['id']}",
                "pipe_id": p["id"],
                "pipe_label": p.get("label", p["id"]),
                "predicted_at": now,
                "horizon_days": 90,
                "failure_probability": fail_prob,
                "model_version": "v1.0-isolation-forest",
                "criticality": crit,
                "recommended_action": "replace" if fail_prob > 0.6 else "inspect",
            }
        )

    # Sort by failure probability descending
    items.sort(key=lambda x: x["failure_probability"], reverse=True)

    return {
        "items": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": len(items),
            "total_pages": 1,
        },
    }
