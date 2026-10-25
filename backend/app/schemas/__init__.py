"""
Pydantic Schemas Package.
"""

from app.schemas.common import Pagination, PaginatedResponse, ErrorResponse, ErrorDetail
from app.schemas.network import NetworkBase, NetworkResponse
from app.schemas.pipe import PipeBase, PipeCreate, PipeResponse, PipeDetailResponse
from app.schemas.gis import (
    GeoJSONGeometry,
    PipelineProperties,
    NetworkNodeProperties,
    LeakMarkerProperties,
    GeoJSONFeature,
    GeoJSONFeatureCollection,
)
from app.schemas.anomaly import AnomalyBase, AnomalyCreate, AnomalyResponse, LeakAlert
from app.schemas.maintenance import (
    MaintenanceBase,
    MaintenanceCreate,
    MaintenanceUpdate,
    MaintenanceResponse,
    MaintenanceTaskFrontend,
)
from app.schemas.simulation import (
    SimulationRunRequest,
    SimulationRunResponse,
    SimulationTelemetry,
)
from app.schemas.observation import ObservationResponse, TimeSeriesPoint
from app.schemas.health import HealthAssessmentResponse, RiskPredictionResponse

__all__ = [
    "Pagination",
    "PaginatedResponse",
    "ErrorResponse",
    "ErrorDetail",
    "NetworkBase",
    "NetworkResponse",
    "PipeBase",
    "PipeCreate",
    "PipeResponse",
    "PipeDetailResponse",
    "GeoJSONGeometry",
    "PipelineProperties",
    "NetworkNodeProperties",
    "LeakMarkerProperties",
    "GeoJSONFeature",
    "GeoJSONFeatureCollection",
    "AnomalyBase",
    "AnomalyCreate",
    "AnomalyResponse",
    "LeakAlert",
    "MaintenanceBase",
    "MaintenanceCreate",
    "MaintenanceUpdate",
    "MaintenanceResponse",
    "MaintenanceTaskFrontend",
    "SimulationRunRequest",
    "SimulationRunResponse",
    "SimulationTelemetry",
    "ObservationResponse",
    "TimeSeriesPoint",
    "HealthAssessmentResponse",
    "RiskPredictionResponse",
]
