from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from typing import Tuple

import numpy as np
import pandas as pd

try:
    from pydantic import BaseModel, Field
except ModuleNotFoundError:  # pragma: no cover - fallback for offline environments
    class BaseModel:  # type: ignore[override]
        """Very small fallback shim replicating minimal Pydantic behaviour."""

        def __init__(self, **data):
            expected = getattr(self, "__annotations__", {})
            missing = [name for name in expected if name not in data]
            if missing:
                raise TypeError(f"Missing fields: {', '.join(missing)}")
            unexpected = [name for name in data if name not in expected]
            if unexpected:
                raise TypeError(f"Unexpected fields: {', '.join(unexpected)}")
            for key, value in data.items():
                setattr(self, key, value)

    def Field(default=..., description=""):
        return default


class HeatingRow(BaseModel):
    time_s: float = Field(..., description="Time in seconds")
    energy_quanta: float = Field(..., description="Motional quanta")


class TrialRow(BaseModel):
    trial_id: int
    counts: float


class EventRow(BaseModel):
    t_s: float
    event: str


@dataclass
class TriadThresholds:
    # Simple demo thresholds; adjust later from real baselines
    A_slope_warn: float = 0.10   # quanta/s warning
    A_slope_fail: float = 0.20   # quanta/s fail
    D_fano_warn: float = 1.0     # unitless
    D_fano_fail: float = 1.2
    M_ac_warn: float = 0.20      # short-lag autocorrelation
    M_ac_fail: float = 0.35


def _load_csv_strict(csv_path: str, model) -> pd.DataFrame:
    header: list[str] | None = None
    with open(csv_path, "r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                candidate = stripped.lstrip("#").strip()
                if candidate:
                    header = [col.strip() for col in candidate.split(",")]
                continue
            break

    df = pd.read_csv(csv_path, comment="#", header=None if header else "infer", names=header)
    # Normalize columns (strip)
    df.columns = [c.strip() for c in df.columns]
    # Validate schema row-wise with Pydantic for friendly errors
    _ = [model(**row._asdict()) if hasattr(row, "_asdict") else model(**row.to_dict())
         for _, row in df.iterrows()]
    return df


def metric_A_slope(heating: pd.DataFrame) -> float:
    """A: linear slope of energy vs time (quanta/s)."""
    t = heating["time_s"].to_numpy(dtype=float)
    e = heating["energy_quanta"].to_numpy(dtype=float)
    # robust to order:
    idx = np.argsort(t)
    t, e = t[idx], e[idx]
    # fit slope with simple LS
    A = np.vstack([t, np.ones_like(t)]).T
    slope, _ = np.linalg.lstsq(A, e, rcond=None)[0]
    return float(slope)


def metric_D_fano(trials: pd.DataFrame) -> float:
    """D: Fano factor for counts (variance/mean)."""
    x = trials["counts"].to_numpy(dtype=float)
    mean = np.mean(x)
    var = np.var(x, ddof=1) if x.size > 1 else 0.0
    return float(var / mean) if mean > 0 else 0.0


def metric_M_shortlag(events: pd.DataFrame, lag_s: float = 1.0) -> float:
    """
    M: Short-lag temporal autocorrelation proxy.
    For the toy model, compute fraction of inter-event intervals < lag_s.
    """
    t = np.sort(events["t_s"].to_numpy(dtype=float))
    if t.size < 2:
        return 0.0
    dt = np.diff(t)
    return float(np.mean(dt < lag_s))


def triad_decision(A_slope: float, D_fano: float, M_ac: float, thr: TriadThresholds) -> Tuple[str, dict]:
    """
    Returns ("OK" | "WARN" | "FAIL", details)
    Decision heuristic: if any metric crosses fail -> FAIL; else if any crosses warn -> WARN; else OK.
    """
    flags = {
        "A": "OK" if A_slope < thr.A_slope_warn else ("WARN" if A_slope < thr.A_slope_fail else "FAIL"),
        "D": "OK" if D_fano < thr.D_fano_warn else ("WARN" if D_fano < thr.D_fano_fail else "FAIL"),
        "M": "OK" if M_ac   < thr.M_ac_warn   else ("WARN" if M_ac   < thr.M_ac_fail   else "FAIL"),
    }
    summary_state = "OK"
    if "FAIL" in flags.values():
        summary_state = "FAIL"
    elif "WARN" in flags.values():
        summary_state = "WARN"

    details = {
        "A_slope_quanta_per_s": A_slope,
        "D_fano": D_fano,
        "M_shortlag_ac": M_ac,
        "flags": flags,
        "decision": summary_state,
    }
    return summary_state, details


def run_triad(data_root: str, out_dir: str, thresholds: TriadThresholds) -> dict:
    os.makedirs(out_dir, exist_ok=True)
    heating = _load_csv_strict(os.path.join(data_root, "heating.csv"), HeatingRow)
    trials  = _load_csv_strict(os.path.join(data_root, "sb_trials.csv"), TrialRow)
    events  = _load_csv_strict(os.path.join(data_root, "events.csv"), EventRow)

    A = metric_A_slope(heating)
    D = metric_D_fano(trials)
    M = metric_M_shortlag(events)

    state, details = triad_decision(A, D, M, thresholds)

    # Write CSV and JSON summary
    csv_path = os.path.join(out_dir, "triad_summary.csv")
    pd.DataFrame([{
        "A_slope_quanta_per_s": details["A_slope_quanta_per_s"],
        "D_fano": details["D_fano"],
        "M_shortlag_ac": details["M_shortlag_ac"],
        "flag_A": details["flags"]["A"],
        "flag_D": details["flags"]["D"],
        "flag_M": details["flags"]["M"],
        "decision": details["decision"],
    }]).to_csv(csv_path, index=False)

    json_path = os.path.join(out_dir, "triad_report.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(details, f, indent=2)

    return {"csv": csv_path, "json": json_path, "decision": state}


def main():
    parser = argparse.ArgumentParser(description="Run toy A–D–M triad on dataset folder.")
    parser.add_argument("--data-root", type=str, required=True, help="Folder containing heating.csv, sb_trials.csv, events.csv")
    parser.add_argument("--out", type=str, required=True, help="Output folder")
    parser.add_argument("--strict", action="store_true", help="Use stricter thresholds (more sensitive)")
    args = parser.parse_args()

    thr = TriadThresholds()
    if args.strict:
        thr = TriadThresholds(
            A_slope_warn=0.08, A_slope_fail=0.15,
            D_fano_warn=0.9,  D_fano_fail=1.1,
            M_ac_warn=0.18,   M_ac_fail=0.30
        )

    result = run_triad(args.data_root, args.out, thr)
    print(f"[TRIAD] decision={result['decision']} csv={result['csv']} json={result['json']}")


if __name__ == "__main__":
    main()
