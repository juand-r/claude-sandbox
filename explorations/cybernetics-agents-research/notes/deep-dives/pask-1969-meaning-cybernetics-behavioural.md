# Pask — The Meaning of Cybernetics in the Behavioural Sciences (1969)

## Bibliographic Details
- **Author:** Gordon Pask
- **Full title:** "The meaning of cybernetics in the behavioural sciences (The cybernetics
  of behaviour and cognition; extending the meaning of 'goal')"
- **Published in:** J. Rose (Ed.), *Progress of Cybernetics — Vol. I*, pp. 15–44/45.
  London: Gordon and Breach Science Publishers, 1970 (proceedings from 1969).
- **Full text:** [Pangaro archive](https://www.pangaro.com/pask/pask%20meaning%20of%20cybernetics%20in%20behavioural%20sciences.pdf), [Scribd](https://www.scribd.com/document/500994688/pask-meaning-of-cybernetics-in-behavioural-sciences)

## Significance

This paper is considered a pivotal transition point in Pask's career. Its subtitle —
"extending the meaning of 'goal'" — signals the core problem: classical cybernetics
(Wiener, Ashby) had formalized goal-directed behavior in terms of homeostatic set-points
and error-correction. But human cognition and behavior involve goals that are not
pre-specified, that evolve through interaction, and that can be self-referential.

Pask argued here for **a cybernetics that could address human cognition and consciousness.**
The requirements he spelled out represent the distillation of nearly two decades of work
as a cybernetician. He then spent the next decade (1970s) answering his own challenge
with Conversation Theory.

## Key Arguments

### Extending "Goal" Beyond Homeostasis
Classical cybernetics defined a goal as a fixed reference state — a thermostat's set-point.
Pask argued this was too narrow for behavioral science. Human goals are:
- **Self-modifying** — we change our goals as we pursue them
- **Emergent** — goals can arise from interaction, not just from prior specification
- **Hierarchically nested** — goals contain sub-goals, and the hierarchy itself evolves
- **Socially constructed** — goals are negotiated through conversation

### Cybernetics of Behavior and Cognition
Pask argued that cybernetics needed to move beyond input-output behaviorism and address
the internal dynamics of cognitive systems — not by opening the black box (which violates
cybernetic methodology) but by building models of how cognitive processes interact through
conversation.

### Self-Regulatory Systems as Homeostats
A self-regulatory system should act as a homeostat: a device capable of adapting itself
to the environment through behaviors such as habituation and learning. But for cognitive
systems, the "environment" includes other cognitive systems, and adaptation involves
mutual adjustment, not one-way regulation.

### Intelligence in Interaction
As Pangaro summarized Pask's position: "intelligence resides in interaction, not inside
a head or box." Human intellectual activity exists as part of a resonance loop from an
individual through an environment or apparatus, and back.

## Relevance to Agent Architectures

### The Goal Problem in AI Agents
This paper directly addresses the fundamental challenge of agent design: how do you
specify goals for autonomous agents? The options are:
1. **Fixed goals** (classical AI, GOFAI) — too rigid, fails in novel situations
2. **Reward functions** (RL) — still externally specified, subject to reward hacking
3. **Emergent goals** (Pask's proposal) — goals arise from and evolve through interaction

Current LLM agents operate mostly with fixed goals (system prompts) or short-horizon
adaptive goals (ReAct loop). Pask's framework suggests a richer model where agent goals
emerge from and are modified through ongoing conversation with users and environments.

### Self-Modifying Goal Hierarchies
The idea of goals that modify themselves through interaction anticipates:
- **Meta-learning** in modern ML
- **Reflexion-style** self-correction where agents modify their strategies
- **Constitutional AI** where agents internalize and evolve behavioral principles

### Intelligence as Interaction, Not Computation
This is perhaps the most important insight for agent design: intelligence is not a
property of the agent alone, but of the agent-environment-user system. This implies:
- Evaluation of agents should focus on interaction quality, not isolated performance
- Agent design should prioritize interaction protocols over internal architecture
- The "smartest" agent is not the one with the most parameters but the one that creates
  the most productive interactions

## Connection to Other Pask Work

This paper is the intellectual bridge between:
- The early machines (Musicolour, SAKI) which demonstrated adaptive interaction in hardware
- Conversation Theory (1975-1976) which formalized these insights into a theory of
  knowledge construction through conversation
- The Architectural Relevance paper (1969) which applied these ideas to design
