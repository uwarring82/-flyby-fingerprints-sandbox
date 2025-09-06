# SPDX-License-Identifier: GPL-3.0-or-later
# (c) 2025 Ulrich Warring and contributors

from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from flyby.triad import FastTriadAnalyzer


def main() -> None:
    """Command-line entry point for Fast Triad analysis."""
    parser = argparse.ArgumentParser(
        description="Run Fast Triad A–D–M screening"
    )
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--out", type=Path, default=Path("out"))
    args = parser.parse_args()

    analyzer = FastTriadAnalyzer()
    analyzer.load_data(args.data_root)
    analyzer.evaluate_data()
    analyzer.generate_output(args.out)


if __name__ == "__main__":
    main()
