"""
Leak anomaly detector.

Approach (per pipe, per signal):
  1. Learn the normal diurnal pattern by least-squares regression on a
     Fourier basis (24h fundamental + harmonics) over a warm-up window of
     leak-free telemetry.
  2. Score live readings as standardised residuals (z-scores).
  3. A leak signature is a pressure DROP combined with a flow SURGE, so the
     anomaly score is sqrt(max(-z_p,0)^2 + max(z_f,0)^2).

This is deliberately lightweight and explainable (no black box) so operators
can see why an alert fired.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

HARMONICS = 3
MLD_TO_M3H = 1000.0 / 24.0
PRESSURE_DROP_PER_M3H = 0.02  # bar per m3/h of leakage (matches simulator physics)


def _basis(hour: float) -> np.ndarray:
    w = 2.0 * math.pi * hour / 24.0
    cols = [1.0]
    for k in range(1, HARMONICS + 1):
        cols.extend((math.sin(k * w), math.cos(k * w)))
    return np.array(cols)


@dataclass(frozen=True)
class AnomalyScore:
    z_pressure: float
    z_flow: float
    score: float
    expected_pressure: float
    expected_flow: float
    pressure_deviation: float   # observed - expected (bar)
    flow_deviation: float       # observed - expected (MLD)
    est_loss_m3h: float
    is_leak_signature: bool


class _SignalModel:
    def __init__(self, coef: np.ndarray, sigma: float) -> None:
        self.coef = coef
        self.sigma = sigma

    def predict(self, hour: float) -> float:
        return float(_basis(hour) @ self.coef)


class AnomalyDetector:
    """Per-pipe seasonal-regression residual detector."""

    def __init__(self, threshold: float = 4.5, min_sigma_pressure: float = 0.015,
                 min_sigma_flow_frac: float = 0.004) -> None:
        self.threshold = threshold
        self._min_sp = min_sigma_pressure
        self._min_sf = min_sigma_flow_frac
        self._pressure: dict[str, _SignalModel] = {}
        self._flow: dict[str, _SignalModel] = {}

    @property
    def fitted(self) -> bool:
        return bool(self._pressure)

    def _fit_signal(self, hours: list[float], values: list[float], min_sigma: float) -> _SignalModel:
        x = np.vstack([_basis(h) for h in hours])
        y = np.asarray(values)
        coef, *_ = np.linalg.lstsq(x, y, rcond=None)
        resid = y - x @ coef
        sigma = max(float(resid.std(ddof=x.shape[1])), min_sigma)
        return _SignalModel(coef, sigma)

    def fit(self, pipe_id: str, hours: list[float], pressures: list[float], flows: list[float]) -> None:
        mean_flow = float(np.mean(flows))
        self._pressure[pipe_id] = self._fit_signal(hours, pressures, self._min_sp)
        self._flow[pipe_id] = self._fit_signal(hours, flows, self._min_sf * mean_flow)

    def score(self, pipe_id: str, hour: float, pressure: float, flow: float) -> AnomalyScore:
        pm, fm = self._pressure[pipe_id], self._flow[pipe_id]
        ep, ef = pm.predict(hour), fm.predict(hour)
        dp, df = pressure - ep, flow - ef
        zp, zf = dp / pm.sigma, df / fm.sigma
        s = math.sqrt(max(-zp, 0.0) ** 2 + max(zf, 0.0) ** 2)
        flow_loss = max(df, 0.0) * MLD_TO_M3H
        pres_loss = max(-dp, 0.0) / PRESSURE_DROP_PER_M3H
        # Pressure is a far less noisy loss estimator than flow, so weight it more.
        est = (0.8 * pres_loss + 0.2 * flow_loss) if (flow_loss > 0 and pres_loss > 0) else max(flow_loss, pres_loss)
        return AnomalyScore(
            z_pressure=zp, z_flow=zf, score=s,
            expected_pressure=ep, expected_flow=ef,
            pressure_deviation=dp, flow_deviation=df,
            est_loss_m3h=est,
            is_leak_signature=(zp < -2.0 and zf > 0.5) or s >= self.threshold,
        )
