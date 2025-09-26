import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    import matplotlib  # noqa: F401  (imported for availability check)
except ModuleNotFoundError:
    _HAS_MPL = False
else:
    _HAS_MPL = True

def test_run_and_save_smoke(tmp_path: Path):
    if not _HAS_MPL:
        pytest.skip(
            "Matplotlib is required for the background simulation smoke test; run `pip install -r requirements.txt`."
        )

    from scripts.run_background_sim import run_and_save

    report, files = run_and_save(
        T=300,
        rf_rms=0.5,
        mains=50,
        em_coupling=1e-3,
        patch=5,
        corr=50,
        cps=200,
        tint_ms=1.0,
        n_samples=2000,
        dt_s=2e-4,
        seed=7,
        outdir=str(tmp_path),
    )
    assert report.get("inventory_ok", False)
    assert Path(files["time_series_png"]).exists()
    assert Path(files["report"]).exists()
    with open(files["report"], encoding="utf-8") as f:
        json.load(f)
