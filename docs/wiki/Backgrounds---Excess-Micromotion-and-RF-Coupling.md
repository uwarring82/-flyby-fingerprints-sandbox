SPDX-License-Identifier: GPL-3.0-or-later

# Excess Micromotion & RF Coupling

**What it is.** Displacement from the RF null or phase imbalances create micromotion at \(\Omega_{\rm RF}\) that couples to noise and laser interactions.

## Key relations
- Displacement \(x_{\rm dc}\) ⇒ micromotion amplitude \(x_\mu \propto q\, x_{\rm dc}\).  
- RF amplitude modulation \( \Delta V_0 / V_0 \) induces frequency modulation \( \Delta \omega / \omega \approx \Delta V_0 / V_0 \) and can parametrically heat motion near \(2\omega\).

## Diagnostics we will run
- **Berkeland cross-correlation** and **sideband spectroscopy** of micromotion.
- **Drive-amplitude scans** to identify parametric sensitivity.
- **3D compensation** (dc electrodes) with iterative nulling while monitoring sidebands.

## Mitigations / controls
- Routine 3-axis micromotion compensation; phase balancing of RF feeds; symmetric cabling.
- Stabilize RF amplitude; monitor and log \(\Omega_{\rm RF}\) and amplitude over time.

## Primary references
- Berkeland et al., **J. Appl. Phys. 83, 5025 (1998)**. DOI: 10.1063/1.367318  
- Leibfried et al., **RMP 75, 281 (2003)**. DOI: 10.1103/RevModPhys.75.281
