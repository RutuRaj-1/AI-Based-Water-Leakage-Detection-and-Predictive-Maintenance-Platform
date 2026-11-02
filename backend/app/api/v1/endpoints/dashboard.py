"""Dashboard + domain endpoints backed by the live simulation engine."""

from __future__ import annotations

import csv
import io
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response

from app.core.security import require_api_key
from app.schemas import dashboard as s
from app.services import dashboard as svc
from app.simulation import runtime
from app.simulation.engine import SimulationEngine

router = APIRouter()
Engine = Depends(runtime.get_engine)
Protected = [Depends(require_api_key)]


# ---------------------------------------------------------------- dashboard
@router.get("/dashboard/snapshot", response_model=s.DashboardSnapshot, tags=["Dashboard"],
            summary="Everything the dashboard needs in one request")
async def snapshot(engine: SimulationEngine = Engine) -> s.DashboardSnapshot:
    return svc.snapshot(engine)


@router.get("/telemetry", response_model=s.SimulationTelemetry, tags=["Dashboard"])
async def telemetry(engine: SimulationEngine = Engine) -> s.SimulationTelemetry:
    return svc.telemetry(engine)


@router.get("/telemetry/history", response_model=list[s.TelemetryPoint], tags=["Dashboard"])
async def telemetry_history(limit: int = Query(60, ge=1, le=240), engine: SimulationEngine = Engine):
    return svc.history(engine, limit)


@router.get("/events", response_model=list[s.EventOut], tags=["Dashboard"], summary="Automation activity log")
async def events(limit: int = Query(30, ge=1, le=120), engine: SimulationEngine = Engine):
    return svc.events(engine, limit)


@router.get("/gis/network", tags=["GIS"], summary="Pipelines, nodes and leak markers as GeoJSON")
async def gis_network(engine: SimulationEngine = Engine) -> dict:
    return {"pipelines": svc.pipelines_geojson(engine), "nodes": svc.nodes_geojson(engine),
            "leaks": svc.leaks_geojson(engine)}


# ------------------------------------------------------------------- alerts
@router.get("/alerts", response_model=list[s.LeakAlert], tags=["Alerts"])
async def list_alerts(status: s.AlertStatus | None = None, severity: s.Severity | None = None,
                      limit: int = Query(50, ge=1, le=200), engine: SimulationEngine = Engine):
    return svc.alerts(engine, status=status, severity=severity, limit=limit)


@router.patch("/alerts/{alert_id}", response_model=s.LeakAlert, tags=["Alerts"], dependencies=Protected)
async def patch_alert(alert_id: str, body: s.AlertPatch, engine: SimulationEngine = Engine):
    try:
        alert = engine.set_alert_status(alert_id, body.status)
    except KeyError:
        raise HTTPException(404, f"Alert {alert_id} not found") from None
    return svc._alert_dto(engine, alert)


@router.get("/reports/alerts.csv", tags=["Reports"], summary="Export alerts as CSV")
async def alerts_csv(engine: SimulationEngine = Engine) -> Response:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["id", "pipeline", "severity", "status", "title", "location", "detected_at", "est_loss_m3h"])
    for a in engine.alerts:
        w.writerow([a.id, a.pipe_id, a.severity, a.status, a.title, a.location, a.detected_at.isoformat(),
                    round(a.est_loss_m3h, 1)])
    return Response(buf.getvalue(), media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=alerts.csv"})


# ------------------------------------------------------------ assets / pipes
@router.get("/assets/critical", response_model=list[s.CriticalAsset], tags=["Assets"])
async def critical_assets(limit: int = Query(8, ge=1, le=50), engine: SimulationEngine = Engine):
    return svc.critical_assets(engine, limit)


@router.get("/network/summary", response_model=s.NetworkSummary, tags=["Assets"])
async def network_summary(engine: SimulationEngine = Engine):
    return svc.summary(engine)


@router.get("/pipes", response_model=list[s.PipeDetail], tags=["Assets"])
async def list_pipes(engine: SimulationEngine = Engine):
    return [svc.pipe_detail(engine, pid) for pid in engine.pipes]


@router.get("/pipes/{pipe_id}", response_model=s.PipeDetail, tags=["Assets"])
async def get_pipe(pipe_id: str, engine: SimulationEngine = Engine):
    if pipe_id not in engine.pipes:
        raise HTTPException(404, f"Pipe {pipe_id} not found")
    return svc.pipe_detail(engine, pipe_id)


@router.get("/pipes/{pipe_id}/history", response_model=list[s.PipeReading], tags=["Assets"])
async def pipe_history(pipe_id: str, limit: int = Query(96, ge=1, le=288), engine: SimulationEngine = Engine):
    if pipe_id not in engine.pipes:
        raise HTTPException(404, f"Pipe {pipe_id} not found")
    return svc.pipe_history(engine, pipe_id, limit)


# -------------------------------------------------------------- maintenance
@router.get("/maintenance/tasks", response_model=list[s.MaintenanceTask], tags=["Maintenance"])
async def list_tasks(include_completed: bool = False, engine: SimulationEngine = Engine):
    return svc.maintenance_tasks(engine, include_completed=include_completed)


@router.patch("/maintenance/tasks/{task_id}", response_model=s.MaintenanceTask, tags=["Maintenance"],
              dependencies=Protected)
async def patch_task(task_id: str, body: s.WorkOrderPatch, engine: SimulationEngine = Engine):
    try:
        wo = engine.set_work_order_status(task_id, body.status)
    except KeyError:
        raise HTTPException(404, f"Work order {task_id} not found") from None
    return svc._wo_dto(wo)


# --------------------------------------------------------------- simulation
@router.get("/simulation/status", response_model=s.SimulationStatus, tags=["Simulation"])
async def sim_status(engine: SimulationEngine = Engine):
    return svc.status(engine)


@router.post("/simulation/step", response_model=s.SimulationStatus, tags=["Simulation"], dependencies=Protected,
             summary="Advance the simulation by N ticks (useful while paused)")
async def sim_step(body: s.StepRequest, engine: SimulationEngine = Engine):
    for _ in range(body.ticks):
        engine.tick()
    return svc.status(engine)


@router.post("/simulation/leaks", tags=["Simulation"], dependencies=Protected,
             summary="Inject a leak scenario on a pipe")
async def inject_leak(body: s.LeakInject, engine: SimulationEngine = Engine) -> dict:
    try:
        lk = engine.inject_leak(body.pipe_id, body.rate_m3h, body.fraction, source="manual")
    except KeyError:
        raise HTTPException(404, f"Pipe {body.pipe_id} not found") from None
    return {"leakId": lk.id, "pipeId": lk.pipe_id, "rateM3h": lk.rate_m3h}


@router.post("/simulation/{action}", response_model=s.SimulationStatus, tags=["Simulation"], dependencies=Protected)
async def sim_control(action: Literal["pause", "resume", "reset"], engine: SimulationEngine = Engine):
    if action == "pause":
        engine.paused = True
    elif action == "resume":
        engine.paused = False
    else:
        engine.reset()
    return svc.status(engine)
