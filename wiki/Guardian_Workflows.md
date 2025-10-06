# Guardian Workflows

## Merge Gates & Thresholds
| Gate | Threshold | Source |
| --- | --- | --- |
| Physics deviation | `< 0.1%` vs. analytics | [`scripts/guardian-cli.py`](../blob/main/scripts/guardian-cli.py) |
| Background coverage | Tier-1..3 modeled + validated before collisions | [Background Effects Catalog](Background_Effects_Catalog) |
| Ground-truth integrity | Metadata preserved end-to-end | [`STATUS.md`](../blob/main/STATUS.md#guardian-gates-phase-1-exit) |
| Detection performance | ROC AUC `> 0.95` @ 10:1 SNR | [`STATUS.md`](../blob/main/STATUS.md#guardian-gates-phase-1-exit) |
| Signal quality | Claimed signatures satisfy `SNR ≥ 10` | [`REPORTING.md`](../blob/main/REPORTING.md#statistical-thresholds-phase-1) |

All checks roll up via the Guardian CLI and CI workflows. Pending checks must pass `--strict` before merges into `main`.

## Local Run
```bash
# from repo root
python scripts/guardian-cli.py --all --summary-json --strict
```
- Emits JSON summary plus exit code suitable for local gating.
- Pair with targeted tests: `pytest -q tests/guardian` when available.

## Continuous Integration
- Guardian validation runs via workflows under [`.github/workflows/`](../tree/main/.github/workflows/).
- PRs into `main` must show the **Guardian Validation** check as passing before review sign-off.
- Additional smoke checks (e.g., Binder imports) may surface as optional jobs.

---
Last synchronized with main on 2025-10-06 (commit fe72749). Owner: CODEX.
