# The Artificial Life Roots of Artificial Intelligence

## Citation
Steels, L. (1993). "The Artificial Life Roots of Artificial Intelligence." *Artificial Life*, 1(1-2), 75-110. MIT Press.

Also relevant:
- Steels, L. & Brooks, R. A. (Eds.). (1995). *The Artificial Life Route to Artificial Intelligence: Building Embodied, Situated Agents.* Lawrence Erlbaum Associates / Routledge.

## Summary

Steels defines "Behavior-oriented AI" as a scientific discipline studying how agent behavior emerges and becomes intelligent and adaptive. The paper reviews the behavior-based approach to AI, identifies its core concepts (emergent functionality, self-organization, evolutionary mechanisms), and maps out unresolved issues. It is both a manifesto for the approach and a sober assessment of its challenges.

## Key Arguments

1. **Behavior-oriented AI defined.** Success is measured by building physical agents capable of maximizing self-preservation in interaction with a dynamically changing environment. This is a survival criterion, not a problem-solving criterion — a fundamental reorientation of what AI is for.

2. **Against top-down AI.** Traditional AI focused on higher-order cognitive activities (expert problem-solving, language, formal reasoning). Steels argues this skipped the hard part: generating adaptive behavior in dynamic physical environments. You cannot build the top without the bottom.

3. **Emergent functionality.** The central concept: complex, intelligent behavior arises from the interaction of simpler subsystems with each other and the environment. No single component contains the plan for the overall behavior — it emerges from the coupled dynamics. This is not a mystical claim but an engineering observation: the behavior of the whole system is not predictable from the behaviors of the parts in isolation.

4. **Behavior systems.** Agents are organized as collections of behavior systems, each coupling sensors to actuators for a specific competence. Behavior systems run in parallel and interact through the environment (not through a central data structure). This is Brooks' subsumption architecture generalized.

5. **Embodiment and situatedness.** Agents must be physically embodied and situated in real environments. Simulation is a tool but not a substitute. The agent's body and environment are constitutive of its intelligence, not just inputs to it.

6. **Evolutionary and self-organizing mechanisms.** Steels explores how evolution (genetic algorithms, evolutionary strategies) and self-organization (spontaneous pattern formation, positive feedback loops) can replace hand-design in producing intelligent behavior. He argues for removing the fitness function from genetic algorithms to better enable open-ended emergence — because we cannot specify what intelligence is, we cannot specify what to optimize for.

7. **Analogical representations (middle ground).** In the Maes (1991) volume, Steels argued that purely reactive agents are limited but classical symbolic representations are too abstract. His solution: "analogical representations" — internal structures that are close to sensor data but still enable anticipation and reasoning. This is a pragmatic middle ground between Brooks' anti-representationalism and GOFAI's symbol manipulation.

## The 1995 Edited Volume (Steels & Brooks)

The edited volume *The Artificial Life Route to Artificial Intelligence* collected papers from a 1991 NATO workshop. Key contributions beyond Steels and Brooks included chapters by Clancey, Varela, Pfeifer, Kaelbling, Langton, and Mataric. The volume defined the research agenda for behavior-based AI in the mid-1990s.

## Connection to Cybernetics

- **Emergent functionality** is the cybernetic principle of emergence formalized for engineering: the system-level behavior is not reducible to component behaviors but arises from their coupling. This is what Ashby called "self-organization" in a precise technical sense.
- **Behavior systems** are cybernetic feedback loops — each one a regulator maintaining some relationship between the agent and its environment.
- **Self-organization without a fitness function** connects to Ashby's design-for-a-brain approach: let the system organize itself through interaction with its environment, rather than optimizing for a pre-specified objective.
- **The survival criterion** is fundamentally cybernetic: the agent's goal is to maintain its own viability (homeostasis), not to achieve externally specified objectives.
- **Embodiment and situatedness** restate the cybernetic insistence that control cannot be understood apart from the system being controlled and the environment in which it operates.

## Relevance to Agent Design

1. **Emergent functionality in multi-agent systems.** When multiple LLM agents interact, their collective behavior is not predictable from individual agent behaviors. Steels' framework provides a theoretical basis for analyzing and designing emergent functionality in agent swarms.

2. **The fitness function problem.** Steels' argument against explicit fitness functions resonates with the difficulty of specifying reward functions for LLM agents. What is the "fitness function" for a general-purpose AI assistant? Steels would say: don't try to specify one; let the agent adapt through interaction.

3. **Analogical representations for agent grounding.** Steels' middle-ground position — representations that are close to the data but support reasoning — describes what modern retrieval-augmented generation (RAG) does: the agent's "representations" are retrieved documents (close to the data) rather than abstract internal models.

4. **The embodiment gap.** Steels' insistence on physical embodiment highlights a fundamental limitation of current LLM agents: they are disembodied. Their "environment" is text. Steels would predict that this limits the kind of intelligence they can develop.

5. **Behavior-oriented evaluation.** Steels' criterion — can the agent survive and function in a dynamic environment? — is more demanding than benchmark performance. It asks whether the agent can adapt when conditions change, recover from errors, and handle novelty. Most current agent evaluations measure something weaker.
