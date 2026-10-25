"""
CLI Runner for Hydraulic Simulation & AI/ML Analysis.

Usage:
    python scripts/run_simulation.py --scenario pipe_burst --hours 24
"""

import argparse
import json
import logging
import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.workers.simulation_worker import simulation_worker


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("simulation-cli")


def main():
    parser = argparse.ArgumentParser(description="Pune Water Network Simulation CLI Runner")
    parser.add_argument(
        "--scenario",
        default="pipe_burst",
        choices=["normal", "pipe_burst", "slow_leak", "demand_surge", "blockage"],
        help="Hydraulic failure scenario to simulate",
    )
    parser.add_argument(
        "--hours",
        type=int,
        default=24,
        help="Simulation duration in hours",
    )
    parser.add_argument(
        "--step",
        type=int,
        default=15,
        help="Time-step resolution in minutes",
    )

    args = parser.parse_args()

    logger.info(f"Triggering {args.scenario} simulation for {args.hours} hours...")
    result = simulation_worker.run_pipeline(
        scenario_type=args.scenario,
        duration_hours=args.hours,
        time_step_minutes=args.step,
    )

    print("\n" + "=" * 60)
    print("  PUNE WATER NETWORK AI — SIMULATION RESULTS")
    print("=" * 60)
    print(f"Status:               {result['status'].upper()}")
    print(f"Scenario:             {result['scenario_type']}")
    print(f"Anomalies Detected:   {result['anomalies_detected']}")
    print(f"Pipes Assessed:       {result['pipes_assessed']}")
    print("-" * 60)
    print("Real-time Telemetry Summary:")
    print(json.dumps(result["telemetry"], indent=2))
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
