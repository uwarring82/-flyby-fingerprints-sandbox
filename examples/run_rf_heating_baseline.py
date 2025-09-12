"""Run a simple RF heating baseline calculation."""

import numpy as np
from simulations.backgrounds.rf_heating import (
    RFHeatingParams,
    RFHeatingUncertainty,
    heating_rate_with_bounds,
)

params = RFHeatingParams(
    omega_sec=2 * np.pi * 1e6,
    d_elec=50e-6,
    S_E0=1e-12,
    alpha=1.0,
    mass=2.29e-25,
)
nominal, lower, upper = heating_rate_with_bounds(
    params, 300.0, RFHeatingUncertainty()
)
print(
    f"Heating rate: {nominal:.3e} (+{upper-nominal:.3e}/-{nominal-lower:.3e})"
)
