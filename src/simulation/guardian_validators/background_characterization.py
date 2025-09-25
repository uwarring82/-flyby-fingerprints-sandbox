"""Background inventory checks for Guardian validations."""

from typing import Dict


REQUIRED_CHANNELS = {
    "position",
    "em_pickup",
    "surface_drift",
    "detector_counts",
    "heating_rate",
    "metadata",
}


def background_inventory_complete(data: Dict) -> bool:
    """Return True when all required background channels are present."""

    return REQUIRED_CHANNELS.issubset(set(data.keys()))
