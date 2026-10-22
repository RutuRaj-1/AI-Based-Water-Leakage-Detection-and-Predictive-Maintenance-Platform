# Pune Water Network AI

**AI-Based Water Distribution Network Leakage Detection and Predictive Asset Management Platform**

> ⚠️ **Status: Foundation / Repository Initialisation**
> This repository contains the project scaffold and architecture documentation only.
> The complete product has **not** yet been implemented. See [Implementation Status](#implementation-status) for details.

---

## Overview

Pune Water Network AI is a software-only platform designed to simulate Pune's water distribution network, detect pressure and flow anomalies that may indicate leaks, calculate Pipeline Health Scores, estimate failure risk, and prioritise maintenance work orders — all displayed through an interactive GIS dashboard.

The project targets Pune, Maharashtra, India and relies entirely on hydraulic software simulation and synthetic/open datasets. **No physical sensor hardware integration is required.**

---

## Objectives

| # | Objective |
|---|-----------|
| 1 | Simulate water distribution network pressure and flow using hydraulic modelling software |
| 2 | Detect anomalies associated with potential pipe leaks using AI/ML algorithms |
| 3 | Calculate a composite **Pipeline Health Score** for each pipe segment |
| 4 | Estimate **failure risk probability** using predictive models |
| 5 | Prioritise maintenance work orders by risk, cost, and impact |
| 6 | Provide an interactive **GIS dashboard** for network visualisation and operations |

---

## Scope

- **Geographic focus:** Pune Municipal Corporation water supply network (simulated)
- **Data source:** Software-generated synthetic data; open government/academic datasets where available and licensed
- **No hardware:** Pure software simulation — no IoT sensors, SCADA, or physical telemetry integration
- **No real-time operations:** The MVP uses batch simulation; live data ingestion is a future phase

---

## Technology Stack

### Frontend
| Tool | Purpose |
|------|---------|
| React 18 + TypeScript | Component framework |
| Vite | Build tool and dev server |
| Tailwind CSS | Utility-first styling |
| React Router v6 | Client-side routing |
| React-Leaflet / Leaflet | GIS map visualisation |
| Recharts | Charts and time-series visualisation |
| Vitest + React Testing Library | Unit and component testing |

### Backend
| Tool | Purpose |
|------|---------|
| Python 3.11+ | Primary language |
| FastAPI | Async REST API framework |
| Pydantic v2 | Data validation and settings |
| SQLAlchemy (async) | ORM and database abstraction |
| PostgreSQL 16 + PostGIS 3 | Relational DB with geospatial support |
| Alembic | Database migrations |
| pytest + pytest-asyncio | Backend testing |

### Infrastructure (local development)
| Tool | Purpose |
|------|---------|
| Docker + Docker Compose | Local database service |
| GitHub Actions | CI/CD (planned) |

---

## Repository Structure

```
CDAC/
├── frontend/           # React + Vite application (Bhargavi)
├── backend/            # FastAPI application (Sanskar, Shardul)
├── shared/
│   ├── api-contract/   # OpenAPI specification (Ruturaj)
│   └── schemas/        # Shared JSON Schema definitions
├── docs/               # Architecture, design, and workflow documents
├── data/
│   ├── raw/            # Source datasets (NOT committed)
│   ├── processed/      # Cleaned datasets (NOT committed)
│   └── synthetic/      # Generated simulation data (NOT committed)
├── infra/
│   ├── docker/         # Dockerfile and init scripts
│   └── scripts/        # Utility scripts
├── tests/              # Root-level integration / E2E tests
├── .github/workflows/  # CI/CD pipeline definitions
├── .gitignore
├── .gitattributes
├── .editorconfig
├── .env.example
├── docker-compose.yml
├── LICENSE
└── README.md
```

---

## Team

| Member | Role | Primary Responsibilities |
|--------|------|--------------------------|
| **Ruturaj** | Team Lead | Database architecture, shared API contracts, frontend-backend integration, release coordination |
| **Sanskar** | Backend Dev | Hydraulic simulation, network data processing, backend services |
| **Shardul** | Backend Dev (AI/ML) | Anomaly detection, Pipeline Health Scoring, failure-risk estimation, maintenance prioritisation |
| **Bhargavi** | Frontend Dev | Dashboard, charts, GIS visualisation, API integration |

> Every team member participates in code reviews, testing, debugging, and integration.

---

## Planned Development Stages

### Stage 1 — Foundation (Current)
- [x] Repository structure and configuration
- [x] Minimal FastAPI app with health endpoint
- [x] Minimal React + Vite app scaffold
- [x] OpenAPI contract skeleton
- [x] Database design documentation
- [ ] Create `frontend` and `backend` branches from `main`

### Stage 2 — Simulation and Data
- [ ] Define network topology (synthetic Pune-inspired graph)
- [ ] Implement hydraulic simulation engine integration (EPANET/WNTR or equivalent)
- [ ] Design and populate synthetic sensor observation dataset
- [ ] Database schema implementation and initial migrations
- [ ] Dataset evaluation (AIKosh, CWRIS, NRSC, PMC open data)

### Stage 3 — AI/ML Core
- [ ] Anomaly detection model (leak signature identification)
- [ ] Pipeline Health Score algorithm
- [ ] Failure risk estimation model
- [ ] Maintenance prioritisation logic

### Stage 4 — API and Integration
- [ ] Full API implementation (networks, pipelines, observations, anomalies, health, predictions, maintenance)
- [ ] Frontend-backend integration
- [ ] GIS feature service

### Stage 5 — Dashboard and Polish
- [ ] Interactive Leaflet map with pipeline layer
- [ ] Real-time anomaly alerts panel
- [ ] Pipeline health heat map
- [ ] Maintenance work-order management view
- [ ] Charts: pressure/flow trends, risk distributions

### Stage 6 — Testing and Deployment
- [ ] Full test coverage (unit, integration, E2E)
- [ ] CI/CD pipeline
- [ ] Docker production configuration
- [ ] Final documentation and demo

---

## Dataset Strategy

No verified Pune-specific municipal pipeline telemetry or official network geometry has been confirmed as available or licensed. The project will:

1. **Evaluate publicly accessible datasets** — AIKosh, CWRIS (Central Water Resources Information System), NRSC, Smart Cities Mission portals, PMC open data releases.
2. **Maintain a Dataset Register** (`docs/dataset-register.md`) with provenance, license, and data-quality notes for every dataset examined or used.
3. **Generate synthetic data** if real telemetry is unavailable or not licensed for use — using hydraulic modelling software to produce realistic pressure/flow traces.
4. **Never fabricate real infrastructure data.** Synthetic data will be clearly labelled as synthetic.

---

## Local Setup

### Prerequisites

| Tool | Minimum Version |
|------|----------------|
| Node.js | 18+ |
| Python | 3.11+ |
| Docker Desktop | any recent version |
| Git | 2.x |

### 1. Clone and configure environment

```bash
git clone https://github.com/RutuRaj-1/AI-Based-Water-Leakage-Detection-and-Predictive-Maintenance-Platform.git
cd AI-Based-Water-Leakage-Detection-and-Predictive-Maintenance-Platform

# Copy environment template
cp .env.example .env
# Edit .env with your local values (see .env.example for descriptions)
```

### 2. Start the database

```bash
docker compose up -d db
# Wait for the health check to pass (about 10 s on first run)
```

### 3. Start the backend (minimal health endpoint)

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy backend env example
cp .env.example .env

# Start the dev server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Health check: `GET http://localhost:8000/api/v1/health`

### 4. Start the frontend (minimal scaffold)

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Open: `http://localhost:5173`

---

## Git Branching Strategy

See [`docs/git-workflow.md`](docs/git-workflow.md) for the full workflow.

```
main            ← stable foundation (this branch)
 ├── frontend   ← all frontend development (Bhargavi)
 └── backend    ← all backend development (Sanskar, Shardul)
```

Feature work happens on short-lived feature branches cut from `frontend` or `backend`, then merged back via pull requests.

---

## Implementation Status

| Component | Status | Notes |
|-----------|--------|-------|
| Repository scaffold | ✅ Done | All directories and config files created |
| FastAPI app (minimal) | ✅ Done | Health endpoint only |
| React app (minimal) | ✅ Done | Placeholder landing page only |
| OpenAPI contract | ✅ Done (skeleton) | Planned endpoints documented; not implemented |
| Database schema | 🔲 Planned | Design documented; no migrations created |
| Hydraulic simulation | 🔲 Planned | — |
| Anomaly detection (ML) | 🔲 Planned | — |
| Pipeline Health Score | 🔲 Planned | — |
| Failure risk model | 🔲 Planned | — |
| Maintenance prioritisation | 🔲 Planned | — |
| GIS map (Leaflet) | 🔲 Planned | — |
| Authentication | 🔲 Planned | — |
| CI/CD pipeline | 🔲 Planned | — |
| Production deployment | 🔲 Planned | — |

---

## License

MIT — see [LICENSE](LICENSE).