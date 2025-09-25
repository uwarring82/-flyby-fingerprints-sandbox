"""Systematic effect quantification utilities for Guardian validations."""

from typing import Dict

import numpy as np


def quantify_contributions(data: Dict) -> Dict[str, float]:
    """Return simple variance-based contribution metrics for background channels."""

    return {
        "em_pickup_var": float(np.var(data["em_pickup"])),
        "surface_drift_var": float(np.var(data["surface_drift"])),
        "detector_counts_var": float(np.var(data["detector_counts"])),
    }
