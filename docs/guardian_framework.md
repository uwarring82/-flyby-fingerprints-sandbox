# Guardian Framework

## Purpose
Automated, impartial gate that blocks merges if validation is insufficient.

## Checks (examples)
- Physics deviation tests
- Background coverage tests
- Ground-truth conservation tests
- ROC / Null-hypothesis harness

## Usage
```bash
python scripts/guardian-cli.py --summary-json
python scripts/guardian-cli.py --strict  # treat pending checks as failures
echo $?
```

Exit code 0 == pass; non-zero blocks PR via CI. Without `--strict`, pending
checks surface as warnings so contributors can iterate locally before enabling
the hard gate.
