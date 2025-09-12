from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class RFHeatingParams:
    """Parameters for the RF heating model."""

    omega_sec: float
    d_elec: float
    S_E0: float
    alpha: float
    mass: float
    charge: float = 1.602176634e-19


def heating_rate(params: RFHeatingParams, T: float) -> float:
    """Compute the nominal electric-field heating rate."""
    return params.S_E0 * (T / params.omega_sec) ** params.alpha


def sample_energy_kick(params: RFHeatingParams, dt: float, rng: np.random.Generator) -> float:
    """One-step energy increment Δn over dt using Poisson with mean=dot{n}*dt."""
    lam = heating_rate(params, T=300.0) * dt
    return rng.poisson(lam)


@dataclass(frozen=True)
class RFHeatingUncertainty:
    """Guardian-mandated uncertainty tracking for RF heating."""

    S_E0_relative: float = 0.30      # ±30% on noise floor
    alpha_absolute: float = 0.20     # ±0.2 on spectral slope
    validity_range_hz: tuple = (1e5, 1e7)  # frequency range where the model is valid


def heating_rate_with_bounds(params: RFHeatingParams, T: float) -> tuple[float, float, float]:
    """
    Returns (nominal, lower_bound, upper_bound) including uncertainty from S_E0.
    (Alpha contribution can be added once benchmark data is curated.)
    """
    nominal = heating_rate(params, T)
    lower = nominal * (1 - RFHeatingUncertainty.S_E0_relative)
    upper = nominal * (1 + RFHeatingUncertainty.S_E0_relative)
    return nominal, lower, upper
