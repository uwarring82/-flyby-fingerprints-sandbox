import numpy as np
from simulations.backgrounds.rf_heating import (
    RFHeatingParams,
    heating_rate,
    sample_energy_kick,
    heating_rate_with_bounds,
)


def test_positive_rates_seeded():
    p = RFHeatingParams(
        omega_sec=2 * np.pi * 1e6,
        d_elec=50e-6,
        S_E0=1e-12,
        alpha=1.0,
        mass=2.29e-25,
    )
    rng = np.random.default_rng(123)
    r = sample_energy_kick(p, dt=1.0, rng=rng)
    assert r >= 0
    assert heating_rate(p, 300.0) > 0.0


def test_uncertainty_bounds_monotonic():
    p = RFHeatingParams(
        omega_sec=2 * np.pi * 1e6,
        d_elec=50e-6,
        S_E0=1e-12,
        alpha=1.0,
        mass=2.29e-25,
    )
    n, lo, hi = heating_rate_with_bounds(p, 300.0)
    assert lo <= n <= hi
    # sanity: 30% band
    assert (hi - n) / n >= 0.29
