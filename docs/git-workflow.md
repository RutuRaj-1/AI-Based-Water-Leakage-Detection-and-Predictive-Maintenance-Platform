# Git Workflow — Pune Water Network AI

---

## Long-Lived Integration Branches

The repository maintains three long-lived integration branches:

- **`main`**: Stable, reviewed integration and release branch. Production releases and version tags originate here. Direct commits and direct pushes are strictly prohibited.
- **`frontend`**: Frontend integration branch. All frontend features, UI components, and client-side integrations merge here prior to reaching `main`.
- **`backend`**: Backend integration branch. All backend services, API routes, simulation engines, and AI/ML models merge here prior to reaching `main`.

```
main (stable, reviewed integration & release branch)
 ├── frontend (frontend integration branch)
 └── backend  (backend integration branch)
```

---

## Short-Lived Feature Branches

Feature work lives on short-lived branches cut from their corresponding integration branch (`frontend` or `backend`) and merged back into that same branch through pull requests.

### Naming Convention: `feature/<task-name>`

All feature branches must use the shared **`feature/<task-name>`** naming convention with lowercase, hyphen-separated descriptions of the task.

Examples:
- `feature/gis-dashboard` (cut from `frontend`)
- `feature/database-api` (cut from `backend`)
- `feature/hydraulic-simulator` (cut from `backend`)
- `feature/anomaly-detection` (cut from `backend`)

```
frontend
 └── feature/gis-dashboard

backend
 ├── feature/database-api
 ├── feature/hydraulic-simulator
 └── feature/anomaly-detection
```

> [!WARNING]
> ### Git Reference Namespace Collision
> **Do not prescribe or use `frontend/*` or `backend/*` as branch prefixes.**
> In Git, branch references are stored under `.git/refs/heads/`. Because long-lived branches named `frontend` and `backend` exist as references (files) in the Git ref namespace (e.g., `.git/refs/heads/frontend`), creating a branch prefixed with `frontend/<task-name>` would require Git to create a directory with the same name (`.git/refs/heads/frontend/`). This causes a fatal reference namespace conflict in Git.
>
> All developers must use the shared `feature/<task-name>` prefix regardless of whether the branch targets `frontend` or `backend`.

---

## Branch Descriptions

| Branch | Type | Purpose | How Changes Enter |
|--------|------|---------|-------------------|
| `main` | Long-lived | Stable, reviewed integration and release branch | Reviewed pull requests from `frontend` or `backend` after all tests and integration checks pass |
| `frontend` | Long-lived | Frontend integration branch | Reviewed pull requests from `feature/*` branches cut from `frontend` |
| `backend` | Long-lived | Backend integration branch | Reviewed pull requests from `feature/*` branches cut from `backend` |
| `feature/<task-name>` | Short-lived | Individual task or feature development | Feature commits; merged into base integration branch via pull request |

---

## Setting Up Integration Branches

Developers set up their local tracking branches from the remote integration branches:

```bash
# Frontend integration branch
git checkout frontend
git pull origin frontend

# Backend integration branch
git checkout backend
git pull origin backend
```

---

## Feature Branch Workflow

Feature branches are created from their corresponding integration branch (`frontend` or `backend`) and merged back into that integration branch through pull requests.

```bash
# 1. Start from the correct integration branch and pull latest changes
git checkout frontend          # or: git checkout backend
git pull origin frontend       # or: git pull origin backend

# 2. Create your feature branch using the shared feature/<task-name> convention
git checkout -b feature/gis-dashboard          # example: frontend feature
# or:
# git checkout -b feature/database-api         # example: backend feature
# git checkout -b feature/hydraulic-simulator  # example: backend feature
# git checkout -b feature/anomaly-detection    # example: backend feature

# 3. Implement changes and commit using conventional commit messages
git add .
git commit -m "feat(gis): add pipeline network layer to map"

# 4. Push feature branch to remote
git push -u origin feature/gis-dashboard

# 5. Open a Pull Request targeting the corresponding integration branch:
#    - Base branch: frontend (or backend)
#    - Compare branch: feature/<task-name>

# 6. Request review from at least one other team member
# 7. Ensure all automated tests and CI checks pass
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
docs(git): update branching model and ref namespace conflict rules
chore(deps): update fastapi to 0.111.0
```

---

## Integration with `main`

Frontend and backend integration branches are merged to `main` at stable milestones (such as the completion of development stages).

Changes reach `main` exclusively through reviewed pull requests after relevant tests and integration checks pass:

1. **Pre-requisite Checks**:
   - All unit, integration, and contract tests pass on the source integration branch (`frontend` or `backend`).
   - Code adheres to linting and formatting standards.
2. **Pull Request**:
   - Open a pull request targeting `main` with `frontend` or `backend` as the compare branch.
3. **Review & Approval**:
   - Integration PRs require review and approval from repository maintainers / team leads.
4. **Merge**:
   - Merge is executed through the pull request interface once all status checks pass. Direct pushes and direct merges to `main` without a PR are prohibited.

---

## Pull Request Requirements

- All PRs require at least **one approval** from a team member who did not author the branch.
- Feature PRs must target their respective integration branch (`frontend` or `backend`).
- Integration PRs to `main` must verify all relevant tests and integration checks pass.
- PR descriptions must reference the relevant work item, development stage, or task.
- No direct pushes to `main`, `frontend`, or `backend` — always use a pull request.

---

## Release Tagging

Stable releases are tagged on `main`:

```bash
git checkout main
git pull origin main
git tag -a v0.1.0 -m "Stage 1: Foundation release"
git push origin v0.1.0
```

---

## Important Rules Summary

- **Never commit directly to `main`, `frontend`, or `backend`**: All updates enter these branches via reviewed pull requests.
- **Never use `frontend/*` or `backend/*` prefixes**: Avoids fatal Git reference namespace collisions with the long-lived `frontend` and `backend` branch refs.
- **Always use `feature/<task-name>`**: Shared prefix across frontend and backend contributors.
- **Integration via PR**: Feature branches merge into `frontend` or `backend` via PR; changes reach `main` through reviewed PRs after passing tests and checks.
