# Pune Water Network AI — Backend Architecture, Implementation & Handover Guide

> **Project:** Pune Water Network AI (C-DAC Industry Project)  
> **Backend Contributors:** Sanskar, Shardul, Ruturaj  
> **Target Branch:** `backend`  
> **Tech Stack:** Python 3.11+ | FastAPI | PostgreSQL 16 + PostGIS 3 | SQLAlchemy 2.0 (Async) | Scikit-Learn | GeoJSON | Pytest  
> **Status:** ✅ Core System 100% Implemented & Tested (19/19 Tests Passing)  

---

## 1. Executive Summary

The **Pune Water Network AI** backend is an intelligent hydraulic simulation, AI leak detection, and predictive maintenance platform designed for municipal water distribution networks (modeled on the Pune Municipal Corporation / PMC DMAs).

It provides:
1. **Dynamic Hydraulic Simulation**: 24-hour diurnal water consumption cycles with real-time pressure and flow calculations across key Pune zones (Katraj, Kothrud, Shivajinagar, Swargate, Hadapsar, Cantonment, Aundh/Baner, Vadgaon Sheri).
2. **AI/ML Leak Detection Engine**: Dual-layer detection combining diurnal residual Z-Score statistics ($> 2.8\sigma$) with multi-feature **Scikit-Learn Isolation Forest** vectors to detect bursts and subtle joint leaks.
3. **Composite Pipeline Health Scoring (0–100 Index)**: Multidimensional asset integrity algorithm evaluating pipe age, material vulnerability, diurnal pressure fatigue, and historical anomaly penalties.
4. **Predictive Maintenance Priority Matrix**: Logistic failure hazard model prioritizing repair work orders (`WO-2026-001`, etc.) by criticality, diameter, and risk score.
5. **GeoJSON GIS Layer Services**: RFC 7946 compliant GeoJSON FeatureCollections directly consumed by the frontend **React-Leaflet** interactive map.

---

## 2. Directory Structure & Architecture

```text
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── health.py               # Service operational health & version
│   │       │   ├── gis.py                  # GeoJSON endpoints for Leaflet (/gis/pipes, /gis/nodes, /gis/leaks)
│   │       │   ├── networks.py             # Water network zones & DMA listings
│   │       │   ├── pipes.py                # Asset inventory, single pipe details, time-series, health breakdown
│   │       │   ├── observations.py         # Pressure & flow sensor readings
│   │       │   ├── anomalies.py            # Detected leak events & status updates (active, investigating, resolved)
│   │       │   ├── health_assessments.py   # Composite health score history (0-100 index)
│   │       │   ├── predictions.py          # Failure probability & risk forecast (90-day horizon)
│   │       │   ├── maintenance.py          # Prioritised repair work orders & team dispatch
│   │       │   └── simulations.py          # Trigger hydraulic simulations & real-time telemetry
│   │       └── router.py                   # Aggregates and mounts all v1 endpoints under /api/v1
│   ├── core/
│   │   ├── config.py                       # Pydantic settings & environment configuration (.env)
│   │   └── logging.py                      # Application logging
│   ├── db/
│   │   ├── base.py                         # SQLAlchemy DeclarativeBase & UTC TimestampMixin
│   │   ├── session.py                      # Async database engine & sessionmaker (PostGIS + SQLite fallback)
│   │   └── models/                         # ORM Models (PostgreSQL / SQLite compatible)
│   │       ├── network.py                  # Network zone container
│   │       ├── node.py                     # Junctions, high-lift pumps, elevated reservoirs
│   │       ├── pipe.py                     # Pipeline segments with LineString geometries & health attributes
│   │       ├── sensor.py                   # Pressure & acoustic flow sensors
│   │       ├── observation.py              # Time-series telemetry readings
│   │       ├── anomaly.py                  # Detected bursts and leaks
│   │       ├── health.py                   # Health assessment score records
│   │       ├── maintenance.py              # Work order maintenance recommendations
│   │       └── simulation.py               # Simulation run executions
│   ├── ml/
│   │   ├── anomaly_detector.py             # Residual Z-Score + Isolation Forest leak detector
│   │   ├── health_scorer.py                # Composite 0-100 pipeline health index calculation
│   │   └── risk_predictor.py               # Logistic failure probability & maintenance priority ranker
│   ├── repositories/                       # Data access abstractions (pre-seeded with Pune network state)
│   │   ├── network_repo.py
│   │   ├── pipe_repo.py
│   │   ├── observation_repo.py
│   │   ├── anomaly_repo.py
│   │   ├── maintenance_repo.py
│   │   └── simulation_repo.py
│   ├── schemas/                            # Pydantic V2 validation schemas (matches frontend types)
│   │   ├── common.py                       # Pagination & Error response schemas
│   │   ├── gis.py                          # GeoJSON FeatureCollection, LineString, and Point schemas
│   │   ├── pipe.py                         # Pipeline inventory & detailed schemas
│   │   ├── anomaly.py                      # Anomaly & LeakAlert schemas
│   │   ├── maintenance.py                  # MaintenanceTask schemas
│   │   ├── simulation.py                   # SimulationRun & SimulationTelemetry schemas
│   │   ├── observation.py                  # TimeSeriesPoint telemetry schemas
│   │   ├── health.py                       # HealthAssessment & RiskPrediction schemas
│   │   └── network.py                      # Network DMA schemas
│   ├── simulation/
│   │   ├── network_builder.py              # Pune DMA topological graph with exact EPSG:4326 coordinates
│   │   ├── scenarios.py                    # Pune 24h diurnal demand multiplier & failure scenario configurations
│   │   └── engine.py                       # Hydraulic solver computing pressure, flow, and transients
│   ├── workers/
│   │   └── simulation_worker.py            # End-to-end simulation -> ML detection -> health updates pipeline
│   └── main.py                             # FastAPI application factory & CORS configuration
├── scripts/
│   ├── seed_pune_network.py                # Database seeder populating all nodes, pipes, and leaks
│   └── run_simulation.py                   # CLI runner executing hydraulic simulation scenarios
├── tests/
│   ├── integration/
│   │   ├── test_gis_endpoints.py           # GeoJSON API endpoint tests
│   │   └── test_pipes_and_anomalies.py     # Pipes, anomalies, maintenance, and telemetry tests
│   └── unit/
│       ├── test_health.py                  # Base health check tests
│       ├── test_ml.py                      # Isolation Forest, health scorer, and risk predictor tests
│       └── test_simulation.py              # Diurnal cycle, network builder, and hydraulic solver tests
├── pyproject.toml
└── requirements.txt
```

---

## 3. What Has Been Done (Completed Features)

### 3.1. Frontend Contract Handshake
- The backend schemas were built to **directly match the frontend TypeScript contracts** (`frontend/src/types/dashboard.ts` and `frontend/src/data/puneSyntheticNetworkGeoJSON.ts` developed by Bhargavi).
- GeoJSON endpoints (`/api/v1/gis/pipes`, `/api/v1/gis/nodes`, `/api/v1/gis/leaks`) output exact RFC 7946 coordinates and properties (`diameterMm`, `healthScore`, `condition`, `pressureBar`, `flowRateMld`), allowing instant rendering in the React-Leaflet dashboard.

### 3.2. Hydraulic Simulation & Diurnal Modeling
- **Diurnal Multipliers**:
  - `00:00 - 05:00`: 0.30× (Low night flow / minimum night flow analysis)
  - `06:00 - 09:30`: 1.80× (Morning peak extraction)
  - `10:00 - 17:00`: 0.90× (Afternoon steady commercial demand)
  - `18:00 - 21:30`: 1.50× (Evening peak demand)
- **Scenarios Supported**:
  - `normal`: Clean baseline diurnal cycle.
  - `pipe_burst`: Major rupture on Katraj Feeder `P-104` with sudden 40–50 kPa pressure drop and localized flow surge.
  - `slow_leak`: Subtle joint gasket degradation on Kothrud `P-211` with elevated night flow.
  - `demand_surge`: 1.65× abnormal peak demand simulating summer heatwaves.
  - `blockage`: Valve throttled on Shivajinagar `P-042` with backpressure and downstream starvation.

### 3.3. AI/ML Analytics Core
- **Anomaly Detection**: Combines statistical diurnal residual deviation ($Z = \frac{P_{actual} - P_{expected}}{\sigma} < -2.8$) with Isolation Forest multi-feature vectors `[pressure, flow, delta_P]`.
- **Composite Pipeline Health Score (0–100 Index)**:
  $$\text{Health Score} = 100 - (\text{MaterialRisk} + \text{AgeFactor} + \text{PressureStress} + \text{AnomalyPenalty})$$
  - *Material Risk*: Cast Iron (CI): 25 pts, Mild Steel (MS): 15 pts, PVC: 15 pts, Ductile Iron (DI): 8 pts, HDPE/PSC: 5 pts.
  - *Age Factor*: $(\text{Current Year} - \text{Installed}) \times 0.60$ (capped at 30 pts).
  - *Pressure Stress*: Diurnal transient swings / water hammer (capped at 20 pts).
  - *Anomaly Penalty*: Active/recent leaks $\times 15$ pts (capped at 25 pts).
- **Maintenance Priority Ranking**:
  $$\text{Priority Score} = (100 - \text{Health Score}) \times \text{Criticality Multiplier} + \text{Leak Severity Weight}$$
  Trunk mains ($\ge 350\text{mm}$) receive a $1.45\times$ criticality multiplier over distribution lines. Work orders are generated with INR cost estimates, recommended actions, and due dates.

### 3.4. Dual-Mode Database Resilience
- Configured for **PostgreSQL 16 + PostGIS 3** in production/Docker (`docker-compose.yml`).
- Includes automatic fallback to an async SQLite database (`aiosqlite`) when Docker is offline, allowing immediate zero-setup execution and local testing.

---

## 4. How to Run, Test & Seed

### 4.1. Run the Backend API Server
```powershell
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- **Interactive Swagger Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative ReDoc UI**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 4.2. Run the Automated Test Suite
```powershell
cd backend
pytest tests/ -v
```
*Current test result: 19 passed, 0 failures.*

### 4.3. Run CLI Simulation Scenarios
```powershell
cd backend
# Run a pipe burst simulation:
python scripts/run_simulation.py --scenario pipe_burst --hours 24

# Run a slow joint leak simulation:
python scripts/run_simulation.py --scenario slow_leak --hours 24
```

### 4.4. Seed the Database
```powershell
cd backend
python scripts/seed_pune_network.py
```

---

## 5. What More Can Be Done (Roadmap for the Next Developer)

Here is a prioritised list of high-value enhancements for the next developer joining this project:

### 🌟 1. Real EPANET Network `.inp` File Import
- **Current State:** Network topology is built synthetically via `PuneNetworkBuilder` based on Pune coordinates.
- **Next Step:** Implement an EPANET file parser using `wntr.network.WaterNetworkModel` to import official `.inp` hydraulic network model files directly exported from AutoCAD / GIS by PMC engineers.

### 🌟 2. WebSocket Streaming for Live Telemetry
- **Current State:** Telemetry and observations are queried via standard REST endpoints (`/api/v1/simulations/telemetry`, `/api/v1/pipes/{id}/observations`).
- **Next Step:** Add a FastAPI WebSocket endpoint (`/api/v1/ws/telemetry`) that pushes 1-second or 5-second live sensor ticks to the frontend, allowing the Leaflet map to animate pressure waves and leak pulses in real time.

### 🌟 3. Graph Neural Networks (GNN) for Spatial Leak Localization
- **Current State:** Leak detection uses Isolation Forest and residual Z-score per pipe.
- **Next Step:** Train a Graph Convolutional Network (GCN / PyTorch Geometric) where junctions are nodes and pipes are edges. GNNs can predict the exact spatial coordinate along a pipe where a rupture occurred based on pressure sensor gradients at adjacent junctions.

### 🌟 4. Celery & Redis Task Queue
- **Current State:** Hydraulic simulations run synchronously or via lightweight async tasks in `simulation_worker.py`.
- **Next Step:** For large-scale networks with thousands of junctions (e.g. 5,000+ pipes), connect Celery with a Redis broker to distribute 72-hour hydraulic simulations across worker processes without blocking API request threads.

### 🌟 5. Automated Alert Notifications (SMS / WhatsApp / Email)
- **Current State:** When an anomaly is detected, it is saved in the database and visible in `/api/v1/anomalies`.
- **Next Step:** Integrate Twilio or Fast2SMS / SendGrid in `simulation_worker.py` to automatically dispatch SMS alerts to the assigned PMC Quick Response Team when an anomaly has `severity == "critical"`.

### 🌟 6. User Authentication & Role-Based Access Control (RBAC)
- **Current State:** Open development endpoints without authentication.
- **Next Step:** Add JWT token authentication (`OAuth2PasswordBearer` in FastAPI):
  - **PMC Admin:** Can trigger simulations, create pipelines, and update network models.
  - **Field Engineer:** Can view alerts and update work order statuses (`in_progress`, `completed`).
  - **Executive Viewer:** Read-only access to GIS dashboard and telemetry summaries.

---

## 6. Daily Git Workflow

When committing your work:
```powershell
# 1. Check changed files
git status

# 2. Stage backend files
git add backend/ BACKEND_HANDOVER.md .gitignore

# 3. Commit
git commit -m "feat(backend): <describe your feature>"

# 4. Push to backend branch
git push origin backend
```
