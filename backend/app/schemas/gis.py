"""
GeoJSON Pydantic Schemas complying with RFC 7946 and frontend Leaflet map layer formats.
"""

from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field


class GeoJSONGeometry(BaseModel):
    type: Literal["Point", "LineString", "Polygon", "MultiLineString"]
    coordinates: Union[List[float], List[List[float]], List[List[List[float]]]]


class PipelineProperties(BaseModel):
    id: str
    name: str
    zone: str
    diameterMm: float
    material: str
    healthScore: float
    condition: Literal["healthy", "monitor", "attention", "critical"]
    pressureBar: float
    flowRateMld: float
    lengthKm: float


class NetworkNodeProperties(BaseModel):
    id: str
    name: str
    nodeType: Literal["reservoir", "pump", "junction", "treatment_plant"]
    zone: str
    pressureBar: float
    elevationM: float
    baseDemandLps: Optional[float] = 0.0


class LeakMarkerProperties(BaseModel):
    id: str
    pipelineId: str
    severity: Literal["critical", "high", "moderate", "low", "normal"]
    estimatedLoss: str
    location: str
    detectionTime: str
    status: Literal["active", "investigating", "resolved"]


class GeoJSONFeature(BaseModel):
    type: Literal["Feature"] = "Feature"
    id: Optional[str] = None
    geometry: GeoJSONGeometry
    properties: Dict[str, Any]


class GeoJSONFeatureCollection(BaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: List[GeoJSONFeature]
