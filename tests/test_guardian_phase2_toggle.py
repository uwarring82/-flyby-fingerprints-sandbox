import os
from pathlib import Path
from simulations.validation.guardian_gates import _phase2_enabled  # type: ignore


def test_phase2_toggle(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    os.makedirs("docs/wiki/Phase_Gates", exist_ok=True)
    # Initially off
    assert _phase2_enabled() is False
    # Create gate file -> on
    Path("docs/wiki/Phase_Gates/Phase_2_Integration.md").write_text("# Phase 2", encoding="utf-8")
    # Need to re-import to pick new cwd? The function resolves absolute path each call, so OK.
    assert _phase2_enabled() is True
