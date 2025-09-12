import numpy as np
from simulations.backgrounds.rf_heating import (
    RFHeatingParams,
    heating_rate,
    heating_rate_with_bounds,
    sample_energy_kick,
)


def test_heating_rate_nominal():
    params = RFHeatingParams(S_E0=1.0, alpha=1.0)
    assert heating_rate(params, 1e6) == 1.0


def test_sample_energy_kick_seeded():
    params = RFHeatingParams(S_E0=1.0, alpha=1.0)
    rng1 = np.random.default_rng(123)
    draws1 = sample_energy_kick(params, rng1, size=100)
    rng2 = np.random.default_rng(123)
    draws2 = sample_energy_kick(params, rng2, size=100)
    assert draws1.shape == (100,)
    assert np.allclose(draws1, draws2)


def test_heating_rate_with_bounds():
    params = RFHeatingParams(S_E0=2.0, alpha=0.5)
    nominal, lower, upper = heating_rate_with_bounds(params, 1e6)
    assert lower < nominal < upper
    assert np.isclose(lower, nominal * (1 - 0.30))
    assert np.isclose(upper, nominal * (1 + 0.30))
