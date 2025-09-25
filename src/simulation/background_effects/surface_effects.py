"""Surface effect proxies for Guardian background simulations."""

import numpy as np


def sample_patch_potential_drift(
    n_samples: int,
    dt_s: float,
    rms_mV: float,
    corr_length_um: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Generate a slow drift trace using a normalized random walk proxy."""

    _ = dt_s, corr_length_um  # Parameters reserved for more detailed models.
    white = rng.normal(0.0, 1.0, size=n_samples)
    drift = np.cumsum(white)
    std = np.std(drift) or 1.0
    drift = drift / std * rms_mV
    return drift
