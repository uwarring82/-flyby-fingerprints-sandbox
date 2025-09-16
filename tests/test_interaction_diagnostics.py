import os, json
from simulations.integration.interaction_diagnostics import diagnose_interactions


def test_zero_sum_safe(tmp_path, monkeypatch):
    """No div-by-zero when all individual totals are zero."""
    monkeypatch.chdir(tmp_path)
    individual = {"rf": {"k": 0.0}, "patch": {"k": 0.0}}
    combined = {"k": 0.0}
    flagged = diagnose_interactions(individual, combined, rel_threshold=0.10, noise_floor=1e-9)
    assert flagged == {}  # should not flag; denominator clamped by noise_floor
    assert (tmp_path / "artifacts/baseline/interaction_matrix.json").exists()


def test_flags_above_threshold_and_writes_json(tmp_path, monkeypatch):
    """If combined deviates >10% from sum, it must be flagged and JSON written."""
    monkeypatch.chdir(tmp_path)
    individual = {"rf": {"rate": 1.0}, "patch": {"rate": 0.0}}
    combined = {"rate": 1.2}  # 20% deviation
    flagged = diagnose_interactions(individual, combined, rel_threshold=0.10, noise_floor=1e-12)
    assert "rate" in flagged and flagged["rate"] > 0.10
    out = json.loads(open("artifacts/baseline/interaction_matrix.json").read())
    assert isinstance(out, dict) and "rate" in out
    assert out["rate"] == flagged["rate"]  # stored strengths match returned values
