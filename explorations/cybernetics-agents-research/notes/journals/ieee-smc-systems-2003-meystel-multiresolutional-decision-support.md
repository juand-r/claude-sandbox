# Meystel (2003) — Multiresolutional Hierarchical Decision Support Systems

## Citation
Meystel, A.M. (2003). "Multiresolutional Hierarchical Decision Support Systems." IEEE Transactions on Systems, Man, and Cybernetics—Part C: Applications and Reviews, 33(1), 86-101.

## Source
- IEEE Xplore (via author page): https://ieeexplore.ieee.org/author/37349013300

## Full Text Access
Not accessed. Behind IEEE paywall.

## Key Ideas

### Multiresolutional Representation
Meystel's core idea is that intelligent systems must represent the world at multiple resolutions simultaneously. High-resolution representations capture fine details for immediate action; low-resolution representations capture broad patterns for long-range planning.

This is the spatial/temporal counterpart to Albus's order-of-magnitude scaling: at each hierarchical level, the system operates at a different "grain size" of representation.

### Hierarchical Decision Support
The paper extends the NIST RCS / Albus-Meystel framework specifically to decision support. Decisions at higher levels are made with coarser information but over longer time horizons and wider scopes. Lower-level decisions are made with fine-grained information but narrow scope.

### Nested Hierarchical Controllers
Meystel developed the concept of "nested hierarchical controllers" where each level contains a planning → execution → feedback loop that operates at a characteristic resolution. The nesting means each level's planner generates subgoals for the level below.

### Connection to Cognitive Architecture
Meystel and Albus co-authored "Intelligent Systems: Architecture, Design, and Control" (Wiley, 2002), which presents this multiresolutional approach as a computational theory of intelligence. The claim is that biological intelligence also uses multiresolutional representations — coarse-grained for strategic thinking, fine-grained for motor control.

## Relevance to Agent Design
- **Multiresolutional planning** is directly applicable to LLM agents: high-level plans are expressed in natural language (coarse), decomposed into specific tool calls (fine-grained)
- The idea that each level has its own planning loop with appropriate resolution suggests that a hierarchical agent should not just decompose tasks top-down, but maintain feedback loops at each level
- Decision support systems are an important application of agent technology — this paper provides a principled framework for how agents should structure information across levels of abstraction
- The nested controller concept maps to nested function calls or recursive agent invocations

## Context
Meystel was a close collaborator of Albus at NIST. This paper represents the application of the RCS/hierarchical intelligent control framework specifically to decision-making and planning, extending beyond the original robotics domain.

## Citations
Cited in hydrogeology, manufacturing, and autonomous systems literature.
