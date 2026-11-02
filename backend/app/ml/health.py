"""
Pipeline health scoring, condition banding and failure-risk estimation.

Health score (0-100, higher is better) is a transparent additive penalty model:

    100
    - 45 * min(age / design_life, 1.2)     ageing
    - 30 * corrosion_index                  material degradation
    - active-leak penalty (by severity)     current fault
    - 3  * min(leak_history, 5)             recurring failures
    + refurbishment credit                  completed maintenance

Failure risk is the logistic probability of a failure within a 30-day horizon.
"""

from __future__ import annotations

import math

from app.simulation.network_data import MATERIAL_LIFESPAN_YEARS, PipeSpec

LEAK_PENALTY = {"critical": 22.0, "high": 15.0, "moderate": 9.0, "low": 4.0}


def condition_for(score: float) -> str:
    if score >= 80:
        return "healthy"
    if score >= 60:
        return "monitor"
    if score >= 40:
        return "attention"
    return "critical"


def pipe_health(spec: PipeSpec, *, active_leak_severity: str | None, leak_history: int,
                refurb_bonus: float) -> float:
    life = MATERIAL_LIFESPAN_YEARS[spec.material_class]
    score = 100.0
    score -= 45.0 * min(spec.age_years / life, 1.2)
    score -= 30.0 * spec.corrosion_index
    if active_leak_severity:
        score -= LEAK_PENALTY.get(active_leak_severity, 0.0)
    score -= 3.0 * min(leak_history, 5)
    score += refurb_bonus
    return max(0.0, min(100.0, score))


def failure_risk(health: float, *, active_leak: bool) -> float:
    """Probability (0-1) of failure in the next 30 days."""
    x = 0.06 * (100.0 - health) - 3.2 + (1.2 if active_leak else 0.0)
    return 1.0 / (1.0 + math.exp(-x))


def criticality_label(health: float) -> str:
    if health < 35:
        return "urgent"
    if health < 50:
        return "high"
    return "medium"


def pump_health(base_health: float, wear_index: float, ticks: int) -> float:
    """Slow mechanical wear: loses ~0.5 points per 1000 ticks, scaled by wear."""
    return max(0.0, base_health - 0.5 * wear_index * (ticks / 1000.0))

