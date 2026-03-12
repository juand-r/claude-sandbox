# Information Decomposition Based on Cooperative Game Theory

- **Authors:** Nihat Ay, Daniel Polani, Nathaniel Virgo
- **Journal:** Kybernetika, Vol. 56, No. 5, pp. 979-1014
- **Year:** 2020
- **DOI:** 10.14736/kyb-2020-5-0979
- **URL:** https://www.kybernetika.cz/content/2020/5/979
- **Access:** Open access (diamond OA)

## Abstract

Proposes "Information Attribution" (IA), a novel decomposition of mutual information
using cooperative game theory. Assigns a "fair share" of mutual information to each
combination of source variables. Uses an alternative lattice structure compared to
traditional partial information decomposition (PID), resulting in fewer terms while
still capturing synergy and unique information. Satisfies axioms (local positivity,
identity) that cannot be simultaneously met by conventional PID measures.

## Key Concepts

### Information Attribution (IA)
- Decomposes I(X1,...,Xn ; Y) -- the mutual information between source variables
  and a target -- into contributions from each subset of sources.
- Uses Shapley-value-like decomposition from cooperative game theory.
- Each "player" (source variable) gets a fair share based on their marginal contribution.

### Connection to Cooperative Game Theory
- The mutual information is treated as the "value" of a cooperative game.
- Source variables are the "players."
- Coalition values are defined by the mutual information between subsets of sources
  and the target.
- Shapley value provides the allocation mechanism -- satisfying efficiency, symmetry,
  null player, and additivity axioms.

### Comparison with Partial Information Decomposition (PID)
- PID (Williams & Beer) decomposes into redundancy, unique info, and synergy.
- IA uses a different lattice: fewer terms, more interpretable.
- IA satisfies local positivity (no negative terms) which PID struggles with.

## Mathematical Framework

- Information geometry provides the geometric foundation.
- The framework lives in the space of probability distributions.
- Kullback-Leibler divergence is the core information measure.
- Game-theoretic allocation (Shapley value) provides the decomposition rule.

## Relevance to Cybernetics-Agents Research

This paper is highly relevant to agent design for several reasons:

1. **Sensor fusion / multi-source integration:** Agents receive information from multiple
   sources (sensors, memory, context). Understanding how much each source uniquely
   contributes vs. provides redundant information is critical for efficient processing.

2. **Information-theoretic regulation:** Connects to Ashby's law of requisite variety --
   an agent needs sufficient information channels to regulate a system. IA quantifies
   exactly how much each channel contributes.

3. **Cooperative game theory + information theory bridge:** This is exactly the kind of
   mathematical bridge between game theory and information theory that cybernetics
   promised but rarely delivered in formal terms.

4. **Polani connection:** Daniel Polani is a key figure in information-theoretic approaches
   to agent design (empowerment, relevant information, intrinsic motivation). His
   involvement in this paper connects it directly to the agent design literature.

5. **Fair allocation:** The Shapley value ensures "fair" attribution -- relevant for
   multi-agent systems where credit assignment is a core challenge.

## Key References from Paper

- Williams & Beer (2010) - original PID framework
- Shapley (1953) - Shapley value in cooperative games
- Ay, Polani & Virgo have prior work on information geometry and agent-environment
  interaction
