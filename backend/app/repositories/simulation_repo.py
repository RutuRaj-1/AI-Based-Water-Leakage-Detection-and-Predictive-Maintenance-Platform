"""
Simulation Repository.
Tracks hydraulic simulation executions and real-time telemetry metrics.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid
from app.simulation.engine import HydraulicEngine


class SimulationRepository:
    def __init__(self):
        self.engine = HydraulicEngine()
        self._runs: List[Dict[str, Any]] = []

        # Initialize with baseline initial simulation
        initial_sim = self.engine.run_simulation(scenario_type="normal", duration_hours=24)
        run_id = "sim-run-pune-001"
        self._runs.append(
            {
                "id": run_id,
                "scenario_type": "normal",
                "duration_hours": 24,
                "started_at": datetime.now(timezone.utc).isoformat(),
                "completed_at": datetime.now(timezone.utc).isoformat(),
                "status": "completed",
                "summary_metrics": initial_sim["telemetry"],
            }
        )
        self._latest_telemetry = initial_sim["telemetry"]

    def list_runs(self, page: int = 1, page_size: int = 50) -> Dict[str, Any]:
        total = len(self._runs)
        start = (page - 1) * page_size
        items = self._runs[start : start + page_size]
        return {
            "items": items,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_items": total,
                "total_pages": max(1, (total + page_size - 1) // page_size),
            },
        }

    def get_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        for r in self._runs:
            if r["id"] == run_id:
                return r
        return None

    def execute_simulation(
        self,
        scenario_type: str = "normal",
        duration_hours: int = 24,
        time_step_minutes: int = 15,
    ) -> Dict[str, Any]:
        sim_result = self.engine.run_simulation(
            scenario_type=scenario_type,
            duration_hours=duration_hours,
            time_step_minutes=time_step_minutes,
        )
        run_id = f"sim-run-{len(self._runs) + 1:03d}"
        run_entry = {
            "id": run_id,
            "scenario_type": scenario_type,
            "duration_hours": duration_hours,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "status": "completed",
            "summary_metrics": sim_result["telemetry"],
        }
        self._runs.insert(0, run_entry)
        self._latest_telemetry = sim_result["telemetry"]

        return {
            "run": run_entry,
            "time_series_by_pipe": sim_result["time_series_by_pipe"],
            "telemetry": sim_result["telemetry"],
        }

    def get_telemetry(self) -> Dict[str, Any]:
        return dict(self._latest_telemetry)
