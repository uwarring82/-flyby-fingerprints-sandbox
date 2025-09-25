"""Simple proxies for thermal secular motion used in Guardian simulations."""

from typing import Tuple

import numpy as np

kB = 1.380649e-23
m_YB171 = 2.84e-25  # kg (placeholder mass; replace with actual ion mass used in repo)


def sample_positions(
    n_samples: int,
    dt_s: float,
    T_K: float,
    secular_freqs_khz: Tuple[float, float, float],
    rng: np.random.Generator,
) -> np.ndarray:
    """Draw a thermal secular motion position trace using a simple sinusoidal proxy."""

    freqs = np.array(secular_freqs_khz, dtype=float) * 1e3
    t = np.arange(n_samples) * dt_s
    omega_mean = 2 * np.pi * freqs.mean()
    amplitude = np.sqrt(kB * T_K / m_YB171) / omega_mean
    phase = rng.uniform(0.0, 2 * np.pi)
    return amplitude * np.sin(omega_mean * t + phase)


def estimate_heating_rate_quanta_s(position_ts: np.ndarray, dt_s: float) -> float:
    """Estimate a proxy heating rate from a position time series."""

    if position_ts.size < 2:
        return 0.0
    velocity = np.diff(position_ts) / dt_s
    return float(np.var(velocity))
