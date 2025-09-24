from __future__ import annotations

"""Null validation helpers mandated by the Guardian policy framework.

The functions in this module provide a reproducible baseline for generating
background-only datasets alongside lightweight statistical checks.  The real
project will eventually replace these utilities with high-fidelity simulations
and domain specific analytics; however, the Guardian gate requires a working
scaffold so that CI can exercise the background catalogue immediately.
"""

from dataclasses import dataclass
from math import erf, sqrt
from typing import Iterable, Sequence

import numpy as np

from .background_effects import (
    BackgroundComponent,
    boulder_nist_2006_emi_patterns,
    detector_dead_time_effects,
    electromagnetic_pickup_models,
    innsbruck_2010_surface_signatures,
    surface_patch_potential_drift,
    vacuum_system_transients,
)

__all__ = [
    "BackgroundDataset",
    "generate_background_only_datasets",
    "statistical_power_analysis",
    "false_positive_rate_validation",
]


@dataclass(frozen=True)
class BackgroundDataset:
    """Container for a synthetic background-only dataset.

    Parameters
    ----------
    seed:
        Integer seed used to create the dataset (documented for reproducibility).
    data:
        Array of shape ``(n_samples, n_components)`` containing the simulated
        background draws.
    component_names:
        Tuple mirroring the catalogue order returned by
        :func:`generate_background_only_datasets`.
    metadata:
        Lightweight dictionary with helper information useful when emitting
        JSON artefacts.  The structure is intentionally minimal for ease of use
        in unit tests.
    """

    seed: int
    data: np.ndarray
    component_names: tuple[str, ...]
    metadata: dict[str, float | int]

    def summary(self) -> dict[str, float | int]:
        """Return a compact summary suitable for logging or JSON export."""

        return {
            "seed": self.seed,
            "n_samples": int(self.data.shape[0]),
            "n_components": int(self.data.shape[1]),
        }


def _catalogue() -> tuple[BackgroundComponent, ...]:
    """Return the flattened catalogue of all Guardian background components."""

    catalogues: tuple[Iterable[BackgroundComponent], ...] = (
        electromagnetic_pickup_models(),
        vacuum_system_transients(),
        detector_dead_time_effects(),
        surface_patch_potential_drift(),
        boulder_nist_2006_emi_patterns(),
        innsbruck_2010_surface_signatures(),
    )
    components: list[BackgroundComponent] = []
    for group in catalogues:
        components.extend(group)
    if not components:
        raise RuntimeError("Guardian background catalogue is empty")
    return tuple(components)


def generate_background_only_datasets(
    num_runs: int = 3,
    n_samples: int = 512,
    rng_seed: int = 2024,
) -> list[BackgroundDataset]:
    """Generate reproducible background-only datasets.

    Parameters
    ----------
    num_runs:
        Number of independent random seeds to realise.
    n_samples:
        Number of samples to draw for each dataset.  A minimum of 32 is
        enforced to guarantee stable summary statistics for Guardian checks.
    rng_seed:
        Base seed used for the deterministic seed ladder.  The ladder ensures
        independent draws while keeping the global sequence reproducible.
    """

    if num_runs <= 0:
        raise ValueError("num_runs must be positive")
    if n_samples < 32:
        raise ValueError("n_samples must be at least 32 for stable statistics")

    components = _catalogue()
    component_names = tuple(component.name for component in components)

    datasets: list[BackgroundDataset] = []
    for run_index in range(num_runs):
        run_seed = int((rng_seed + run_index * 9973) % (2**32))
        rng = np.random.default_rng(run_seed)
        draws = np.vstack([
            component.sample(rng, n_samples) for component in components
        ]).T
        metadata = {
            "run_index": run_index,
            "rng_seed": run_seed,
        }
        datasets.append(
            BackgroundDataset(
                seed=run_seed,
                data=draws,
                component_names=component_names,
                metadata=metadata,
            )
        )
    return datasets


def _normal_cdf(x: np.ndarray | float) -> np.ndarray | float:
    """Gaussian CDF helper without depending on SciPy."""

    return 0.5 * (1.0 + erf(x / sqrt(2.0)))


def statistical_power_analysis(
    datasets: Sequence[BackgroundDataset],
    injection_strength: float = 0.5,
    detection_threshold: float = 2.5,
) -> dict[str, float | tuple[float, ...]]:
    """Estimate statistical power for a mean-shift detection test.

    The simple analytic approximation assumes a signal injection equal to
    ``injection_strength`` times the background sigma on each component.  The
    Guardian requirement is to have a quick, conservative indicator; therefore
    the calculation uses a z-test on the sample mean.
    """

    if not datasets:
        raise ValueError("datasets must not be empty")
    if injection_strength <= 0:
        raise ValueError("injection_strength must be positive")
    if detection_threshold <= 0:
        raise ValueError("detection_threshold must be positive")

    per_dataset: list[float] = []
    for dataset in datasets:
        n = dataset.data.shape[0]
        z_score = injection_strength * sqrt(float(n))
        power = float(1.0 - _normal_cdf(detection_threshold - z_score))
        per_dataset.append(max(0.0, min(1.0, power)))

    mean_power = float(np.mean(per_dataset))
    return {
        "mean_power": mean_power,
        "per_dataset": tuple(per_dataset),
        "threshold": detection_threshold,
    }


def false_positive_rate_validation(
    datasets: Sequence[BackgroundDataset],
    detection_threshold: float = 3.0,
) -> dict[str, float | tuple[float, ...]]:
    """Estimate the empirical false-positive rate across the datasets."""

    if not datasets:
        raise ValueError("datasets must not be empty")
    if detection_threshold <= 0:
        raise ValueError("detection_threshold must be positive")

    rates: list[float] = []
    for dataset in datasets:
        data = dataset.data
        n = data.shape[0]
        std = data.std(axis=0, ddof=1)
        # Guard against zero variance; those channels are treated as benign.
        safe_std = np.where(std > 0, std, 1.0)
        se = safe_std / sqrt(float(n))
        z_scores = np.abs(data.mean(axis=0) / se)
        rate = float(np.mean(z_scores > detection_threshold))
        rates.append(max(0.0, min(1.0, rate)))

    mean_rate = float(np.mean(rates))
    return {
        "rate": mean_rate,
        "per_dataset": tuple(rates),
        "threshold": detection_threshold,
    }
