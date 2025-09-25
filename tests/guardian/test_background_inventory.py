"""Tests for Guardian background inventory coverage."""

from simulation.null_controls import generate_null_controls, NullControlConfig
from simulation.background_effects_simulator import BackgroundConfig
from simulation.guardian_validators.background_characterization import (
    background_inventory_complete,
)


def test_inventory_complete():
    data = generate_null_controls(
        NullControlConfig(n_samples=1000, dt_s=1e-4, seed=7), BackgroundConfig()
    )
    assert background_inventory_complete(data)
