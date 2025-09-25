"""Electromagnetic artifact models for Guardian background simulations."""

import numpy as np


def sample_electrode_pickup(
    n_samples: int,
    dt_s: float,
    rms_mV: float,
    mains_hz: float,
    coupling: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Generate a synthetic electrode pickup trace including mains hum and broadband noise."""

    t = np.arange(n_samples) * dt_s
    mains = np.sin(2 * np.pi * mains_hz * t)
    broadband = rng.normal(0.0, 1.0, size=n_samples)
    signal = mains + 0.1 * broadband
    return coupling * rms_mV * signal
