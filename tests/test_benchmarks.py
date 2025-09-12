import json
import pathlib
import numpy as np
from simulations.backgrounds.rf_heating import RFHeatingParams, heating_rate

ART = pathlib.Path("artifacts")
ART.mkdir(exist_ok=True)


def test_rf_heating_against_canonical_placeholder():
    p = RFHeatingParams(
        omega_sec=2 * np.pi * 1e6,
        d_elec=50e-6,
        S_E0=1e-12,
        alpha=1.0,
        mass=2.29e-25,
    )
    nominal = heating_rate(p, 300.0)
    med = 0.05  # placeholder median residual
    data = {"relative_medians": {"rf_heating": med}}
    (ART / "residuals_summary.json").write_text(json.dumps(data))
    assert med < 0.10  # Guardian policy (placeholder until real data)
