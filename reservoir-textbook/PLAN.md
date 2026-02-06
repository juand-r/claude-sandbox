# Reservoir Computing Textbook — Project Plan

## Overview

An introductory expository textbook aimed at mathematics undergraduates, covering three deeply connected topics:

1. **Dynamical Systems** — the foundation
2. **Ergodic Theory** — the statistical/measure-theoretic lens on dynamics
3. **Reservoir Computing** — a modern application where these ideas converge

The narrative arc: dynamical systems provide the language and tools, ergodic theory reveals the long-term statistical behavior of those systems, and reservoir computing harnesses dynamical systems as computational substrates — where properties like the echo state property are intimately connected to ergodic-theoretic and stability concepts.

## Audience

Mathematics undergraduates with background in:
- Linear algebra
- Multivariable calculus
- Basic real analysis (limits, continuity, sequences/series)
- Some exposure to ODEs is helpful but not strictly required

## Format

- Markdown files with LaTeX math (rendered via MathJax/KaTeX)
- One file per chapter
- Each chapter: exposition, definitions, theorems with proofs (or proof sketches), examples, exercises, references, recommended reading

## Chapter Outline

### Part I: Dynamical Systems

- **Chapter 1: Introduction to Dynamical Systems**
  - What is a dynamical system? Discrete vs. continuous. Phase space, orbits, trajectories.
  - Motivating examples: population models, planetary motion, weather.

- **Chapter 2: Discrete Dynamical Systems**
  - Maps, iteration, orbits. Fixed points and periodic orbits.
  - Stability of fixed points (linear stability analysis).
  - The logistic map as a running example.
  - Cobweb diagrams.

- **Chapter 3: Continuous Dynamical Systems**
  - ODEs as dynamical systems. Flows and vector fields.
  - Phase portraits in 2D. Nullclines.
  - Existence and uniqueness (Picard-Lindelöf, stated without proof).
  - Linear systems, classification of fixed points.
  - Nonlinear systems: linearization and the Hartman-Grobman theorem.

- **Chapter 4: Poincaré Maps and Recurrence**
  - Sections and first-return maps.
  - Reducing continuous systems to discrete ones.
  - Poincaré recurrence theorem (statement, proof sketch, significance).
  - Examples: periodically forced oscillators, limit cycles.

- **Chapter 5: Bifurcations**
  - Structural stability and bifurcation.
  - Saddle-node, transcritical, pitchfork bifurcations (1D).
  - Hopf bifurcation.
  - Period-doubling and the route to chaos.
  - Bifurcation diagrams (logistic map).

- **Chapter 6: Chaos and Attractors**
  - Sensitive dependence on initial conditions.
  - Lyapunov exponents.
  - Strange attractors: Lorenz, Rössler, Hénon.
  - Topological transitivity, dense periodic orbits (Devaney's definition of chaos).
  - Fractal dimension of attractors (Hausdorff dimension, box-counting).
  - Takens' embedding theorem (preview for Part III).

### Part II: Ergodic Theory

- **Chapter 7: Measure Theory Essentials**
  - Sigma-algebras, measures, measurable functions.
  - Lebesgue measure and integration (review).
  - Probability spaces. L^p spaces (brief).
  - This is a toolbox chapter — minimal but self-contained.

- **Chapter 8: Measure-Preserving Transformations**
  - Definition and examples (rotations, doubling map, baker's map, Arnold's cat map).
  - Invariant measures. Existence (Krylov-Bogolyubov theorem).
  - Natural/physical measures (SRB measures — introduction).

- **Chapter 9: Ergodicity and the Ergodic Theorems**
  - Von Neumann's mean ergodic theorem.
  - Birkhoff's pointwise ergodic theorem (statement, proof sketch, full proof in appendix).
  - Ergodicity: equivalent characterizations.
  - Examples of ergodic systems: irrational rotation, doubling map.
  - Unique ergodicity.
  - Physical interpretation: time averages = space averages.

- **Chapter 10: Mixing and Spectral Theory**
  - Weak mixing and strong mixing.
  - The hierarchy: mixing ⟹ ergodic (but not conversely).
  - Spectral characterization via the Koopman operator.
  - Examples: Bernoulli shifts, hyperbolic toral automorphisms.

- **Chapter 11: Entropy**
  - Shannon entropy (motivation from information theory).
  - Measure-theoretic entropy (Kolmogorov-Sinai entropy).
  - Topological entropy.
  - The variational principle.
  - Computing entropy: shift spaces, Markov chains.
  - Pesin's formula (relating entropy to Lyapunov exponents).

- **Chapter 12: Connections — From Ergodic Theory Back to Dynamics**
  - Ergodic theory of hyperbolic systems.
  - SRB measures revisited.
  - Statistical properties of chaotic systems (decay of correlations, CLT).
  - The ergodic hierarchy in physics.
  - Summary: how ergodic theory provides the "right" framework for understanding chaotic dynamics.

### Part III: Reservoir Computing

- **Chapter 13: From Dynamical Systems to Computation**
  - Computation with dynamics: historical perspective.
  - Neural networks as dynamical systems.
  - Recurrent neural networks and the problem of training them.
  - The key insight: separate the dynamics from the readout.

- **Chapter 14: Echo State Networks**
  - Architecture: input, reservoir, readout.
  - The echo state property (ESP): definition and significance.
  - Sufficient conditions for ESP (spectral radius, input scaling).
  - Training: ridge regression on the readout layer.
  - Concrete example: time series prediction.

- **Chapter 15: Theoretical Foundations of Reservoir Computing**
  - Universal approximation properties of reservoirs.
  - Fading memory and the Stone-Weierstrass theorem.
  - Separation property and approximation property.
  - Connections to Volterra series and functional analysis.
  - The role of the reservoir's dynamical regime (edge of chaos).

- **Chapter 16: Reservoir Computing Meets Ergodic Theory**
  - The reservoir as a measure-preserving (or dissipative) dynamical system.
  - Generalization and ergodic averages.
  - Lyapunov exponents and the echo state property.
  - Information processing capacity and entropy.
  - Takens' embedding theorem and reservoir computing.
  - Physical reservoirs and their dynamics.

- **Chapter 17: Applications, Frontiers, and Open Problems**
  - Time series prediction and generation.
  - Chaotic system modeling (Lorenz, Mackey-Glass).
  - Physical reservoir computing (photonic, mechanical, quantum).
  - Next-generation reservoir computing (NGRC).
  - Deep reservoirs.
  - Open theoretical questions.

## Status

- [x] Chapter 1
- [x] Chapter 2
- [ ] Chapter 3
- [x] Chapter 4
- [ ] Chapter 5
- [x] Chapter 6
- [ ] Chapter 7
- [ ] Chapter 8
- [x] Chapter 9
- [ ] Chapter 10
- [ ] Chapter 11
- [ ] Chapter 12
- [ ] Chapter 13
- [ ] Chapter 14
- [ ] Chapter 15
- [ ] Chapter 16
- [ ] Chapter 17
- [ ] README / Index
