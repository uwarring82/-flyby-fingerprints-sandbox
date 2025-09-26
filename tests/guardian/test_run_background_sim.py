import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_background_sim import run_and_save


def test_run_and_save_generates_plots(tmp_path: Path):
    report, files = run_and_save(
        T=300, rf_rms=0.8, mains=50, em_coupling=1e-3,
        patch=10, corr=120, cps=300, tint_ms=1.5,
        n_samples=3000, dt_s=1e-4, seed=9, outdir=str(tmp_path)
    )
    # JSON report parsable and keys present
    with open(files["report"]) as f:
        data = json.load(f)
    assert "inventory_ok" in data and "guardian_pass" in data
    # PNGs created
    assert Path(files["time_series_png"]).exists()
    assert Path(files["psd_png"]).exists()
    assert Path(files["allan_png"]).exists()
    # HTML overview generated for quick visualization
    assert Path(files["overview_html"]).exists()
