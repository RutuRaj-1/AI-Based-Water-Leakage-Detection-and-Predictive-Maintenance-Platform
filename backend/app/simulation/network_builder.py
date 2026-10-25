"""
Pune DMA Network Generator.
Models the water distribution topology of Pune across key zones:
- Katraj DMA (Zone 4)
- Shivajinagar / Central (Zone 1)
- Kothrud DMA (Zone 2)
- Swargate DMA (Zone 3)
- Hadapsar DMA (Zone 7)
- Cantonment DMA (Zone 5)
- Aundh / Baner (Zone 6)
- Vadgaon Sheri (Zone 8)

Coordinates match EPSG:4326 GeoJSON standard [longitude, latitude].
"""

from typing import Any, Dict, List
import uuid

# Base geographic center of Pune
PUNE_CENTER_LAT = 18.5204
PUNE_CENTER_LNG = 73.8567

PUNE_NODES_DATA: List[Dict[str, Any]] = [
    {
        "id": "RES-PARVATI",
        "name": "Parvati Water Treatment Plant & Clear Water Reservoir",
        "node_type": "treatment_plant",
        "zone": "Parvati WTP",
        "coordinates": [73.8474, 18.4975],
        "elevation_m": 570.0,
        "base_demand_lps": 0.0,
        "pressure_bar": 5.8,
    },
    {
        "id": "RES-KATRAJ",
        "name": "Katraj Elevated Storage Reservoir",
        "node_type": "reservoir",
        "zone": "Zone 4 — Katraj",
        "coordinates": [73.8560, 18.4485],
        "elevation_m": 615.0,
        "base_demand_lps": 220.0,
        "pressure_bar": 3.2,
    },
    {
        "id": "RES-CHATURSHRINGI",
        "name": "Chaturshringi High Reservoir",
        "node_type": "reservoir",
        "zone": "Zone 6 — Aundh/Baner",
        "coordinates": [73.8290, 18.5370],
        "elevation_m": 595.0,
        "base_demand_lps": 180.0,
        "pressure_bar": 3.9,
    },
    {
        "id": "PS-02",
        "name": "Parvati High-Lift Pump PS-02",
        "node_type": "pump",
        "zone": "Parvati WTP",
        "coordinates": [73.8485, 18.4990],
        "elevation_m": 568.0,
        "base_demand_lps": 320.0,
        "pressure_bar": 5.4,
    },
    {
        "id": "PS-05",
        "name": "Swargate Booster Station PS-05",
        "node_type": "pump",
        "zone": "Zone 3 — Swargate DMA",
        "coordinates": [73.8580, 18.5018],
        "elevation_m": 555.0,
        "base_demand_lps": 210.0,
        "pressure_bar": 4.1,
    },
    {
        "id": "J-SWARGATE",
        "name": "Swargate Main Junction",
        "node_type": "junction",
        "zone": "Zone 3 — Swargate DMA",
        "coordinates": [73.8585, 18.5025],
        "elevation_m": 554.0,
        "base_demand_lps": 120.0,
        "pressure_bar": 3.8,
    },
    {
        "id": "J-SHIVAJINAGAR",
        "name": "Shivajinagar Interconnect",
        "node_type": "junction",
        "zone": "Zone 1 — Central",
        "coordinates": [73.8520, 18.5315],
        "elevation_m": 560.0,
        "base_demand_lps": 150.0,
        "pressure_bar": 3.5,
    },
    {
        "id": "J-KOTHRUD",
        "name": "Kothrud West Junction",
        "node_type": "junction",
        "zone": "Zone 2 — Kothrud",
        "coordinates": [73.8080, 18.5075],
        "elevation_m": 565.0,
        "base_demand_lps": 130.0,
        "pressure_bar": 3.4,
    },
    {
        "id": "J-HADAPSAR",
        "name": "Hadapsar Industrial Terminal",
        "node_type": "junction",
        "zone": "Zone 7 — Hadapsar",
        "coordinates": [73.9280, 18.5020],
        "elevation_m": 558.0,
        "base_demand_lps": 190.0,
        "pressure_bar": 3.1,
    },
    {
        "id": "J-CANTONMENT",
        "name": "Camp Cantonment Junction",
        "node_type": "junction",
        "zone": "Zone 5 — Cantonment",
        "coordinates": [73.8930, 18.5360],
        "elevation_m": 562.0,
        "base_demand_lps": 110.0,
        "pressure_bar": 3.7,
    },
    {
        "id": "J-AUNDH",
        "name": "Aundh University Chowk Junction",
        "node_type": "junction",
        "zone": "Zone 6 — Aundh/Baner",
        "coordinates": [73.8050, 18.5600],
        "elevation_m": 572.0,
        "base_demand_lps": 140.0,
        "pressure_bar": 3.6,
    },
    {
        "id": "J-VADGAON",
        "name": "Vadgaon Sheri Arterial Point",
        "node_type": "junction",
        "zone": "Zone 8 — Vadgaon Sheri",
        "coordinates": [73.9350, 18.5580],
        "elevation_m": 565.0,
        "base_demand_lps": 95.0,
        "pressure_bar": 3.8,
    },
]

PUNE_PIPES_DATA: List[Dict[str, Any]] = [
    {
        "id": "P-104",
        "code": "P-104",
        "name": "Katraj Feeder Main (P-104)",
        "zone": "Zone 4 — Katraj",
        "start_node": "PS-05",
        "end_node": "RES-KATRAJ",
        "coordinates": [
            [73.8580, 18.5018],
            [73.8610, 18.4790],
            [73.8550, 18.4650],
            [73.8560, 18.4485],
        ],
        "diameter_mm": 300.0,
        "material": "Cast Iron (CI 300mm)",
        "length_km": 6.8,
        "installation_year": 1988,
        "health_score": 24.0,
        "condition": "critical",
        "pressure_bar": 1.9,
        "flow_rate_mld": 28.4,
    },
    {
        "id": "P-042",
        "code": "P-042",
        "name": "Shivajinagar Sub-main (P-042)",
        "zone": "Zone 1 — Central",
        "start_node": "J-SWARGATE",
        "end_node": "J-SHIVAJINAGAR",
        "coordinates": [
            [73.8585, 18.5025],
            [73.8440, 18.5200],
            [73.8520, 18.5315],
        ],
        "diameter_mm": 250.0,
        "material": "Ductile Iron (DI 250mm)",
        "length_km": 4.2,
        "installation_year": 1995,
        "health_score": 31.0,
        "condition": "critical",
        "pressure_bar": 2.3,
        "flow_rate_mld": 19.2,
    },
    {
        "id": "P-067",
        "code": "P-067",
        "name": "Swargate DMA-3 Feeder (P-067)",
        "zone": "Zone 3 — Swargate DMA",
        "start_node": "RES-PARVATI",
        "end_node": "PS-05",
        "coordinates": [
            [73.8474, 18.4975],
            [73.8530, 18.4985],
            [73.8580, 18.5018],
        ],
        "diameter_mm": 350.0,
        "material": "Mild Steel (MS 350mm)",
        "length_km": 2.1,
        "installation_year": 2002,
        "health_score": 52.0,
        "condition": "attention",
        "pressure_bar": 3.1,
        "flow_rate_mld": 24.1,
    },
    {
        "id": "P-088",
        "code": "P-088",
        "name": "Hadapsar Distribution (P-088)",
        "zone": "Zone 7 — Hadapsar",
        "start_node": "J-SWARGATE",
        "end_node": "J-HADAPSAR",
        "coordinates": [
            [73.8585, 18.5025],
            [73.8920, 18.4980],
            [73.9280, 18.5020],
        ],
        "diameter_mm": 200.0,
        "material": "Mild Steel (MS 200mm)",
        "length_km": 7.6,
        "installation_year": 1992,
        "health_score": 38.0,
        "condition": "critical",
        "pressure_bar": 2.7,
        "flow_rate_mld": 14.5,
    },
    {
        "id": "P-211",
        "code": "P-211",
        "name": "Kothrud West Arterial (P-211)",
        "zone": "Zone 2 — Kothrud",
        "start_node": "RES-PARVATI",
        "end_node": "J-KOTHRUD",
        "coordinates": [
            [73.8474, 18.4975],
            [73.8280, 18.5030],
            [73.8150, 18.5050],
            [73.8080, 18.5075],
        ],
        "diameter_mm": 250.0,
        "material": "Ductile Iron (DI 250mm)",
        "length_km": 4.8,
        "installation_year": 2010,
        "health_score": 68.0,
        "condition": "monitor",
        "pressure_bar": 3.2,
        "flow_rate_mld": 18.0,
    },
    {
        "id": "P-015",
        "code": "P-015",
        "name": "Cantonment Main Trunk (P-015)",
        "zone": "Zone 5 — Cantonment",
        "start_node": "RES-PARVATI",
        "end_node": "J-CANTONMENT",
        "coordinates": [
            [73.8474, 18.4975],
            [73.8780, 18.5140],
            [73.8930, 18.5360],
        ],
        "diameter_mm": 500.0,
        "material": "Prestressed Concrete (PSC 500mm)",
        "length_km": 6.1,
        "installation_year": 2015,
        "health_score": 92.0,
        "condition": "healthy",
        "pressure_bar": 4.2,
        "flow_rate_mld": 42.0,
    },
    {
        "id": "P-033",
        "code": "P-033",
        "name": "Aundh-Baner Feeder (P-033)",
        "zone": "Zone 6 — Aundh/Baner",
        "start_node": "J-SHIVAJINAGAR",
        "end_node": "J-AUNDH",
        "coordinates": [
            [73.8520, 18.5315],
            [73.8290, 18.5370],
            [73.8050, 18.5600],
        ],
        "diameter_mm": 350.0,
        "material": "Ductile Iron (DI 350mm)",
        "length_km": 5.9,
        "installation_year": 2018,
        "health_score": 86.0,
        "condition": "healthy",
        "pressure_bar": 3.7,
        "flow_rate_mld": 26.5,
    },
    {
        "id": "P-050",
        "code": "P-050",
        "name": "Vadgaon Sheri Connector (P-050)",
        "zone": "Zone 8 — Vadgaon Sheri",
        "start_node": "J-CANTONMENT",
        "end_node": "J-VADGAON",
        "coordinates": [
            [73.8930, 18.5360],
            [73.9020, 18.5480],
            [73.9350, 18.5580],
        ],
        "diameter_mm": 200.0,
        "material": "High Density Polyethylene (HDPE 200mm)",
        "length_km": 5.3,
        "installation_year": 2021,
        "health_score": 89.0,
        "condition": "healthy",
        "pressure_bar": 3.8,
        "flow_rate_mld": 15.2,
    },
]

PUNE_LEAKS_DATA: List[Dict[str, Any]] = [
    {
        "id": "ALT-104",
        "pipeline_id": "P-104",
        "severity": "critical",
        "estimated_loss": "~42 m³/hr",
        "location": "Katraj Trunk Sector 4",
        "detection_time": "12m ago",
        "status": "active",
        "coordinates": [73.8550, 18.4650],
        "confidence": 0.94,
        "anomaly_type": "pipe_burst",
    },
    {
        "id": "ALT-089",
        "pipeline_id": "P-067",
        "severity": "high",
        "estimated_loss": "~18 m³/hr",
        "location": "Swargate DMA-3 Feeder",
        "detection_time": "35m ago",
        "status": "investigating",
        "coordinates": [73.8530, 18.4985],
        "confidence": 0.88,
        "anomaly_type": "joint_failure",
    },
    {
        "id": "ALT-062",
        "pipeline_id": "P-211",
        "severity": "moderate",
        "estimated_loss": "~8 m³/hr",
        "location": "Kothrud Depot Section B",
        "detection_time": "1h 14m ago",
        "status": "investigating",
        "coordinates": [73.8150, 18.5050],
        "confidence": 0.79,
        "anomaly_type": "slow_leak",
    },
]


class PuneNetworkBuilder:
    """Builds and provides topological and spatial access to Pune Water Distribution Network."""

    @classmethod
    def get_network_metadata(cls) -> Dict[str, Any]:
        return {
            "id": "c8a41280-9281-4f10-91b4-21950e436001",
            "name": "Pune Municipal Water Network (Central & Suburban DMAs)",
            "code": "PMC-NET-01",
            "description": "Synthetic hydraulic distribution model of Pune including Katraj, Kothrud, Shivajinagar, Swargate, and Hadapsar zones.",
            "srid": 4326,
            "center": [PUNE_CENTER_LNG, PUNE_CENTER_LAT],
        }

    @classmethod
    def get_nodes(cls) -> List[Dict[str, Any]]:
        return list(PUNE_NODES_DATA)

    @classmethod
    def get_pipes(cls) -> List[Dict[str, Any]]:
        return list(PUNE_PIPES_DATA)

    @classmethod
    def get_leaks(cls) -> List[Dict[str, Any]]:
        return list(PUNE_LEAKS_DATA)
