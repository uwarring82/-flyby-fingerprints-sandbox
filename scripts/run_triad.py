from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from flyby.triad import TriadThresholds, run_triad


def main() -> None:
    """Command-line entry point for toy A–D–M triad analysis."""
    parser = argparse.ArgumentParser(description="Run Fast Triad A–D–M screening")
    parser.add_argument("--data-root", type=Path, default=Path("data/toy"))
    parser.add_argument("--out", type=Path, default=Path("out"))
    parser.add_argument("--strict", action="store_true", help="Use stricter thresholds")
    args = parser.parse_args()

    thresholds = TriadThresholds()
    if args.strict:
        thresholds = TriadThresholds(
            A_slope_warn=0.08, A_slope_fail=0.15,
            D_fano_warn=0.9,  D_fano_fail=1.1,
            M_ac_warn=0.18,   M_ac_fail=0.30,
        )

    result: dict[str, Any] = run_triad(str(args.data_root), str(args.out), thresholds)
    print(result)


if __name__ == "__main__":
    main()
