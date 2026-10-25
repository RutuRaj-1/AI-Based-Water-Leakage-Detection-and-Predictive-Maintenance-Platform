"""
Database Seeding Script for Pune Water Distribution Network.
Populates PostgreSQL / SQLite database with initial networks, nodes, pipes, and sensors.

Usage:
    python scripts/seed_pune_network.py
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db.session import async_session_factory, engine
from app.db.base import Base
from app.db.models import Network, Node, Pipe, Sensor, Anomaly
from app.simulation.network_builder import PuneNetworkBuilder


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")


async def seed_database():
    logger.info("Initializing database schema...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:
        # 1. Create or verify Network
        net_meta = PuneNetworkBuilder.get_network_metadata()
        network = Network(
            name=net_meta["name"],
            code=net_meta["code"],
            description=net_meta["description"],
            srid=net_meta["srid"],
        )
        session.add(network)
        await session.flush()
        logger.info(f"Seeded network: {network.name}")

        # 2. Seed Nodes
        nodes_data = PuneNetworkBuilder.get_nodes()
        node_lookup = {}
        for nd in nodes_data:
            node = Node(
                network_id=network.id,
                label=nd["name"],
                node_type=nd["node_type"],
                elevation_m=nd["elevation_m"],
                base_demand_lps=nd.get("base_demand_lps", 0.0),
                latitude=nd["coordinates"][1],
                longitude=nd["coordinates"][0],
                zone=nd.get("zone"),
            )
            session.add(node)
            node_lookup[nd["id"]] = node

        await session.flush()
        logger.info(f"Seeded {len(nodes_data)} network nodes.")

        # 3. Seed Pipes
        pipes_data = PuneNetworkBuilder.get_pipes()
        for pd in pipes_data:
            pipe = Pipe(
                network_id=network.id,
                label=pd["name"],
                code=pd["code"],
                zone=pd.get("zone"),
                length_m=pd.get("length_km", 1.0) * 1000.0,
                diameter_mm=pd["diameter_mm"],
                material=pd["material"],
                installation_year=pd.get("installation_year", 2005),
                current_health_score=pd.get("health_score", 100.0),
                condition=pd.get("condition", "healthy"),
                pressure_bar=pd.get("pressure_bar", 3.5),
                flow_rate_mld=pd.get("flow_rate_mld", 10.0),
                coordinates=pd.get("coordinates", []),
            )
            session.add(pipe)

        await session.flush()
        logger.info(f"Seeded {len(pipes_data)} pipeline segments.")

        # 4. Seed Leaks / Anomalies
        leaks_data = PuneNetworkBuilder.get_leaks()
        for lk in leaks_data:
            anomaly = Anomaly(
                pipe_code=lk["pipeline_id"],
                title=f"Detected leak: {lk['location']}",
                location=lk["location"],
                anomaly_type=lk.get("anomaly_type", "pipe_burst"),
                severity=lk["severity"],
                confidence=lk.get("confidence", 0.90),
                estimated_loss=lk.get("estimated_loss"),
                status=lk.get("status", "active"),
                details=lk,
            )
            session.add(anomaly)

        await session.commit()
        logger.info("Database seeding successfully completed!")


if __name__ == "__main__":
    asyncio.run(seed_database())
