# Setup Guide — Pune Water Network AI

> **Status:** Foundation stage. Only the minimal backend (health endpoint) and frontend (scaffold) are running. This guide will be expanded as each component is implemented.

---

## Prerequisites

| Tool | Minimum Version | Installation |
|------|----------------|-------------|
| Node.js | 18.x | https://nodejs.org |
| Python | 3.11 | https://python.org |
| Docker Desktop | Latest | https://docs.docker.com/get-docker/ |
| Git | 2.x | https://git-scm.com |

---

## 1. Clone the Repository

```bash
git clone https://github.com/RutuRaj-1/AI-Based-Water-Leakage-Detection-and-Predictive-Maintenance-Platform.git
cd AI-Based-Water-Leakage-Detection-and-Predictive-Maintenance-Platform
```

---

## 2. Environment Configuration

```bash
# Root environment (shared variables)
cp .env.example .env

# Backend-specific environment
cp backend/.env.example backend/.env

# Frontend-specific environment
cp frontend/.env.example frontend/.env.local
```

Edit each `.env` file with your local values. See the comments inside each file for descriptions.

---

## 3. Start the Database

```bash
docker compose up -d db
```

The PostgreSQL/PostGIS container will start on port `5432` (default).

Check it is healthy:

```bash
docker compose ps
```

---

## 4. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Activate (Linux / macOS / Git Bash)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Verify: `GET http://localhost:8000/api/v1/health`

Expected response:
```json
{
  "status": "ok",
  "version": "0.1.0",
  "environment": "development"
}
```

---

## 5. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open: `http://localhost:5173`

---

## 6. Running Tests

### Backend

```bash
cd backend
pytest
```

### Frontend

```bash
cd frontend
npm run test
```

---

## Pending Setup Steps

These steps are not yet possible because the corresponding features have not been implemented:

- [ ] Database migrations (`alembic upgrade head`) — schema not yet designed
- [ ] ML model initialisation — models not yet trained
- [ ] Hydraulic simulation setup — WNTR/EPANET not yet integrated
- [ ] GIS dataset loading — sources not yet identified

This document will be updated as each stage is completed.
