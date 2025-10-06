# Contributing Shortcuts

## Branching & Scope
- [ ] Use `feat/<track>-<short-name>` (e.g., `feat/theory-p1-micromotion`). Source: [README ▸ Contributing](../blob/main/README.md#contributing--reviews).
- [ ] Keep PRs small and focused; attach validation snippet notes.

## Review Roles
| Role | Focus | Notes |
| --- | --- | --- |
| Guardian | Enforces acceptance items & validation snippets | Runs Guardian CLI / CI checks. |
| Architect | Structure & doc cohesion | Confirms interface alignment. |
| Integrator | Merge readiness | Ensures branch hygiene + status links. |

## Rituals
- [ ] Reference [`CONTRIBUTING.md`](../blob/main/CONTRIBUTING.md) for the full workflow.
- [ ] Update glossary entries **only** in [`theory/_glossary.md`](../blob/main/theory/_glossary.md).
- [ ] Link to `STATUS.md` / `REPORTING.md` updates in PR descriptions when relevant.
- [ ] Run Guardian CLI (`python scripts/guardian-cli.py --strict`) before requesting review when applicable.

---
Last synchronized with main on 2025-10-06 (commit 7fb7095). Owner: CODEX.
