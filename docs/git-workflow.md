# Git Workflow — Pune Water Network AI

---

## Branch Model

```
main
 ├── frontend          (Bhargavi — all frontend development)
 └── backend           (Sanskar, Shardul — all backend development)
```

Feature work lives on short-lived branches cut from the relevant base branch:

```
frontend
 └── feature/bhargavi/gis-map-layer
 └── feature/bhargavi/anomaly-alert-panel

backend
 └── feature/sanskar/hydraulic-simulation-engine
 └── feature/shardul/anomaly-detection-model
```

---

## Branch Descriptions

| Branch | Purpose | Who writes here |
|--------|---------|----------------|
| `main` | Stable foundation; production releases | Ruturaj (integration PRs) |
| `frontend` | All React application development | Bhargavi |
| `backend` | All Python/FastAPI development | Sanskar, Shardul |
| `feature/*` | Individual features — short-lived | All team members |

---

## Setting Up Your Working Branch

After the foundation commit is on `main`, each developer sets up their base branch:

```bash
# Create frontend branch from main (Bhargavi)
git checkout main
git checkout -b frontend

# Create backend branch from main (Sanskar / Shardul)
git checkout main
git checkout -b backend
```

---

## Feature Branch Workflow

```bash
# 1. Start from the correct base
git checkout frontend          # or backend

# 2. Pull latest
git pull origin frontend

# 3. Create your feature branch
git checkout -b feature/your-name/short-description

# 4. Do your work, commit frequently
git add .
git commit -m "feat: describe what you did"

# 5. Push to remote
git push origin feature/your-name/short-description

# 6. Open a Pull Request → target: frontend (or backend)
# 7. Request review from at least one other team member
# 8. After approval, merge (prefer squash merge for clean history)
# 9. Delete the feature branch after merge
```

---

## Commit Message Convention

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short summary>

[optional body]
[optional footer: issue refs]
```

**Types:**

| Type | When to use |
|------|------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test` | Adding or fixing tests |
| `chore` | Build, config, dependencies |
| `perf` | Performance improvement |

**Examples:**

```
feat(anomaly): implement isolation-forest detector for pressure drops
fix(api): return 422 on invalid pipe_id in health endpoint
docs(arch): add PostGIS geometry strategy to database-design.md
chore(deps): update fastapi to 0.111.0
```

---

## Integration with Main

Frontend and backend branches are merged to `main` at stable milestones (e.g., end of each development stage). Ruturaj coordinates these integration merges.

```bash
# Example: merge frontend into main after Stage 3
git checkout main
git pull origin main
git merge --no-ff frontend -m "chore: merge frontend stage-3 dashboard"
git push origin main
```

---

## Pull Request Requirements

- All PRs require at least **one approval** from a team member who did not author the branch.
- All automated checks must pass (when CI is configured).
- PR description must reference the relevant work item or task.
- No direct pushes to `main`, `frontend`, or `backend` — always use a PR.

---

## Release Tagging

Stable releases are tagged on `main`:

```bash
git tag -a v0.1.0 -m "Stage 1: Foundation release"
git push origin v0.1.0
```

---

## Important: Do Not Commit to `main` Directly After Initialisation

The initial foundation commit is an exception. After that commit, `main` receives changes only through reviewed, approved pull requests from `frontend` or `backend`.
