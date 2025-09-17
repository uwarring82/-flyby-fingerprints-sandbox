# Contributing

## Branching
- `main` = **certified** state only (protected).
- Work on feature branches: `feat/*`, `fix/*`, `docs/*`.
- PRs into `main` must pass **Guardian Validation** CI.

## Paths
- Simulation fidelity → `simulation_backend/*`
- Validation/Gate → `simulations/validation/*`, `scripts/guardian-cli.py`
- Docs → `docs/*`

## PR Checklist
- [ ] Tests added/updated
- [ ] `scripts/guardian-cli.py --summary-json` runs locally (use `--strict` once
      your checks are ready to gate merges)
- [ ] Affected Guardian checks explained in PR template
- [ ] Relevant docs updated

See `.github/pull_request_template.md`.
