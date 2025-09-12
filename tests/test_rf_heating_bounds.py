import numpy as np
from simulations.backgrounds.rf_heating import (
    RFHeatingParams, heating_rate, heating_rate_with_bounds
)
import math


def _params(f_hz: float = 1.0e6, alpha: float = 1.0) -> RFHeatingParams:
    return RFHeatingParams(
        omega_sec=2 * math.pi * f_hz,
        d_elec=50e-6,
        S_E0=1e-12,
        alpha=alpha,
        mass=2.29e-25,
    )


def test_bounds_monotone_and_band():
    p = _params()
    n, lo, hi = heating_rate_with_bounds(p, 300.0)
    assert lo <= n <= hi
    # ~30% band (allowing small numerical tolerance)
    assert (hi - n) / max(n, 1e-30) >= 0.29


def test_frequency_scaling_inverse_when_alpha_zero():
    p1 = _params(1.0e6, alpha=0.0)
    p2 = _params(2.0e6, alpha=0.0)
    r1 = heating_rate(p1, 300.0)
    r2 = heating_rate(p2, 300.0)
    # Doubling ω should ~halve rate when spectrum is flat (alpha=0)
    assert r2 < r1 / 1.9


def test_positive_and_finite():
    p = _params(1.2e6)
    r = heating_rate(p, 300.0)
    assert np.isfinite(r) and r > 0.0
