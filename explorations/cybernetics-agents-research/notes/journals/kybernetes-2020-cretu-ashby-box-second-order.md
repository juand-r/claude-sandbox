# Cretu (2020) - Learning the Ashby Box: Second Order Cybernetic Modeling

**Citation:** Cretu, A. (2020), "Learning the Ashby Box: an experiment in second order cybernetic modeling", *Kybernetes*, Vol. 49 No. 8, pp. 2073-2090.

**DOI:** 10.1108/K-06-2019-0439

**Access:** Emerald Insight (paywalled). Also available on Academia.edu (partial access confirmed).

## Purpose

Construct an elementary observer/controller for the class of systems exemplified by the Ashby Box -- variable structure black box systems with parallel input.

## The Ashby Box

W. Ross Ashby's "elementary non-trivial machine" -- the prototypical black box system in cybernetic literature. Based on Ashby's journal, the device was intended to exemplify the environment where an "artificial brain" may operate. It has variable internal structure, making it a fundamentally different challenge from trivial machines.

## Method

- Strictly system-theoretic approach, without recourse to disciplinary metaphors or current theories of learning/cognition
- Synthesized from the ground up based on second-order cybernetic assumptions implicit in the Ashby Box design
- Primary theoretical guidance from Heinz von Foerster
- The system's combinatorial complexity reaches ~10^126 states, necessitating stochastic approaches

## Key Findings

- Develops a **"Read, Act, Read, Learn" (RWRL) four-step algorithm** for adaptive controller behavior
- Unlike fixed-memory systems, uses **dynamic probability tables** evolved from past interactions
- The observer/controller defines basic specifications of a general-purpose, unsupervised learning architecture
- Second-order cybernetics provides adequate foundation for mathematical modeling of black box interaction
- Understanding cognitive systems does not require disclosing underlying "black box" mechanisms

## Keywords

Cybernetic modelling, Machine learning, Non-trivial machine, Second-order cybernetics, W. Ross Ashby

## Relevance to Our Project

This is perhaps the most directly relevant paper to agent design from a cybernetic perspective:

1. **The RWRL algorithm** is essentially a cybernetic formulation of what modern AI calls an agent loop: observe, act, observe result, update model. The correspondence to ReAct-style agent architectures is striking.

2. **Black box interaction** is exactly the problem LLM agents face: they interact with tools and environments whose internal mechanisms are opaque. Cretu shows that second-order cybernetics provides a principled framework for this.

3. **Stochastic learning over fixed programs** -- the argument that the combinatorial space is too large for exhaustive search, requiring probabilistic/adaptive approaches, parallels the argument for neural/learned approaches over rule-based systems.

4. **Unsupervised learning architecture from cybernetic first principles** -- this is what we want: deriving agent architecture requirements from cybernetic theory rather than engineering heuristics.
