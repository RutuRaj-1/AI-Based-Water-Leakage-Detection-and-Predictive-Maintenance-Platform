"""
FastAPI application factory.

Configures the FastAPI application instance:
  - CORS middleware (frontend dev server + configured origins)
  - Request logging / timing middleware
  - API v1 router mounted at /api/v1
  - Lifespan hook that starts the live simulation + automation heartbeat

The simulation engine is in-memory (see app.simulation). The SQLAlchemy models
and Alembic migration under app.db / migrations are the persistence target for
the next stage.
"""

import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as api_v1_router
from app.core.config import settings
from app.simulation import runtime

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-7s %(name)s: %(message)s")
log = logging.getLogger("pune_water.api")


@asynccontextmanager
async def lifespan(_: FastAPI):
    runtime.get_engine()  # build + calibrate once at startup
    if settings.simulation_autostart:
        runtime.start_ticker()
    yield
    await runtime.stop_ticker()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "AI-Based Water Distribution Network Leakage Detection "
        "and Predictive Asset Management Platform.\n\n"
        "Live simulation engine -> anomaly detection -> alerts -> health scoring -> "
        "predictive maintenance work orders, with automated escalation, dispatch and repair.\n\n"
        "**All data is synthetic.**"
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
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


class TimingMiddleware:
    """Pure-ASGI request timing/logging middleware (adds X-Process-Time-ms)."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        start = time.perf_counter()
        status_holder = {"code": 0}

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                ms = (time.perf_counter() - start) * 1000
                status_holder["code"] = message["status"]
                message.setdefault("headers", []).append((b"x-process-time-ms", f"{ms:.1f}".encode()))
            await send(message)

        await self.app(scope, receive, send_wrapper)
        if scope["method"] != "GET" or status_holder["code"] >= 400:
            log.info("%s %s -> %s (%.1fms)", scope["method"], scope["path"], status_holder["code"],
                     (time.perf_counter() - start) * 1000)


app.add_middleware(TimingMiddleware)


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(api_v1_router, prefix="/api/v1")


# ---------------------------------------------------------------------------
# Root (informational)
# ---------------------------------------------------------------------------
@app.get("/", include_in_schema=False)
async def root() -> dict:
    return {
        "message": "Pune Water Network AI — Backend API",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/api/v1/health",
        "snapshot": "/api/v1/dashboard/snapshot",
    }
