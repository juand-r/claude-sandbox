# Seth (2015) — The Cybernetic Bayesian Brain

**Paper:** Seth, A.K. (2015). "The Cybernetic Bayesian Brain: From Interoceptive
Inference to Sensorimotor Contingencies." In T. Metzinger & J.M. Windt (Eds).
*Open MIND*: 35(T). Frankfurt am Main: MIND Group.
**URL:** https://open-mind.net/papers/the-cybernetic-bayesian-brain
**PDF:** https://open-mind.net/papers/the-cybernetic-bayesian-brain/at_download/paperPDF

---

## Summary

This paper makes the most explicit case for understanding predictive processing
(PP) and the Free Energy Principle (FEP) as inheriting from **cybernetics** rather
than from Helmholtzian perception-as-inference. Seth argues that the intellectual
origin of PP should be traced to 20th-century cybernetic principles of homeostasis
and predictive control, not to 19th-century Helmholtzian inference.

## Core Thesis

There are two ways to read predictive processing:

1. **Helmholtzian reading:** The brain is primarily an inference machine that
   reconstructs the external world from ambiguous sensory data. Predictions serve
   perception; action is secondary.

2. **Cybernetic reading:** The brain is primarily a control system that maintains
   homeostasis. Predictions serve *regulation*; perception is in service of control.
   Action (including autonomic regulation) is primary, not secondary.

Seth argues for the second reading. This has major consequences for how we understand
consciousness, emotion, and embodied cognition.

## Key Arguments

### 1. Interoceptive Inference

The body's internal states (heartbeat, breathing, gut signals) are predicted by the
brain just as exteroceptive signals are. Emotional experience arises from interoceptive
predictive processing — the brain's best guess about the causes of internal signals.

Predictions about internal states function as **cybernetic setpoints**: they specify
what the body *should* be doing. Prediction errors drive corrective action (autonomic
regulation) to bring the body into line with predictions. This is homeostasis
implemented via predictive coding.

### 2. From Homeostasis to Allostasis

Simple homeostasis maintains fixed setpoints. But biological systems anticipate
future needs and adjust setpoints proactively — this is **allostasis**. Under the
cybernetic reading of PP, the generative model encodes not just current expected
states but anticipated future states, enabling predictive regulation.

### 3. Predictive Control vs. Perception-as-Inference

In the cybernetic reading:
- Perception serves control, not vice versa
- The generative model is a control model, not primarily a world-model
- Prediction errors are signals for corrective action, not just information for
  belief updating
- The fundamental imperative is maintaining viability, not accurate representation

### 4. Sensorimotor Contingencies

Seth connects PP to the sensorimotor contingency theory (O'Regan & Noë): perceptual
experience depends on the agent's mastery of sensorimotor contingencies — the lawful
ways that sensory input changes as a function of action. Under the cybernetic PP
framework, the generative model encodes these contingencies.

## Cybernetic Heritage

Seth explicitly traces the intellectual lineage:

```
Cannon (1932): Homeostasis
    ↓
Ashby (1952): Ultrastability, error correction
    ↓
Conant & Ashby (1970): Good Regulator Theorem
    ↓
Powers (1973): Perceptual Control Theory
    ↓
Seth (2015): Cybernetic Bayesian Brain
    ↓
Friston: Active inference as cybernetic control
```

Key quote from Ashby: "The whole function of the brain is summed up in: error
correction."

Seth shows that this cybernetic framing is not merely historical but provides
different and sometimes better explanations for:
- Emotion (as interoceptive prediction error)
- Consciousness (as integrated prediction of body + world)
- Agency (as prediction-driven control, not stimulus-response)

## How This Differs from Standard FEP

Standard FEP (Friston's presentation) emphasizes the Helmholtzian inference angle.
Seth's contribution is to show that the **same mathematics** supports a different
interpretation:

| Dimension | Helmholtzian FEP | Cybernetic FEP (Seth) |
|-----------|-----------------|----------------------|
| Primary function | World-modeling | Regulation/control |
| Predictions serve | Perception | Action (control) |
| Fundamental imperative | Accurate inference | Maintaining viability |
| Emotional experience | Separate from perception | Interoceptive inference |
| Body | Source of noise | Central to cognition |

Both interpretations use the same free energy mathematics. The difference is which
aspect is treated as primary.

## Relevance to Agent Design

Seth's cybernetic reading suggests agent architectures where:
1. The generative model is primarily a **control model**, not a world-model
2. Internal state monitoring (analogous to interoception) drives behavior
3. Goals are encoded as expected internal states (setpoints/priors)
4. "Emotions" are interoceptive prediction errors signaling regulatory challenges
5. Agency emerges from prediction-driven control, not explicit planning

This aligns naturally with homeostatic agent architectures and with Pihlakas'
homeostatic goals work.

## Connection to PCT

Seth's cybernetic reading is very close to Powers' Perceptual Control Theory:
- Both frame action as controlling perception (maintaining perceptual variables at
  reference values)
- Both see the fundamental operation as error-driven control
- The mathematical difference: PCT uses classical negative feedback; FEP/PP uses
  variational Bayesian inference

Recent work (2025 papers) has begun formalizing this connection, with category-theoretic
arguments that PCT is a formal subset of FEP.

## Status

Freely available as open-access chapter in Open MIND collection.
