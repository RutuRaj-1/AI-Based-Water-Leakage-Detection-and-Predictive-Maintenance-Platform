"""
Anomaly and Leak Alerts Repository.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from app.simulation.network_builder import PuneNetworkBuilder


class AnomalyRepository:
    def __init__(self):
        self._anomalies: Dict[str, Dict[str, Any]] = {}
        # Pre-populate with baseline synthetic leaks
        for leak in PuneNetworkBuilder.get_leaks():
            aid = leak["id"]
            self._anomalies[aid] = {
                "id": aid,
                "pipe_id": leak["pipeline_id"],
                "pipe_code": leak["pipeline_id"],
                "title": f"Leak Detected: {leak['location']}",
                "location": leak["location"],
                "anomaly_type": leak.get("anomaly_type", "pipe_burst"),
                "severity": leak["severity"],
                "confidence": leak.get("confidence", 0.90),
                "estimated_loss": leak["estimated_loss"],
                "status": leak.get("status", "active"),
                "detected_at": datetime.now(timezone.utc).isoformat(),
                "coordinates": leak.get("coordinates", [73.8550, 18.4650]),
                "details": {
                    "detectionTime": leak.get("detection_time", "15m ago"),
                },
            }

    def list_anomalies(
        self,
        active: Optional[bool] = None,
        severity: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> Dict[str, Any]:
        items = list(self._anomalies.values())
        if active is not None:
            if active:
                items = [a for a in items if a.get("status") in ["active", "investigating"]]
            else:
                items = [a for a in items if a.get("status") == "resolved"]
        if severity:
            items = [a for a in items if a.get("severity") == severity]

        total = len(items)
        start = (page - 1) * page_size
        paginated_items = items[start : start + page_size]

        return {
            "items": paginated_items,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_items": total,
                "total_pages": max(1, (total + page_size - 1) // page_size),
            },
        }

    def get_anomaly(self, anomaly_id: str) -> Optional[Dict[str, Any]]:
        return self._anomalies.get(anomaly_id)

    def update_status(self, anomaly_id: str, status: str) -> Optional[Dict[str, Any]]:
        anomaly = self._anomalies.get(anomaly_id)
        if anomaly:
            anomaly["status"] = status
            return anomaly
        return None

    def add_anomaly(self, anomaly_data: Dict[str, Any]) -> Dict[str, Any]:
        aid = anomaly_data.get("id") or f"ALT-{len(self._anomalies) + 101}"
        anomaly_data["id"] = aid
        if "detected_at" not in anomaly_data:
            anomaly_data["detected_at"] = datetime.now(timezone.utc).isoformat()
        self._anomalies[aid] = anomaly_data
        return anomaly_data

    def get_leaks_geojson(self) -> Dict[str, Any]:
        """Returns GeoJSON FeatureCollection of active leak markers for Leaflet map."""
        features = []
        for a in self._anomalies.values():
            features.append(
                {
                    "type": "Feature",
                    "id": a["id"],
                    "geometry": {
                        "type": "Point",
                        "coordinates": a.get("coordinates", [73.8550, 18.4650]),
                    },
                    "properties": {
                        "id": a["id"],
                        "pipelineId": a.get("pipe_id", a.get("pipe_code", "P-104")),
                        "severity": a.get("severity", "moderate"),
                        "estimatedLoss": a.get("estimated_loss", "~25 m³/hr"),
                        "location": a.get("location", "Pune"),
                        "detectionTime": a.get("details", {}).get("detectionTime", "Recently"),
                        "status": a.get("status", "active"),
                    },
                }
            )
        return {
            "type": "FeatureCollection",
            "features": features,
        }
