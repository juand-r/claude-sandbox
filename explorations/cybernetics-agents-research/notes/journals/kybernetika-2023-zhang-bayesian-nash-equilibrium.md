# Bayesian Nash Equilibrium Seeking for Multi-Agent Incomplete-Information Aggregative Games

**Authors:** Hanzheng Zhang, Huashu Qin, Guanpu Chen
**Journal:** Kybernetika, Vol. 59, No. 4, pp. 575-591, 2023
**DOI:** 10.14736/kyb-2023-4-0575
**URL:** https://www.kybernetika.cz/content/2023/4/575
**PDF:** https://www.kybernetika.cz/content/2023/4/575/paper.pdf
**Keywords:** aggregative games, Bayesian games, equilibrium approximation, distributed algorithms

## Summary

Addresses distributed Bayesian Nash equilibrium (BNE) seeking in incomplete-information
aggregative games -- a generalization of both Bayesian games and deterministic aggregative games.

## Core Problem

In multi-agent settings with incomplete information, agents must make decisions based on
private type information while interacting through an aggregation function. Feasible strategies
are infinite-dimensional functions in non-compact sets, and the continuity of types creates
barriers to finding equilibria.

## Approach

1. Handle aggregation function to adapt to incomplete-information situations
2. Discretize continuous types to make the problem tractable
3. Prove that the equilibrium of the discretized model constitutes an epsilon-BNE
4. Propose a distributed algorithm for epsilon-BNE seeking
5. Prove convergence of the distributed algorithm

## Relevance to Cybernetics-Agents Research

This is directly at the intersection of:
- **Multi-agent decision making** under uncertainty
- **Bayesian approaches** to strategic interaction
- **Distributed algorithms** -- no central coordinator needed
- **Game-theoretic regulation** -- agents reach equilibrium through local interactions

The paper shows how cybernetic principles (distributed feedback, local information processing)
can be applied to Bayesian game settings. The discretization approach is a practical method
for handling the infinite-dimensional nature of Bayesian strategy spaces.

## Key References Cited

- Xu, Chen, Qi, Hong (2023) - Efficient algorithm for approximating Nash equilibrium of distributed aggregative games, IEEE Trans. Cybernet.
- Guo, Xu, Zhang (2021) - Existence and approximation of continuous BNE, SIAM J. Optim.

## Access Status

Full text accessible (open access, diamond OA journal).
