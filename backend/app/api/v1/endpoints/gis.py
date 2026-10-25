"""
GIS GeoJSON Endpoints for Leaflet Water Network Map Layers.
"""

from typing import Any, Dict
from fastapi import APIRouter
from app.repositories import pipe_repo, anomaly_repo
from app.schemas.gis import GeoJSONFeatureCollection

router = APIRouter(prefix="/gis", tags=["GIS"])


@router.get(
    "/pipes",
    response_model=GeoJSONFeatureCollection,
    summary="Get pipe segments as GeoJSON FeatureCollection",
    description="Returns pipeline segments formatted as GeoJSON LineStrings for direct rendering on Leaflet maps.",
)
async def get_pipes_geojson() -> Dict[str, Any]:
    return pipe_repo.get_pipes_geojson()


@router.get(
    "/nodes",
    response_model=GeoJSONFeatureCollection,
    summary="Get network nodes as GeoJSON FeatureCollection",
    description="Returns junctions, reservoirs, and pumps as GeoJSON Points with hydraulic elevations and pressures.",
)
async def get_nodes_geojson() -> Dict[str, Any]:
    return pipe_repo.get_nodes_geojson()


@router.get(
    "/leaks",
    response_model=GeoJSONFeatureCollection,
    summary="Get active leak markers as GeoJSON FeatureCollection",
    description="Returns active leak locations, severity levels, and estimated losses as GeoJSON Points.",
)
async def get_leaks_geojson() -> Dict[str, Any]:
    return anomaly_repo.get_leaks_geojson()
