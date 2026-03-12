# Schilling, Hoinville, Schmitz & Cruse (2013) — Walknet, a Bio-Inspired Controller for Hexapod Walking

## Bibliographic Details
- **Authors:** Malte Schilling, Thierry Hoinville, Josef Schmitz, Holk Cruse
- **Title:** Walknet, a bio-inspired controller for hexapod walking
- **Journal:** Biological Cybernetics, Vol. 107(4), pp. 397-419
- **Year:** 2013
- **DOI:** 10.1007/s00422-013-0563-5
- **Key precursor:** Cruse et al. (1998), "Walknet–a biologically inspired network to control
  six-legged walking," Neural Networks 11, 1435-1447
- **Note:** Cruse published 30 papers in Biol. Cybernetics; the Walknet program spans decades

## Summary

Walknet is a decentralized neural network controller for hexapod (insect-like) walking, built
on decades of biological experiments with stick insects (primarily by Holk Cruse's group at
Bielefeld University). Each leg is controlled by its own local controller ("ganglion"), and
inter-leg coordination emerges from simple local rules acting between neighbors — no central
coordinator required.

## Key Concepts

### Decentralized Architecture
- Each leg has an independent controller (hemiganglia, as in real stick insects)
- No central pattern generator dictates the gait
- Inter-leg coordination arises from **local coordination rules** between neighboring legs
- "Gaits" (tripod, tetrapod, wave) are not explicitly programmed but emerge as continuous
  phenomena from the coordination rules

### Coordination Rules (Cruse's Rules)
Historically, Cruse identified a small set of local coordination rules from biological experiments:
1. A leg starting its swing inhibits its posterior neighbor from starting swing
2. A leg ending its stance influences the start of swing in its anterior neighbor
3. Position information is exchanged between adjacent legs
These simple rules suffice to produce the full repertoire of insect walking patterns.

### Sensorimotor Loop Through Environment
- The controller uses **internal recurrent connections** but critically also relies on
  **the loop through the environment** as a recurrent pathway
- Ground contact provides essential feedback that modulates the control
- The environment is not an obstacle to overcome but an integral part of the control architecture

### Emergent Capabilities
Without explicit programming, Walknet produces:
- Full continuum of walking gaits (not discrete gait patterns)
- Coordination of 18+ leg joints during stance
- Forward and backward walking
- Walking over uneven terrain and negotiating curves
- Graceful degradation after leg loss (leg amputation)
- Adaptation to perturbations

### Cybernetic Significance
- **Decentralization** — no central command; order emerges from local interactions
  (cf. Ashby's Design for a Brain — adaptation through local homeostats)
- **Requisite variety at the local level** — each leg controller has the variety needed
  to handle its local situation; coordination emerges without needing global variety
- **Environment as controller** — the physical environment provides constraints and feedback
  that are essential parts of the control system
- **Graceful degradation** — losing a leg doesn't crash the system; the remaining legs
  re-coordinate automatically (robustness through decentralization)

## Relevance to Our Research

1. **Decentralized agent architectures** — Walknet is a working proof that complex coordinated
   behavior can emerge from simple local rules without central planning. Directly applicable
   to multi-agent systems and modular agent designs.
2. **Coordination without communication overhead** — legs coordinate through minimal local
   signals, not by sharing full state. Agents could coordinate similarly.
3. **Environment as coordination medium** — the physical world serves as a shared medium
   for indirect coordination (cf. stigmergy in insect colonies)
4. **Graceful degradation** — a key desideratum for robust agent systems; Walknet shows
   how decentralization achieves this naturally
5. **Biological grounding** — every aspect of the model is tied to real experimental data
   from stick insects, giving it strong empirical validity

## Extended Work: reaCog
Cruse extended Walknet into **reaCog**, which adds:
- Navigation capabilities (Navinet)
- Decision-making for non-trivial situations
- A cognitive expansion on the reactive Walknet base
- Demonstrates how higher cognition can emerge from a reactive, embodied foundation

## Impact
- Cruse is one of the most prolific Biol. Cybernetics authors (30 papers)
- Walknet has been influential in bio-inspired robotics
- Open source implementations available:
  - Simulation: https://github.com/malteschilling/hector
  - Controller: https://github.com/hcruse/neuro_walknet

## Access
- Full text behind Springer paywall
- ResearchGate preprint may be available
