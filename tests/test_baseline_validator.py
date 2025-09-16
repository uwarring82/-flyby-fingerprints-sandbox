import os, json
from simulations.integration.baseline_validator import validate_baseline


def test_uncertainty_aware_pass(tmp_path, monkeypatch):
    """
    With value=1.1 and sigma=0.08 (=> 2σ/val ~ 0.145),
    a 1.0 baseline (dev ~ 0.091) should pass via uncertainty rule.
    """
    monkeypatch.chdir(tmp_path)
    baseline = {"x": 1.0}
    refs = {"x": {"value": 1.1, "sigma": 0.08}}
    report = validate_baseline(baseline, refs, rel_tolerance=0.20, sigma_N=2.0)
    assert report["x"]["pass"] is True
    assert os.path.exists("artifacts/baseline/benchmark_comparisons.json")


def test_fixed_tolerance_fail_then_pass(tmp_path, monkeypatch):
    """
    For a ref without sigma, rely on rel_tolerance.
    Dev = 0.25 with tol=0.20 -> fail; with tol=0.30 -> pass.
    """
    monkeypatch.chdir(tmp_path)
    baseline = {"y": 1.25}
    refs = {"y": 1.0}
    report = validate_baseline(baseline, refs, rel_tolerance=0.20)
    assert report["y"]["pass"] is False
    report = validate_baseline(baseline, refs, rel_tolerance=0.30)
    assert report["y"]["pass"] is True


def test_missing_sim_value_is_reported(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    baseline = {}
    refs = {"z": {"value": 1.0, "sigma": 0.0}}
    report = validate_baseline(baseline, refs)
    assert report["z"]["pass"] is False
    assert report["z"]["reason"] == "missing_sim_value"
