import json, os, textwrap
from pathlib import Path
from simulations.integration.constraint_mapper import apply_physical_constraints

PC_PATH = Path("data/metadata/physical_constraints.json")


def test_schema_file_exists_and_is_json():
    assert PC_PATH.exists(), "constraints file missing"
    with open(PC_PATH, "r", encoding="utf-8") as f:
        spec = json.load(f)
    assert "relations" in spec and isinstance(spec["relations"], list)


def test_no_c_like_and_in_when_clauses():
    """Guard against accidental '&&' which Python eval cannot parse."""
    txt = PC_PATH.read_text(encoding="utf-8")
    assert "&&" not in txt, "replace '&&' with 'and' in 'when' expressions"


def test_mapper_handles_missing_schema_gracefully(tmp_path, monkeypatch):
    """If file absent, mapper must no-op and return input unchanged."""
    monkeypatch.chdir(tmp_path)
    # ensure file is absent in cwd
    os.makedirs("data/metadata", exist_ok=True)
    # do not create physical_constraints.json here
    params = {"pressure": 1.0, "temperature": 300.0}
    out = apply_physical_constraints(params)
    assert out == params


def test_mapper_applies_example_relation(tmp_path, monkeypatch):
    """Simple P-T scaling rule should update 'pressure' when condition is true."""
    monkeypatch.chdir(tmp_path)
    os.makedirs("data/metadata", exist_ok=True)
    Path("data/metadata/physical_constraints.json").write_text(
        textwrap.dedent("""\
        {
          "relations": [
            {
              "out": "pressure",
              "expr": "pressure * (temperature/300.0)",
              "when": "'pressure' in locals() and 'temperature' in locals()"
            }
          ]
        }
        """),
        encoding="utf-8",
    )
    params = {"pressure": 1.0, "temperature": 600.0}
    out = apply_physical_constraints(params)
    assert out["pressure"] == 2.0
    # other keys preserved
    assert out["temperature"] == 600.0
