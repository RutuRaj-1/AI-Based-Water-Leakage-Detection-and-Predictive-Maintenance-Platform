# Simulation Design — Pune Water Network AI

> **Status:** Planned. This document describes the intended hydraulic simulation approach. No simulation code has been implemented yet.

**Lead:** Sanskar

---

## Purpose

The hydraulic simulation engine is responsible for generating realistic synthetic pressure and flow data for the Pune water distribution network. This data serves as the primary input to the AI/ML analysis pipeline.

---

## Planned Approach

### Simulation Software

Two candidates are under evaluation:

| Option | Pros | Cons |
|--------|------|------|
| **WNTR (Water Network Tool for Resilience)** | Python-native, active development, leak scenario support | Requires EPANET solver dependency |
| **EPANET CLI** via `epynet` | Industry-standard solver | Less Pythonic interface |

**Decision pending.** WNTR is currently preferred due to native Python integration and built-in resilience analysis tools.

---

## Network Topology

### Current Status

No verified Pune municipal pipeline network geometry has been confirmed available under an open licence. The team will:

1. Evaluate AIKosh, PMC Open Data, Smart Cities Mission portals for network GIS data.
2. If no suitable dataset is found, construct a **synthetic Pune-inspired network** — a plausible tree/loop graph representing district metered areas (DMAs) in zones such as Kothrud, Shivajinagar, or Hadapsar.

### Topology Requirements

- Minimum: ~200 pipe segments and ~150 junctions for meaningful ML training
- Include: source reservoirs, elevated storage tanks, demand nodes
- Spatial embedding in WGS84 coordinates within Pune city bounds

---

## Scenario Types (Planned)

| Scenario | Description |
|----------|-------------|
| Normal operation | Baseline demand patterns (diurnal cycle, seasonal variation) |
| Pipe burst | Sudden large-flow leak at a node |
| Background leakage | Small, slow leak simulated by increased emitter coefficient |
| Demand surge | Unexpected peak demand (e.g., festival, water rationing end) |
| Partial blockage | Increased pipe roughness reducing flow |

---

## Output Data

Each simulation run produces time-series readings for every sensor location:

| Signal | Unit | Description |
|--------|------|-------------|
| Pressure | kPa | Hydraulic pressure at node |
| Flow | L/s | Volumetric flow rate at pipe |
| Head | m | Hydraulic head at node |
| Velocity | m/s | Flow velocity in pipe |

---

## Decisions Pending

- [ ] WNTR vs EPANET CLI final selection
- [ ] Network topology source (real GIS vs synthetic)
- [ ] Time-step granularity (5-min, 15-min, 1-hour)
- [ ] Number of simulation scenarios for initial ML training dataset
- [ ] Leak injection methodology and labelling strategy
- [ ] Integration with the background worker queue
