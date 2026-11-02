"""
Process-wide simulation runtime: lazy engine singleton + background ticker.

The ticker is the platform's "automation heartbeat": while it runs, telemetry
streams in, leaks appear, alerts auto-open/escalate, crews are dispatched and
repairs are completed without any manual action.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging

from app.core.config import settings
from app.simulation.engine import SimulationEngine

log = logging.getLogger("pune_water.runtime")

_engine: SimulationEngine | None = None
_task: asyncio.Task | None = None


def get_engine() -> SimulationEngine:
    global _engine
    if _engine is None:
        _engine = SimulationEngine(
            seed=settings.simulation_seed,
            minutes_per_tick=settings.simulation_minutes_per_tick,
            auto_leaks=settings.simulation_auto_leaks,
            auto_leak_probability=settings.simulation_auto_leak_probability,
            auto_dispatch=settings.automation_auto_dispatch,
            auto_repair=settings.automation_auto_repair,
        )
    return _engine


def set_engine(engine: SimulationEngine | None) -> None:
    """Test hook: replace (or clear) the singleton."""
    global _engine
    _engine = engine


def is_running() -> bool:
    return _task is not None and not _task.done()


async def _loop() -> None:
    engine = get_engine()
    log.info("Simulation ticker started (every %.1fs)", settings.simulation_tick_seconds)
    while True:
        await asyncio.sleep(settings.simulation_tick_seconds)
        if not engine.paused:
            try:
                engine.tick()
            except Exception:  # keep the heartbeat alive
                log.exception("Simulation tick failed")


def start_ticker() -> None:
    global _task
    if not is_running():
        _task = asyncio.create_task(_loop(), name="simulation-ticker")


async def stop_ticker() -> None:
    global _task
    if _task is not None:
        _task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await _task
        _task = None

