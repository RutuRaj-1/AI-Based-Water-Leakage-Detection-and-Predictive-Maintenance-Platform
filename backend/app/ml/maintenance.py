"""
Maintenance prioritisation.

Turns asset health, failure risk and live leak alerts into ranked work-order
candidates. Priority score (0-100):

    0.40 * risk*100 + 0.30 * (100-health) + 0.20 * criticality*100 + 20 if leaking
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    asset_id: str
    asset_label: str
    kind: str            # emergency | rehab | inspection | corrosion | routine | pump
    title: str
    team: str
    priority_score: float
    zone: str


def priority_score(*, health: float, risk: float, criticality: float, leaking: bool) -> float:
    s = 0.40 * risk * 100 + 0.30 * (100 - health) + 0.20 * criticality * 100 + (20.0 if leaking else 0.0)
    return max(0.0, min(100.0, s))


def priority_label(score: float, *, emergency_critical: bool = False) -> str:
    if emergency_critical or score >= 85:
        return "urgent"
    if score >= 68:
        return "high"
    if score >= 50:
        return "medium"
    return "routine"


def diameter_criticality(diameter_mm: int) -> float:
    """Larger mains serve more customers, so failures matter more."""
    return min(diameter_mm / 500.0, 1.0)


def pipe_candidate_kind(*, health: float, risk: float, leaking: bool, corrosion: float) -> str | None:
    if leaking:
        return "emergency"
    if health < 40:
        return "rehab"
    if health < 60 or risk > 0.4:
        return "corrosion" if corrosion >= 0.7 else "inspection"
    if health < 72:
        return "routine"
    return None


KIND_TITLE = {
    "emergency": "Emergency acoustic survey & pipe joint clamp",
    "rehab": "Pipe rehabilitation & relining assessment",
    "inspection": "Ultrasonic pipe wall thickness diagnostic",
    "corrosion": "Cathodic protection & soil pH corrosion survey",
    "routine": "Routine valve exercise & leak-noise logging",
    "pump": "Pumping impeller dynamic balance test",
}
KIND_TEAM = {
    "rehab": "Asset Rehabilitation Team",
    "inspection": "Asset Inspection Team",
    "corrosion": "Corrosion Survey Unit",
    "routine": "South Maintenance Crew",
    "pump": "Electro-Mechanical Unit",
}


def team_for(kind: str, zone: str) -> str:
    if kind == "emergency":
        return f"Rapid Response Unit {1 + (sum(map(ord, zone)) % 3)}"
    return KIND_TEAM[kind]

