# Database Design — Pune Water Network AI

> **Status:** Planned. The entities and relationships described here are design proposals. No Alembic migrations implementing this schema have been created yet. The schema will evolve during Stage 2 development.

**Owner:** Ruturaj  
**Technology:** PostgreSQL 16 + PostGIS 3, SQLAlchemy (async), Alembic

---

## Entity Overview

| Entity | Table Name | Purpose |
|--------|-----------|---------|
| Network | `networks` | Top-level container for a water distribution network (e.g., a named Pune zone) |
| Node | `nodes` | Junctions, reservoirs, and tanks in the network graph |
| Pipe | `pipes` | Pipe segments connecting nodes |
| Sensor | `sensors` | Logical sensor definitions attached to nodes or pipes |
| Observation | `observations` | Time-series pressure/flow readings from sensors |
| Anomaly | `anomalies` | Detected anomalous events with severity and confidence |
| HealthAssessment | `health_assessments` | Composite health score per pipe per assessment run |
| RiskPrediction | `risk_predictions` | Failure probability estimate per pipe for a planning horizon |
| MaintenanceRecommendation | `maintenance_recommendations` | Ranked work orders derived from risk predictions |
| SimulationRun | `simulation_runs` | Metadata for each hydraulic simulation execution |

---

## Planned Entity Relationships

```
networks 1──* nodes
networks 1──* pipes
nodes    1──* sensors
pipes    1──* sensors
sensors  1──* observations
pipes    1──* anomalies        (via observations FK)
pipes    1──* health_assessments
pipes    1──* risk_predictions
risk_predictions 1──1 maintenance_recommendations
simulation_runs  1──* observations
```

---

## Key Entity Descriptions

### `networks`

Represents a named water distribution network or zone.

| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| name | TEXT | e.g., "Pune Zone A (Synthetic)" |
| description | TEXT | |
| srid | INTEGER | Spatial reference ID (e.g., 4326 = WGS84) |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

### `nodes`

Network junctions, source reservoirs, and tanks.

| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| network_id | UUID FK → networks | |
| node_type | ENUM | `junction`, `reservoir`, `tank` |
| label | TEXT | Human-readable label |
| elevation_m | FLOAT | Elevation in metres |
| location | GEOMETRY(Point, 4326) | PostGIS spatial point |
| attributes | JSONB | Extensible metadata |

### `pipes`

Pipe segments connecting pairs of nodes.

| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| network_id | UUID FK → networks | |
| start_node_id | UUID FK → nodes | |
| end_node_id | UUID FK → nodes | |
| label | TEXT | |
| length_m | FLOAT | |
| diameter_mm | FLOAT | |
| material | TEXT | e.g., "CI", "PVC", "DI" |
| roughness | FLOAT | Hazen-Williams or Darcy-Weisbach coefficient |
| installation_year | INTEGER | |
| geometry | GEOMETRY(LineString, 4326) | PostGIS linestring |
| attributes | JSONB | Extensible metadata |

### `observations`

Time-series pressure and flow readings (real or synthetic).

| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| sensor_id | UUID FK → sensors | |
| simulation_run_id | UUID FK → simulation_runs | nullable; null = real reading |
| observed_at | TIMESTAMPTZ | Index candidate |
| pressure_kpa | FLOAT | nullable |
| flow_lps | FLOAT | nullable (litres per second) |
| quality_flag | SMALLINT | 0=ok, 1=suspect, 2=bad |

> **Note:** If the volume of observations grows large, partitioning by `observed_at` (range partitioning) or adopting the TimescaleDB extension will be evaluated.

### `anomalies`

| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| pipe_id | UUID FK → pipes | |
| detected_at | TIMESTAMPTZ | |
| anomaly_type | TEXT | e.g., `pressure_drop`, `flow_surge` |
| severity | ENUM | `low`, `medium`, `high`, `critical` |
| confidence | FLOAT | Model confidence 0.0–1.0 |
| details | JSONB | Raw model output, feature values |

### `health_assessments`

| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| pipe_id | UUID FK → pipes | |
| assessed_at | TIMESTAMPTZ | |
| health_score | FLOAT | 0 (failed) – 100 (perfect) |
| component_scores | JSONB | Breakdown by contributing factor |

### `risk_predictions`

| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| pipe_id | UUID FK → pipes | |
| predicted_at | TIMESTAMPTZ | |
| horizon_days | INTEGER | Planning horizon for the prediction |
| failure_probability | FLOAT | 0.0–1.0 |
| model_version | TEXT | |

### `maintenance_recommendations`

| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| risk_prediction_id | UUID FK → risk_predictions | |
| pipe_id | UUID FK → pipes | |
| priority_rank | INTEGER | Lower = higher priority |
| recommended_action | TEXT | e.g., `inspect`, `repair`, `replace` |
| estimated_cost_inr | FLOAT | Estimated cost in Indian Rupees |
| status | ENUM | `open`, `in_progress`, `completed`, `deferred` |
| created_at | TIMESTAMPTZ | |

---

## Open Questions / Decisions Pending

- [ ] UUID vs BIGSERIAL for primary keys — UUIDs aid eventual distribution; BIGSERIAL is simpler for a single-node deployment
- [ ] TimescaleDB vs plain partitioned tables for `observations`
- [ ] Should `anomalies` reference `observations` directly (M2M) or link only to `pipes`?
- [ ] SRID strategy — store all geometries in WGS84 (4326) or a local projected CRS (e.g., EPSG:32643 for Pune)?
- [ ] Soft-delete vs hard-delete for network entities
- [ ] Audit logging strategy (separate audit table vs `updated_at` / `created_by` columns)
