# Being There: Putting Brain, Body, and World Together Again

## Citation
Clark, A. (1997). *Being There: Putting Brain, Body, and World Together Again.* MIT Press.

## Summary

A philosophical synthesis of the embodied, situated, and behavior-based approaches to cognition that emerged in the late 1980s and early 1990s. Clark draws on Brooks' robotics, connectionism, dynamical systems theory, and developmental psychology to argue that minds are fundamentally for doing, not for representing — brains are controllers for embodied activity, not disembodied reasoning engines.

## Key Arguments

1. **Minds are for doing, not for thinking.** The central thesis: cognitive systems evolved not to construct elaborate internal models but to produce adaptive behavior in real time. "Might it not be more fruitful to think of brains as controllers for embodied activity?" This reframing has large implications for what counts as intelligence.

2. **The 007 Principle.** "James Bond is told only what he needs to know in order to complete his mission." Biological systems acquire and process only the information needed for the task at hand, avoiding costly internal representations. Evolution favors cognitive frugality.

3. **Cheap design.** Related to the 007 principle: evolution favors solutions that exploit environmental structure rather than building expensive internal models. Mounting assembler arms on rubber joints so parts "jiggle and slide into place" eliminates the need for complex computational feedback loops. Let the physics do the computing.

4. **The world as its own best model.** Drawing on Brooks (and anticipating later work on "embodied computation"), Clark argues that agents can use the world directly as an external memory and model, rather than internalizing everything. Perception is cheaper than representation.

5. **Cognitive scaffolding.** Agents alter their environments to enhance their cognitive capacities. External structures — notes, diagrams, tools, social institutions — are cognitive scaffolds that offload computation from brain to world. This anticipates Clark's later "extended mind" thesis.

6. **Wideware.** Environmental states, structures, or processes that play a functional role in cognitive processing. The calculator, the notebook, the shared whiteboard — these are part of the cognitive system, not mere inputs to it. Cognition extends beyond the skull.

7. **Brain as controller, not mirror.** The brain does not build a complete, accurate model of the world. It builds partial, action-oriented, task-specific representations sufficient for the current behavioral demands. Internal representations exist, but they are "action-oriented" — geared toward control, not toward truth.

8. **Continuous reciprocal causation.** Brain, body, and environment are locked in continuous, mutually causal interaction. You cannot understand cognition by studying the brain in isolation, because the brain's activity is shaped in real time by bodily and environmental dynamics.

## Connection to Cybernetics

Clark is one of the most cybernetics-adjacent philosophers of mind, even though he does not foreground the connection:

- **Brain as controller** is exactly the cybernetic view. Wiener's "control and communication in the animal and the machine."
- **Feedback through the environment** is the basic cybernetic loop. Clark makes it constitutive of cognition, not just instrumental.
- **The 007 principle** is an informal version of Ashby's Law of Requisite Variety applied conservatively: don't build more variety into the controller than the task requires.
- **Cheap design** aligns with Ashby's emphasis on finding the minimal regulator for a given disturbance set.
- **Cognitive scaffolding and wideware** extend the cybernetic system beyond the individual agent to include the environment — exactly what second-order cybernetics (the observer-system boundary is drawn by the observer) would predict.
- **Continuous reciprocal causation** is the cybernetic feedback loop made constitutive.

## Relevance to Agent Design

1. **The 007 principle for LLM agents.** Current LLM agents often stuff everything into the context window — massive system prompts, entire documents, full conversation histories. Clark's 007 principle suggests this is cognitively wasteful. Agents should retrieve only what they need for the current action. This supports lazy evaluation, just-in-time retrieval, and minimal context strategies.

2. **Cognitive scaffolding as tool design.** Tools are cognitive scaffolds for LLM agents. The quality of an agent's cognition depends not just on the LLM but on the quality of its scaffolding — its tools, memory systems, and environmental structures. This reframes agent design from "build a better brain" to "build better scaffolding."

3. **Wideware for agents.** The agent's cognitive system extends beyond the LLM. Code interpreters, databases, file systems, APIs — these are wideware. Designing good wideware is as important as designing good prompts.

4. **Cheap design for agent architectures.** Don't over-engineer the agent's internal reasoning when you can exploit environmental structure. If the information is in the database, query it rather than trying to derive it. If the computation is expressible as code, execute it rather than trying to reason about it. Let the tools do the work.

5. **Action-oriented representations.** Clark's insight that internal representations should be action-oriented (geared toward control, not truth) suggests that LLM agents' internal reasoning should be organized around what to do next, not around building comprehensive world models. This supports the ReAct pattern (Thought → Action → Observation) over pure chain-of-thought reasoning.

6. **Continuous reciprocal causation in agent loops.** The best agent architectures implement something like continuous reciprocal causation: the agent acts, the environment changes, the change is observed, the observation shapes the next action. ReAct, Reflexion, and similar frameworks approximate this, but with discrete rather than continuous coupling.
