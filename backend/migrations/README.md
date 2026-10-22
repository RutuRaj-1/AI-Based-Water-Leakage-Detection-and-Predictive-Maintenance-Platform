# Database Migrations

This directory is managed by [Alembic](https://alembic.sqlalchemy.org/).

Alembic has not been initialised yet. Initialise it in Stage 2 when the
SQLAlchemy models and database connection are implemented:

```bash
cd backend
alembic init migrations
```

Then configure `migrations/env.py` to import from `app.models` and point at the
`DATABASE_URL` from `app.core.config.settings`.
