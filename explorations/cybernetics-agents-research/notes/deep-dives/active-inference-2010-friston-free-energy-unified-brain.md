# Friston (2010) — The Free-Energy Principle: A Unified Brain Theory?

**Paper:** Friston, K. (2010). "The free-energy principle: a unified brain theory?"
*Nature Reviews Neuroscience*, 11, 127-138.
**URL:** https://www.nature.com/articles/nrn2787

---

## Summary

This is the landmark review that established the Free Energy Principle (FEP) as a
candidate unifying framework for neuroscience. Friston argues that all brain function
can be understood as minimizing variational free energy — an information-theoretic
quantity that bounds surprise.

## Core Argument

The brain is fundamentally an inference machine. It maintains a generative model of
the world and uses it to predict sensory inputs. When predictions fail, prediction
errors drive updates to the model (perception) or actions that change the input to
match predictions (action). Both serve the same objective: minimizing variational
free energy.

## Mathematical Core

Variational free energy:
```
F = E_q[ln q(s) - ln p(o, s)]
```

This decomposes two ways:

1. **Energy minus entropy:** F = E_q[-ln p(o,s)] - H[q(s)]
2. **Surprise plus KL divergence:** F = -ln p(o) + D_KL[q(s) || p(s|o)]

Since D_KL >= 0, F is always an upper bound on surprise. Minimizing F w.r.t. q(s)
performs approximate Bayesian inference (makes beliefs approximate the true posterior).
Minimizing F w.r.t. action makes observations conform to predictions.

## Cybernetic Connections

### Homeostasis
FEP formalizes homeostasis: if a system persists, it occupies a limited set of
characteristic states (low entropy over state space = low average surprise). The
system must therefore minimize surprise on average — which it does by minimizing
free energy.

- **Essential variables** (Ashby) = **characteristic states** (Friston)
- **Homeostasis** = **minimizing surprise** = staying in expected states
- **Ultrastability** = **active inference** = acting to maintain expected states

### Good Regulator Theorem
Minimizing surprise = maximizing model evidence p(o). An agent that maximizes model
evidence literally *becomes a model of its environment*. This is exactly the claim
of Conant & Ashby (1970): "Every good regulator of a system must be a model of that
system."

### Requisite Variety
Ashby's Law maps to the expressiveness of the generative model — it must be rich
enough to account for environmental structure. Too simple a model = persistently
high free energy = dissolution.

## Connection to Predictive Coding

FEP provides the objective function; predictive coding is the process theory.
Hierarchical predictive coding implements free energy minimization in neural
circuits:
- Forward connections carry prediction errors
- Backward connections carry predictions
- Lateral connections encode precision (attention)

## What This Paper Adds Beyond Earlier Formulations

The 2010 paper is primarily a review and synthesis. The key mathematical work was
done in earlier papers (Friston 2005, Friston & Stephan 2007). This paper's
contribution is:

1. Presenting FEP as a **unifying principle** for neuroscience (not just a model)
2. Making the cybernetic connections explicit
3. Distinguishing the principle from process theories derived from it
4. Positioning active inference as the action-side of free energy minimization

## Significance for Agent Design

The paper establishes the theoretical foundation: agents that persist must minimize
free energy, which means they must:
1. Maintain generative models of their environment
2. Update beliefs to match evidence (perception)
3. Act to make evidence match beliefs (action)
4. Balance model complexity with accuracy

## Critiques (See Also: Critiques File)

- The principle itself is unfalsifiable (acknowledged by Friston)
- Applies to everything with a Markov blanket, including rocks
- Practical algorithms can often be derived without invoking FEP

## Status

Accessible via Nature Reviews Neuroscience (paywalled, but widely available).
