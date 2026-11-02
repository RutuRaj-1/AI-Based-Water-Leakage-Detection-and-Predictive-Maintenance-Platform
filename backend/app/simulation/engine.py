"""
Live hydraulic simulation + automation engine.

Pipeline executed on every tick (one tick = `minutes_per_tick` simulated minutes):

    physics (diurnal demand + noise + injected leaks)
      -> anomaly detection (seasonal-regression residual z-scores)
      -> alert lifecycle (open / auto-escalate / auto-resolve)
      -> health + failure-risk update
      -> maintenance prioritisation -> work orders (auto-create / auto-dispatch)
      -> crew repair simulation (auto-repair) -> leak removed -> alert resolves

The engine is pure Python (no I/O) so it is deterministic under a fixed seed
and easy to unit test. The FastAPI layer owns scheduling (see app.main).
"""

from __future__ import annotations

import logging
import math
import random
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

from app.ml import health as health_ml
from app.ml import maintenance as maint_ml
from app.ml.anomaly import MLD_TO_M3H, PRESSURE_DROP_PER_M3H, AnomalyDetector
from app.simulation.network_data import NODES, PIPES, PUMPS, NodeSpec, PipeSpec, PumpSpec

log = logging.getLogger("pune_water.engine")

WARMUP_DAYS = 5
BREACH_TICKS_TO_OPEN = 2
CLEAR_TICKS_TO_RESOLVE = 4
AUTO_ESCALATE_AFTER_TICKS = 3
AUTO_REPAIR_AFTER_TICKS = 40
PRESSURE_NOISE_BAR = 0.025
FLOW_NOISE_FRAC = 0.006


# --------------------------------------------------------------------------- #
# State containers
# --------------------------------------------------------------------------- #
@dataclass
class Leak:
    id: str
    pipe_id: str
    rate_m3h: float
    initial_rate_m3h: float
    fraction: float                 # 0..1 position along the pipe polyline
    started_tick: int
    repaired: bool = False
    source: str = "scenario"        # scenario | auto | manual


@dataclass
class Alert:
    id: str
    pipe_id: str
    severity: str
    status: str                     # active | investigating | resolved
    detected_at: datetime
    location: str
    fraction: float
    est_loss_m3h: float
    peak_score: float
    peak_pressure_drop: float
    ticks_open: int = 0
    resolved_at: datetime | None = None
    auto_dispatched: bool = False
    emergency_wo_created: bool = False
    title: str = "Pressure-Flow Divergence"


@dataclass
class WorkOrder:
    id: str
    number: str
    asset_id: str
    asset_label: str
    kind: str
    title: str
    team: str
    priority_score: float
    priority: str
    due: str
    status: str                     # open | in_progress | completed
    created_at: datetime
    zone: str = ""
    in_progress_ticks: int = 0
    completed_at: datetime | None = None
    auto_created: bool = True


@dataclass
class Event:
    id: int
    time: datetime
    level: str                      # info | warning | critical | success
    kind: str
    message: str


@dataclass
class PipeState:
    spec: PipeSpec
    pressure: float
    flow: float
    health: float = 100.0
    risk: float = 0.0
    condition: str = "healthy"
    leak_history: int = 0
    refurb_bonus: float = 0.0
    z_pressure: float = 0.0
    z_flow: float = 0.0
    score: float = 0.0
    breach_streak: int = 0
    clear_streak: int = 0
    history: deque = field(default_factory=lambda: deque(maxlen=288))


@dataclass
class NodeState:
    spec: NodeSpec
    pressure: float


@dataclass
class PumpState:
    spec: PumpSpec
    health: float
    refurb_bonus: float = 0.0


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def demand_factor(hour: float) -> float:
    """Diurnal demand multiplier (morning + evening peaks, night trough)."""
    return (
        1.0
        + 0.35 * math.exp(-(((hour - 7.0) / 1.8) ** 2))
        + 0.30 * math.exp(-(((hour - 19.0) / 2.0) ** 2))
        - 0.35 * math.exp(-(((hour - 3.0) / 2.5) ** 2))
    )


def interpolate(coords: tuple[tuple[float, float], ...], fraction: float) -> tuple[float, float]:
    fraction = max(0.0, min(1.0, fraction))
    seg = [math.dist(coords[i], coords[i + 1]) for i in range(len(coords) - 1)]
    target = sum(seg) * fraction
    acc = 0.0
    for i, length in enumerate(seg):
        if acc + length >= target or i == len(seg) - 1:
            t = 0.0 if length == 0 else (target - acc) / length
            a, b = coords[i], coords[i + 1]
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        acc += length
    return coords[-1]


def severity_for(loss_m3h: float) -> str:
    if loss_m3h >= 30:
        return "critical"
    if loss_m3h >= 12:
        return "high"
    if loss_m3h >= 5:
        return "moderate"
    return "low"


SEVERITY_RANK = {"low": 0, "moderate": 1, "high": 2, "critical": 3}


def humanize_age(delta: timedelta) -> str:
    minutes = max(int(delta.total_seconds() // 60), 0)
    if minutes < 1:
        return "just now"
    if minutes < 60:
        return f"{minutes}m ago"
    hours, mins = divmod(minutes, 60)
    if hours < 24:
        return f"{hours}h {mins}m ago" if mins else f"{hours}h ago"
    return f"{hours // 24}d ago"


# --------------------------------------------------------------------------- #
# Engine
# --------------------------------------------------------------------------- #
class SimulationEngine:
    def __init__(
        self,
        *,
        seed: int = 42,
        minutes_per_tick: int = 5,
        auto_leaks: bool = True,
        auto_leak_probability: float = 0.03,
        auto_dispatch: bool = True,
        auto_repair: bool = True,
        seeded_scenario: bool = True,
    ) -> None:
        self.seed = seed
        self.minutes_per_tick = minutes_per_tick
        self.auto_leaks = auto_leaks
        self.auto_leak_probability = auto_leak_probability
        self.auto_dispatch = auto_dispatch
        self.auto_repair = auto_repair
        self.seeded_scenario = seeded_scenario
        self.paused = False
        self.reset()

    # ------------------------------------------------------------------ setup
    def reset(self) -> None:
        self.rng = random.Random(self.seed)
        self.tick_count = 0
        self.scenario_name = "Baseline + seeded leak scenario"
        self.detector = AnomalyDetector()
        self.leaks: list[Leak] = []
        self.alerts: list[Alert] = []
        self.work_orders: list[WorkOrder] = []
        self.events: deque[Event] = deque(maxlen=120)
        self.telemetry_history: deque[dict] = deque(maxlen=240)
        self._leak_seq = 0
        self._alert_seq = 0
        self._wo_seq = 800
        self._event_seq = 0

        self.pipes: dict[str, PipeState] = {
            p.id: PipeState(p, p.base_pressure_bar, p.base_flow_mld) for p in PIPES
        }
        self.nodes: dict[str, NodeState] = {n.id: NodeState(n, n.base_pressure_bar) for n in NODES}
        self.pumps: dict[str, PumpState] = {p.id: PumpState(p, p.base_health) for p in PUMPS}

        preroll = 14 if self.seeded_scenario else 0
        warmup_ticks = WARMUP_DAYS * 24 * 60 // self.minutes_per_tick
        now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
        now -= timedelta(minutes=now.minute % self.minutes_per_tick)
        self.sim_time = now - timedelta(minutes=(warmup_ticks + preroll) * self.minutes_per_tick)

        self._warm_up(warmup_ticks)
        for ps in self.pipes.values():
            self._refresh_health(ps)
        self._event("info", "engine", f"Detector calibrated on {WARMUP_DAYS} days of baseline telemetry "
                                      f"for {len(self.pipes)} pipes.")

        if self.seeded_scenario:
            plan = {0: ("P-104", 42.0, 0.69), 3: ("P-067", 18.0, 0.50), 6: ("P-211", 6.5, 0.62)}
            for i in range(preroll):
                if i in plan:
                    pid, rate, frac = plan[i]
                    self.inject_leak(pid, rate, frac, source="scenario")
                self.tick()

    def _warm_up(self, ticks: int) -> None:
        series: dict[str, tuple[list[float], list[float], list[float]]] = {
            pid: ([], [], []) for pid in self.pipes
        }
        for _ in range(ticks):
            self.sim_time += timedelta(minutes=self.minutes_per_tick)
            hour = self.sim_time.hour + self.sim_time.minute / 60.0
            for pid, ps in self.pipes.items():
                p, q = self._measure(ps.spec, hour, leak_rate=0.0, leak_drop=0.0)
                h, ps_, qs = series[pid]
                h.append(hour)
                ps_.append(p)
                qs.append(q)
        for pid, (h, p, q) in series.items():
            self.detector.fit(pid, h, p, q)

    # ---------------------------------------------------------------- physics
    def _measure(self, spec: PipeSpec, hour: float, *, leak_rate: float, leak_drop: float) -> tuple[float, float]:
        d = demand_factor(hour)
        pressure_factor = 1.0 - 0.18 * (d - 1.0)
        pressure = spec.base_pressure_bar * pressure_factor + self.rng.gauss(0.0, PRESSURE_NOISE_BAR) - leak_drop
        flow = spec.base_flow_mld * d + self.rng.gauss(0.0, FLOW_NOISE_FRAC * spec.base_flow_mld)
        flow += leak_rate / MLD_TO_M3H
        return max(pressure, 0.0), max(flow, 0.0)

    def _pipe_leaks(self, pipe_id: str) -> list[Leak]:
        return [lk for lk in self.leaks if lk.pipe_id == pipe_id and not lk.repaired]

    # ------------------------------------------------------------------- tick
    def tick(self) -> None:
        self.tick_count += 1
        self.sim_time += timedelta(minutes=self.minutes_per_tick)
        hour = self.sim_time.hour + self.sim_time.minute / 60.0

        self._maybe_spawn_leak()
        for lk in self.leaks:
            if not lk.repaired:
                lk.rate_m3h = min(lk.rate_m3h * 1.003, lk.initial_rate_m3h * 1.5)  # slow growth

        drops: dict[str, float] = {}
        for pid, ps in self.pipes.items():
            rate = sum(lk.rate_m3h for lk in self._pipe_leaks(pid))
            drop = min(PRESSURE_DROP_PER_M3H * rate, 0.45 * ps.spec.base_pressure_bar)
            drops[pid] = drop
            ps.pressure, ps.flow = self._measure(ps.spec, hour, leak_rate=rate, leak_drop=drop)
            sc = self.detector.score(pid, hour, ps.pressure, ps.flow)
            ps.z_pressure, ps.z_flow, ps.score = sc.z_pressure, sc.z_flow, sc.score
            ps.breach_streak = ps.breach_streak + 1 if sc.score >= self.detector.threshold else 0
            if sc.score < 2.0:
                ps.clear_streak += 1
            elif sc.score >= self.detector.threshold:
                ps.clear_streak = 0
            ps.history.append({"time": self.sim_time, "pressureBar": ps.pressure, "flowMld": ps.flow,
                               "anomalyScore": sc.score})
            self._update_alert_for(ps, sc.est_loss_m3h, -sc.pressure_deviation)

        self._update_nodes(hour, drops)
        for ps in self.pipes.values():
            self._refresh_health(ps)
        for pump in self.pumps.values():
            pump.health = min(100.0, health_ml.pump_health(pump.spec.base_health, pump.spec.wear_index,
                                                            self.tick_count) + pump.refurb_bonus)
        self._sync_work_orders()
        self._progress_work_orders()
        self._record_telemetry()

    def _update_nodes(self, hour: float, drops: dict[str, float]) -> None:
        d = demand_factor(hour)
        pf = 1.0 - 0.18 * (d - 1.0)
        node_drop: dict[str, float] = {}
        for pid, drop in drops.items():
            spec = self.pipes[pid].spec
            for nid in (spec.from_node, spec.to_node):
                node_drop[nid] = max(node_drop.get(nid, 0.0), drop * 0.5)
        for nid, ns in self.nodes.items():
            ns.pressure = max(ns.spec.base_pressure_bar * pf + self.rng.gauss(0, 0.02) - node_drop.get(nid, 0.0), 0.0)

    # ---------------------------------------------------------------- leaks
    def inject_leak(self, pipe_id: str, rate_m3h: float, fraction: float | None = None, *,
                    source: str = "manual") -> Leak:
        if pipe_id not in self.pipes:
            raise KeyError(pipe_id)
        self._leak_seq += 1
        lk = Leak(
            id=f"LK-{self._leak_seq:03d}", pipe_id=pipe_id, rate_m3h=rate_m3h, initial_rate_m3h=rate_m3h,
            fraction=self.rng.uniform(0.15, 0.85) if fraction is None else fraction,
            started_tick=self.tick_count, source=source,
        )
        self.leaks.append(lk)
        self._event("warning", "leak_injected",
                    f"{source.capitalize()} leak of {rate_m3h:.1f} m³/hr injected on {pipe_id}.")
        return lk

    def _maybe_spawn_leak(self) -> None:
        if not self.auto_leaks or self.rng.random() > self.auto_leak_probability:
            return
        open_pipes = {lk.pipe_id for lk in self.leaks if not lk.repaired}
        if len(open_pipes) >= 4:
            return
        candidates = [ps for pid, ps in self.pipes.items() if pid not in open_pipes]
        weights = [(1.0 - ps.health / 100.0) + 0.1 for ps in candidates]
        target = self.rng.choices(candidates, weights=weights, k=1)[0]
        rate = min(max(self.rng.lognormvariate(math.log(14), 0.7), 6.0), 60.0)
        self.inject_leak(target.spec.id, rate, source="auto")

    # --------------------------------------------------------------- alerts
    def open_alert(self, pipe_id: str) -> Alert | None:
        for a in self.alerts:
            if a.pipe_id == pipe_id and a.status != "resolved":
                return a
        return None

    def _update_alert_for(self, ps: PipeState, est_loss: float, pressure_drop: float) -> None:
        alert = self.open_alert(ps.spec.id)
        if alert is None:
            if ps.breach_streak >= BREACH_TICKS_TO_OPEN:
                self._open_alert(ps, est_loss, pressure_drop)
            return

        alert.ticks_open += 1
        alert.est_loss_m3h = 0.5 * alert.est_loss_m3h + 0.5 * est_loss
        alert.peak_score = max(alert.peak_score, ps.score)
        alert.peak_pressure_drop = max(alert.peak_pressure_drop, pressure_drop)
        sev = severity_for(alert.est_loss_m3h)
        if SEVERITY_RANK[sev] > SEVERITY_RANK[alert.severity]:
            alert.severity = sev
            self._event("critical" if sev == "critical" else "warning", "alert_escalated",
                        f"{alert.id} on {ps.spec.id} escalated to {sev}.")
        alert.title = self._title(alert, self.sim_time.hour)

        if (self.auto_dispatch and alert.status == "active" and alert.ticks_open >= AUTO_ESCALATE_AFTER_TICKS
                and SEVERITY_RANK[alert.severity] >= SEVERITY_RANK["high"]):
            alert.status = "investigating"
            alert.auto_dispatched = True
            self._event("info", "auto_dispatch", f"{alert.id} auto-escalated: crew dispatched to {ps.spec.location}.")

        if ps.clear_streak >= CLEAR_TICKS_TO_RESOLVE and not self._pipe_leaks(ps.spec.id):
            self._resolve_alert(alert, "anomaly cleared")

    def _open_alert(self, ps: PipeState, est_loss: float, pressure_drop: float) -> None:
        self._alert_seq += 1
        leaks = self._pipe_leaks(ps.spec.id)
        # Localisation estimate: true position + sensor-triangulation error.
        frac = (leaks[0].fraction + self.rng.gauss(0, 0.03)) if leaks else 0.5
        alert = Alert(
            id=f"ALT-{self._alert_seq:03d}", pipe_id=ps.spec.id, severity=severity_for(est_loss),
            status="active", detected_at=self.sim_time, location=ps.spec.location,
            fraction=max(0.05, min(0.95, frac)), est_loss_m3h=est_loss, peak_score=ps.score,
            peak_pressure_drop=pressure_drop,
        )
        alert.title = self._title(alert, self.sim_time.hour)
        self.alerts.append(alert)
        ps.leak_history += 1
        self._event("critical" if alert.severity in ("critical", "high") else "warning", "alert_opened",
                    f"{alert.id}: {alert.title} on {ps.spec.id} (~{est_loss:.0f} m³/hr, {alert.severity}).")
        log.info("Alert opened %s pipe=%s sev=%s loss=%.1f", alert.id, ps.spec.id, alert.severity, est_loss)

    def _title(self, alert: Alert, hour: int) -> str:
        if 0 <= hour < 5 and alert.est_loss_m3h >= 3:
            return "Night Flow Rate Deviation"
        if alert.peak_pressure_drop >= 0.4:
            return f"Sudden Pressure Drop (>{math.floor(alert.peak_pressure_drop * 10) / 10:.1f} bar)"
        if alert.est_loss_m3h < 8:
            return "Flow Micro-Turbulence Spike"
        return "Pressure-Flow Divergence"

    def _resolve_alert(self, alert: Alert, reason: str) -> None:
        alert.status = "resolved"
        alert.resolved_at = self.sim_time
        self._event("success", "alert_resolved", f"{alert.id} on {alert.pipe_id} resolved ({reason}).")
        for wo in self.work_orders:
            if wo.asset_id == alert.pipe_id and wo.kind == "emergency" and wo.status != "completed":
                self._complete_work_order(wo, repair=False)

    def set_alert_status(self, alert_id: str, status: str) -> Alert:
        alert = next((a for a in self.alerts if a.id == alert_id), None)
        if alert is None:
            raise KeyError(alert_id)
        if status == "resolved":
            # Operator override: a still-leaking pipe will re-alert after the debounce window.
            self.pipes[alert.pipe_id].breach_streak = 0
            self._resolve_alert(alert, "operator action")
        elif alert.status != "resolved":
            alert.status = status
            self._event("info", "alert_status", f"{alert.id} marked {status} by operator.")
        return alert

    # ---------------------------------------------------------- health / risk
    def _refresh_health(self, ps: PipeState) -> None:
        alert = self.open_alert(ps.spec.id)
        ps.health = health_ml.pipe_health(
            ps.spec, active_leak_severity=alert.severity if alert else None,
            leak_history=ps.leak_history, refurb_bonus=ps.refurb_bonus,
        )
        ps.condition = health_ml.condition_for(ps.health)
        ps.risk = health_ml.failure_risk(ps.health, active_leak=alert is not None)

    # ------------------------------------------------------------ work orders
    def _active_wo(self, asset_id: str, *, emergency: bool) -> WorkOrder | None:
        for wo in self.work_orders:
            if wo.asset_id == asset_id and wo.status != "completed" and (wo.kind == "emergency") == emergency:
                return wo
        return None

    def _due(self, label: str) -> str:
        d = self.sim_time
        if label == "urgent":
            return "Today · Immediate"
        if label == "high":
            return "Tomorrow · 09:00"
        if label == "medium":
            return f"{(d + timedelta(days=3)):%b %d} · Scheduled"
        return f"{(d + timedelta(days=7)):%b %d} · Routine"

    def _new_wo(self, *, asset_id: str, asset_label: str, kind: str, score: float, zone: str,
                emergency_critical: bool = False) -> WorkOrder:
        self._wo_seq += 1
        label = maint_ml.priority_label(score, emergency_critical=emergency_critical)
        wo = WorkOrder(
            id=f"task-{self._wo_seq}", number=f"WO-{self._wo_seq}", asset_id=asset_id, asset_label=asset_label,
            kind=kind, title=maint_ml.KIND_TITLE[kind], team=maint_ml.team_for(kind, zone),
            priority_score=round(score), priority=label, due=self._due(label), status="open",
            created_at=self.sim_time, zone=zone,
        )
        self.work_orders.append(wo)
        self._event("info", "work_order_created", f"{wo.number} created: {wo.title} → {asset_label} ({label}).")
        return wo

    def _sync_work_orders(self) -> None:
        for pid, ps in self.pipes.items():
            alert = self.open_alert(pid)
            leaking = alert is not None
            crit = maint_ml.diameter_criticality(ps.spec.diameter_mm)
            score = maint_ml.priority_score(health=ps.health, risk=ps.risk, criticality=crit, leaking=leaking)
            label = f"Pipe {pid} ({ps.spec.location.split(' ')[0]})"
            kind = maint_ml.pipe_candidate_kind(health=ps.health, risk=ps.risk, leaking=leaking,
                                                corrosion=ps.spec.corrosion_index)
            emergency = self._active_wo(pid, emergency=True)
            if leaking and emergency is None and not alert.emergency_wo_created:
                alert.emergency_wo_created = True
                self._new_wo(asset_id=pid, asset_label=label, kind="emergency", score=score, zone=ps.spec.zone,
                             emergency_critical=alert.severity == "critical")
            elif emergency is not None:
                emergency.priority_score = round(score)
                emergency.priority = maint_ml.priority_label(score, emergency_critical=bool(alert and alert.severity == "critical"))

            routine = self._active_wo(pid, emergency=False)
            non_emergency_kind = kind if kind != "emergency" else maint_ml.pipe_candidate_kind(
                health=ps.health, risk=ps.risk, leaking=False, corrosion=ps.spec.corrosion_index)
            if non_emergency_kind is None:
                if routine is not None and routine.status == "open":
                    self.work_orders.remove(routine)
            elif routine is None:
                self._new_wo(asset_id=pid, asset_label=label, kind=non_emergency_kind, score=score, zone=ps.spec.zone)
            elif routine.status == "open":
                routine.kind, routine.title = non_emergency_kind, maint_ml.KIND_TITLE[non_emergency_kind]
                routine.team = maint_ml.team_for(non_emergency_kind, ps.spec.zone)
                routine.priority_score = round(score)
                routine.priority = maint_ml.priority_label(score)

        for pid, pump in self.pumps.items():
            wo = self._active_wo(pid, emergency=False)
            if pump.health < 60:
                score = maint_ml.priority_score(health=pump.health, risk=health_ml.failure_risk(pump.health, active_leak=False),
                                                criticality=0.8, leaking=False)
                if wo is None:
                    self._new_wo(asset_id=pid, asset_label=f"Pump {pid} ({pump.spec.zone})", kind="pump",
                                 score=score, zone=pump.spec.zone)
                elif wo.status == "open":
                    wo.priority_score, wo.priority = round(score), maint_ml.priority_label(score)

        # Keep the history of completed orders bounded.
        done = [w for w in self.work_orders if w.status == "completed"]
        for w in done[:-15]:
            self.work_orders.remove(w)

    def _progress_work_orders(self) -> None:
        for wo in list(self.work_orders):
            if wo.kind == "emergency" and wo.status == "open" and self.auto_dispatch:
                alert = self.open_alert(wo.asset_id)
                if alert is not None and alert.status == "investigating":
                    wo.status = "in_progress"
                    self._event("info", "work_order_started", f"{wo.number} dispatched to {wo.team}.")
            if wo.status == "in_progress":
                wo.in_progress_ticks += 1
                if self.auto_repair and wo.kind == "emergency" and wo.in_progress_ticks >= AUTO_REPAIR_AFTER_TICKS:
                    self._complete_work_order(wo, repair=True)

    def _complete_work_order(self, wo: WorkOrder, *, repair: bool) -> None:
        wo.status = "completed"
        wo.completed_at = self.sim_time
        if wo.asset_id in self.pumps:
            self.pumps[wo.asset_id].refurb_bonus += 30.0
        elif wo.asset_id in self.pipes:
            ps = self.pipes[wo.asset_id]
            if wo.kind == "emergency":
                if repair:
                    for lk in self._pipe_leaks(wo.asset_id):
                        lk.repaired = True
                ps.refurb_bonus += 8.0
            else:
                ps.refurb_bonus += 30.0
        self._event("success", "work_order_completed", f"{wo.number} completed by {wo.team}.")

    def set_work_order_status(self, wo_id: str, status: str) -> WorkOrder:
        wo = next((w for w in self.work_orders if w.id == wo_id or w.number == wo_id), None)
        if wo is None:
            raise KeyError(wo_id)
        if wo.status == "completed":
            return wo
        if status == "completed":
            self._complete_work_order(wo, repair=True)
        elif status == "in_progress" and wo.status == "open":
            wo.status = "in_progress"
            if wo.kind == "emergency":
                alert = self.open_alert(wo.asset_id)
                if alert is not None and alert.status == "active":
                    alert.status = "investigating"
            self._event("info", "work_order_started", f"{wo.number} started by operator.")
        elif status == "open":
            wo.status = "open"
        return wo

    # -------------------------------------------------------------- telemetry
    def _record_telemetry(self) -> None:
        self.telemetry_history.append(self.telemetry_point())

    def telemetry_point(self) -> dict:
        pipes = list(self.pipes.values())
        total_flow = sum(p.flow for p in pipes)
        loss_m3h = sum(a.est_loss_m3h for a in self.alerts if a.status != "resolved")
        loss_pct = (loss_m3h * 24.0 / 1000.0) / total_flow * 100.0 if total_flow else 0.0
        total_len = sum(p.spec.length_km for p in pipes) or 1.0
        return {
            "time": self.sim_time,
            "meanPressureBar": round(sum(p.pressure for p in pipes) / len(pipes), 3),
            "totalFlowMld": round(total_flow, 2),
            "estimatedLossPct": round(loss_pct, 2),
            "activeLeaksCount": sum(1 for a in self.alerts if a.status != "resolved"),
            "networkHealthScore": round(sum(p.health * p.spec.length_km for p in pipes) / total_len, 1),
        }

    def _event(self, level: str, kind: str, message: str) -> None:
        self._event_seq += 1
        self.events.append(Event(self._event_seq, self.sim_time, level, kind, message))

    # ------------------------------------------------------------------ views
    def pipe_history(self, pipe_id: str, limit: int = 96) -> list[dict]:
        return list(self.pipes[pipe_id].history)[-limit:]
