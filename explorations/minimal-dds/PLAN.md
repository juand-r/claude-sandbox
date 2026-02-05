# Minimal Discrete Dynamical Systems: Plan

## Motivation

Understand patterns that emerge when LLMs interact (with themselves or each other)
by studying the simplest possible formal models. Key insight: an LLM prompt encodes
both a function f and an input x. Feeding output back as input creates a dynamical
system on (f, x) pairs where the function itself can mutate.

## Core Formalization

```
State = (f, x) ∈ F × X
Transition: (f, x) → (φ(f, x), f(x))
```

- F = finite set of functions (f: X → X)
- X = finite set of values
- φ: F × X → F is the "meta-rule" that updates the function
- When φ = identity, this is ordinary iteration of a fixed function
- When φ is nontrivial, the system rewrites its own rules

## Questions

1. What structures arise in the functional graph of (f,x) → (φ(f,x), f(x))?
2. Which meta-rules φ produce long transients / complex orbits?
3. Can we formalize "creativity" as a property of the dynamics?
   - Long transients before cycling
   - High Kolmogorov complexity of orbit sequences
   - Escape from attractors (stochastic case)
   - Function mutation (f changes often vs. stabilizes)
4. How does this connect to symbolic dynamics, tag systems, etc.?
5. Multi-agent extension: coupled maps on product spaces.

## Stages

### Stage 1: Literature Review
- [x] Self-modifying Turing machines, reflective towers
- [x] AIXI and related frameworks
- [x] Post tag systems
- [x] Iterated function systems (IFS)
- [x] Symbolic dynamics: subshifts, sliding block codes
- [x] Kolmogorov complexity and algorithmic randomness
- [x] Computational mechanics (epsilon-machines, Crutchfield)
- [x] LLM self-play, iterative refinement, constitutional AI loops
- [x] Write report (LIT_REVIEW.md)
- [x] Download available papers to papers/

### Stage 2: Implementation & Experiments
- [x] Core engine: (f, x) dynamical system with finite F, X (dds.py)
- [x] Enumerate all meta-rules φ for small F, X (enumerate_meta.py: 65536 for n=2)
- [x] Functional graph construction and visualization (visualize.py)
- [x] Orbit classification: fixed points, cycles, transient lengths
- [x] Complexity measures on orbits (LZ complexity, mutation rate, creativity score)
- [x] Stochastic extension (stochastic.py: noisy meta-rules, temperature-based, escape rates)
- [x] Visualizations (functional graphs, comparison charts, orbit complexity scatter)

### Stage 3 (future): Extensions
- [ ] Multi-agent coupled maps
- [ ] Substitution systems / growing strings
- [ ] Tag system connection
- [ ] Larger state spaces with sampled analysis
