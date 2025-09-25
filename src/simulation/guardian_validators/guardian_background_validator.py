"""Guardian background validation orchestration."""

from typing import Dict

from .signal_to_background_analyzer import passes_threshold
from .null_hypothesis_tests import null_is_consistent
from .background_characterization import background_inventory_complete
from .systematic_effect_analysis import quantify_contributions


def guardian_check_backgrounds(data: Dict) -> Dict:
    """Run the Guardian background validation checks and return a report."""

    report = {"inventory_ok": background_inventory_complete(data)}
    report["null_95_ok"] = null_is_consistent(counts=data["detector_counts"], alpha=0.05)
    report["snr_10_ok"] = passes_threshold(data, threshold=10.0)
    report["contributions"] = quantify_contributions(data)
    report["guardian_pass"] = all(
        [report["inventory_ok"], report["null_95_ok"], report["snr_10_ok"]]
    )
    return report
