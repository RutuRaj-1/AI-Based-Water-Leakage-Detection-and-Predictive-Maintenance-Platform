"""
Unit tests for Simulation and Hydraulic modeling.
"""

import pytest
from app.simulation.scenarios import DiurnalPattern, ScenarioManager
from app.simulation.engine import HydraulicEngine
from app.simulation.network_builder import PuneNetworkBuilder


def test_diurnal_pattern_ranges():
    # Night flow should be low (~0.3x)
    night_mult = DiurnalPattern.get_multiplier(2.0)
    assert 0.25 <= night_mult <= 0.45

    # Morning peak should be high (~1.8x)
    morning_mult = DiurnalPattern.get_multiplier(7.5)
    assert 1.4 <= morning_mult <= 2.0

    # Afternoon should be steady (~0.9x)
    afternoon_mult = DiurnalPattern.get_multiplier(14.0)
    assert 0.8 <= afternoon_mult <= 1.1


def test_network_builder_nodes_and_pipes():
    nodes = PuneNetworkBuilder.get_nodes()
    pipes = PuneNetworkBuilder.get_pipes()

    assert len(nodes) >= 10
    assert len(pipes) >= 8

    # Verify Katraj feeder P-104 exists
    p104 = next((p for p in pipes if p["id"] == "P-104"), None)
    assert p104 is not None
    assert p104["diameter_mm"] == 300.0
    assert len(p104["coordinates"]) >= 2


def test_hydraulic_engine_normal_simulation():
    engine = HydraulicEngine()
    result = engine.run_simulation(scenario_type="normal", duration_hours=6, time_step_minutes=30)

    assert result["scenario_type"] == "normal"
    assert result["duration_hours"] == 6
    assert "telemetry" in result
    assert result["telemetry"]["meanPressureBar"] > 0
    assert len(result["time_series_by_pipe"]["P-104"]) == 12  # 6 hours * 2 steps/hr
