"""
Integration tests for Pipes, Anomalies, Maintenance, and Simulation endpoints.
"""

import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_list_pipes():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/pipes")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "pagination" in data
    assert len(data["items"]) >= 8


@pytest.mark.asyncio
async def test_get_single_pipe():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/pipes/P-104")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "P-104"
    assert "current_health_score" in data
    assert "failure_probability" in data


@pytest.mark.asyncio
async def test_get_pipe_observations():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/pipes/P-104/observations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "pressure_bar" in data[0]
    assert "flow_mld" in data[0]


@pytest.mark.asyncio
async def test_anomalies_and_status_update():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. List anomalies
        res = await client.get("/api/v1/anomalies")
        assert res.status_code == 200
        anomalies = res.json()["items"]
        assert len(anomalies) >= 1
        first_id = anomalies[0]["id"]

        # 2. Update status to investigating
        patch_res = await client.patch(
            f"/api/v1/anomalies/{first_id}",
            json={"status": "investigating"},
        )
        assert patch_res.status_code == 200
        assert patch_res.json()["status"] == "investigating"


@pytest.mark.asyncio
async def test_maintenance_recommendations():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/v1/maintenance")
        assert res.status_code == 200
        items = res.json()["items"]
        assert len(items) >= 1
        assert "work_order_number" in items[0]
        assert "priority" in items[0]


@pytest.mark.asyncio
async def test_simulation_telemetry():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/v1/simulations/telemetry")
        assert res.status_code == 200
        data = res.json()
        assert "meanPressureBar" in data
        assert "totalFlowMld" in data
        assert "networkHealthScore" in data
