"""Mapping from systematic effects to potential mitigations."""

from typing import Dict


def map_systematics_to_mitigations() -> Dict[str, str]:
    """Return a static mapping between background channels and mitigation strategies."""

    return {
        "em_pickup": "Improve shielding; synchronize readout away from mains phases.",
        "surface_drift": "Bake/clean surfaces; interleave baseline runs; high-pass detrending.",
        "detection_counts": "Longer integration; dark counts calibration; electronics grounding.",
    }
