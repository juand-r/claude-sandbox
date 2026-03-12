# Intelligence without Representation

## Citation
Brooks, R. A. (1991). "Intelligence without Representation." *Artificial Intelligence*, 47(1-3), 139-159.

## Summary

A manifesto for behavior-based robotics. Brooks argued that AI had foundered on the question of representation, and that intelligence — at least at the level demonstrated by insects and simple animals — can be generated without internal symbolic models. He proposed the **subsumption architecture**: decomposing an intelligent system not into functional modules (perception, planning, execution) but into parallel, independent **behavior layers**, each coupling sensors directly to actuators. Higher layers can subsume (suppress/inhibit) lower ones, but there is no central executive.

## Key Arguments

1. **The world is its own best model.** Rather than constructing internal representations of the environment and reasoning over them, agents should use perception to access the world directly. Internal models are expensive to build, hard to keep accurate, and often unnecessary.

2. **Decomposition by behavior, not function.** Traditional AI decomposes systems horizontally: perception → modeling → planning → execution. Brooks decomposes vertically: each layer is a complete perception-to-action loop implementing a specific competence (e.g., "avoid obstacles," "explore," "follow walls"). Layers operate concurrently and asynchronously.

3. **Incremental, evolutionary design.** Intelligence should be built bottom-up, starting with basic survival behaviors and adding complexity. This mirrors biological evolution: locomotion and obstacle avoidance evolved over hundreds of millions of years; language and abstract reasoning are recent additions. AI research erred by starting at the top.

4. **Intelligence as emergent property.** Complex behavior arises from interaction of simple behaviors with each other and the environment. No single component "has" the intelligence — it emerges from the coupled system.

5. **The symbol grounding problem.** Traditional representations are "theoretically suspect" because they lack grounding in physical reality. Brooks' agents sidestep this by never constructing ungrounded symbols.

6. **Critique of "disembodied" AI.** Expert systems, theorem provers, and blocks-world planners operate in sanitized, pre-digested environments. Brooks argued this was not intelligence but an elaborate trick enabled by human engineers doing most of the hard work.

## The Subsumption Architecture (Technical Details)

- Each layer is a network of **augmented finite state machines (AFSMs)** running asynchronously.
- Layers communicate via simple signals; there is no shared blackboard or central data structure.
- Higher layers can **suppress** inputs to lower layers or **inhibit** their outputs.
- No layer has a complete model of the world; each has only the sensory access it needs (the **007 principle**, as Clark later termed it).
- Successfully demonstrated on mobile robots (Allen, Herbert, Genghis) operating in real office environments.

## Connection to Cybernetics

Brooks is not usually classified as a cyberneticist, but the connections are deep:

- **Feedback loops through the environment** are the core control mechanism — exactly the cybernetic pattern. Each behavior layer is a closed-loop controller.
- **No central controller** echoes second-order cybernetics and distributed regulation.
- **The world as its own model** resonates with Ashby's idea that a regulator need not have a richer internal model than what its regulatory task requires (requisite variety applied economically).
- **Emergent behavior** from coupled subsystems parallels cybernetic accounts of self-organization.
- **Subsumption as priority arbitration** is a form of variety management — higher-level goals suppress lower-level behaviors only when needed, preserving autonomy otherwise.

## Relevance to Modern Agent Design

1. **LLMs are the antithesis of Brooks' vision** — massive internal representations, no embodiment, no direct sensory coupling. Yet modern LLM agent frameworks (ReAct, tool-use architectures) re-introduce Brooks-like patterns: tight perception-action loops via tool calls, the environment providing feedback, iterative grounding.

2. **Layered agent architectures** (safety layers, planning layers, execution layers) echo subsumption. Modern guardrail systems that can override agent actions are structurally similar to higher subsumption layers inhibiting lower ones.

3. **The core tension Brooks identified** — between rich internal models and direct environmental interaction — remains unresolved. Current agents over-rely on internal "reasoning" and under-use environmental feedback, leading to hallucination and drift. Brooks would predict this.

4. **Tool use as environmental coupling.** When an LLM agent executes code, calls an API, or queries a database, it is (briefly) coupling to the world. This is the Brooks pattern, applied intermittently rather than continuously.

5. **Fragility of plans.** Brooks' critique of GOFAI planning (plans break on contact with reality) anticipates the well-documented failure modes of LLM agents that generate multi-step plans without intermediate verification.
