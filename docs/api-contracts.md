# API Contracts — Pune Water Network AI

> **Owner:** Ruturaj  
> **Contract location:** `shared/api-contract/openapi.yaml`

---

## Purpose

This document explains how the frontend and backend teams will share, maintain, and evolve the REST API contract for this project.

A single versioned OpenAPI 3.1 specification (`shared/api-contract/openapi.yaml`) is the **source of truth** for all API interactions. Both teams use it to:
- Agree on request/response shapes before implementation begins.
- Generate TypeScript client types for the frontend.
- Validate backend responses in tests.

---

## Workflow

```
1. Ruturaj (or any author) proposes a change to openapi.yaml in a PR
2. Frontend and backend leads review and approve the change
3. Once merged to main, both teams implement against the agreed contract
4. Neither team should make undocumented changes to API shapes
```

---

## Versioning

- All endpoints are prefixed with `/api/v1/`.
- When breaking changes are required, a new prefix (`/api/v2/`) is introduced; v1 is not removed until migration is complete.

---

## Current Contract State

See [`shared/api-contract/openapi.yaml`](../shared/api-contract/openapi.yaml).

| Endpoint | Status |
|----------|--------|
| `GET /api/v1/health` | ✅ Implemented |
| All network, pipeline, simulation, and ML endpoints | 🔲 Planned (documented in spec as proposals) |

---

## Frontend Code Generation (Planned)

Once the API stabilises, the frontend can generate typed API clients from the OpenAPI spec:

```bash
# Planned — not yet configured
npx openapi-typescript shared/api-contract/openapi.yaml -o frontend/src/types/api.generated.ts
```

---

## Backend Validation (Planned)

Backend tests can validate response shapes against the OpenAPI spec using `schemathesis` or `pytest-httpx` with schema assertions.

---

## Decisions Pending

- [ ] Confirm pagination convention: cursor-based vs limit/offset
- [ ] Confirm error envelope shape: `{ error: { code, message, details } }`
- [ ] Confirm authentication header: `Authorization: Bearer <token>` vs API key header
- [ ] Confirm GeoJSON feature format for network endpoints
- [ ] Decide whether to use strict OpenAPI 3.1 or remain with 3.0.3 for tooling compatibility
