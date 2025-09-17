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
python scripts/guardian-cli.py --all
echo $?
```

Exit code 0 == pass; non-zero blocks PR via CI.
