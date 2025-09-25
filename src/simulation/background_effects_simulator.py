"""Background effects simulator used to generate Guardian validation inputs."""

from dataclasses import dataclass, asdict
from typing import Dict, Any, Tuple

import numpy as np

from .background_effects import thermal_motion, em_artifacts, surface_effects, detection_noise


@dataclass
class BackgroundConfig:
    """Configuration parameters controlling the background effects simulation."""

    # Thermal secular motion
    T_kelvin: float = 300.0
    secular_freqs_khz: Tuple[float, float, float] = (200.0, 200.0, 500.0)
    # Electromagnetic pickup
    rf_pickup_rms: float = 0.5  # mV equivalent at electrode
    mains_hz: float = 50.0
    em_coupling_coeff: float = 1e-3
    # Surface effects
    patch_potential_rms_mV: float = 5.0
    patch_corr_length_um: float = 50.0
    # Detection chain noise
    photon_rate_bg_cps: float = 200.0
    readout_integration_ms: float = 1.0


def simulate_background_timeseries(
    n_samples: int,
    dt_s: float,
    cfg: BackgroundConfig,
    seed: int = 0,
) -> Dict[str, Any]:
    """Generate background-only observables for Guardian validation gates."""

    rng = np.random.default_rng(seed)

    position = thermal_motion.sample_positions(
        n_samples=n_samples,
        dt_s=dt_s,
        T_K=cfg.T_kelvin,
        secular_freqs_khz=cfg.secular_freqs_khz,
        rng=rng,
    )

    em_pickup = em_artifacts.sample_electrode_pickup(
        n_samples=n_samples,
        dt_s=dt_s,
        rms_mV=cfg.rf_pickup_rms,
        mains_hz=cfg.mains_hz,
        coupling=cfg.em_coupling_coeff,
        rng=rng,
    )

    surface_drift = surface_effects.sample_patch_potential_drift(
        n_samples=n_samples,
        dt_s=dt_s,
        rms_mV=cfg.patch_potential_rms_mV,
        corr_length_um=cfg.patch_corr_length_um,
        rng=rng,
    )

    detector_counts = detection_noise.sample_counts(
        n_samples=n_samples,
        bg_rate_cps=cfg.photon_rate_bg_cps,
        tint_ms=cfg.readout_integration_ms,
        rng=rng,
    )

    heating_rate = thermal_motion.estimate_heating_rate_quanta_s(position, dt_s)

    return {
        "position": position,
        "em_pickup": em_pickup,
        "surface_drift": surface_drift,
        "detector_counts": detector_counts,
        "heating_rate": heating_rate,
        "metadata": {
            "n_samples": n_samples,
            "dt_s": dt_s,
            "seed": seed,
            "config": asdict(cfg),
        },
    }
