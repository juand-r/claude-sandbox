# Ueltzhöffer (2018) - Deep Active Inference

**Journal:** Biological Cybernetics, 112, 547-573
**Authors:** Kai Ueltzhöffer
**DOI:** 10.1007/s00422-018-0785-7
**Year:** 2018
**Access:** Springer paywall. arXiv preprint available at arxiv.org/abs/1709.02341

## Summary

Combines the free energy principle and active inference with deep generative models
and evolution strategies to create the "deep active inference" agent. This is the
first paper to scale active inference to deep neural network implementations.

## Key Arguments

- **Homeostatic motivation:** The agent minimizes a variational free energy bound on
  average surprise, motivated by homeostasis -- organisms must keep sensory states
  within viable bounds.
- **Deep generative model:** Uses deep and recurrent neural networks to parameterize
  the generative model, making active inference scalable and flexible.
- **Three optimization targets:**
  1. Parameters of the generative latent variable model
  2. Variational density approximating posterior over latent variables
  3. Actions on the environment to sample likely inputs
- **Goal-directed behavior via priors:** Goals are encoded as prior preferences over
  latent states. No separate reward/cost function needed.

## Methods

- Mountain car problem as demonstration environment
- Deep and recurrent neural networks for internal dynamics
- Evolution strategies for optimization
- Variational inference for posterior approximation

## Key Results

- Agent learns a generative model of the environment
- Goal-directed behavior emerges from appropriate priors on latent states
- The learned generative model can be sampled to visualize the agent's beliefs
- Demonstrates that active inference can scale beyond toy problems

## Relevance to Our Research

This is the bridge between theoretical active inference and practical AI implementation.
Shows how the cybernetic principles (homeostasis, free energy minimization) can be
implemented in modern deep learning architectures. Directly relevant to building
agents grounded in cybernetic principles.

- Scalability of active inference to real problems
- Homeostatic argument as foundation for agent behavior
- Prior preferences replacing reward functions
- Generative models as world models

## Impact

Highly cited. Spawned follow-up work:
- Fountas et al. (2020) - Deep active inference with Monte-Carlo methods
- Various extensions to more complex environments

## Tags
`active-inference` `deep-learning` `generative-models` `homeostasis` `scalability`
