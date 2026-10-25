"""
Composite Pipeline Health Scoring Engine (0-100 Index).
Evaluates structural integrity based on material vulnerability, pipe age,
hydraulic pressure transients, and active anomaly incidents.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class HealthScorer:
    """Calculates multidimensional 0-100 health index for water pipeline segments."""

    MATERIAL_RISK_MAP = {
        "CI": 25.0,  # Cast Iron: high brittleness / graphitization
        "CAST IRON": 25.0,
        "MS": 15.0,  # Mild Steel: internal/external corrosion
        "MILD STEEL": 15.0,
        "PVC": 15.0,  # Polyvinyl Chloride: joint shear / UV degradation
        "DI": 8.0,   # Ductile Iron: modern corrosion lining
        "DUCTILE IRON": 8.0,
        "HDPE": 5.0, # High Density Polyethylene: flexible, corrosion proof
        "PSC": 5.0,  # Prestressed Concrete: robust heavy transmission
    }

    @classmethod
    def calculate_health_score(
        cls,
        pipe_dict: Dict[str, Any],
        active_anomalies_count: int = 0,
        pressure_variance: float = 0.5,
    ) -> Dict[str, Any]:
        """Computes comprehensive health score breakdown for a pipeline."""
        current_year = datetime.now(timezone.utc).year
        installed_year = pipe_dict.get("installation_year", 2005)
        age = max(0, current_year - installed_year)

        # 1. Material Risk (max 25 pts)
        material_str = str(pipe_dict.get("material", "DI")).upper()
        matched_material_risk = 10.0
        for mat_key, risk_val in cls.MATERIAL_RISK_MAP.items():
            if mat_key in material_str:
                matched_material_risk = risk_val
                break
        material_risk = min(25.0, matched_material_risk)

        # 2. Age Factor (max 30 pts)
        age_factor = min(30.0, round(age * 0.60, 1))

        # 3. Pressure Stress Factor (max 20 pts)
        # Higher diurnal pressure swings / water hammer increase fatigue
        pressure_stress = min(20.0, round(pressure_variance * 14.0, 1))

        # 4. Anomaly Penalty (max 25 pts)
        anomaly_penalty = min(25.0, float(active_anomalies_count * 15.0))

        # Composite calculation
        total_deduction = material_risk + age_factor + pressure_stress + anomaly_penalty
        health_score = round(max(0.0, min(100.0, 100.0 - total_deduction)), 1)

        # Determine condition category
        if health_score >= 80.0:
            condition = "healthy"
        elif health_score >= 65.0:
            condition = "monitor"
        elif health_score >= 50.0:
            condition = "attention"
        else:
            condition = "critical"

        return {
            "health_score": health_score,
            "condition": condition,
            "material_risk": material_risk,
            "age_factor": age_factor,
            "pressure_stress": pressure_stress,
            "anomaly_penalty": anomaly_penalty,
            "component_scores": {
                "material": 25.0 - material_risk,
                "age": 30.0 - age_factor,
                "hydraulics": 20.0 - pressure_stress,
                "integrity": 25.0 - anomaly_penalty,
            },
        }
