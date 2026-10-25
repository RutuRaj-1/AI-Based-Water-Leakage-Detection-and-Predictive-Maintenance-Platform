"""
Failure Risk Predictor and Maintenance Prioritisation Engine.
Ranks pipelines by failure probability, criticality, and generates work orders.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List
import numpy as np


class RiskPredictor:
    """Predicts failure probabilities and prioritises maintenance operations."""

    @staticmethod
    def calculate_failure_probability(
        health_score: float,
        horizon_days: int = 90,
    ) -> float:
        """
        Calculates failure probability using logistic hazard model:
        P(fail) = 1 / (1 + exp(-(0.05 * (100 - health_score) - 2.0)))
        Scaled by horizon factor.
        """
        stress = 100.0 - health_score
        base_logit = 0.052 * stress - 2.10
        horizon_factor = (horizon_days / 90.0) ** 0.5
        prob = 1.0 / (1.0 + np.exp(-base_logit * horizon_factor))
        return round(float(max(0.01, min(0.99, prob))), 3)

    @staticmethod
    def get_criticality_multiplier(diameter_mm: float) -> float:
        """Larger transmission trunks have higher failure impact / criticality."""
        if diameter_mm >= 350.0:
            return 1.45  # Trunk transmission
        elif diameter_mm >= 250.0:
            return 1.20  # Sub-main distribution
        else:
            return 0.95  # Local reticulation

    @classmethod
    def generate_maintenance_recommendations(
        cls,
        pipes: List[Dict[str, Any]],
        active_leaks: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        leak_map = {
            (l.get("pipeline_id") or l.get("pipe_id") or l.get("pipe_code")): l
            for l in active_leaks
            if (l.get("pipeline_id") or l.get("pipe_id") or l.get("pipe_code"))
        }
        recommendations = []
        now = datetime.now(timezone.utc)

        for pipe in pipes:
            pid = pipe["id"]
            pname = pipe.get("name", pipe.get("label", pid))
            health_score = pipe.get("health_score", 100.0)
            diameter = pipe.get("diameter_mm", 200.0)
            has_leak = pid in leak_map

            crit_mult = cls.get_criticality_multiplier(diameter)
            fail_prob = cls.calculate_failure_probability(health_score)

            leak_weight = 0.0
            if has_leak:
                sev = leak_map[pid].get("severity", "moderate")
                leak_weight = 40.0 if sev == "critical" else (25.0 if sev == "high" else 15.0)

            priority_score = round(
                (100.0 - health_score) * crit_mult + leak_weight, 1
            )

            # Assign priority label & recommended action
            if priority_score >= 110.0 or (has_leak and leak_map[pid].get("severity") == "critical"):
                priority = "urgent"
                action = "Emergency Pipe Replacement & Isolation"
                due_days = 1
                cost = 145000.0
                team = "PMC Quick Response Team (Emergency)"
            elif priority_score >= 75.0:
                priority = "high"
                action = "Acoustic Survey & Joint Clamp Collar Installation"
                due_days = 3
                cost = 62000.0
                team = "Central Zone Maintenance Crew"
            elif priority_score >= 45.0:
                priority = "medium"
                action = "Pressure Regulating Valve (PRV) Calibration & Flange Inspection"
                due_days = 7
                cost = 28000.0
                team = "DMA Leakage Detection Unit"
            else:
                priority = "routine"
                action = "Annual Ultrasonic Thickness Survey"
                due_days = 30
                cost = 12000.0
                team = "Preventive Maintenance Team"

            due_date = now + timedelta(days=due_days)

            recommendations.append(
                {
                    "pipe_id": pid,
                    "target_asset": pname,
                    "title": f"{action} — {pid}",
                    "priority": priority,
                    "priority_score": priority_score,
                    "failure_probability": fail_prob,
                    "recommended_action": action,
                    "estimated_cost_inr": cost,
                    "assigned_team": team,
                    "status": "open",
                    "due_date": due_date.isoformat(),
                    "has_active_leak": has_leak,
                }
            )

        # Sort descending by priority score
        recommendations.sort(key=lambda r: r["priority_score"], reverse=True)

        # Assign work order numbers
        for idx, rec in enumerate(recommendations, start=1):
            rec["id"] = f"wo-pune-{idx:03d}"
            rec["work_order_number"] = f"WO-2026-{idx:03d}"

        return recommendations
