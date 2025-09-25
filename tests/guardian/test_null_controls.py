"""Smoke tests for the Guardian null-control generation."""

from simulation.null_controls import generate_null_controls, NullControlConfig
from simulation.background_effects_simulator import BackgroundConfig
from simulation.guardian_validators.guardian_background_validator import (
    guardian_check_backgrounds,
)


def test_null_controls_guardian_pass_smoke():
    data = generate_null_controls(
        NullControlConfig(n_samples=2000, dt_s=2e-4, seed=42), BackgroundConfig()
    )
    report = guardian_check_backgrounds(data)
    assert report["inventory_ok"], "Background inventory incomplete"
    assert report["null_95_ok"], "Null hypothesis (95%) failed on detector counts"
