"""
Simulation Worker Pipeline.
Connects hydraulic simulation -> observation ingestion -> ML anomaly detection
-> composite health scoring -> maintenance recommendation generation.
"""

import logging
from typing import Any, Dict
from app.repositories import (
    pipe_repo,
    observation_repo,
    anomaly_repo,
    maintenance_repo,
    simulation_repo,
)
from app.ml.anomaly_detector import LeakAnomalyDetector
from app.ml.health_scorer import HealthScorer
from app.ml.risk_predictor import RiskPredictor

logger = logging.getLogger(__name__)


class SimulationWorker:
    """Orchestrates end-to-end hydraulic simulation and AI/ML analysis."""

    def __init__(self):
        self.anomaly_detector = LeakAnomalyDetector()

    def run_pipeline(
        self,
        scenario_type: str = "normal",
        duration_hours: int = 24,
        time_step_minutes: int = 15,
    ) -> Dict[str, Any]:
        logger.info(f"Starting simulation pipeline with scenario: {scenario_type}")

        # 1. Execute simulation
        sim_data = simulation_repo.execute_simulation(
            scenario_type=scenario_type,
            duration_hours=duration_hours,
            time_step_minutes=time_step_minutes,
        )

        time_series = sim_data["time_series_by_pipe"]
        observation_repo.update_with_simulation_result(time_series)

        # 2. Run ML Anomaly Detection across all pipelines
        detected_anomalies = []
        for pipe_id, readings in time_series.items():
            anomalies = self.anomaly_detector.detect_anomalies(
                pipe_id=pipe_id,
                recent_time_series=readings,
            )
            for a in anomalies:
                saved_a = anomaly_repo.add_anomaly(a)
                detected_anomalies.append(saved_a)

        # 3. Dynamic Health Scoring for each pipe
        active_leaks_res = anomaly_repo.list_anomalies(active=True)
        active_leaks = active_leaks_res["items"]
        active_map = {}
        for lk in active_leaks:
            pid = lk.get("pipe_id") or lk.get("pipe_code")
            active_map[pid] = active_map.get(pid, 0) + 1

        pipes_res = pipe_repo.list_pipes(page=1, page_size=100)
        pipes = pipes_res["items"]

        for pipe in pipes:
            pid = pipe["id"]
            active_cnt = active_map.get(pid, 0)
            score_data = HealthScorer.calculate_health_score(
                pipe_dict=pipe,
                active_anomalies_count=active_cnt,
            )
            pipe_repo.update_pipe_health(
                pipe_id=pid,
                new_score=score_data["health_score"],
                condition=score_data["condition"],
            )

        # 4. Generate updated maintenance work orders
        updated_pipes = pipe_repo.list_pipes(page=1, page_size=100)["items"]
        new_recs = RiskPredictor.generate_maintenance_recommendations(
            pipes=updated_pipes,
            active_leaks=active_leaks,
        )
        for rec in new_recs:
            maintenance_repo.update_recommendation(rec["id"], rec)

        logger.info(
            f"Simulation pipeline finished: {len(detected_anomalies)} anomalies detected."
        )

        return {
            "status": "completed",
            "scenario_type": scenario_type,
            "telemetry": sim_data["telemetry"],
            "anomalies_detected": len(detected_anomalies),
            "pipes_assessed": len(pipes),
        }


# Global worker instance
simulation_worker = SimulationWorker()
