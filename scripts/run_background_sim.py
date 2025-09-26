#!/usr/bin/env python3
"""
Run background-only simulation with user-selected parameters and save plots + a Guardian report.

Outputs (written to artifacts/simulations/<timestamp>_*.{png,json}):
  - <stamp>_time_series.png
  - <stamp>_psd.png
  - <stamp>_allan.png
  - <stamp>_guardian_report.json
  - <stamp>_config.json
"""

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

try:
    from simulation.background_effects_simulator import (
        BackgroundConfig,
        simulate_background_timeseries,
    )
    from simulation.guardian_validators.guardian_background_validator import (
        guardian_check_backgrounds,
    )
except ModuleNotFoundError:  # pragma: no cover - fallback when package isn't installed
    ROOT = Path(__file__).resolve().parents[1]
    SRC = ROOT / "src"
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))
    from simulation.background_effects_simulator import (
        BackgroundConfig,
        simulate_background_timeseries,
    )
    from simulation.guardian_validators.guardian_background_validator import (
        guardian_check_backgrounds,
    )


# ---------- plotting helpers ----------

def _plot_time_series(
    data: Dict[str, Any],
    show_pos: bool = True,
    show_em: bool = True,
    show_surf: bool = True,
    show_det: bool = True,
    outpath: Path | None = None,
) -> None:
    plt.figure(figsize=(10, 4))
    if show_pos:
        plt.plot(data["position"], label="position")
    if show_em:
        plt.plot(data["em_pickup"], label="em_pickup")
    if show_surf:
        plt.plot(data["surface_drift"], label="surface_drift")
    if show_det:
        plt.plot(data["detector_counts"], label="detector_counts")
    plt.legend()
    plt.title("Background channels (time domain)")
    plt.xlabel("Sample")
    plt.ylabel("arb.")
    plt.tight_layout()
    if outpath is not None:
        plt.savefig(outpath, dpi=180)
    plt.close()


def _plot_psd_em(data: Dict[str, Any], dt_s: float, outpath: Path | None = None) -> None:
    from numpy.fft import rfft, rfftfreq

    y = np.asarray(data["em_pickup"])
    y = y - float(np.mean(y))
    Y = np.abs(rfft(y)) ** 2
    f = rfftfreq(len(y), dt_s)
    # avoid the DC bin for log scale
    f = f[1:]
    Y = Y[1:]

    plt.figure(figsize=(10, 4))
    plt.loglog(f, Y)
    plt.title("EM pickup PSD")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Power")
    plt.tight_layout()
    if outpath is not None:
        plt.savefig(outpath, dpi=180)
    plt.close()


def _allan_like(x: np.ndarray, dt_s: float, taus: np.ndarray) -> np.ndarray:
    out = []
    for tau in taus:
        m = max(1, int(tau / dt_s))
        blocks = len(x) // m
        if blocks < 2:
            out.append(np.nan)
            continue
        means = np.mean(x[: blocks * m].reshape(blocks, m), axis=1)
        out.append(0.5 * np.mean(np.diff(means) ** 2))
    return np.array(out)


def _plot_allan_like_surface(
    data: Dict[str, Any], dt_s: float, outpath: Path | None = None
) -> None:
    y = np.asarray(data["surface_drift"])
    if len(y) < 2:
        taus = np.array([dt_s])
        ad = np.array([np.nan])
    else:
        taus = np.logspace(np.log10(10 * dt_s), np.log10(len(y) * dt_s / 5.0), 30)
        ad = _allan_like(y, dt_s, taus)

    plt.figure(figsize=(10, 4))
    plt.loglog(taus, ad)
    plt.title("Surface drift — Allan-like variance")
    plt.xlabel("Tau [s]")
    plt.ylabel("Allan-like var")
    plt.tight_layout()
    if outpath is not None:
        plt.savefig(outpath, dpi=180)
    plt.close()


# ---------- IO helpers ----------

def _save_json(obj: Dict[str, Any], outpath: Path) -> None:
    outpath.parent.mkdir(parents=True, exist_ok=True)
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)


# ---------- main ----------

def run_and_save(
    *,
    T: float,
    rf_rms: float,
    mains: float,
    em_coupling: float,
    patch: float,
    corr: float,
    cps: float,
    tint_ms: float,
    n_samples: int,
    dt_s: float,
    seed: int,
    outdir: str = "artifacts/simulations",
    show_pos: bool = True,
    show_em: bool = True,
    show_surf: bool = True,
    show_det: bool = True,
):
    stamp = time.strftime("%Y%m%dT%H%M%S")
    outdir_p = Path(outdir)
    outdir_p.mkdir(parents=True, exist_ok=True)

    cfg = BackgroundConfig(
        T_kelvin=T,
        rf_pickup_rms=rf_rms,
        mains_hz=mains,
        em_coupling_coeff=em_coupling,
        patch_potential_rms_mV=patch,
        patch_corr_length_um=corr,
        photon_rate_bg_cps=cps,
        readout_integration_ms=tint_ms,
    )

    data = simulate_background_timeseries(
        n_samples=n_samples, dt_s=dt_s, cfg=cfg, seed=seed
    )
    report = guardian_check_backgrounds(data)

    # save config + report
    _save_json(
        {
            "timestamp": stamp,
            "params": {
                "T_kelvin": T,
                "rf_pickup_rms_mV": rf_rms,
                "mains_hz": mains,
                "em_coupling_coeff": em_coupling,
                "patch_potential_rms_mV": patch,
                "patch_corr_length_um": corr,
                "photon_rate_bg_cps": cps,
                "readout_integration_ms": tint_ms,
                "n_samples": n_samples,
                "dt_s": dt_s,
                "seed": seed,
            },
            "metadata": data.get("metadata", {}),
        },
        outdir_p / f"{stamp}_config.json",
    )
    _save_json(report, outdir_p / f"{stamp}_guardian_report.json")

    # plots
    _plot_time_series(
        data,
        show_pos,
        show_em,
        show_surf,
        show_det,
        outdir_p / f"{stamp}_time_series.png",
    )
    _plot_psd_em(data, dt_s, outdir_p / f"{stamp}_psd.png")
    _plot_allan_like_surface(data, dt_s, outdir_p / f"{stamp}_allan.png")

    return report, {
        "config": str(outdir_p / f"{stamp}_config.json"),
        "report": str(outdir_p / f"{stamp}_guardian_report.json"),
        "time_series_png": str(outdir_p / f"{stamp}_time_series.png"),
        "psd_png": str(outdir_p / f"{stamp}_psd.png"),
        "allan_png": str(outdir_p / f"{stamp}_allan.png"),
    }


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Run background-only simulation and save plots + Guardian report."
    )
    p.add_argument("--T", type=float, default=300.0, help="Temperature [K]")
    p.add_argument("--rf_rms", type=float, default=0.5, help="RF pickup RMS [mV]")
    p.add_argument("--mains", type=float, default=50.0, help="Mains frequency [Hz]")
    p.add_argument(
        "--em_coupling", type=float, default=1e-3, help="EM coupling coefficient"
    )
    p.add_argument("--patch", type=float, default=5.0, help="Patch potential RMS [mV]")
    p.add_argument(
        "--corr", type=float, default=50.0, help="Patch correlation length [um]"
    )
    p.add_argument("--cps", type=float, default=200.0, help="Background photon rate [counts/s]")
    p.add_argument(
        "--tint",
        dest="tint_ms",
        type=float,
        default=1.0,
        help="Readout integration time [ms]",
    )
    p.add_argument("--n_samples", type=int, default=10000, help="Number of samples")
    p.add_argument("--dt", dest="dt_s", type=float, default=1e-4, help="Sample period [s]")
    p.add_argument("--seed", type=int, default=42, help="PRNG seed")
    p.add_argument(
        "--outdir",
        type=str,
        default="artifacts/simulations",
        help="Output directory",
    )
    # visibility toggles
    p.add_argument("--hide_pos", action="store_true", help="Hide position trace")
    p.add_argument("--hide_em", action="store_true", help="Hide EM pickup trace")
    p.add_argument("--hide_surf", action="store_true", help="Hide surface drift trace")
    p.add_argument(
        "--hide_det", action="store_true", help="Hide detector counts trace"
    )
    return p


def main() -> None:
    args = _build_parser().parse_args()
    report, files = run_and_save(
        T=args.T,
        rf_rms=args.rf_rms,
        mains=args.mains,
        em_coupling=args.em_coupling,
        patch=args.patch,
        corr=args.corr,
        cps=args.cps,
        tint_ms=args.tint_ms,
        n_samples=args.n_samples,
        dt_s=args.dt_s,
        seed=args.seed,
        outdir=args.outdir,
        show_pos=not args.hide_pos,
        show_em=not args.hide_em,
        show_surf=not args.hide_surf,
        show_det=not args.hide_det,
    )
    print("Guardian report:", json.dumps(report, indent=2))
    print("Files:", json.dumps(files, indent=2))


if __name__ == "__main__":
    main()
