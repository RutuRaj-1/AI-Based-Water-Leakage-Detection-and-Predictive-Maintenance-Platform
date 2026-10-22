"""
Health endpoint tests.

These tests verify the /api/v1/health endpoint behaves as documented.
They use httpx's ASGITransport to test the FastAPI app without a running server.
"""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_health_returns_200():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_response_shape():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/health")
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "environment" in data


@pytest.mark.asyncio
async def test_health_does_not_claim_db_is_ready():
    """
    The health endpoint must not report on database or ML service readiness
    until those services are actually checked. Verify the response only
    contains the expected keys.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/health")
    data = response.json()
    assert set(data.keys()) == {"status", "version", "environment"}, (
        "Health response contains unexpected keys — do not add DB/ML status "
        "to this endpoint without implementing actual health checks."
    )
