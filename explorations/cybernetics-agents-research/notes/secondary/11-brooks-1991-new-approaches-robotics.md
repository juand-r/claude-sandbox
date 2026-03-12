# New Approaches to Robotics

## Citation
Brooks, R. A. (1991). "New Approaches to Robotics." *Science*, 253(5025), 1227-1232.

## Summary

A companion piece to "Intelligence without Representation," published in *Science* for a broader audience. Summarizes the behavior-based approach to robotics: tight coupling of sensing to action produces architectures that are "quite broad, but not very deep" — networks of simple computational elements rather than deep reasoning pipelines.

## Key Arguments

1. **Reactive vs. deliberative agents.** Traditional AI robotics (SHAKEY, etc.) used a sense-model-plan-act cycle with explicit world models and symbolic planning. Brooks' robots eliminated the model and plan stages, going directly from sensing to action via behavior layers. This made them fast, robust, and able to operate in dynamic environments.

2. **Subsumption in practice.** Describes Genghis, a six-legged robot that walks over rough terrain. Walking is not centrally planned; instead, layers of behaviors handle: (a) standing up, (b) walking without feedback, (c) terrain adaptation. Each layer is simple; coordinated walking emerges from their interaction.

3. **Hybrid approaches acknowledged.** Brooks concedes that purely reactive systems have limits. The paper describes a hybrid: a traditional planner generates high-level assembly plans, but a behavior-based system executes them, providing robust low-level primitives. This is a pragmatic concession — use planning where it helps, but give it robust, situated primitives to work with.

4. **No central representations, but representations can emerge.** The paper shows that "recent work within this approach demonstrated the use of representations, expectations, plans, goals, and learning, but without resorting to the traditional uses of central, abstractly manipulable or symbolic representations." Representations exist, but they are local, action-oriented, and tied to specific behaviors.

## Connection to Agent Design

- **The hybrid architecture described here** — planner + behavior-based executor — is structurally identical to modern LLM agent architectures where the LLM plans and tool-use systems execute. Brooks' insight was that the executor needs to be robust and situated, not just a dumb command follower. Modern tool-use systems that can handle errors, retry, and adapt are implementing this principle.

- **Broad but not deep.** This characterization applies well to current LLM agents: they have broad capability (many tools, much knowledge) but shallow grounding (no persistent embodiment, no continuous environmental coupling). Brooks would argue for deepening the grounding.

## Relation to Note 10

This paper is the accessible, condensed version of the "Intelligence without Representation" arguments. Both appeared in 1991. The *Science* paper is less philosophical and more focused on concrete robotic demonstrations. Together they constitute the definitive statement of the behavior-based robotics paradigm.
