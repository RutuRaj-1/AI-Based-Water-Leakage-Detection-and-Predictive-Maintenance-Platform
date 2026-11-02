"""
Synthetic Pune-inspired water distribution network definition.

All geometry and asset attributes are SYNTHETIC and do not represent verified
Pune Municipal Corporation (PMC) infrastructure. Coordinates are
[longitude, latitude] (EPSG:4326, GeoJSON order).
"""

from __future__ import annotations

from dataclasses import dataclass, field

SYNTHETIC_DATA_NOTICE = (
    "SIMULATED DATA: Synthetic water distribution hydraulic geometry for Pune "
    "network demonstration and AI predictive maintenance testing. Coordinates "
    "and sensor telemetry do not represent verified Pune Municipal Corporation "
    "(PMC) infrastructure."
)

# Design service life (years) per pipe material class.
MATERIAL_LIFESPAN_YEARS: dict[str, float] = {
    "CI": 70.0,    # Cast iron
    "DI": 80.0,    # Ductile iron
    "MS": 50.0,    # Mild steel
    "PSC": 75.0,   # Prestressed concrete
    "HDPE": 100.0,
}

MATERIAL_LABEL: dict[str, str] = {
    "CI": "Cast Iron",
    "DI": "Ductile Iron",
    "MS": "Mild Steel",
    "PSC": "Prestressed Concrete",
    "HDPE": "HDPE",
}


@dataclass(frozen=True)
class PipeSpec:
    id: str
    name: str
    location: str            # human readable location used on alerts
    zone: str
    material_class: str      # key of MATERIAL_LIFESPAN_YEARS
    diameter_mm: int
    age_years: float
    corrosion_index: float   # 0 (pristine) .. 1 (severely corroded)
    length_km: float
    base_pressure_bar: float
    base_flow_mld: float
    from_node: str
    to_node: str
    coordinates: tuple[tuple[float, float], ...] = field(default_factory=tuple)

    @property
    def material(self) -> str:
        return f"{MATERIAL_LABEL[self.material_class]} ({self.material_class} {self.diameter_mm}mm)"


@dataclass(frozen=True)
class NodeSpec:
    id: str
    name: str
    node_type: str           # reservoir | pump | junction | treatment_plant
    zone: str
    base_pressure_bar: float
    elevation_m: float
    base_demand_lps: float
    coordinate: tuple[float, float]


@dataclass(frozen=True)
class PumpSpec:
    id: str
    name: str
    zone: str
    rating: str
    age_years: float
    wear_index: float        # 0..1 mechanical wear
    base_health: float


PIPES: tuple[PipeSpec, ...] = (
    PipeSpec("P-104", "Katraj Feeder Main (P-104)", "Katraj Trunk Sector 4", "Zone 4 — Katraj",
             "CI", 300, 38, 0.90, 6.8, 1.9, 28.4, "J-SWARGATE", "RES-KATRAJ",
             ((73.858, 18.5018), (73.861, 18.479), (73.855, 18.465), (73.856, 18.4485))),
    PipeSpec("P-042", "Shivajinagar Sub-main (P-042)", "Shivajinagar Sub-main", "Zone 1 — Central",
             "DI", 250, 29, 0.80, 4.2, 2.3, 19.2, "J-SWARGATE", "J-SHIVAJINAGAR",
             ((73.8585, 18.5025), (73.844, 18.52), (73.852, 18.5315))),
    PipeSpec("P-067", "Swargate DMA-3 Feeder (P-067)", "Swargate DMA-3 Feeder", "Zone 3 — Swargate DMA",
             "MS", 350, 24, 0.60, 2.1, 3.1, 24.1, "RES-PARVATI", "PS-05",
             ((73.8474, 18.4975), (73.853, 18.4985), (73.858, 18.5018))),
    PipeSpec("P-088", "Hadapsar Distribution (P-088)", "Hadapsar Distribution Line", "Zone 7 — Hadapsar",
             "MS", 200, 22, 0.85, 7.6, 2.7, 14.5, "J-SWARGATE", "J-HADAPSAR",
             ((73.8585, 18.5025), (73.892, 18.498), (73.928, 18.502))),
    PipeSpec("P-211", "Kothrud West Arterial (P-211)", "Kothrud West Arterial", "Zone 2 — Kothrud",
             "DI", 250, 18, 0.35, 4.8, 3.2, 18.0, "RES-PARVATI", "J-KOTHRUD",
             ((73.8474, 18.4975), (73.828, 18.503), (73.815, 18.505), (73.808, 18.5075))),
    PipeSpec("P-015", "Cantonment Main Trunk (P-015)", "Cantonment Main Trunk", "Zone 5 — Cantonment",
             "PSC", 500, 8, 0.10, 6.1, 4.2, 42.0, "RES-PARVATI", "J-CANTONMENT",
             ((73.8474, 18.4975), (73.878, 18.514), (73.893, 18.536))),
    PipeSpec("P-033", "Aundh-Baner Feeder (P-033)", "Aundh-Baner Feeder", "Zone 6 — Aundh/Baner",
             "DI", 350, 11, 0.15, 5.9, 3.7, 26.5, "J-SHIVAJINAGAR", "RES-CHATURSHRINGI",
             ((73.852, 18.5315), (73.829, 18.537), (73.805, 18.56))),
    PipeSpec("P-050", "Viman Nagar Primary Main (P-050)", "Viman Nagar Primary Main", "Zone 8 — Viman Nagar",
             "DI", 300, 9, 0.12, 5.3, 3.5, 21.0, "J-CANTONMENT", "J-VIMANNAGAR",
             ((73.893, 18.536), (73.902, 18.548), (73.914, 18.567))),
    PipeSpec("P-101", "Sinhagad Main Feed Branch (P-101)", "Sinhagad Main Feed Branch", "Zone 2 — Sinhagad Road",
             "CI", 300, 27, 0.55, 3.9, 3.0, 22.5, "RES-PARVATI", "J-SINHAGAD",
             ((73.8474, 18.4975), (73.83, 18.482), (73.815, 18.468))),
    PipeSpec("P-130", "Pashan Link Main (P-130)", "Pashan Link Main", "Zone 6 — Pashan",
             "HDPE", 250, 6, 0.05, 4.1, 3.6, 15.2, "RES-CHATURSHRINGI", "J-PASHAN",
             ((73.829, 18.537), (73.81, 18.538), (73.79, 18.537))),
    PipeSpec("P-140", "Kharadi Distribution (P-140)", "Kharadi Distribution Line", "Zone 9 — Kharadi",
             "DI", 250, 12, 0.20, 3.8, 3.3, 16.8, "J-VIMANNAGAR", "J-KHARADI",
             ((73.914, 18.567), (73.928, 18.558), (73.94, 18.551))),
    PipeSpec("P-150", "Kondhwa Feeder (P-150)", "Kondhwa Feeder Line", "Zone 10 — Kondhwa",
             "CI", 250, 33, 0.70, 4.6, 2.8, 17.4, "J-SWARGATE", "J-KONDHWA",
             ((73.8585, 18.5025), (73.88, 18.48), (73.89, 18.465))),
    PipeSpec("P-175", "Yerawada Sub-main (P-175)", "Yerawada Sub-main", "Zone 5 — Yerawada",
             "MS", 200, 19, 0.45, 3.3, 3.4, 12.6, "J-CANTONMENT", "J-YERAWADA",
             ((73.893, 18.536), (73.88, 18.555), (73.875, 18.565))),
)

NODES: tuple[NodeSpec, ...] = (
    NodeSpec("RES-PARVATI", "Parvati WTP & Master Reservoir", "treatment_plant", "Central Water Works", 4.8, 570, 450, (73.8474, 18.4975)),
    NodeSpec("RES-KATRAJ", "Katraj Elevated Storage Reservoir", "reservoir", "Zone 4 — Katraj", 3.2, 615, 220, (73.856, 18.4485)),
    NodeSpec("RES-CHATURSHRINGI", "Chaturshringi High Reservoir", "reservoir", "Zone 6 — Aundh/Baner", 3.9, 595, 180, (73.829, 18.537)),
    NodeSpec("PS-01", "Parvati Intake Pumping PS-01", "pump", "Parvati WTP", 5.1, 566, 300, (73.8465, 18.496)),
    NodeSpec("PS-02", "Parvati High-Lift Pump PS-02", "pump", "Parvati WTP", 5.4, 568, 320, (73.8485, 18.499)),
    NodeSpec("PS-05", "Swargate Booster Station PS-05", "pump", "Zone 3 — Swargate DMA", 4.1, 555, 210, (73.858, 18.5018)),
    NodeSpec("J-SWARGATE", "Swargate Main Junction", "junction", "Zone 3 — Swargate DMA", 3.8, 554, 120, (73.8585, 18.5025)),
    NodeSpec("J-SHIVAJINAGAR", "Shivajinagar Interconnect", "junction", "Zone 1 — Central", 3.5, 552, 140, (73.852, 18.5315)),
    NodeSpec("J-HADAPSAR", "Hadapsar Terminal Junction", "junction", "Zone 7 — Hadapsar", 3.1, 550, 160, (73.928, 18.502)),
    NodeSpec("J-KOTHRUD", "Kothrud West Junction", "junction", "Zone 2 — Kothrud", 3.4, 565, 130, (73.808, 18.5075)),
    NodeSpec("J-CANTONMENT", "Cantonment Interchange", "junction", "Zone 5 — Cantonment", 4.0, 556, 150, (73.893, 18.536)),
    NodeSpec("J-VIMANNAGAR", "Viman Nagar Terminal Junction", "junction", "Zone 8 — Viman Nagar", 3.4, 553, 125, (73.914, 18.567)),
    NodeSpec("J-SINHAGAD", "Sinhagad Road Junction", "junction", "Zone 2 — Sinhagad Road", 3.0, 575, 95, (73.815, 18.468)),
    NodeSpec("J-PASHAN", "Pashan Terminal Junction", "junction", "Zone 6 — Pashan", 3.5, 590, 85, (73.79, 18.537)),
    NodeSpec("J-KHARADI", "Kharadi Terminal Junction", "junction", "Zone 9 — Kharadi", 3.2, 548, 110, (73.94, 18.551)),
    NodeSpec("J-KONDHWA", "Kondhwa Terminal Junction", "junction", "Zone 10 — Kondhwa", 2.9, 580, 105, (73.89, 18.465)),
    NodeSpec("J-YERAWADA", "Yerawada Terminal Junction", "junction", "Zone 5 — Yerawada", 3.3, 551, 90, (73.875, 18.565)),
)

PUMPS: tuple[PumpSpec, ...] = (
    PumpSpec("PS-01", "Parvati Intake Pumping PS-01", "Parvati WTP", "Centrifugal 75kW", 9, 0.30, 84),
    PumpSpec("PS-02", "Parvati High-Lift Pump PS-02", "Parvati WTP", "Centrifugal 45kW", 14, 0.72, 46),
    PumpSpec("PS-05", "Swargate Booster Station PS-05", "Zone 3 — Swargate DMA", "Booster 30kW", 11, 0.50, 71),
)

