"""
Integration tests for GIS GeoJSON endpoints.
"""

import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_get_pipes_geojson():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/gis/pipes")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert "features" in data
    assert len(data["features"]) >= 8

    # Check first feature structure
    first = data["features"][0]
    assert first["type"] == "Feature"
    assert first["geometry"]["type"] == "LineString"
    props = first["properties"]
    assert "healthScore" in props
    assert "condition" in props
    assert "diameterMm" in props
    assert "pressureBar" in props


@pytest.mark.asyncio
async def test_get_nodes_geojson():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/gis/nodes")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) >= 10

    first = data["features"][0]
    assert first["geometry"]["type"] == "Point"
    assert "nodeType" in first["properties"]
    assert "elevationM" in first["properties"]


@pytest.mark.asyncio
async def test_get_leaks_geojson():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/gis/leaks")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) >= 1

    first = data["features"][0]
    assert first["geometry"]["type"] == "Point"
    assert "severity" in first["properties"]
    assert "pipelineId" in first["properties"]
