"""Engine, ML and automation behaviour tests."""

import pytest

from app.ml import health as health_ml
from app.simulation.engine import SimulationEngine, interpolate
from app.simulation.network_data import PIPES


@pytest.fixture(scope="module")
def clean_engine() -> SimulationEngine:
    return SimulationEngine(seed=7, auto_leaks=False, seeded_scenario=False)


def test_no_false_alarms_on_clean_network(clean_engine: SimulationEngine):
    for _ in range(1500):
        clean_engine.tick()
    assert clean_engine.alerts == []


def test_leak_is_detected_and_localised():
    e = SimulationEngine(seed=11, auto_leaks=False, seeded_scenario=False, auto_dispatch=False)
    e.inject_leak("P-033", 25.0, 0.4)
    for _ in range(6):
        e.tick()
    alert = e.open_alert("P-033")
    assert alert is not None
    assert alert.severity in {"high", "moderate", "critical"}
    assert abs(alert.fraction - 0.4) < 0.15


def test_full_automation_loop_repairs_leak():
    e = SimulationEngine(seed=3, auto_leaks=False, seeded_scenario=False)
    e.inject_leak("P-104", 40.0, 0.5)
    for _ in range(120):
        e.tick()
    alert = next(a for a in e.alerts if a.pipe_id == "P-104")
    assert alert.auto_dispatched
    assert alert.status == "resolved"
    emergency = [w for w in e.work_orders if w.asset_id == "P-104" and w.kind == "emergency"]
    assert len(emergency) == 1 and emergency[0].status == "completed"
    assert not any(not lk.repaired for lk in e.leaks)


def test_manual_work_order_completion_repairs_leak():
    e = SimulationEngine(seed=5, auto_leaks=False, seeded_scenario=False, auto_repair=False)
    e.inject_leak("P-050", 30.0, 0.5)
    for _ in range(8):
        e.tick()
    wo = next(w for w in e.work_orders if w.kind == "emergency")
    e.set_work_order_status(wo.id, "completed")
    for _ in range(12):
        e.tick()
    assert e.open_alert("P-050") is None


def test_reset_is_deterministic():
    a = SimulationEngine(seed=42, auto_leaks=False)
    b = SimulationEngine(seed=42, auto_leaks=False)
    assert [x.pipe_id for x in a.alerts] == [x.pipe_id for x in b.alerts]
    assert {k: round(v.health) for k, v in a.pipes.items()} == {k: round(v.health) for k, v in b.pipes.items()}


def test_health_and_risk_bounds():
    for spec in PIPES:
        h = health_ml.pipe_health(spec, active_leak_severity="critical", leak_history=9, refurb_bonus=0)
        assert 0 <= h <= 100
    assert health_ml.failure_risk(10, active_leak=True) > health_ml.failure_risk(90, active_leak=False)
    assert health_ml.condition_for(85) == "healthy" and health_ml.condition_for(20) == "critical"


def test_interpolate_endpoints():
    coords = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0))
    assert interpolate(coords, 0.0) == (0.0, 0.0)
    assert interpolate(coords, 1.0) == (1.0, 1.0)
    assert interpolate(coords, 0.5) == pytest.approx((1.0, 0.0))

