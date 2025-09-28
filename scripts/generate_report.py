#!/usr/bin/env python3
"""Generate Guardian-compliant simulation reports (Phase 1 standard)."""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
import textwrap
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import scipy
from scipy import signal, stats

try:  # pragma: no cover - fallback for editable installs
    from simulation.background_effects_simulator import (
        BackgroundConfig,
        simulate_background_timeseries,
    )
except ModuleNotFoundError:  # pragma: no cover
    ROOT = Path(__file__).resolve().parents[1]
    SRC = ROOT / "src"
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))
    from simulation.background_effects_simulator import (
        BackgroundConfig,
        simulate_background_timeseries,
    )

try:  # pragma: no cover
    from scripts.util_hashes import write_manifest
except ModuleNotFoundError:  # pragma: no cover
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from scripts.util_hashes import write_manifest

PRESETS: Dict[str, Dict[str, Any]] = {
    "default": {
        "T": 300.0,
        "rf_rms": 0.5,
        "mains": 50.0,
        "em_coupling": 1e-3,
        "patch": 5.0,
        "corr": 50.0,
        "cps": 200.0,
        "tint": 1.0,
        "n_samples": 20000,
        "dt": 1e-4,
        "seed": 42,
        "signal_level": 200.0,
        "signal_freq": 150.0,
    },
    "mains60": {
        "T": 300.0,
        "rf_rms": 0.6,
        "mains": 60.0,
        "em_coupling": 1.5e-3,
        "patch": 7.5,
        "corr": 80.0,
        "cps": 260.0,
        "tint": 1.2,
        "n_samples": 24000,
        "dt": 1e-4,
        "seed": 77,
        "signal_level": 260.0,
        "signal_freq": 120.0,
    },
}


def _apply_watermark(fig: matplotlib.figure.Figure, text: str = "SIMULATION") -> None:
    fig.text(
        0.99,
        0.01,
        text,
        ha="right",
        va="bottom",
        fontsize=18,
        alpha=0.18,
        color="#444444",
        weight="bold",
    )


def _welch_psd(y: np.ndarray, dt: float) -> Tuple[np.ndarray, np.ndarray]:
    freqs, psd = signal.welch(y, fs=1.0 / dt, nperseg=min(len(y), 4096))
    mask = freqs > 0
    return freqs[mask], psd[mask]


def _allan_like(x: np.ndarray, dt_s: float) -> Tuple[np.ndarray, np.ndarray]:
    if len(x) < 2:
        taus = np.array([dt_s])
        allan = np.array([np.nan])
    else:
        taus = np.logspace(np.log10(10 * dt_s), np.log10(len(x) * dt_s / 5.0), 30)
        allan = []
        for tau in taus:
            m = max(1, int(tau / dt_s))
            blocks = len(x) // m
            if blocks < 2:
                allan.append(np.nan)
                continue
            means = np.mean(x[: blocks * m].reshape(blocks, m), axis=1)
            allan.append(0.5 * np.mean(np.diff(means) ** 2))
        allan = np.array(allan)
    return taus, allan


def _cohens_d(exp: np.ndarray, null: np.ndarray) -> float:
    n1, n2 = len(exp), len(null)
    if n1 < 2 or n2 < 2:
        return float("nan")
    var1 = np.var(exp, ddof=1)
    var2 = np.var(null, ddof=1)
    pooled = ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)
    if pooled <= 0:
        return float("nan")
    return (np.mean(exp) - np.mean(null)) / np.sqrt(pooled)


def _cohens_d_ci(d: float, n1: int, n2: int, alpha: float = 0.05) -> Tuple[float, float]:
    if np.isnan(d) or n1 < 2 or n2 < 2:
        return float("nan"), float("nan")
    se = np.sqrt((n1 + n2) / (n1 * n2) + (d**2) / (2 * (n1 + n2 - 2)))
    z = stats.norm.ppf(1 - alpha / 2)
    return d - z * se, d + z * se


def _git_state(repo: Path) -> Tuple[str, str, bool]:
    try:
        sha = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo)
            .decode()
            .strip()
        )
        short = sha[:7]
    except Exception:  # pragma: no cover - git missing
        sha = "unknown"
        short = "unknown"
    try:
        status = (
            subprocess.check_output(["git", "status", "--porcelain"], cwd=repo)
            .decode()
            .strip()
        )
        clean = status == ""
    except Exception:  # pragma: no cover
        clean = False
    return sha, short, clean


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a paired experimental/null simulation report",
    )
    parser.add_argument(
        "--preset",
        type=str,
        default="default",
        choices=sorted(PRESETS),
        help="Named parameter preset",
    )
    parser.add_argument(
        "--params",
        type=Path,
        help="JSON file with parameter overrides",
    )
    parser.add_argument("--T", type=float, help="Temperature [K]")
    parser.add_argument("--rf_rms", type=float, help="RF pickup RMS [mV]")
    parser.add_argument("--mains", type=float, help="Mains frequency [Hz]")
    parser.add_argument("--em_coupling", type=float, help="EM coupling coefficient")
    parser.add_argument("--patch", type=float, help="Patch potential RMS [mV]")
    parser.add_argument("--corr", type=float, help="Patch correlation length [um]")
    parser.add_argument("--cps", type=float, help="Background photon rate [counts/s]")
    parser.add_argument(
        "--tint",
        type=float,
        help="Readout integration time [ms]",
    )
    parser.add_argument("--n_samples", type=int, help="Number of samples")
    parser.add_argument("--dt", type=float, help="Sample spacing [s]")
    parser.add_argument("--seed", type=int, help="Experimental seed")
    parser.add_argument(
        "--null_seed",
        type=int,
        help="Override seed for null control (defaults to seed+1)",
    )
    parser.add_argument(
        "--signal_level",
        type=float,
        help="Injected signal amplitude on detector counts",
    )
    parser.add_argument(
        "--signal_freq",
        type=float,
        help="Injected signal frequency [Hz]",
    )
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("artifacts/reports"),
        help="Root directory for report artifacts",
    )
    return parser


def _resolve_params(args: argparse.Namespace) -> Dict[str, Any]:
    params = dict(PRESETS[args.preset])
    if args.params:
        overrides = json.loads(Path(args.params).read_text(encoding="utf-8"))
        params.update(overrides)
    for key in [
        "T",
        "rf_rms",
        "mains",
        "em_coupling",
        "patch",
        "corr",
        "cps",
        "tint",
        "n_samples",
        "dt",
        "seed",
        "signal_level",
        "signal_freq",
    ]:
        value = getattr(args, key)
        if value is not None:
            params[key] = value
    if args.null_seed is not None:
        params["null_seed"] = args.null_seed
    else:
        params["null_seed"] = params.get("seed", PRESETS["default"]["seed"]) + 1
    return params


def _run_background(cfg: BackgroundConfig, n_samples: int, dt: float, seed: int) -> Dict[str, Any]:
    data = simulate_background_timeseries(
        n_samples=n_samples,
        dt_s=dt,
        cfg=cfg,
        seed=seed,
    )
    return data


def _make_null_variant(data: Dict[str, Any]) -> Dict[str, Any]:
    null_data = {key: np.copy(value) if isinstance(value, np.ndarray) else value for key, value in data.items()}
    if "position" in null_data:
        null_data["position"] = np.zeros_like(null_data["position"])
    null_data["heating_rate"] = 0.0
    return null_data


def _inject_signal(exp_counts: np.ndarray, time_s: np.ndarray, level: float, freq: float) -> Tuple[np.ndarray, np.ndarray]:
    baseline = level
    signal_wave = baseline + level * np.sin(2 * np.pi * freq * time_s)
    injected = exp_counts.astype(float) + signal_wave
    return injected, signal_wave


def _save_time_series_plot(
    path: Path,
    time_s: np.ndarray,
    exp_counts: np.ndarray,
    null_counts: np.ndarray,
    signal_wave: np.ndarray,
) -> None:
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    axes[0].plot(time_s, null_counts, label="Null", color="#1f77b4")
    axes[0].plot(time_s, exp_counts, label="Experimental", color="#d62728", alpha=0.8)
    axes[0].set_ylabel("Counts")
    axes[0].legend()
    axes[0].set_title("Detector counts")

    axes[1].plot(time_s, exp_counts - null_counts, color="#2ca02c")
    axes[1].set_ylabel("Δ Counts")
    axes[1].set_title("Experimental - Null")

    axes[2].plot(time_s, signal_wave, color="#9467bd")
    axes[2].set_ylabel("Injected")
    axes[2].set_xlabel("Time [s]")
    axes[2].set_title("Injected signal")
    fig.tight_layout()
    _apply_watermark(fig)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200)
    plt.close(fig)


def _save_psd_plot(path: Path, dt: float, exp_counts: np.ndarray, null_counts: np.ndarray) -> None:
    exp_freqs, exp_psd = _welch_psd(exp_counts - np.mean(exp_counts), dt)
    null_freqs, null_psd = _welch_psd(null_counts - np.mean(null_counts), dt)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.loglog(null_freqs, null_psd, label="Null")
    ax.loglog(exp_freqs, exp_psd, label="Experimental", alpha=0.8)
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("PSD")
    ax.set_title("Detector counts PSD")
    ax.legend()
    fig.tight_layout()
    _apply_watermark(fig)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200)
    plt.close(fig)


def _save_allan_plot(path: Path, dt: float, exp_counts: np.ndarray, null_counts: np.ndarray) -> None:
    taus_e, allan_e = _allan_like(exp_counts, dt)
    taus_n, allan_n = _allan_like(null_counts, dt)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.loglog(taus_n, allan_n, label="Null")
    ax.loglog(taus_e, allan_e, label="Experimental", alpha=0.8)
    ax.set_xlabel("Tau [s]")
    ax.set_ylabel("Allan-like var")
    ax.set_title("Allan-like drift")
    ax.legend()
    fig.tight_layout()
    _apply_watermark(fig)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200)
    plt.close(fig)


def _generate_pdf(report_path: Path, guardian: Dict[str, Any], metadata: Dict[str, Any]) -> None:
    lines = [
        "Simulation Report Standard (Phase 1)",
        "",
        f"Timestamp: {metadata['timestamp']}",
        f"Git SHA: {metadata['git']['sha']} (clean={metadata['git']['clean']})",
        f"Preset: {metadata['preset']}",
        "",
        "Key Metrics:",
        f"  Null p-value: {guardian['metrics']['null']['p_value']:.4f} (pass={guardian['metrics']['null']['pass']})",
        f"  Experimental vs Null p-value: {guardian['metrics']['effect']['p_value']:.4e} (pass={guardian['metrics']['effect']['pass']})",
        f"  Cohen's d: {guardian['metrics']['effect']['cohens_d']:.3f} (95% CI: {guardian['metrics']['effect']['ci_95'][0]:.3f}, {guardian['metrics']['effect']['ci_95'][1]:.3f})",
        f"  SNR: {guardian['metrics']['snr']['value']:.2f} (pass={guardian['metrics']['snr']['pass']})",
        "",
        "Environment:",
        f"  Python: {metadata['environment']['python']}",
        f"  Platform: {metadata['environment']['platform']}",
        f"  Packages: numpy={metadata['environment']['packages']['numpy']}, scipy={metadata['environment']['packages']['scipy']}, matplotlib={metadata['environment']['packages']['matplotlib']}",
    ]
    with PdfPages(report_path) as pdf:
        fig, ax = plt.subplots(figsize=(8.27, 11.69))
        ax.axis("off")
        ax.text(
            0.02,
            0.98,
            "\n".join(lines),
            va="top",
            ha="left",
            family="monospace",
            fontsize=11,
        )
        pdf.savefig(fig)
        plt.close(fig)


def generate_report(args: argparse.Namespace) -> Path:
    params = _resolve_params(args)

    cfg = BackgroundConfig(
        T_kelvin=params["T"],
        rf_pickup_rms=params["rf_rms"],
        mains_hz=params["mains"],
        em_coupling_coeff=params["em_coupling"],
        patch_potential_rms_mV=params["patch"],
        patch_corr_length_um=params["corr"],
        photon_rate_bg_cps=params["cps"],
        readout_integration_ms=params["tint"],
    )

    n_samples = int(params["n_samples"])
    dt = float(params["dt"])
    seed = int(params["seed"])
    null_seed = int(params["null_seed"])
    signal_level = float(params["signal_level"])
    signal_freq = float(params["signal_freq"])

    experimental = _run_background(cfg, n_samples, dt, seed)
    null_base = _run_background(cfg, n_samples, dt, null_seed)
    null_data = _make_null_variant(null_base)

    time_s = np.arange(n_samples, dtype=float) * dt
    exp_counts_raw = experimental["detector_counts"].astype(float)
    null_counts = null_data["detector_counts"].astype(float)
    injected_counts, signal_wave = _inject_signal(exp_counts_raw, time_s, signal_level, signal_freq)
    experimental_counts = injected_counts

    expected_counts = cfg.photon_rate_bg_cps * (cfg.readout_integration_ms * 1e-3)
    null_test = stats.ttest_1samp(null_counts, popmean=expected_counts)
    effect_test = stats.ttest_ind(experimental_counts, null_counts, equal_var=False)

    effect_claimed = bool(signal_level > 0)
    snr = float(
        np.sqrt(np.mean(signal_wave**2))
        / (np.std(null_counts - expected_counts) + 1e-12)
    )

    d = _cohens_d(experimental_counts, null_counts)
    ci_low, ci_high = _cohens_d_ci(d, len(experimental_counts), len(null_counts))

    guardian = {
        "standard": "Simulation Report Standard (Phase 1)",
        "null_control_present": True,
        "metrics": {
            "null": {
                "statistic": null_test.statistic,
                "p_value": float(null_test.pvalue),
                "threshold": {"min_p_value": 0.05},
                "pass": bool(null_test.pvalue >= 0.05),
            },
            "effect": {
                "statistic": effect_test.statistic,
                "p_value": float(effect_test.pvalue),
                "threshold": {"max_p_value": 0.01},
                "pass": (not effect_claimed) or bool(effect_test.pvalue < 0.01),
                "effect_claimed": effect_claimed,
                "cohens_d": float(d),
                "ci_95": [float(ci_low), float(ci_high)],
            },
            "snr": {
                "value": snr,
                "threshold": {"min": 10.0},
                "pass": (not effect_claimed) or bool(snr >= 10.0),
            },
        },
    }

    repo_root = Path(__file__).resolve().parents[1]
    git_sha, git_short, git_clean = _git_state(repo_root)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    report_dir = args.outdir / f"{timestamp}_{git_short}"
    report_dir.mkdir(parents=True, exist_ok=True)

    environment = {
        "python": sys.version.replace("\n", " "),
        "platform": platform.platform(),
        "packages": {
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "matplotlib": matplotlib.__version__,
        },
    }

    metadata = {
        "timestamp": timestamp,
        "preset": args.preset,
        "params": params,
        "git": {"sha": git_sha, "short": git_short, "clean": git_clean},
        "environment": environment,
        "seeds": {"experimental": seed, "null": null_seed},
        "paths": {"root": str(report_dir)},
    }

    (report_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )
    (report_dir / "guardian.json").write_text(
        json.dumps(guardian, indent=2), encoding="utf-8"
    )

    np.savez(
        report_dir / "results.npz",
        time_s=time_s,
        experimental_counts=experimental_counts,
        null_counts=null_counts,
        signal_wave=signal_wave,
        experimental_position=experimental["position"],
        null_position=null_data["position"],
        experimental_em=experimental["em_pickup"],
        null_em=null_data["em_pickup"],
        experimental_surface=experimental["surface_drift"],
        null_surface=null_data["surface_drift"],
    )

    _save_time_series_plot(
        report_dir / "detector_time_series.png",
        time_s,
        experimental_counts,
        null_counts,
        signal_wave,
    )
    _save_psd_plot(report_dir / "detector_psd.png", dt, experimental_counts, null_counts)
    _save_allan_plot(
        report_dir / "detector_allan.png",
        dt,
        experimental_counts,
        null_counts,
    )

    code_state_path = report_dir / "code_state.txt"
    code_state_path.write_text(
        textwrap.dedent(
            f"""
            git_sha: {git_sha}
            short_sha: {git_short}
            clean_tree: {str(git_clean).lower()}
            generated_at_utc: {timestamp}
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )

    report_pdf = report_dir / "report.pdf"
    _generate_pdf(report_pdf, guardian, metadata)

    manifest_path = write_manifest(report_dir)

    summary = {
        "report_dir": str(report_dir),
        "sha256sum": str(manifest_path),
        "metrics": guardian["metrics"],
    }
    (report_dir / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    return report_dir


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    report_dir = generate_report(args)
    print(json.dumps({"report_dir": str(report_dir)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
