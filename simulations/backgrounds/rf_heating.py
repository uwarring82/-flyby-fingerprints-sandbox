from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from numpy.random import Generator


@dataclass(frozen=True)
class RFHeatingParams:
    """Parameters for the RF heating model."""

    S_E0: float
    alpha: float


def heating_rate(params: RFHeatingParams, T: float) -> float:
    """Compute the electric-field heating rate.

    Parameters
    ----------
    params:
        Heating model parameters.
    T:
        Trap frequency in Hz.
    """
    return params.S_E0 * (T / 1e6) ** params.alpha


def sample_energy_kick(
    params: RFHeatingParams, rng: Generator, size: int = 1
) -> np.ndarray:
    """Sample energy kicks from a normal distribution.

    The distribution mean is the heating rate at 300 K with 10% standard deviation.
    """
    mean = heating_rate(params, 300.0)
    return rng.normal(loc=mean, scale=0.1 * mean, size=size)


@dataclass(frozen=True)
class RFHeatingUncertainty:
    S_E0_relative: float = 0.30  # 30% relative
    alpha_absolute: float = 0.20  # ±0.2 in spectral index
    model_validity_range_hz: tuple = (1e5, 1e7)


def heating_rate_with_bounds(
    params: RFHeatingParams, T: float
) -> tuple[float, float, float]:
    nominal = heating_rate(params, T)
    lower = nominal * (1 - RFHeatingUncertainty.S_E0_relative)
    upper = nominal * (1 + RFHeatingUncertainty.S_E0_relative)
    return nominal, lower, upper
