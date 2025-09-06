# SPDX-License-Identifier: GPL-3.0-or-later
# (c) 2025 Ulrich Warring and contributors

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple, Optional, Iterable

import json
import math
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt


@dataclass
class TriadResult:
    trap_id: str
    run_id: str
    A_stat: float
    A_p: float
    b_A: int
    D_stat: float
    D_p: float
    b_D: int
    M_stat: float
    M_p: float
    b_M: int


class FastTriadAnalyzer:
    """Minimal A–D–M fast-screening for fly-by fingerprints.

    This class provides a lightweight interface to load historical data, run the
    Fast Triad screening, and emit summary tables, JSON reports, and quick-look
    diagnostic plots.  The current statistics are first-order placeholders; the
    calibration of cutoffs and error models is left for future work.

    Data expectations (CSV in ``data_root``)::

        heating.csv  : trap_id, run_id, mode, frequency_hz,
                        heating_rate_quanta_per_s, heating_rate_err
        sb_trials.csv: trap_id, run_id, sequence, outcome (0/1), t_rel_s
        events.csv   : trap_id, run_id, t_s

    Methods
    -------
    load_data(data_root)
        Load three tables from ``data_root``.
    evaluate_data()
        Compute per-run A/D/M statistics and decisions.
    generate_output(out_dir)
        Write ``triad_summary.csv`` and ``triad_report.json`` to ``out_dir`` and
        save diagnostic plots under ``out_dir/plots``.
    """

    def __init__(self) -> None:
        self.heating: Optional[pd.DataFrame] = None
        self.trials: Optional[pd.DataFrame] = None
        self.events: Optional[pd.DataFrame] = None
        self.results: Optional[pd.DataFrame] = None

    # ------------------------
    # Public API
    # ------------------------
    def load_data(self, data_root: Path) -> None:
        """Load required CSV files from ``data_root``.

        Missing files are tolerated and replaced with empty data frames containing
        the expected columns so that subsequent steps can proceed without raising
        exceptions.  This enables graceful handling of minimal demo datasets.
        """
        data_root = Path(data_root)
        self.heating = self._read_csv(
            data_root / "heating.csv",
            [
                "trap_id",
                "run_id",
                "mode",
                "frequency_hz",
                "heating_rate_quanta_per_s",
                "heating_rate_err",
            ],
        )
        self.trials = self._read_csv(
            data_root / "sb_trials.csv",
            ["trap_id", "run_id", "sequence", "outcome", "t_rel_s"],
        )
        self.events = self._read_csv(
            data_root / "events.csv", ["trap_id", "run_id", "t_s"]
        )

        # basic normalization
        for df in (self.heating, self.trials, self.events):
            if df is not None and not df.empty:
                df["trap_id"] = df["trap_id"].astype(str)
                df["run_id"] = df["run_id"].astype(str)

    def evaluate_data(self) -> pd.DataFrame:
        """Compute the A/D/M statistics for each (trap_id, run_id) pair."""
        assert self.heating is not None, "heating.csv not loaded"
        assert self.trials is not None, "sb_trials.csv not loaded"
        assert self.events is not None, "events.csv not loaded"

        runs = (
            self.heating[["trap_id", "run_id"]].drop_duplicates()
            .merge(
                self.trials[["trap_id", "run_id"]].drop_duplicates(),
                how="outer",
            )
            .merge(
                self.events[["trap_id", "run_id"]].drop_duplicates(),
                how="outer",
            )
            .dropna(subset=["trap_id", "run_id"])
        )

        out_rows: list[Dict[str, object]] = []
        for _, r in runs.iterrows():
            trap_id, run_id = str(r.trap_id), str(r.run_id)
            dfH = self.heating.query("trap_id==@trap_id and run_id==@run_id")
            dfT = self.trials.query("trap_id==@trap_id and run_id==@run_id")
            dfE = self.events.query("trap_id==@trap_id and run_id==@run_id")

            A_stat, A_p = self._analog_stat(dfH)
            D_stat, D_p = self._digital_stat(dfT)
            M_stat, M_p = self._memory_stat(dfE)

            b_A = int(np.isfinite(A_p) and A_p < 5e-3)
            b_D = int(np.isfinite(D_p) and D_p < 5e-3)
            b_M = int(np.isfinite(M_p) and M_p < 5e-3)

            out_rows.append(
                TriadResult(
                    trap_id,
                    run_id,
                    float(A_stat),
                    float(A_p),
                    b_A,
                    float(D_stat),
                    float(D_p),
                    b_D,
                    float(M_stat),
                    float(M_p),
                    b_M,
                ).__dict__
            )

        cols = list(TriadResult.__annotations__.keys())
        self.results = pd.DataFrame(out_rows, columns=cols)
        return self.results

    def generate_output(self, out_dir: Path) -> None:
        """Write CSV/JSON outputs and per-run diagnostic plots."""
        assert self.results is not None, "run evaluate_data() first"
        out_dir = Path(out_dir)
        (out_dir / "plots").mkdir(parents=True, exist_ok=True)

        # tabular outputs
        self.results.to_csv(out_dir / "triad_summary.csv", index=False)

        by_trap = (
            self.results.groupby("trap_id")[["b_A", "b_D", "b_M"]]
            .sum()
            .astype(int)
            .to_dict(orient="index")
        )
        report = {
            "n_runs": int(len(self.results)),
            "n_flags": int(self.results[["b_A", "b_D", "b_M"]].sum().sum()),
            "by_trap": by_trap,
        }
        with open(out_dir / "triad_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        # plots per run
        for _, row in self.results.iterrows():
            self._plot_run(row["trap_id"], row["run_id"], out_dir / "plots")

    # ------------------------
    # I/O helpers
    # ------------------------
    @staticmethod
    def _read_csv(path: Path, columns: Iterable[str]) -> pd.DataFrame:
        """Return a DataFrame from ``path`` or an empty frame with ``columns``."""
        if not path.exists():
            return pd.DataFrame(columns=list(columns))
        return pd.read_csv(path)

    # ------------------------
    # A/D/M statistics
    # ------------------------
    @staticmethod
    def _analog_stat(df: pd.DataFrame) -> Tuple[float, float]:
        """A: test for impulsive mixture on heating vs frequency."""
        if df is None or df.empty:
            return float("nan"), float("nan")
        d = df.dropna(
            subset=["frequency_hz", "heating_rate_quanta_per_s", "heating_rate_err"]
        ).copy()
        d = d[d["heating_rate_quanta_per_s"] > 0]
        if len(d) < 4:
            return float("nan"), float("nan")

        x = np.log(d["frequency_hz"].values)
        y = np.log(d["heating_rate_quanta_per_s"].values)
        frac_err = d["heating_rate_err"].values / d["heating_rate_quanta_per_s"].values
        w = 1.0 / np.clip(frac_err, 1e-6, None) ** 2

        X = np.vstack([np.ones_like(x), -x]).T
        beta_bg = np.linalg.lstsq(X * np.sqrt(w[:, None]), y * np.sqrt(w), rcond=None)[0]
        yhat_bg = X @ beta_bg
        rss_bg = np.sum(w * (y - yhat_bg) ** 2)

        g_bg = np.exp(yhat_bg)
        g = np.exp(y)
        kappas = np.logspace(-6, 6, 241)

        def obj(k: float) -> float:
            return float(np.sum((g - (g_bg + max(float(k), 0.0))) ** 2))

        errs = [obj(k) for k in kappas]
        k_best = kappas[int(np.argmin(errs))]
        rss_mix = np.sum((g - (g_bg + k_best)) ** 2)

        stat = max(0.0, rss_bg - rss_mix)
        p = float(stats.chi2.sf(stat, 1))
        return float(stat), p

    @staticmethod
    def _digital_stat(df: pd.DataFrame, window_s: float = 5.0) -> Tuple[float, float]:
        """D: overdispersion + runs test on interleaved binary trials."""
        if df is None or df.empty or "t_rel_s" not in df:
            return float("nan"), float("nan")
        d = df.dropna(subset=["t_rel_s", "outcome"]).copy()
        if len(d) < 20:
            return float("nan"), float("nan")

        # windowed counts of '1' outcomes
        t0, t1 = d["t_rel_s"].min(), d["t_rel_s"].max()
        bins = np.arange(t0, t1 + window_s, window_s)
        counts, _ = np.histogram(d["t_rel_s"].values[d["outcome"] == 1], bins=bins)
        lam = counts.mean() if len(counts) else 0.0
        var = counts.var(ddof=1) if len(counts) > 1 else 0.0

        if lam > 0 and len(counts) > 5:
            z = (var - lam) / (math.sqrt(2 * (lam ** 2) / max(len(counts) - 1, 1)) + 1e-12)
            p_disp = float(stats.norm.sf(z))
        else:
            p_disp = float("nan")

        seq = d.sort_values("t_rel_s")["outcome"].astype(int).values
        n1, n2 = int(seq.sum()), int(len(seq) - seq.sum())
        runs = 1 + int(np.sum(seq[1:] != seq[:-1])) if len(seq) > 1 else 1
        mu_runs = 1 + 2 * n1 * n2 / (n1 + n2) if (n1 + n2) > 0 else float("nan")
        var_runs = (
            (2 * n1 * n2 * (2 * n1 * n2 - n1 - n2))
            / (((n1 + n2) ** 2) * (n1 + n2 - 1))
            if (n1 + n2) > 1
            else float("nan")
        )
        if np.isfinite(var_runs) and var_runs > 0:
            z_runs = (runs - mu_runs) / math.sqrt(var_runs)
            p_runs = float(2 * stats.norm.sf(abs(z_runs)))
        else:
            p_runs = float("nan")

        plist = [p for p in (p_disp, p_runs) if np.isfinite(p) and p > 0]
        if not plist:
            return float("nan"), float("nan")
        stat = float(-2 * np.sum(np.log(plist)))
        p = float(stats.chi2.sf(stat, 2 * len(plist)))
        return stat, p

    @staticmethod
    def _memory_stat(
        df: pd.DataFrame, bin_s: float = 5.0, m_lags: int = 10
    ) -> Tuple[float, float]:
        """M: Ljung–Box on binned event counts."""
        if df is None or df.empty or "t_s" not in df:
            return float("nan"), float("nan")
        d = df.dropna(subset=["t_s"]).copy()
        if len(d) < 10:
            return float("nan"), float("nan")

        t0, t1 = d["t_s"].min(), d["t_s"].max()
        bins = np.arange(t0, t1 + bin_s, bin_s)
        counts, _ = np.histogram(d["t_s"].values, bins=bins)
        x = counts - counts.mean()
        n = len(x)
        if n < m_lags + 1:
            return float("nan"), float("nan")

        ac = [1.0]
        for k in range(1, m_lags + 1):
            x1, x2 = x[:-k], x[k:]
            num = np.sum((x1 - x1.mean()) * (x2 - x2.mean()))
            den = math.sqrt(
                np.sum((x1 - x1.mean()) ** 2) * np.sum((x2 - x2.mean()) ** 2)
            ) + 1e-12
            ac.append(float(num / den))
        ac = np.array(ac)

        Q = float(n * (n + 2) * np.sum((ac[1:] ** 2) / (np.arange(1, m_lags + 1))))
        p = float(stats.chi2.sf(Q, m_lags))
        return Q, p

    # ------------------------
    # Plotting
    # ------------------------
    def _plot_run(self, trap_id: str, run_id: str, plot_dir: Path) -> None:
        """One-page diagnostic figure for a given run."""
        fig, axes = plt.subplots(3, 1, figsize=(8, 10))
        fig.suptitle(f"{trap_id} / {run_id} — Fast Triad diagnostics")

        # A: heating vs frequency
        dfH = self.heating.query("trap_id==@trap_id and run_id==@run_id")
        if dfH is not None and not dfH.empty:
            dH = dfH.dropna(subset=["frequency_hz", "heating_rate_quanta_per_s"]).copy()
            axes[0].loglog(
                dH["frequency_hz"], dH["heating_rate_quanta_per_s"], "o"
            )
            axes[0].set_xlabel("Mode frequency (Hz)")
            axes[0].set_ylabel("Heating rate (quanta/s)")
            axes[0].grid(True, which="both", ls=":")

        # D: binary outcomes over time
        dfT = self.trials.query("trap_id==@trap_id and run_id==@run_id")
        if dfT is not None and not dfT.empty and "t_rel_s" in dfT:
            dT = dfT.sort_values("t_rel_s")
            axes[1].step(dT["t_rel_s"], dT["outcome"], where="post")
            axes[1].set_xlabel("t_rel (s)")
            axes[1].set_ylabel("Outcome (0/1)")
            axes[1].grid(True, ls=":")

        # M: binned event counts
        dfE = self.events.query("trap_id==@trap_id and run_id==@run_id")
        if dfE is not None and not dfE.empty and "t_s" in dfE:
            dE = dfE.sort_values("t_s")
            if len(dE) > 1:
                bin_s = max((dE["t_s"].max() - dE["t_s"].min()) / 30.0, 1.0)
                bins = np.arange(dE["t_s"].min(), dE["t_s"].max() + bin_s, bin_s)
                counts, edges = np.histogram(dE["t_s"], bins=bins)
                centers = 0.5 * (edges[:-1] + edges[1:])
                axes[2].plot(centers, counts, "-o")
        axes[2].set_xlabel("t (s)")
        axes[2].set_ylabel("Event count per bin")
        axes[2].grid(True, ls=":")

        plot_dir.mkdir(parents=True, exist_ok=True)
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        out_path = plot_dir / f"{trap_id}__{run_id}.png"
        fig.savefig(out_path, dpi=150)
        plt.close(fig)


# TODO: Introduce bootstrap calibration, Allan-variance diagnostics, and
#       incorporate Hamming inner-code mapping as the project evolves.
