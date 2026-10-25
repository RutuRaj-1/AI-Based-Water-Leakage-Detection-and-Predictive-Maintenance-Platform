"""
Unit tests for AI/ML anomaly detection, composite health scoring, and risk prediction.
"""

import pytest
from app.ml.health_scorer import HealthScorer
from app.ml.risk_predictor import RiskPredictor
from app.ml.anomaly_detector import LeakAnomalyDetector


def test_health_scorer_new_pipe():
    # Modern ductile iron pipe installed in 2024
    pipe = {
        "material": "Ductile Iron (DI)",
        "installation_year": 2024,
    }
    score_data = HealthScorer.calculate_health_score(pipe, active_anomalies_count=0)
    assert score_data["health_score"] >= 80.0
    assert score_data["condition"] == "healthy"


def test_health_scorer_old_cast_iron_with_leak():
    # 1980s Cast Iron pipe with an active leak
    pipe = {
        "material": "Cast Iron (CI)",
        "installation_year": 1985,
    }
    score_data = HealthScorer.calculate_health_score(pipe, active_anomalies_count=1)
    assert score_data["health_score"] < 50.0
    assert score_data["condition"] == "critical"
    assert score_data["material_risk"] == 25.0


def test_risk_predictor_failure_probability():
    # Healthy pipe should have low failure probability
    p_healthy = RiskPredictor.calculate_failure_probability(95.0)
    assert p_healthy < 0.20

    # Critical pipe should have high failure probability
    p_critical = RiskPredictor.calculate_failure_probability(25.0)
    assert p_critical > 0.70


def test_anomaly_detector_flags_burst():
    detector = LeakAnomalyDetector()
    readings = [
        {"pressure_bar": 3.5, "flow_mld": 15.0, "expected_pressure_bar": 3.5},
        {"pressure_bar": 3.5, "flow_mld": 15.1, "expected_pressure_bar": 3.5},
        {"pressure_bar": 3.4, "flow_mld": 15.0, "expected_pressure_bar": 3.5},
        # Sudden burst drop:
        {"pressure_bar": 1.8, "flow_mld": 24.0, "expected_pressure_bar": 3.5, "is_anomaly": True},
        {"pressure_bar": 1.7, "flow_mld": 24.2, "expected_pressure_bar": 3.5, "is_anomaly": True},
    ]

    anomalies = detector.detect_anomalies("P-TEST", readings)
    assert len(anomalies) >= 1
    assert anomalies[0]["severity"] in ["critical", "high"]
