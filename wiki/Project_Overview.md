# Project Overview

## Three-Track Architecture
- [ ] **Theory Track** — Priority 1; define physics interfaces and Pillars → [Track brief](Tracks/Theory_Track)
- [ ] **Numerics Track** — Priority 2; consume stable theory interfaces → [Track brief](Tracks/Numerics_Track)
- [ ] **Experiments Track** — Priority 3; background-first validation workflows → [Track brief](Tracks/Experiments_Track)
- Decisions roll via Theory → Numerics → Experiments. Only promote interfaces once Guardian acceptance snippets exist.

## Phase Gating
- **Phase 1** (Simulation Backend) is ACTIVE until Guardian gates pass.  Source: [README ▸ Roadmap & Working Agreements](../blob/main/README.md#roadmap--working-agreements).
- **Phase 2** (Algorithm Development) and **Phase 3** (Real Data Analysis) remain **GATED** pending Phase-1 certification.  The README captures the gating narrative; this wiki references it rather than duplicating details.

## Documentation Map
This wiki orients contributors; manuals and specs live in the repo.
- Reference manuals live under [`docs/`](../tree/main/docs/) (rendered via [`mkdocs.yml`](../blob/main/mkdocs.yml)).
- Status rolls up from [`STATUS.md`](../blob/main/STATUS.md) and reporting rituals from [`REPORTING.md`](../blob/main/REPORTING.md).

### Tracks
| Track | Entry point | Interfaces provided |
| --- | --- | --- |
| Theory | [`theory/`](../tree/main/theory/) | Pillars (P1–P9), glossary, acceptance snippets |
| Numerics | [`numerics/`](../tree/main/numerics/) | Integrators, MC kernels, convergence tests |
| Experiments | [`experiments/`](../tree/main/experiments/) | Calibration templates, acquisition flows |

### Quick Sources
| Thing | Source |
| --- | --- |
| Phases & gates | [README](../blob/main/README.md#roadmap--working-agreements) |
| Tracks & entry points | [README](../blob/main/README.md#tracks) + [Track pages](Tracks/) |
| Status | [`STATUS.md`](../blob/main/STATUS.md) |
| Reporting cadence | [`REPORTING.md`](../blob/main/REPORTING.md) |

---
Last synchronized with main on 2025-10-06 (commit 7fb7095). Owner: CODEX.
