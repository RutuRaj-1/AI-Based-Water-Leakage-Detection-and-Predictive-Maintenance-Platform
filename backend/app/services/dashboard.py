"""Maps engine state onto API schemas (camelCase DTOs and GeoJSON)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.core.config import settings
from app.ml import health as health_ml
from app.schemas.dashboard import (
    ConditionCategory, CriticalAsset, DashboardSnapshot, EventOut, LeakAlert, MaintenanceTask,
    NetworkSummary, PipeDetail, PipeReading, SimulationStatus, SimulationTelemetry, TelemetryPoint,
)
from app.simulation import runtime
from app.simulation.engine import Alert, SimulationEngine, WorkOrder, humanize_age, interpolate
from app.simulation.network_data import SYNTHETIC_DATA_NOTICE

CONDITION_META = [
    ("healthy", "Healthy", "80–100 Score", "#16A34A"),
    ("monitor", "Monitor", "60–79 Score", "#D97706"),
    ("attention", "Attention", "40–59 Score", "#EA580C"),
    ("critical", "Critical", "0–39 Score", "#DC2626"),
]
PRIORITY_ORDER = {"urgent": 0, "high": 1, "medium": 2, "routine": 3}


def _alert_dto(engine: SimulationEngine, a: Alert) -> LeakAlert:
    return LeakAlert(
        id=a.id, title=a.title, location=a.location, pipeline_id=f"Pipe {a.pipe_id}",
        estimated_loss=f"~{a.est_loss_m3h:.1f} m³/hr" if a.est_loss_m3h < 10 else f"~{a.est_loss_m3h:.0f} m³/hr",
        severity=a.severity, timestamp=humanize_age(engine.sim_time - a.detected_at),
        status=a.status, detected_at=a.detected_at, estimated_loss_m3h=round(a.est_loss_m3h, 1),
        peak_score=round(a.peak_score, 1), auto_dispatched=a.auto_dispatched,
    )


def alerts(engine: SimulationEngine, *, status: str | None = None, severity: str | None = None,
           limit: int = 50) -> list[LeakAlert]:
    rank = {"critical": 0, "high": 1, "moderate": 2, "low": 3, "normal": 4}
    items = [a for a in engine.alerts if (status is None or a.status == status)
             and (severity is None or a.severity == severity)]
    # Open alerts first (by severity, newest first), then resolved (newest first).
    items.sort(key=lambda a: (a.status == "resolved", rank[a.severity], -a.detected_at.timestamp()))
    return [_alert_dto(engine, a) for a in items[:limit]]


def _wo_dto(w: WorkOrder) -> MaintenanceTask:
    return MaintenanceTask(
        id=w.id, work_order_number=w.number, title=w.title, target_asset=w.asset_label, priority=w.priority,
        priority_score=int(w.priority_score), assigned_team=w.team, due_date=w.due, status=w.status,
        kind=w.kind, asset_id=w.asset_id,
    )


def maintenance_tasks(engine: SimulationEngine, *, include_completed: bool = False) -> list[MaintenanceTask]:
    items = [w for w in engine.work_orders if include_completed or w.status != "completed"]
    items.sort(key=lambda w: (w.status == "completed", -w.priority_score, PRIORITY_ORDER[w.priority]))
    return [_wo_dto(w) for w in items]


def critical_assets(engine: SimulationEngine, limit: int = 8) -> list[CriticalAsset]:
    out: list[CriticalAsset] = []
    for ps in engine.pipes.values():
        if ps.health < 60:
            out.append(CriticalAsset(
                id=ps.spec.id, name=ps.spec.name, asset_type="pipe", health_score=round(ps.health),
                material=ps.spec.material, age_years=int(ps.spec.age_years),
                criticality=health_ml.criticality_label(ps.health), zone=ps.spec.zone,
                failure_risk=round(ps.risk, 3),
            ))
    for pump in engine.pumps.values():
        if pump.health < 60:
            out.append(CriticalAsset(
                id=pump.spec.id, name=pump.spec.name, asset_type="pump", health_score=round(pump.health),
                material=pump.spec.rating, age_years=int(pump.spec.age_years),
                criticality=health_ml.criticality_label(pump.health), zone=pump.spec.zone,
                failure_risk=round(health_ml.failure_risk(pump.health, active_leak=False), 3),
            ))
    out.sort(key=lambda a: a.health_score)
    return out[:limit]


def summary(engine: SimulationEngine) -> NetworkSummary:
    pipes = list(engine.pipes.values())
    total = sum(p.spec.length_km for p in pipes)
    cats = []
    for cid, label, rng, color in CONDITION_META:
        length = sum(p.spec.length_km for p in pipes if p.condition == cid)
        cats.append(ConditionCategory(id=cid, label=label, range=rng, percentage=round(length / total * 100, 1),
                                      length_km=round(length, 1), color=color))
    nodes = [n.spec for n in engine.nodes.values()]
    return NetworkSummary(
        total_length_km=round(total, 1), monitored_pipes=len(pipes),
        junctions=sum(1 for n in nodes if n.node_type == "junction"),
        pumping_stations=sum(1 for n in nodes if n.node_type == "pump"),
        reservoirs=sum(1 for n in nodes if n.node_type in ("reservoir", "treatment_plant")),
        zones=len({p.spec.zone for p in pipes}),
        average_health=round(sum(p.health * p.spec.length_km for p in pipes) / total, 1),
        condition_categories=cats,
    )


def telemetry(engine: SimulationEngine) -> SimulationTelemetry:
    pt = engine.telemetry_point()
    return SimulationTelemetry(
        scenario_name=engine.scenario_name,
        time_step=f"T+{engine.tick_count} · {engine.sim_time:%d %b %H:%M} UTC",
        engine_status="paused" if engine.paused else ("running" if runtime.is_running() else "standby"),
        mean_pressure_bar=pt["meanPressureBar"], total_flow_mld=pt["totalFlowMld"],
        estimated_loss_pct=pt["estimatedLossPct"], active_leaks_count=pt["activeLeaksCount"],
        total_monitored_pipes=len(engine.pipes), total_nodes=len(engine.nodes),
        network_health_score=pt["networkHealthScore"],
    )


def history(engine: SimulationEngine, limit: int = 60) -> list[TelemetryPoint]:
    return [TelemetryPoint(**p) for p in list(engine.telemetry_history)[-limit:]]


def events(engine: SimulationEngine, limit: int = 30) -> list[EventOut]:
    return [EventOut(id=e.id, time=e.time, level=e.level, kind=e.kind, message=e.message)
            for e in list(engine.events)[-limit:][::-1]]


def status(engine: SimulationEngine) -> SimulationStatus:
    return SimulationStatus(
        running=runtime.is_running(), paused=engine.paused, tick=engine.tick_count,
        simulation_time=engine.sim_time, minutes_per_tick=engine.minutes_per_tick,
        tick_seconds=settings.simulation_tick_seconds, auto_leaks=engine.auto_leaks,
        auto_dispatch=engine.auto_dispatch, auto_repair=engine.auto_repair,
        active_leaks=sum(1 for lk in engine.leaks if not lk.repaired),
    )


# ------------------------------------------------------------------- GeoJSON
def pipelines_geojson(engine: SimulationEngine) -> dict[str, Any]:
    feats = []
    for ps in engine.pipes.values():
        s = ps.spec
        feats.append({
            "type": "Feature", "id": s.id,
            "geometry": {"type": "LineString", "coordinates": [list(c) for c in s.coordinates]},
            "properties": {
                "id": s.id, "name": s.name, "zone": s.zone, "diameterMm": s.diameter_mm, "material": s.material,
                "healthScore": round(ps.health), "condition": ps.condition,
                "pressureBar": round(ps.pressure, 2), "flowRateMld": round(ps.flow, 1), "lengthKm": s.length_km,
            },
        })
    return {"type": "FeatureCollection", "features": feats}


def nodes_geojson(engine: SimulationEngine) -> dict[str, Any]:
    feats = []
    for ns in engine.nodes.values():
        s = ns.spec
        feats.append({
            "type": "Feature", "id": s.id,
            "geometry": {"type": "Point", "coordinates": list(s.coordinate)},
            "properties": {
                "id": s.id, "name": s.name, "nodeType": s.node_type, "zone": s.zone,
                "pressureBar": round(ns.pressure, 2), "elevationM": s.elevation_m, "baseDemandLps": s.base_demand_lps,
            },
        })
    return {"type": "FeatureCollection", "features": feats}


def leaks_geojson(engine: SimulationEngine) -> dict[str, Any]:
    feats = []
    for a in engine.alerts:
        if a.status == "resolved":
            continue
        spec = engine.pipes[a.pipe_id].spec
        lon, lat = interpolate(spec.coordinates, a.fraction)
        dto = _alert_dto(engine, a)
        feats.append({
            "type": "Feature", "id": a.id,
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {
                "id": a.id, "pipelineId": a.pipe_id, "severity": a.severity, "estimatedLoss": dto.estimated_loss,
                "location": a.location, "detectionTime": dto.timestamp, "status": a.status,
            },
        })
    return {"type": "FeatureCollection", "features": feats}


def snapshot(engine: SimulationEngine) -> DashboardSnapshot:
    return DashboardSnapshot(
        generated_at=datetime.now(timezone.utc), notice=SYNTHETIC_DATA_NOTICE, telemetry=telemetry(engine),
        summary=summary(engine), alerts=alerts(engine), critical_assets=critical_assets(engine),
        maintenance_tasks=maintenance_tasks(engine), pipelines=pipelines_geojson(engine),
        nodes=nodes_geojson(engine), leaks=leaks_geojson(engine), events=events(engine),
        history=history(engine), simulation=status(engine),
    )


def pipe_detail(engine: SimulationEngine, pipe_id: str) -> PipeDetail:
    ps = engine.pipes[pipe_id]
    s = ps.spec
    alert = engine.open_alert(pipe_id)
    return PipeDetail(
        id=s.id, name=s.name, zone=s.zone, material=s.material, diameter_mm=s.diameter_mm,
        age_years=int(s.age_years), length_km=s.length_km, health_score=round(ps.health), condition=ps.condition,
        failure_risk=round(ps.risk, 3), pressure_bar=round(ps.pressure, 2), flow_rate_mld=round(ps.flow, 1),
        anomaly_score=round(ps.score, 2), active_alert_id=alert.id if alert else None,
    )


def pipe_history(engine: SimulationEngine, pipe_id: str, limit: int) -> list[PipeReading]:
    return [PipeReading(time=r["time"], pressure_bar=round(r["pressureBar"], 3), flow_mld=round(r["flowMld"], 2),
                        anomaly_score=round(r["anomalyScore"], 2)) for r in engine.pipe_history(pipe_id, limit)]
