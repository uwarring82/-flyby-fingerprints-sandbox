SPDX-License-Identifier: GPL-3.0-or-later

# Technical Noise (RF, DAC, Servo, Johnson)

**What it is.** Classical noise from electronics and control systems: RF drive amplitude/phase noise, DAC update noise, ground loops, digitizer/servo artifacts, and Johnson noise.

## How it heats
- **Direct drive:** Electric-field noise at \(\omega\) couples linearly via \(\dot{\bar n} \propto S_E(\omega)\).
- **Parametric heating:** Modulation of trap frequency at \(2\omega\) (e.g., RF amplitude noise) drives heating even if \(S_E(\omega)\) is small.
- **Aliasing / updates:** DAC update steps and digital toggles inject narrowband components near secular/resonant frequencies.

## Practical diagnostics
- Measure **RF amplitude/phase noise**; check for spurs near \(\Omega_{\rm RF} \pm \omega\) and \(2\omega\).
- **Notch/low-noise filters**, differential routing, star grounds; compare with trap electrodes grounded (ion removed) to bound electronics noise.
- **Blind toggles** of control lines in acquisition to expose analysis-coupled artifacts.

## Mitigations / controls
- Quiet RF chain & shielding; amplitude-noise minimization; phase-matched lines.
- Smoothed DAC updates (slew-rate limiters), synchronous updates far from resonances.
- Temperature-stable references; isolation transformers; battery powering where feasible.

## Primary references
- Leibfried, Blatt, Monroe, Wineland, **Rev. Mod. Phys. 75, 281 (2003)**. DOI: 10.1103/RevModPhys.75.281  
- Brownnutt et al., **RMP 87, 1419 (2015)**. DOI: 10.1103/RevModPhys.87.1419  
- Wineland et al., *Experimental Issues in Coherent Quantum-State Manipulation of Trapped Ions* (NIST TN), 1998.  
- Berkeland et al., **J. Appl. Phys. 83, 5025 (1998)** (micromotion & RF modulation). DOI: 10.1063/1.367318
