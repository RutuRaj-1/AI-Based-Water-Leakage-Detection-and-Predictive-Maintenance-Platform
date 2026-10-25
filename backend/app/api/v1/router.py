"""
API v1 Router.
Aggregates all v1 endpoint routers into a single router mounted at /api/v1.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    health,
    gis,
    networks,
    pipes,
    observations,
    anomalies,
    health_assessments,
    predictions,
    maintenance,
    simulations,
)

router = APIRouter()

# Health check
router.include_router(health.router)

# Geospatial endpoints (Leaflet maps)
router.include_router(gis.router)

# Networks & DMAs
router.include_router(networks.router)

# Pipelines & Asset details
router.include_router(pipes.router)

# Sensor time-series telemetry observations
router.include_router(observations.router)

# Anomaly detection & leak alerts
router.include_router(anomalies.router)

# Pipeline health assessments (0-100 score)
router.include_router(health_assessments.router)

# Risk predictions & failure probabilities
router.include_router(predictions.router)

# Prioritised maintenance work orders
router.include_router(maintenance.router)

# Hydraulic simulations & real-time telemetry
router.include_router(simulations.router)
