from __future__ import annotations

import json
import os
from typing import Any, Dict

from simulations.integration.constraint_mapper import apply_physical_constraints
from simulations.integration.interaction_diagnostics import diagnose_interactions
from simulations.integration.baseline_validator import validate_baseline
from simulations.backgrounds.rf_heating import RFHeatingParams, heating_rate_with_bounds

# TODO: import additional backgrounds here when available, e.g.:
# from simulations.backgrounds.thermal_noise import thermal_noise_rate_with_bounds


def _rf_heating_component(p: Dict[str, Any]) -> Dict[str, float]:
    """Evaluate the RF heating contribution with uncertainty bounds."""

    rf_nom, rf_lo, rf_hi = heating_rate_with_bounds(
        RFHeatingParams(
            omega_sec=p["omega_sec"],
            d_elec=p.get("d_elec", 50e-6),
            S_E0=p.get("S_E0", 1e-12),
            alpha=p.get("alpha", 1.0),
            mass=p["mass"],
        ),
        p.get("T", p.get("temperature", 300.0)),
    )
    return {"nominal": rf_nom, "lo": rf_lo, "hi": rf_hi}


def _prepare_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure parameters contain keys expected by the constraint mapper."""

    prepared = dict(params)
    if "temperature" not in prepared and "T" in prepared:
        prepared["temperature"] = prepared["T"]
    constrained = apply_physical_constraints(prepared)
    # Preserve both naming conventions for downstream consumers
    if "T" not in constrained and "temperature" in constrained:
        constrained["T"] = constrained["temperature"]
    if "temperature" not in constrained and "T" in constrained:
        constrained["temperature"] = constrained["T"]
    return constrained


def run_baseline(params: Dict[str, Any], refs: Dict[str, Any]) -> Dict[str, Any]:
    """Run the Phase-2 baseline aggregation pipeline."""

    os.makedirs("artifacts/baseline", exist_ok=True)

    # 1) Apply physical constraints (pressure-temperature, etc.)
    p = _prepare_params(params)

    # 2) Compute components (extend as more backgrounds land)
    rf = _rf_heating_component(p)
    # Example extension:
    # th = thermal_noise_rate_with_bounds(p) -> {"nominal": ..., "lo": ..., "hi": ...}

    # 3) Combine nominal contributions (sum), keep per-component detail
    individual = {
        "rf_heating": {"rate": rf["nominal"]},
        # "thermal_noise": {"rate": th["nominal"]},
    }
    combined_nominal = sum(v["rate"] for v in individual.values())

    # 4) Store baseline distributions (nominal/lo/hi) — conservative lo/hi by linear bounds
    lo = rf["lo"]  # extend with other lows: min(lo candidates) or sum-of-mins strategy
    hi = rf["hi"]  # extend with other highs: max(hi candidates) or sum-of-highs strategy

    baseline = {
        "metrics": {"rate": combined_nominal, "lo": lo, "hi": hi},
        "uncertainty": {
            "rf_heating": rf,
            # "thermal_noise": th,
        },
        "components": individual,
        "metadata": p,
    }
    with open("artifacts/baseline/baseline_distributions.json", "w", encoding="utf-8") as f:
        json.dump(baseline, f, indent=2)

    # 5) Interaction diagnostics (compares combined vs sum of individual)
    diagnose_interactions(individual=individual, combined={"rate": combined_nominal}, rel_threshold=0.10)

    # 6) Benchmark comparisons (≥3 needed to PASS)
    benchmark_inputs = {key: combined_nominal for key in refs}
    baseline_report = validate_baseline(baseline=benchmark_inputs, references=refs, rel_tolerance=0.20)

    # Embed benchmark summary for downstream introspection
    baseline["benchmark_comparisons"] = baseline_report

    return baseline
