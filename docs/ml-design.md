# ML Design — Pune Water Network AI

> **Status:** Planned. This document describes the intended AI/ML approach. No models have been implemented or trained yet.

**Lead:** Shardul

---

## Overview

Four machine-learning / algorithmic components are planned:

| # | Component | Output |
|---|-----------|--------|
| 1 | Anomaly Detector | Binary/multi-class label per observation window |
| 2 | Pipeline Health Scorer | Score 0–100 per pipe segment |
| 3 | Failure Risk Estimator | Probability of failure within N days |
| 4 | Maintenance Prioritiser | Ranked work-order list |

---

## 1. Anomaly Detection

**Goal:** Classify pressure and flow time-series windows as normal or anomalous (and identify the likely anomaly type).

### Candidate Algorithms

| Algorithm | Pros | Cons |
|-----------|------|------|
| Isolation Forest | Unsupervised, robust, fast | Less interpretable |
| LSTM Autoencoder | Captures temporal patterns | Requires more data and tuning |
| One-Class SVM | Well-studied | Scales poorly to high-dimension |
| Statistical thresholding (baseline) | Simple, interpretable | Low recall for subtle leaks |

**Decision pending.** An ensemble of Isolation Forest (unsupervised baseline) + LSTM Autoencoder (deep learning) is under consideration.

---

## 2. Pipeline Health Scoring

**Goal:** Produce a composite 0–100 health score per pipe segment, combining:
- Recent anomaly frequency and severity
- Pipe age, material, and installation year
- Historical failure rate (synthetic or estimated)
- Pressure stress indicators

### Approach (Planned)

Weighted rule-based scoring in Stage 2; upgraded to a learned regression model in Stage 3 once sufficient training data exists.

---

## 3. Failure Risk Estimation

**Goal:** Estimate the probability that a pipe segment will fail within a configurable planning horizon (e.g., 30 days, 90 days).

### Candidate Algorithms

| Algorithm | Notes |
|-----------|-------|
| Gradient Boosted Trees (XGBoost / LightGBM) | Tabular features, interpretable via SHAP |
| Survival Analysis (Cox PH) | Models time-to-failure explicitly |
| Logistic Regression (baseline) | Simple, interpretable |

---

## 4. Maintenance Prioritisation

**Goal:** Rank pipe segments into a prioritised work-order list.

### Prioritisation Factors

| Factor | Weight (TBD) |
|--------|-------------|
| Failure probability | High |
| Pipeline Health Score | High |
| Criticality (diameter, demand served) | Medium |
| Estimated repair cost (INR) | Medium |
| Time since last maintenance | Low |

---

## Feature Engineering (Planned)

Features to be derived from simulation outputs and pipe attributes:

- Rolling mean/std of pressure over 1h, 6h, 24h windows
- Pressure gradient between connected nodes
- Flow deviation from expected demand curve
- Number of anomaly events in the past 7/30 days
- Pipe age (years since installation)
- Material risk factor (CI > PVC > DI)
- Health score trend (slope over last N assessments)

---

## Training Data Strategy

1. Generate synthetic observation data using the hydraulic simulation engine.
2. Inject labelled leak scenarios for supervised learning.
3. Augment with open datasets if available (AIKosh, CWRIS).
4. Maintain strict train/validation/test splits by simulation run (not by time-step) to prevent data leakage.

---

## Decisions Pending

- [ ] Final algorithm selection for each component
- [ ] Feature engineering implementation details
- [ ] Minimum training data volume before meaningful model evaluation
- [ ] Model versioning and artefact storage strategy (MLflow, DVC, or simple file-based)
- [ ] SHAP explainability integration for health and risk endpoints
- [ ] Retraining trigger (manual vs automated after each simulation batch)
