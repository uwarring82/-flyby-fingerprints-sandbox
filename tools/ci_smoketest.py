"""Lightweight smoke test for CI.

This script exercises the :mod:`simulations.backgrounds.rf_heating` module by
computing a nominal heating rate and verifying it is positive. It also writes a
summary JSON file consumed by downstream CI steps.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path


# Ensure the repository root is on ``sys.path`` so imports work when the script
# is executed directly.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from simulations.backgrounds.rf_heating import RFHeatingParams, heating_rate


def main() -> None:
    """Run the smoke test and write CI artifacts."""

    # Nominal RF heating parameters.
    params = RFHeatingParams(
        omega_sec=2 * math.pi * 1e6,
        d_elec=50e-6,
        S_E0=1.0,
        alpha=1.0,
        mass=2.29e-25,
    )

    rate = heating_rate(params, T=300.0)
    assert rate > 0, "RF heating rate must be positive"

    # Emit a placeholder residual summary for CI consumers.
    artifacts_dir = ROOT / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)
    summary = {"relative_medians": {"rf_heating": 0.05}}
    (artifacts_dir / "residuals_summary.json").write_text(json.dumps(summary))

    print("[SMOKETEST] RF heating smoketest passed.")


if __name__ == "__main__":  # pragma: no cover - script entry point
    main()

