"""
Simulation Scenarios and Diurnal Demand Models for Pune Water Network.
"""

from typing import Any, Dict, List
import numpy as np


class DiurnalPattern:
    """Calculates diurnal demand multipliers across 24 hours of Pune diurnal cycle."""

    @staticmethod
    def get_multiplier(hour: float) -> float:
        h = float(hour) % 24.0
        if 0.0 <= h < 5.0:
            # Low night flow: 0.3x
            return 0.30 + 0.05 * np.sin((h / 5.0) * np.pi)
        elif 5.0 <= h < 9.5:
            # Morning peak: 1.8x around 7:30 AM
            t = (h - 5.0) / 4.5
            return 0.70 + 1.10 * np.sin(t * np.pi)
        elif 9.5 <= h < 17.5:
            # Afternoon steady: 0.9x
            return 0.88 + 0.06 * np.cos(((h - 9.5) / 8.0) * np.pi)
        elif 17.5 <= h < 21.5:
            # Evening peak: 1.5x around 19:30 PM
            t = (h - 17.5) / 4.0
            return 0.90 + 0.60 * np.sin(t * np.pi)
        else:
            # Night decay: 0.6x down to 0.35x
            t = (h - 21.5) / 2.5
            return 0.65 - 0.30 * t


class ScenarioManager:
    """Manages hydraulic simulation scenario configurations and injections."""

    @staticmethod
    def get_available_scenarios() -> List[Dict[str, Any]]:
        return [
            {
                "id": "normal",
                "name": "Normal Diurnal Operation",
                "description": "Standard 24-hour cycle following Pune municipal consumption curves without abnormal pipe failures.",
                "severity": "normal",
            },
            {
                "id": "pipe_burst",
                "name": "Major Pipe Burst (Katraj Feeder P-104)",
                "description": "Sudden structural rupture on 300mm Cast Iron trunk with 40-50 kPa pressure plunge and local flow surge.",
                "severity": "critical",
            },
            {
                "id": "slow_leak",
                "name": "Background Joint Leak (Kothrud P-211)",
                "description": "Developing gasket degradation resulting in subtle 10-15% pressure attenuation and elevated minimum night flow.",
                "severity": "moderate",
            },
            {
                "id": "demand_surge",
                "name": "Severe Morning Demand Surge",
                "description": "Abnormal 2.4x peak extraction during summer heatwave testing pump limits.",
                "severity": "high",
            },
            {
                "id": "blockage",
                "name": "Partial Valve Blockage",
                "description": "Silt build-up or partially shut sluice valve causing upstream head rise and downstream starvation.",
                "severity": "high",
            },
        ]
