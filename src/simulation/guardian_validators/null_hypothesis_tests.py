"""Null-hypothesis tests for Guardian background validation."""

import numpy as np
from scipy import stats


def null_is_consistent(counts: np.ndarray, alpha: float = 0.05) -> bool:
    """Perform a chi-squared goodness-of-fit test against a Poisson model."""

    counts = np.asarray(counts)
    lam = float(np.mean(counts))
    values, observed = np.unique(counts, return_counts=True)
    expected = stats.poisson(mu=lam).pmf(values) * len(counts)
    mask = expected > 1e-6
    if not np.any(mask):
        return True
    chi2 = np.sum((observed[mask] - expected[mask]) ** 2 / expected[mask])
    dof = max(1, int(np.sum(mask)) - 1)
    p_value = 1.0 - stats.chi2.cdf(chi2, dof)
    return p_value >= alpha
