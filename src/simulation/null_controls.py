"""Utilities for generating Guardian null-control datasets."""

from dataclasses import dataclass
from typing import Dict, Any

from .background_effects_simulator import BackgroundConfig, simulate_background_timeseries


@dataclass
class NullControlConfig:
    """Configuration describing the null-control simulation grid."""

    n_samples: int = 10_000
    dt_s: float = 1e-4
    seed: int = 123


def vacuum_system_noise_model(cfg: BackgroundConfig) -> BackgroundConfig:
    """Placeholder hook for swapping in different vacuum noise presets."""

    return cfg


def electronic_baseline_simulator(cfg: BackgroundConfig) -> BackgroundConfig:
    """Adjust the configuration to mimic an electronics-only baseline."""

    cfg.T_kelvin *= 0.1
    cfg.rf_pickup_rms *= 0.5
    return cfg


def generate_null_controls(ncfg: NullControlConfig, bcfg: BackgroundConfig) -> Dict[str, Any]:
    """Generate a null-control background snapshot using the provided configs."""

    return simulate_background_timeseries(
        n_samples=ncfg.n_samples,
        dt_s=ncfg.dt_s,
        cfg=bcfg,
        seed=ncfg.seed,
    )
