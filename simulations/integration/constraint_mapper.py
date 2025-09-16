from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any

SCHEMA_PATH = Path("data/metadata/physical_constraints.json")


def apply_physical_constraints(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply relations defined in data/metadata/physical_constraints.json
    Schema:
      {"relations":[
         {"out":"pressure","expr":"pressure*(temperature/300.0)","when":"'pressure' in locals() and 'temperature' in locals()"}
      ]}
    """
    constrained = dict(params)
    if not SCHEMA_PATH.exists():
        return constrained
    try:
        spec = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except Exception:
        return constrained

    for rel in spec.get("relations", []):
        out = rel.get("out")
        expr = rel.get("expr")
        cond = rel.get("when", "True")
        if not out or not expr:
            continue
        # Evaluate in a restricted namespace; expose current params via locals()
        ns = dict(constrained)
        try:
            if eval(cond, {"__builtins__": {}}, ns):
                constrained[out] = eval(expr, {"__builtins__": {}}, ns)
        except Exception:
            # Silent no-op on bad rule; document issues via repo docs if needed
            pass
    return constrained
