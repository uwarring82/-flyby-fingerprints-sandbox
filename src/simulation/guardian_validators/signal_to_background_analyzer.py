"""Signal-to-background estimators used by the Guardian background validator."""

from typing import Dict

import numpy as np


def estimate_snr(data: Dict) -> float:
    """Compute a simple SNR proxy for a claimed background signature."""

    heating_rate = np.asarray(data["heating_rate"], dtype=float)
    counts = np.asarray(data["detector_counts"], dtype=float)
    denom = np.std(counts) or 1e-12
    return float(np.mean(np.abs(heating_rate)) / denom)


def passes_threshold(data: Dict, threshold: float = 10.0) -> bool:
    """Return whether the dataset satisfies the Guardian SNR threshold."""

    return estimate_snr(data) >= threshold
