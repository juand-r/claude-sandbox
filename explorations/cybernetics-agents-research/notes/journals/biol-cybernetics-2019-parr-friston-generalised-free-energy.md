# Parr & Friston (2019) - Generalised free energy and active inference

**Journal:** Biological Cybernetics, 113(5), 495-513
**Authors:** Thomas Parr, Karl J. Friston
**DOI:** 10.1007/s00422-019-00805-w
**Year:** 2019
**Access:** Open-access PDF available via UCL Discovery. Downloaded as PDF but could not parse text.

## Summary

Compares two variational free energy functionals for active inference in Markov decision
processes. Offers a simpler, more general formulation of expected free energy that
clarifies the relationship between perception and action in active inference.

## Key Arguments

- **Two free energy functionals compared:**
  1. A functional of beliefs about states and policies, but a *function* of observations
  2. A functional of beliefs about states, policies, *and* observations (fully Bayesian)
- **Common objective function:** Variational free energy serves as the objective for
  both perception (optimizing beliefs) and action (changing sensory data to fit the model).
- **Brain as generative model:** The brain maintains an internal generative model to
  predict incoming sensory data. Fit can be improved by:
  - Perceptual inference (updating beliefs)
  - Action (changing the world to match predictions)
- **Planning as inference:** The second functional treats planning as inference over
  policies, providing a cleaner formulation.
- **Does not substantially change message passing:** The new formulation provides
  conceptual clarity but the actual belief updating remains similar.

## Relevance to Our Research

This is the most mathematically mature formulation of active inference for discrete
decision-making (MDPs). Important for understanding:
- How to formally implement active inference in agent architectures
- The relationship between perception, action, and planning under one objective
- Why expected free energy naturally balances information-seeking and goal-pursuit

The "generalised" free energy functional that treats observations as random variables
(not fixed) is the more principled approach and maps better onto agent architectures
that must handle uncertainty about future observations.

## Tags
`active-inference` `free-energy-principle` `variational-inference` `markov-decision-process` `planning`
