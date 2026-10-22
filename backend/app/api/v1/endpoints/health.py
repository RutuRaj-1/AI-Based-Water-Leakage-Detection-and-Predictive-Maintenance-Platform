"""
Health check endpoint.

Returns the operational status of the backend service.

Important: This endpoint only confirms the FastAPI application is running.
It does NOT verify database connectivity, ML model availability, or
simulation engine readiness — those checks will be added when the
corresponding services are implemented.
"""

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import settings

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Service health check",
    description=(
        "Returns the current status of the backend service. "
        "Only confirms the API is running — does not check the database, "
        "simulation engine, or ML models."
    ),
    tags=["Health"],
)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="ok",
        version=settings.app_version,
        environment=settings.environment,
    )
