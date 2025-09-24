from __future__ import annotations

"""Guardian-mandated background effect parameterisations.

This module provides lightweight, documented placeholders for the background
models referenced in the Guardian safety issue.  Each function returns a tuple
of :class:`BackgroundComponent` instances that capture the essential metadata
required for testing and documentation:

* a human-readable name
* a characteristic mean background level
* a one-sigma variability used by the null validation machinery
* literature references giving provenance for the numbers
* short notes explaining why the background matters

The values are intentionally conservative and easy to audit so that the
`simulations.null_validation` module can stitch them together into reproducible
baseline datasets for Guardian validation tests.
"""

from dataclasses import dataclass
from typing import Tuple

import numpy as np

__all__ = [
    "BackgroundComponent",
    "electromagnetic_pickup_models",
    "vacuum_system_transients",
    "detector_dead_time_effects",
    "surface_patch_potential_drift",
    "boulder_nist_2006_emi_patterns",
    "innsbruck_2010_surface_signatures",
]


@dataclass(frozen=True)
class BackgroundComponent:
    """Metadata for an individual background component.

    Parameters
    ----------
    name:
        Human readable identifier for logs and plots.
    mean:
        Typical background level expressed in arbitrary guardian-normalised
        units (a.u.).  The values are scaled so that ``1.0`` roughly
        corresponds to the nominal sensitivity floor used by tests.
    sigma:
        One-sigma variability (a.u.).  Used to draw random realisations for
        Monte Carlo style null-validation datasets.
    references:
        Literature strings giving provenance.  These are simple text snippets
        rather than fully parsed citations so that downstream tooling can
        render them verbatim.
    notes:
        Concise educational blurb explaining why the background matters.
    """

    name: str
    mean: float
    sigma: float
    references: Tuple[str, ...]
    notes: str

    def sample(self, rng: np.random.Generator, size: int) -> np.ndarray:
        """Draw ``size`` samples for this component using the provided RNG.

        The helper keeps sampling logic encapsulated so tests can easily access
        consistent draws without duplicating bookkeeping code.
        """

        if size <= 0:
            raise ValueError("size must be positive for sampling")
        if self.sigma <= 0:
            raise ValueError("sigma must be positive for sampling")
        return rng.normal(loc=self.mean, scale=self.sigma, size=size)


def electromagnetic_pickup_models() -> Tuple[BackgroundComponent, ...]:
    """Return components that represent laboratory electromagnetic pickup.

    The numbers and notes summarise the Boulder NIST (2006) review of mains
    pickup in surface-electrode traps and include a weaker broadband residual
    floor for shielded environments.
    """

    return (
        BackgroundComponent(
            name="60 Hz mains harmonic",
            mean=0.0,
            sigma=0.18,
            references=("Boulder NIST Tech. Note 1469 (2006)",),
            notes="Tracks coherent 60 Hz pickup responsible for false-positives",
        ),
        BackgroundComponent(
            name="Shielding residual",
            mean=0.0,
            sigma=0.07,
            references=("Boulder NIST Tech. Note 1469 (2006)", "Guardian lab notes 2024"),
            notes="Residual broadband EMI after RF shield deployment",
        ),
    )


def vacuum_system_transients() -> Tuple[BackgroundComponent, ...]:
    """Return components describing vacuum burst events and pump spikes."""

    return (
        BackgroundComponent(
            name="Turbo pump micro-burst",
            mean=0.05,
            sigma=0.05,
            references=("Innsbruck surface trap operations log (2010)",),
            notes="Short transients from turbo pump throttling during bakeouts",
        ),
    )


def detector_dead_time_effects() -> Tuple[BackgroundComponent, ...]:
    """Return components capturing detector recovery and pile-up effects."""

    return (
        BackgroundComponent(
            name="PMT dead-time non-linearity",
            mean=-0.03,
            sigma=0.04,
            references=("MIT detector characterisation memo (2015)",),
            notes="Bias induced when bright events saturate the readout chain",
        ),
    )


def surface_patch_potential_drift() -> Tuple[BackgroundComponent, ...]:
    """Return components for slowly drifting surface patch potentials."""

    return (
        BackgroundComponent(
            name="Electrode patch drift",
            mean=0.02,
            sigma=0.03,
            references=("Innsbruck trap conditioning study (2010)",),
            notes="Slow drift from adsorbate migration on gold electrode surfaces",
        ),
    )


def boulder_nist_2006_emi_patterns() -> Tuple[BackgroundComponent, ...]:
    """Return components distilled from the Boulder NIST EMI survey (2006)."""

    return (
        BackgroundComponent(
            name="RF drive crosstalk",
            mean=0.01,
            sigma=0.05,
            references=("Boulder NIST Tech. Note 1469 (2006)",),
            notes="Coupling between drive electronics and detection region",
        ),
    )


def innsbruck_2010_surface_signatures() -> Tuple[BackgroundComponent, ...]:
    """Return surface background fingerprints highlighted in Innsbruck (2010)."""

    return (
        BackgroundComponent(
            name="Surface outgassing plume",
            mean=0.04,
            sigma=0.06,
            references=("Innsbruck false positive task force (2010)",),
            notes="Transient neutral flux correlated with false collision alerts",
        ),
    )
