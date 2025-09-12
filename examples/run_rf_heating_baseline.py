"""Run a simple RF heating baseline calculation."""

from simulations.backgrounds.rf_heating import RFHeatingParams, heating_rate_with_bounds

params = RFHeatingParams(S_E0=1.0, alpha=1.0)
nominal, lower, upper = heating_rate_with_bounds(params, 1e6)
print(f"Heating rate: {nominal:.3f} (+{upper-nominal:.3f}/-{nominal-lower:.3f})")
