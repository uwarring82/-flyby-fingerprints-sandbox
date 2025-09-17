import os

from flyby.triad import (
    _load_csv_strict,
    HeatingRow,
    TrialRow,
    EventRow,
    metric_A_slope,
    metric_D_fano,
    metric_M_shortlag,
    triad_decision,
    TriadThresholds,
)

DATA = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "toy"))


def test_loading():
    h = _load_csv_strict(os.path.join(DATA, "heating.csv"), HeatingRow)
    t = _load_csv_strict(os.path.join(DATA, "sb_trials.csv"), TrialRow)
    e = _load_csv_strict(os.path.join(DATA, "events.csv"), EventRow)
    assert {"time_s", "energy_quanta"}.issubset(h.columns)
    assert {"trial_id", "counts"}.issubset(t.columns)
    assert {"t_s", "event"}.issubset(e.columns)


def test_metrics_expected_ranges():
    h = _load_csv_strict(os.path.join(DATA, "heating.csv"), HeatingRow)
    t = _load_csv_strict(os.path.join(DATA, "sb_trials.csv"), TrialRow)
    e = _load_csv_strict(os.path.join(DATA, "events.csv"), EventRow)

    A = metric_A_slope(h)
    D = metric_D_fano(t)
    M = metric_M_shortlag(e, lag_s=1.0)

    # Toy expectations: increasing slope around ~0.2; Fano near ~0.8-1.5; short-lag fraction ~0.5
    assert 0.15 <= A <= 0.25
    assert 0.5 <= D <= 1.6
    assert 0.0 <= M <= 1.0


def test_decision_logic():
    thr = TriadThresholds()
    state, _ = triad_decision(0.12, 0.9, 0.1, thr)  # A warns, others OK
    assert state == "WARN"
    state2, _ = triad_decision(0.25, 0.8, 0.1, thr)  # A fails
    assert state2 == "FAIL"
