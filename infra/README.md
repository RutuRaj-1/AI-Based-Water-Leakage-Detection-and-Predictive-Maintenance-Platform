# Infrastructure

This directory contains Docker and deployment infrastructure for the project.

## Structure

```
infra/
├── docker/
│   └── postgres/
│       └── init/   ← SQL init scripts run by PostgreSQL on first start
└── scripts/        ← Utility shell scripts (backup, restore, seed, etc.)
```

## Current Contents

- `docker/postgres/init/` — Empty. Add `.sql` files here to run during PostgreSQL container initialisation.

## Planned Additions

- `docker/Dockerfile.backend` — Backend container definition
- `docker/Dockerfile.frontend` — Frontend container definition
- `scripts/seed.py` — Seed script for development data
- `scripts/backup.sh` — Database backup utility
