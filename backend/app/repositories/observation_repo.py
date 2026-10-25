"""
Observation Repository.
Provides time-series pressure and flow observation curves for hydraulic analysis.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from app.simulation.engine import HydraulicEngine


class ObservationRepository:
    def __init__(self):
        self.engine = HydraulicEngine()
        # Pre-generate 24h baseline simulation observations
        sim_result = self.engine.run_simulation(scenario_type="normal", duration_hours=24)
        self._time_series = sim_result["time_series_by_pipe"]

    def get_pipe_observations(
        self,
        pipe_id: str,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        readings = self._time_series.get(pipe_id, [])
        if not readings:
            # Fallback generator for un-cached pipe
            fallback_sim = self.engine.run_simulation(scenario_type="normal", duration_hours=24)
            readings = fallback_sim["time_series_by_pipe"].get(pipe_id, [])
        return readings[-limit:]

    def list_observations(
        self,
        pipe_id: Optional[str] = None,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> Dict[str, Any]:
        all_obs = []
        if pipe_id:
            all_obs = self.get_pipe_observations(pipe_id, limit=200)
        else:
            for pid, items in self._time_series.items():
                for it in items:
                    it_copy = dict(it)
                    it_copy["pipe_id"] = pid
                    all_obs.append(it_copy)

        total = len(all_obs)
        start = (page - 1) * page_size
        items = all_obs[start : start + page_size]

        formatted_items = []
        for i, it in enumerate(items, start=1):
            formatted_items.append(
                {
                    "id": f"obs-{i:04d}",
                    "pipe_id": it.get("pipe_id", pipe_id or "P-104"),
                    "observed_at": it["timestamp"],
                    "pressure_bar": it["pressure_bar"],
                    "pressure_kpa": round(it["pressure_bar"] * 100.0, 1),
                    "flow_mld": it["flow_mld"],
                    "flow_lps": round(it["flow_mld"] * 11.574, 1),
                    "quality_flag": 0,
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

    def update_with_simulation_result(self, time_series_by_pipe: Dict[str, List[Dict[str, Any]]]) -> None:
        self._time_series.update(time_series_by_pipe)
