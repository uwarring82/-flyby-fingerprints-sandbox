from simulations.validation import guardian_gates


def test_h_risk_flag_checker_runs(tmp_path):
    # Create a temporary datasets.yaml with a risk:H entry missing the flag
    yaml_file = tmp_path / "datasets.yaml"
    yaml_file.write_text("- risk: H\n")
    original_meta = guardian_gates.DATA_META
    guardian_gates.DATA_META = yaml_file
    try:
        res = guardian_gates.check_datasets_yaml_h_flags()
    finally:
        guardian_gates.DATA_META = original_meta
    assert not res.ok
