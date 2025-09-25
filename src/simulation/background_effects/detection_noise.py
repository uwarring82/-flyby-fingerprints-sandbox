"""Detection system noise proxies for Guardian background simulations."""

import numpy as np


def sample_counts(
    n_samples: int,
    bg_rate_cps: float,
    tint_ms: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Draw Poisson-distributed detector counts for a given integration time."""

    lam = bg_rate_cps * (tint_ms * 1e-3)
    return rng.poisson(lam=lam, size=n_samples)
