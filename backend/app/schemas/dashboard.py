"""Pydantic schemas for the dashboard API. JSON keys are camelCase to match the frontend."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

Severity = Literal["critical", "high", "moderate", "low", "normal"]
AlertStatus = Literal["active", "investigating", "resolved"]
Priority = Literal["urgent", "high", "medium", "routine"]
WorkOrderStatus = Literal["open", "in_progress", "completed"]


class CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class LeakAlert(CamelModel):
    id: str
    title: str
    location: str
    pipeline_id: str
    estimated_loss: str
    severity: Severity
    timestamp: str
    status: AlertStatus
    detected_at: datetime
    estimated_loss_m3h: float
    peak_score: float
    auto_dispatched: bool = False


class CriticalAsset(CamelModel):
    id: str
    name: str
    asset_type: Literal["pipe", "junction", "pump", "reservoir"]
    health_score: int
    material: str
    age_years: int
    criticality: Literal["urgent", "high", "medium"]
    zone: str
    failure_risk: float = Field(description="Probability of failure within 30 days (0-1)")


class MaintenanceTask(CamelModel):
    id: str
    work_order_number: str
    title: str
    target_asset: str
    priority: Priority
    priority_score: int
    assigned_team: str
    due_date: str
    status: WorkOrderStatus
    kind: str
    asset_id: str


class SimulationTelemetry(CamelModel):
    scenario_name: str
    time_step: str
    engine_status: Literal["running", "paused", "standby"]
    mean_pressure_bar: float
    total_flow_mld: float
    estimated_loss_pct: float
    active_leaks_count: int
    total_monitored_pipes: int
    total_nodes: int
    network_health_score: float


class ConditionCategory(CamelModel):
    id: str
    label: str
    range: str
    percentage: float
    length_km: float
    color: str


class NetworkSummary(CamelModel):
    total_length_km: float
    monitored_pipes: int
    junctions: int
    pumping_stations: int
    reservoirs: int
    zones: int
    average_health: float
    condition_categories: list[ConditionCategory]


class TelemetryPoint(CamelModel):
    time: datetime
    mean_pressure_bar: float
    total_flow_mld: float
    estimated_loss_pct: float
    active_leaks_count: int
    network_health_score: float


class EventOut(CamelModel):
    id: int
    time: datetime
    level: Literal["info", "warning", "critical", "success"]
    kind: str
    message: str


class SimulationStatus(CamelModel):
    running: bool
    paused: bool
    tick: int
    simulation_time: datetime
    minutes_per_tick: int
    tick_seconds: float
    auto_leaks: bool
    auto_dispatch: bool
    auto_repair: bool
    active_leaks: int


class DashboardSnapshot(CamelModel):
    generated_at: datetime
    notice: str
    telemetry: SimulationTelemetry
    summary: NetworkSummary
    alerts: list[LeakAlert]
    critical_assets: list[CriticalAsset]
    maintenance_tasks: list[MaintenanceTask]
    pipelines: dict[str, Any]
    nodes: dict[str, Any]
    leaks: dict[str, Any]
    events: list[EventOut]
    history: list[TelemetryPoint]
    simulation: SimulationStatus


class PipeDetail(CamelModel):
    id: str
    name: str
    zone: str
    material: str
    diameter_mm: int
    age_years: int
    length_km: float
    health_score: int
    condition: str
    failure_risk: float
    pressure_bar: float
    flow_rate_mld: float
    anomaly_score: float
    active_alert_id: str | None = None


class PipeReading(CamelModel):
    time: datetime
    pressure_bar: float
    flow_mld: float
    anomaly_score: float


# ---- requests -------------------------------------------------------------
class AlertPatch(CamelModel):
    status: AlertStatus


class WorkOrderPatch(CamelModel):
    status: WorkOrderStatus


class LeakInject(CamelModel):
    pipe_id: str
    rate_m3h: float = Field(default=20.0, gt=0, le=200)
    fraction: float | None = Field(default=None, ge=0, le=1)


class StepRequest(CamelModel):
    ticks: int = Field(default=1, ge=1, le=500)

