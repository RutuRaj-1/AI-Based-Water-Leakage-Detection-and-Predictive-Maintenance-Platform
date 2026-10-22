"""
API v1 router.
Aggregates all v1 endpoint routers into a single router mounted at /api/v1.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import health

router = APIRouter()

# Health check — implemented
router.include_router(health.router)

# Planned endpoint routers — add as implemented:
# from app.api.v1.endpoints import networks, pipes, simulations, observations
# from app.api.v1.endpoints import anomalies, health_assessments, predictions
# from app.api.v1.endpoints import maintenance, gis
# router.include_router(networks.router, prefix="/networks", tags=["Networks"])
# router.include_router(pipes.router, prefix="/pipes", tags=["Pipelines"])
# ...
