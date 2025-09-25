"""Tests for Guardian SNR estimation plumbing."""

from simulation.null_controls import generate_null_controls, NullControlConfig
from simulation.background_effects_simulator import BackgroundConfig
from simulation.guardian_validators.signal_to_background_analyzer import estimate_snr


def test_snr_estimator_runs():
    data = generate_null_controls(NullControlConfig(n_samples=3000), BackgroundConfig())
    snr = estimate_snr(data)
    assert snr >= 0.0
