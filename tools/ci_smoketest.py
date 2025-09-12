from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
from simulations.backgrounds.rf_heating import RFHeatingParams, heating_rate

ART = ROOT / "artifacts"
ART.mkdir(exist_ok=True)


def main() -> None:
    data = np.loadtxt(
        "data/benchmarks/rf_heating_placeholder.csv", delimiter=",", skiprows=1
    )
    rates = data[:, 1]
    rates = rates[rates > 0]
    params = RFHeatingParams(
        omega_sec=2 * np.pi * 1e6,
        d_elec=50e-6,
        S_E0=1.0,
        alpha=1.0,
        mass=2.29e-25,
    )
    if rates.size:
        target = float(np.median(rates))
        tuned = RFHeatingParams(
            omega_sec=params.omega_sec,
            d_elec=params.d_elec,
            S_E0=target * params.omega_sec / 300.0,
            alpha=params.alpha,
            mass=params.mass,
        )
        nominal = heating_rate(tuned, 300.0)
        residuals = np.abs(nominal - rates) / rates
        med = float(np.median(residuals))
    else:
        med = 1.0
    summary = {"relative_medians": {"rf_heating": med}}
    (ART / "residuals_summary.json").write_text(json.dumps(summary))
    print(f"[SMOKETEST] RF heating median residual: {med:.3f}")


if __name__ == "__main__":
    main()
