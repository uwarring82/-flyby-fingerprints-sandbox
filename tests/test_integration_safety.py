import os, json
from simulations.integration.interaction_diagnostics import diagnose_interactions
from simulations.integration.baseline_validator import validate_baseline


def test_diagnose_interactions_zero_safe(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    individual = {"a": {"k": 0.0}, "b": {"k": 0.0}}
    combined = {"k": 0.0}
    flagged = diagnose_interactions(individual, combined, rel_threshold=0.10, noise_floor=1e-9)
    assert flagged == {}
    assert os.path.exists("artifacts/baseline/interaction_matrix.json")


def test_validate_baseline_uncertainty_aware(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    base = {"x": 1.0}
    refs = {"x": {"value": 1.1, "sigma": 0.08}}  # ~7.3% dev; 2σ≈14.5% => pass
    rep = validate_baseline(base, refs, rel_tolerance=0.20)
    assert rep["x"]["pass"] is True
    assert os.path.exists("artifacts/baseline/benchmark_comparisons.json")
