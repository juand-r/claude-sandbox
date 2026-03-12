# Distributed Dual Averaging Algorithm for Multi-Agent Optimization with Coupled Constraints

**Authors:** Zhipeng Tu, Shu Liang
**Journal:** Kybernetika, Vol. 60, No. 4, pp. 427-445, 2024
**DOI:** 10.14736/kyb-2024-4-0427
**URL:** https://www.kybernetika.cz/content/2024/4/427
**PDF:** https://www.kybernetika.cz/content/2024/4/427/paper.pdf
**Keywords:** distributed optimization, variational inequality, coupled constraints, dual averaging, multi-agent networks

## Summary

Tackles multi-agent constrained optimization: minimizing a global objective formed by summing
local convex (possibly nonsmooth) functions under coupled inequality and affine equality
constraints.

## Approach

1. Introduce auxiliary variables to decouple constraints
2. Reformulate as a variational inequality problem with set-valued monotone mapping
3. Propose distributed dual averaging algorithm
4. Achieve O(1/sqrt(k)) convergence rate

## Key Result

Proves that weak solutions are equivalent to strong solutions matching optimal primal-dual
outcomes. This is theoretically significant -- it means the distributed algorithm finds
genuinely optimal solutions, not just approximate ones.

## Relevance to Cybernetics-Agents Research

- **Distributed systems:** No central coordinator; agents cooperate through local communication
- **Multi-agent decision making:** Each agent has local objectives but global constraints
  couple them -- a realistic model of many multi-agent settings
- **Coupled constraints = shared regulation:** In cybernetic terms, the coupled constraints
  represent shared environmental or resource constraints that agents must collectively satisfy
- **Convergence guarantees:** The O(1/sqrt(k)) rate gives practical bounds on how long
  regulation takes to achieve equilibrium
- **Variational inequality reformulation:** Modern mathematical formalism that generalizes
  optimization, equilibrium, and complementarity problems

## Access Status

Full text accessible (open access).
