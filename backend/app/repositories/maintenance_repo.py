"""
Maintenance Work Order Repository.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from app.simulation.network_builder import PuneNetworkBuilder
from app.ml.risk_predictor import RiskPredictor


class MaintenanceRepository:
    def __init__(self):
        # Generate initial ranked maintenance work orders
        pipes = PuneNetworkBuilder.get_pipes()
        leaks = PuneNetworkBuilder.get_leaks()
        initial_recs = RiskPredictor.generate_maintenance_recommendations(pipes, leaks)
        self._work_orders: Dict[str, Dict[str, Any]] = {
            r["id"]: dict(r) for r in initial_recs
        }

    def list_recommendations(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> Dict[str, Any]:
        items = list(self._work_orders.values())
        if status:
            items = [w for w in items if w.get("status") == status]
        if priority:
            items = [w for w in items if w.get("priority") == priority]

        total = len(items)
        start = (page - 1) * page_size
        paginated_items = items[start : start + page_size]

        formatted_items = []
        for w in paginated_items:
            formatted_items.append(
                {
                    "id": w["id"],
                    "work_order_number": w.get("work_order_number", w["id"]),
                    "workOrderNumber": w.get("work_order_number", w["id"]),
                    "pipe_id": w.get("pipe_id", "P-104"),
                    "title": w.get("title", "Pipe Inspection"),
                    "target_asset": w.get("target_asset", w.get("pipe_id", "Asset")),
                    "targetAsset": w.get("target_asset", w.get("pipe_id", "Asset")),
                    "priority": w.get("priority", "medium"),
                    "priority_score": w.get("priority_score", 50.0),
                    "priorityScore": w.get("priority_score", 50.0),
                    "recommended_action": w.get("recommended_action", "inspect"),
                    "estimated_cost_inr": w.get("estimated_cost_inr", 25000.0),
                    "assigned_team": w.get("assigned_team", "PMC Quick Response Team"),
                    "assignedTeam": w.get("assigned_team", "PMC Quick Response Team"),
                    "status": w.get("status", "open"),
                    "due_date": w.get("due_date", datetime.now(timezone.utc).isoformat()),
                    "dueDate": w.get("due_date", datetime.now(timezone.utc).isoformat()),
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }
            )

        return {
            "items": formatted_items,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_items": total,
                "total_pages": max(1, (total + page_size - 1) // page_size),
            },
        }

    def get_recommendation(self, work_order_id: str) -> Optional[Dict[str, Any]]:
        wo = self._work_orders.get(work_order_id)
        if not wo:
            for w in self._work_orders.values():
                if w.get("work_order_number") == work_order_id:
                    wo = w
                    break
        return wo

    def update_recommendation(
        self,
        work_order_id: str,
        update_data: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        wo = self.get_recommendation(work_order_id)
        if not wo:
            return None
        for key, value in update_data.items():
            if value is not None:
                wo[key] = value
        wo["updated_at"] = datetime.now(timezone.utc).isoformat()
        return wo
