"""
Repositories Package and Singleton Instances.
"""

from app.repositories.network_repo import NetworkRepository
from app.repositories.pipe_repo import PipeRepository
from app.repositories.observation_repo import ObservationRepository
from app.repositories.anomaly_repo import AnomalyRepository
from app.repositories.maintenance_repo import MaintenanceRepository
from app.repositories.simulation_repo import SimulationRepository

# Global shared singleton instances
network_repo = NetworkRepository()
pipe_repo = PipeRepository()
observation_repo = ObservationRepository()
anomaly_repo = AnomalyRepository()
maintenance_repo = MaintenanceRepository()
simulation_repo = SimulationRepository()

__all__ = [
    "NetworkRepository",
    "PipeRepository",
    "ObservationRepository",
    "AnomalyRepository",
    "MaintenanceRepository",
    "SimulationRepository",
    "network_repo",
    "pipe_repo",
    "observation_repo",
    "anomaly_repo",
    "maintenance_repo",
    "simulation_repo",
]
