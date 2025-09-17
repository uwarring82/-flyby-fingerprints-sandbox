# Flyby Fingerprints Sandbox

[![CI - Fast (unit)](https://github.com/uwarring82/-flyby-fingerprints-sandbox/actions/workflows/ci-fast.yml/badge.svg)](https://github.com/uwarring82/-flyby-fingerprints-sandbox/actions/workflows/ci-fast.yml)
[![CI - Integration (toy)](https://github.com/uwarring82/-flyby-fingerprints-sandbox/actions/workflows/ci-integration.yml/badge.svg)](https://github.com/uwarring82/-flyby-fingerprints-sandbox/actions/workflows/ci-integration.yml)

---

## Project Aim

This sandbox explores how trapped ions respond to **flyby collisions with residual-gas particles**.  
Our central challenge is to **disentangle true collision fingerprints from background heating mechanisms**.

**Phase-1 priority:**  
We are first of all building a **dedicated simulation backbone** that carefully accounts for relevant background sources (technical noise, trap imperfections, patch potentials). Only once these are quantitatively under control will we search for unique flyby signatures.

---

## Conceptual Motivation

Flyby events and their heating signatures carry a remarkable degree of **self-similarity**:

* **Scaling of Interaction Potentials** — The Coulomb force ∝ 1/r makes deflections look similar across scales; small-impact strong events and large-impact weak events form a continuum.
* **Self-similar distributions** — Many flybys accumulate into power-law tails (Lévy-like), so zooming in reveals the same shape.
* **Scale-invariant heating dynamics** — Normalized groups (impact parameter / Debye length, collision time / trap period) repeat physics independent of absolute trap scale.
* **Experimental observables** — Heating rates vs. pressure often follow power laws, signaling scale-invariant processes.

**Critical nuance:** Real traps break strict self-similarity (finite size, RF drive, screening). What survives experimentally are **approximate scaling laws** whose deviations encode valuable, trap-specific physics.

---

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e . -r requirements.txt

# run toy dataset (fast check)
python -m flyby.triad --data-root data/toy --out out

Outputs:
    •   out/triad_summary.csv
    •   out/triad_report.json
```

⸻

Next steps
1.  Simulation backbone: rigorous modeling of background mechanisms.
2.  Scaling analysis: check if normalized impact-parameter / energy-transfer distributions collapse onto universal curves.
3.  Fingerprint search: identify deviations from scale-invariance as possible flyby collision signatures.
