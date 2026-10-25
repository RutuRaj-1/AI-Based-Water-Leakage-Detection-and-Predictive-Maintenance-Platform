"""
Pipeline Repository with GeoJSON FeatureCollection formatting.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from app.simulation.network_builder import PuneNetworkBuilder
from app.ml.health_scorer import HealthScorer
from app.ml.risk_predictor import RiskPredictor


class PipeRepository:
    def __init__(self):
        self._pipes = {p["id"]: dict(p) for p in PuneNetworkBuilder.get_pipes()}
        self._nodes = {n["id"]: dict(n) for n in PuneNetworkBuilder.get_nodes()}

    def list_pipes(
        self,
        zone: Optional[str] = None,
        condition: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> Dict[str, Any]:
        filtered = list(self._pipes.values())
        if zone:
            filtered = [p for p in filtered if zone.lower() in p.get("zone", "").lower()]
        if condition:
            filtered = [p for p in filtered if p.get("condition") == condition]

        total = len(filtered)
        start = (page - 1) * page_size
        items = filtered[start : start + page_size]

        # Format items to match API specification
        formatted_items = []
        for p in items:
            formatted_items.append(
                {
                    "id": p["id"],
                    "network_id": "c8a41280-9281-4f10-91b4-21950e436001",
                    "label": p.get("name", p["id"]),
                    "code": p.get("code", p["id"]),
                    "zone": p.get("zone", "Pune"),
                    "length_m": round(p.get("length_km", 1.0) * 1000.0, 1),
                    "diameter_mm": p.get("diameter_mm", 250.0),
                    "material": p.get("material", "DI"),
                    "roughness": 130.0,
                    "installation_year": p.get("installation_year", 2005),
                    "current_health_score": p.get("health_score", 100.0),
                    "latest_health_score": p.get("health_score", 100.0),
                    "condition": p.get("condition", "healthy"),
                    "pressure_bar": p.get("pressure_bar", 3.5),
                    "flow_rate_mld": p.get("flow_rate_mld", 10.0),
                    "coordinates": p.get("coordinates", []),
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

    def get_pipe(self, pipe_id: str) -> Optional[Dict[str, Any]]:
        pipe = self._pipes.get(pipe_id)
        if not pipe:
            for p in self._pipes.values():
                if p.get("code") == pipe_id:
                    pipe = p
                    break
        if not pipe:
            return None

        current_year = datetime.now(timezone.utc).year
        age = current_year - pipe.get("installation_year", 2005)
        health_score = pipe.get("health_score", 100.0)
        diameter = pipe.get("diameter_mm", 250.0)

        fail_prob = RiskPredictor.calculate_failure_probability(health_score)
        crit_mult = RiskPredictor.get_criticality_multiplier(diameter)
        criticality = "urgent" if crit_mult >= 1.4 else ("high" if crit_mult >= 1.1 else "medium")

        return {
            "id": pipe["id"],
            "network_id": "c8a41280-9281-4f10-91b4-21950e436001",
            "label": pipe.get("name", pipe["id"]),
            "code": pipe.get("code", pipe["id"]),
            "zone": pipe.get("zone", "Pune"),
            "length_m": round(pipe.get("length_km", 1.0) * 1000.0, 1),
            "diameter_mm": diameter,
            "material": pipe.get("material", "DI"),
            "roughness": 130.0,
            "installation_year": pipe.get("installation_year", 2005),
            "current_health_score": health_score,
            "latest_health_score": health_score,
            "condition": pipe.get("condition", "healthy"),
            "pressure_bar": pipe.get("pressure_bar", 3.5),
            "flow_rate_mld": pipe.get("flow_rate_mld", 10.0),
            "coordinates": pipe.get("coordinates", []),
            "age_years": age,
            "failure_probability": fail_prob,
            "criticality": criticality,
            "active_anomalies_count": 1 if health_score < 50.0 else 0,
        }

    def get_pipes_geojson(self) -> Dict[str, Any]:
        """Returns GeoJSON FeatureCollection formatted for React-Leaflet GeoJSON layer."""
        features = []
        for p in self._pipes.values():
            features.append(
                {
                    "type": "Feature",
                    "id": p["id"],
                    "geometry": {
                        "type": "LineString",
                        "coordinates": p.get("coordinates", []),
                    },
                    "properties": {
                        "id": p["id"],
                        "name": p.get("name", p["id"]),
                        "zone": p.get("zone", "Pune"),
                        "diameterMm": p.get("diameter_mm", 250.0),
                        "material": p.get("material", "DI"),
                        "healthScore": p.get("health_score", 100.0),
                        "condition": p.get("condition", "healthy"),
                        "pressureBar": p.get("pressure_bar", 3.5),
                        "flowRateMld": p.get("flow_rate_mld", 10.0),
                        "lengthKm": p.get("length_km", 1.0),
                    },
                }
            )
        return {
            "type": "FeatureCollection",
            "features": features,
        }

    def get_nodes_geojson(self) -> Dict[str, Any]:
        """Returns GeoJSON FeatureCollection of network junctions, pumps, and reservoirs."""
        features = []
        for n in self._nodes.values():
            features.append(
                {
                    "type": "Feature",
                    "id": n["id"],
                    "geometry": {
                        "type": "Point",
                        "coordinates": n.get("coordinates", [73.8567, 18.5204]),
                    },
                    "properties": {
                        "id": n["id"],
                        "name": n.get("name", n["id"]),
                        "nodeType": n.get("node_type", "junction"),
                        "zone": n.get("zone", "Pune Central"),
                        "pressureBar": n.get("pressure_bar", 3.5),
                        "elevationM": n.get("elevation_m", 560.0),
                        "baseDemandLps": n.get("base_demand_lps", 0.0),
                    },
                }
            )
        return {
            "type": "FeatureCollection",
            "features": features,
        }

    def update_pipe_health(self, pipe_id: str, new_score: float, condition: str) -> None:
        if pipe_id in self._pipes:
            self._pipes[pipe_id]["health_score"] = new_score
            self._pipes[pipe_id]["condition"] = condition
