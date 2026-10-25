"""
Network Management Endpoints.
"""

from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, Query
from app.repositories import network_repo, pipe_repo

router = APIRouter(prefix="/networks", tags=["Networks"])


@router.get("", summary="List water distribution networks")
async def list_networks(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
) -> Dict[str, Any]:
    return network_repo.list_networks(page=page, page_size=page_size)


@router.get("/{network_id}", summary="Get a specific network detail")
async def get_network(network_id: str) -> Dict[str, Any]:
    net = network_repo.get_network(network_id)
    if not net:
        raise HTTPException(status_code=404, detail="Network not found")
    return net


@router.get("/{network_id}/pipes", summary="List pipe segments in a network")
async def list_network_pipes(
    network_id: str,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
) -> Dict[str, Any]:
    return pipe_repo.list_pipes(page=page, page_size=page_size)


@router.get("/{network_id}/features", summary="Get GeoJSON FeatureCollection for a network")
async def get_network_features(network_id: str) -> Dict[str, Any]:
    return pipe_repo.get_pipes_geojson()
