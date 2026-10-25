"""
Simulation Execution and Network Telemetry Endpoints.
"""

from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, Query
from app.repositories import simulation_repo
from app.workers.simulation_worker import simulation_worker
from app.schemas.simulation import SimulationRunRequest, SimulationTelemetry

router = APIRouter(prefix="/simulations", tags=["Simulations"])


@router.get("", summary="List hydraulic simulation runs")
async def list_simulation_runs(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
) -> Dict[str, Any]:
    return simulation_repo.list_runs(page=page, page_size=page_size)


@router.post("/run", summary="Trigger a new hydraulic simulation run and ML analysis")
async def trigger_simulation_run(
    payload: SimulationRunRequest,
) -> Dict[str, Any]:
    result = simulation_worker.run_pipeline(
        scenario_type=payload.scenario_type,
        duration_hours=payload.duration_hours,
        time_step_minutes=payload.time_step_minutes,
    )
    return {
        "status": "completed",
        "scenario_type": payload.scenario_type,
        "telemetry": result["telemetry"],
        "anomalies_detected": result["anomalies_detected"],
        "pipes_assessed": result["pipes_assessed"],
    }


@router.get("/telemetry", response_model=SimulationTelemetry, summary="Get real-time network telemetry summary")
async def get_simulation_telemetry() -> Dict[str, Any]:
    return simulation_repo.get_telemetry()


@router.get("/{run_id}", summary="Get specific simulation run detail")
async def get_simulation_run(run_id: str) -> Dict[str, Any]:
    run = simulation_repo.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Simulation run not found")
    return run
