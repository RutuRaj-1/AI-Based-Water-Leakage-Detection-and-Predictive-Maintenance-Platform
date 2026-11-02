"""
API v1 router.
Aggregates all v1 endpoint routers into a single router mounted at /api/v1.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import dashboard, health

router = APIRouter()

router.include_router(health.router)
router.include_router(dashboard.router)
