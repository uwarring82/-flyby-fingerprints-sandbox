# 🛡️ Flyby Fingerprints: Simulation-First Collision Detection Framework

> **Critical Notice**  
> This project is **simulation-first**. Analysis of real data is **gated** by Guardian certification of the simulation + validation stack. PRs into `main` require the **Guardian Validation** CI check to pass.

![Guardian Validation](https://github.com/uwarring82/-flyby-fingerprints-sandbox/actions/workflows/guardian-validation.yml/badge.svg)

## 🎯 Mission
Detect weak residual-gas collisions in trapped-ion systems via rigorously validated fingerprint analysis—starting with a comprehensive simulation of all known background/systematic effects.

## 🏗️ Three-Phase Architecture

- **Phase 1: Simulation Backend (ACTIVE) ✅**  
  Trapped-ion dynamics (target <0.1% deviation), Tier-1..3 background models, preliminary collision-injection API, Guardian validation framework (ROC, null testing).
- **Phase 2: Algorithm Development (GATED) 🔗**  
  Requires certified Phase-1. A-D-M triad pipeline and Heptad analysis.
- **Phase 3: Real Data Analysis (GATED) 🔗**  
  Requires certified Phase-2. Historical re-analysis, new campaigns, community portal.

> **GATED = dependent on prior certified phase.** Work may proceed on feature branches but **cannot merge to `main`** until certification passes.

## 🚀 Quick Start

### Physicists
```bash
git clone https://github.com/uwarring82/-flyby-fingerprints-sandbox
cd flyby-fingerprints-sandbox
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m simulations.validation.guardian_gates  # if present
```

Algorithm Developers

```
# NOTE: Collision injection API is preliminary and may change pending backend completion.
from simulation_backend import api as sim
data, gt = sim.generate_background_only_with_markers()
# Implement your detector; compare to markers/gt.
```

Experimentalists
•See /docs/systematic_effects.md for the effect catalog and contribution hooks.
•Open an issue with your trap parameters to prioritize validation targets.

📊 Status Dashboard

| Component | Status | Guardian State | Progress | Next Milestone |
| --- | --- | --- | --- | --- |
| Physics Engine | 🟡 | In Review | ~60% | Coulomb interaction precision sweep |
| Background Effects | 🟡 | Pending | ~40% | Tier-2 drift & RF pickup models |
| Collision Injection | 🔴 | Pending | ~10% | Stable API v0 with ground-truth tags |
| Validation FW | 🟡 | In Review | ~30% | ROC harness + null-hypothesis suite |

Legend (Guardian): Pending → In Review → Passed or Action Required

See STATUS.md for details.

🛡️ Guardian Requirements (merge gates)
•Physics deviation target: < 0.1% (tracked tests).
•Tier-1..3 backgrounds modeled with tests & bounds.
•Ground-truth preservation in I/O and APIs.
•ROC AUC > 0.95 at 10:1 SNR (sim suites).
•PRs → CI Guardian Validation must pass.

🤝 Contributing

Start with CONTRIBUTING.md. Choose your path:
•Simulation (physics fidelity, performance)
•Validation (tests, ROC/Null suites, Guardian)
•Documentation (effect catalog, tutorials)

📚 Learn More
•/docs/architecture_overview.md
•/docs/systematic_effects.md
•/docs/guardian_framework.md
•Project docs site (when enabled): see badge/link in STATUS.md

Repository Principle:
Every unvalidated systematic effect is a potential false discovery waiting to happen.
