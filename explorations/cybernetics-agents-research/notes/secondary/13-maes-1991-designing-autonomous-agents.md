# Designing Autonomous Agents

## Citation
Maes, P. (Ed.). (1991). *Designing Autonomous Agents: Theory and Practice from Biology to Engineering and Back.* MIT Press. (Reprinted from *Robotics and Autonomous Systems*, 6(1-2), 1990.)

## Summary

An edited volume that became the manifesto of the "nouvelle AI" movement. Collects key papers from the researchers who, in the late 1980s, rejected classical AI's top-down approach in favor of bottom-up, behavior-based, biologically inspired agent design. Contributors include Brooks, Agre & Chapman, Beer, Steels, Kaelbling, Arkin, and Maes herself.

## Key Arguments (across the volume)

1. **Direct sensing-action coupling.** The new architectures emphasized more direct coupling of sensing to action, distributed and decentralized control, dynamic interaction with the environment, and intrinsic mechanisms to cope with limited resources and incomplete knowledge.

2. **Emergent functionality.** Complex behavior is not explicitly programmed but emerges from the interaction of simple behaviors with each other and the environment. This is a key theme across multiple chapters.

3. **Task-level decomposition.** Instead of functional decomposition (perception, planning, motor control), the system is decomposed by task or behavior — each complete module handles a specific competence.

4. **Maes' activation/inhibition dynamics.** Maes' own contribution ("Situated Agents Can Have Goals") argued that behavior selection can be modeled as an emergent property of activation/inhibition dynamics over goals in relation to the current situation. No central scheduler picks the next behavior; selection emerges from spreading activation.

5. **Steels on analogical representations.** Steels argued that purely reactive agents without internal models are severely limited, but the solution is not symbolic AI's abstract representations. Instead, use "analogical representations" — internal structures close to sensor outputs — with reasoning over these concrete representations. A middle ground between Brooks and classical AI.

6. **Beer on computational neuroethology.** Beer, Chiel & Sterling contributed "A Biological Perspective on Autonomous Agent Design," arguing that biological nervous systems provide working examples of adaptive control that AI should emulate rather than ignore.

7. **Agre & Chapman on plans-as-communication.** "What Are Plans For?" (see note 18) challenged the plan-as-program view from inside the volume.

## Key Contributors and Their Chapters

| Author(s) | Chapter | Key Idea |
|---|---|---|
| Brooks | "Elephants Don't Play Chess" | The world is its own model; subsumption |
| Agre & Chapman | "What Are Plans For?" | Plans as communication, not programs |
| Kaelbling & Rosenschein | "Action and Planning in Embedded Agents" | Situated automata with compiled specifications |
| Maes | "Situated Agents Can Have Goals" | Activation-based behavior selection |
| Steels | "Exploiting Analogical Representations" | Representations grounded in sensor data |
| Beer, Chiel & Sterling | "A Biological Perspective" | Computational neuroethology |
| Arkin | "Integrating Behavioral, Perceptual, and World Knowledge" | Reactive navigation with schema theory |
| Payton | "Internalized Plans" | Gradient-field action representations |

## Connection to Cybernetics

The volume is an implicit return to cybernetic principles, even though cybernetics is rarely cited:

- **Distributed control** (no central executive) is a cybernetic organizational principle.
- **Feedback through the environment** is the fundamental cybernetic loop.
- **Homeostatic behavior selection** (Maes' activation dynamics) resembles Ashby's ultrastability — behaviors compete and the system settles into one that reduces the gap between current and desired states.
- **The emphasis on real-world interaction** over abstract reasoning echoes Wiener's insistence that cybernetics is about control and communication in real systems.

## Relevance to Agent Design

1. **This volume defined "agent" for the 1990s.** The shift from "expert system" to "autonomous agent" that this volume catalyzed is the direct ancestor of modern AI agent design.

2. **Maes' activation dynamics** anticipated modern attention/priority mechanisms in agent frameworks. The idea that behavior selection should emerge from dynamics rather than be explicitly programmed resonates with how LLM agents select tools based on contextual activation rather than rigid rules.

3. **The debate within the volume** — Brooks (no representations) vs. Steels (grounded representations) vs. classical AI (abstract representations) — maps directly onto current debates about whether LLM agents should reason internally or externally, and how much internal state they need.

4. **The emphasis on "complete agents"** — systems that handle perception, decision, and action together — challenges the modern tendency to focus on the reasoning component (the LLM) while treating perception and action as afterthoughts.
