"""
FastAPI application factory.

This module creates and configures the FastAPI application instance.

Current state (Foundation / Stage 1):
  - CORS middleware configured
  - API v1 router mounted at /api/v1
  - Health endpoint available at /api/v1/health

Not yet implemented (Stage 2+):
  - Database connection pool (SQLAlchemy / asyncpg)
  - Startup/shutdown lifespan hooks for DB and ML services
  - Authentication middleware
  - Request logging middleware
  - Background task scheduler
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as api_v1_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "AI-Based Water Distribution Network Leakage Detection "
        "and Predictive Asset Management Platform for Pune Municipal Network.\n\n"
        "Features:\n"
        "- GeoJSON spatial feature endpoints for React-Leaflet maps (/gis/pipes, /gis/nodes, /gis/leaks)\n"
        "- WNTR / EPANET hydraulic simulation engine with 24-hour diurnal modeling\n"
        "- AI/ML Anomaly Detection (Residual Z-Score & Isolation Forest)\n"
        "- Composite 0-100 pipeline health scoring and failure risk predictions\n"
        "- Ranked maintenance work orders and real-time telemetry\n"
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ---------------------------------------------------------------------------
# CORS — allow the frontend dev server (and any configured origins) to call us
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(api_v1_router, prefix="/api/v1")


# ---------------------------------------------------------------------------
# Root redirect (informational)
# ---------------------------------------------------------------------------
@app.get("/", include_in_schema=False)
async def root() -> dict:
    return {
        "message": "Pune Water Network AI — Backend API",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/api/v1/health",
    }
