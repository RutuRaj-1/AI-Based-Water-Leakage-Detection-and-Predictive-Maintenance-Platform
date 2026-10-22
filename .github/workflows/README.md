# GitHub Actions Workflows

This directory will contain CI/CD workflow definitions for the project.

## Planned Workflows

| Workflow File | Purpose | Status |
|--------------|---------|--------|
| `backend-ci.yml` | Run backend tests and lint on PR | Planned |
| `frontend-ci.yml` | Run frontend tests and build check on PR | Planned |
| `docker-build.yml` | Verify Docker image builds | Planned |

## When to Add Workflows

Workflows will be added when:
1. The backend test suite has meaningful tests to run
2. The frontend build is stable and testable in CI
3. The team has confirmed branch protection rules on GitHub

Do not add workflows that will fail due to missing dependencies or unimplemented features.
