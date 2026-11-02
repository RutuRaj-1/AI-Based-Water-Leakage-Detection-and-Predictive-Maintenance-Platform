"""API tests for the live dashboard endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.main import app
from app.simulation import runtime
from app.simulation.engine import SimulationEngine


@pytest.fixture(autouse=True)
def fresh_engine():
    runtime.set_engine(SimulationEngine(seed=42, auto_leaks=False))
    yield
    runtime.set_engine(None)


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


async def test_snapshot_shape(client: AsyncClient):
    r = await client.get("/api/v1/dashboard/snapshot")
    assert r.status_code == 200
    d = r.json()
    for key in ("telemetry", "summary", "alerts", "criticalAssets", "maintenanceTasks", "pipelines",
                "nodes", "leaks", "events", "history", "simulation"):
        assert key in d
    assert d["pipelines"]["type"] == "FeatureCollection"
    assert d["pipelines"]["features"][0]["properties"]["healthScore"] is not None
    assert len(d["alerts"]) >= 1
    assert d["alerts"][0]["pipelineId"].startswith("Pipe ")
    cats = d["summary"]["conditionCategories"]
    assert abs(sum(c["percentage"] for c in cats) - 100) < 0.5


async def test_alert_lifecycle_via_api(client: AsyncClient):
    alerts = (await client.get("/api/v1/alerts?status=investigating")).json()
    assert alerts
    aid = alerts[0]["id"]
    r = await client.patch(f"/api/v1/alerts/{aid}", json={"status": "resolved"})
    assert r.status_code == 200 and r.json()["status"] == "resolved"
    assert (await client.patch("/api/v1/alerts/NOPE", json={"status": "resolved"})).status_code == 404
    assert (await client.patch(f"/api/v1/alerts/{aid}", json={"status": "bogus"})).status_code == 422


async def test_inject_leak_then_detect(client: AsyncClient):
    r = await client.post("/api/v1/simulation/leaks", json={"pipeId": "P-033", "rateM3h": 30})
    assert r.status_code == 200
    await client.post("/api/v1/simulation/step", json={"ticks": 6})
    alerts = (await client.get("/api/v1/alerts")).json()
    assert any(a["pipelineId"] == "Pipe P-033" for a in alerts)
    assert (await client.post("/api/v1/simulation/leaks", json={"pipeId": "ZZ"})).status_code == 404


async def test_pause_resume_reset(client: AsyncClient):
    assert (await client.post("/api/v1/simulation/pause")).json()["paused"] is True
    assert (await client.post("/api/v1/simulation/resume")).json()["paused"] is False
    assert (await client.post("/api/v1/simulation/reset")).json()["tick"] > 0


async def test_work_order_patch_and_pipe_history(client: AsyncClient):
    tasks = (await client.get("/api/v1/maintenance/tasks")).json()
    assert tasks and tasks == sorted(tasks, key=lambda t: -t["priorityScore"])
    r = await client.patch(f"/api/v1/maintenance/tasks/{tasks[0]['id']}", json={"status": "in_progress"})
    assert r.status_code == 200
    h = (await client.get("/api/v1/pipes/P-104/history?limit=10")).json()
    assert len(h) == 10 and {"time", "pressureBar", "flowMld", "anomalyScore"} <= set(h[0])
    assert (await client.get("/api/v1/pipes/XX")).status_code == 404


async def test_csv_export_and_api_key(client: AsyncClient, monkeypatch):
    r = await client.get("/api/v1/reports/alerts.csv")
    assert r.status_code == 200 and r.text.startswith("id,pipeline")
    monkeypatch.setattr(settings, "api_key", "secret")
    assert (await client.post("/api/v1/simulation/pause")).status_code == 401
    ok = await client.post("/api/v1/simulation/pause", headers={"X-API-Key": "secret"})
    assert ok.status_code == 200

