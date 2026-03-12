# Friston & Stephan (2007) — Free-Energy and the Brain

**Paper:** Friston, K.J. & Stephan, K.E. (2007). "Free-energy and the brain."
*Synthese*, 159, 417-458.
**URL:** https://link.springer.com/article/10.1007/s11229-007-9237-y
**Full text (PMC):** https://pmc.ncbi.nlm.nih.gov/articles/PMC2660582/

---

## Summary

This is the foundational paper where Friston and Stephan lay out the full mathematical
apparatus of the Free Energy Principle as applied to the brain. It is more technically
detailed than the 2010 Nature Reviews paper and provides the actual mathematical
formulation.

## Mathematical Framework

### Core Equation

```
F(ỹ,λ|α) = -⟨ln p(ỹ,ϑ|α)⟩_q + ⟨ln q(ϑ;λ)⟩_q ≥ -ln∫p(ỹ,ϑ|α)dϑ
```

Free energy = expected energy minus entropy, always an upper bound on surprise
(negative log evidence). Jensen's inequality guarantees the bound.

### Mean-Field Factorization Across Timescales

The ensemble density factorizes:

```
q(ϑ) = q(ϑ_u; λ_u) q(ϑ_γ; λ_γ) q(ϑ_θ; λ_θ)
```

- **Fast modes (λ_u):** Millisecond-scale neuronal activity — rapid state estimation
- **Intermediate modes (λ_γ):** Second-scale contextual parameters — precision/attention
- **Slow modes (λ_θ):** Synaptic connection strengths — learning

This maps naturally onto: perception, attention, and learning as three timescales
of the same optimization process.

### Generalised Coordinates

States are extended to include temporal derivatives:

```
ϑ_u = {u, u', u'', ...}
```

This allows the brain to represent not just current states but entire trajectories.
The gradient descent dynamics ensure that at equilibrium, the mode's motion matches
the mode of motion: μ̇_u = μ_u'.

### Prediction Error Dynamics

Recognition dynamics depend on hierarchical prediction errors:

```
μ̇_u^(i) = h(ε̃^(i), ε̃^(i+1))
```

Both bottom-up prediction errors (likelihood) and top-down prediction errors (prior)
drive inference. This predicts specific neural architecture:
- Forward connections: obligatory, carry prediction error
- Backward connections: modulatory, carry predictions
- Intrinsic connectivity: lateral gain control (precision/attention)

### Perception and Action Unified

**Perception** (optimizing λ): Internal parameters adjust so q(ϑ;λ) approximates
the true posterior. When minimized, KL divergence vanishes.

**Action** (optimizing α): Motor outputs resample the environment to maximize
likelihood under the current model. Creates circular causation — systems fulfill
their own expectations.

## Helmholtzian Roots

The paper explicitly frames itself as modernizing Helmholtz's "unconscious inference."
Perception = recovering environmental causes from ambiguous sensory data through
probabilistic inference. The key advance: Friston provides the variational calculus
to make this rigorous.

## Hierarchical Generative Models and Empirical Bayes

The brain implements hierarchical models where:
- Level i receives outputs from level i-1 as inputs
- Dynamic states x^(i) evolve within each level
- Causal states v^(i) link hierarchical levels
- Random fluctuations at each level are independent

This is empirical Bayes: higher levels provide context-dependent priors to lower
levels. No need for external priors — they emerge from the hierarchy itself.

## Cybernetic Connections

The paper is less explicit about cybernetics than the 2010 review, but the
connections are clear:

1. **Action as control:** Action resamples the environment to maintain expected
   states — this is negative feedback control.
2. **Self-fulfilling prophecy:** The circularity of action-perception is the
   same circularity as cybernetic feedback loops.
3. **Selectionist argument:** Systems that fail to minimize free energy face
   "elimination through phase-transitions (death)" — Ashby's ultrastability.

## Key Insight: The Brain's Structure Encodes Physical Laws

Through selective exposure and synaptic modification, the brain's structure
"transcribes physical laws governing [the] environment." This is the Good Regulator
Theorem in action: the brain becomes a model of its environment through learning.

## Significance for This Project

This paper provides the **formal apparatus** that later work (2010 review, active
inference textbooks) builds on. Understanding the math here is prerequisite for
understanding how active inference relates to control theory and cybernetics
at a technical level.

## Status

Full text freely available on PMC.
