# Barandiaran, Di Paolo & Rohde (2009) — Defining Agency

## Citation

Barandiaran, X. E., Di Paolo, E. A., & Rohde, M. (2009). Defining Agency: Individuality, Normativity, Asymmetry, and Spatio-temporality in Action. *Adaptive Behavior*, 17(5), 367–386. DOI: 10.1177/1059712309343819

Available: https://xabier.barandiaran.net/wp-content/uploads/2009/07/barandiaran_dipaolo_rohde_-_defining_agency_v_1_0_-_jab_20091.pdf

~373 citations. Foundational paper in the enactivist account of agency.

## The Problem

"Agency" is used loosely in AI and cognitive science. Everyone talks about agents, but there is no rigorous, operational definition of what makes something an agent as opposed to a mere mechanism. This is not pedantry — the lack of a definition means we cannot systematically compare different agent architectures, or say precisely what current AI agents lack.

## Three Necessary Conditions for Agency

The authors propose that genuine agency requires three conditions, all of which must be met simultaneously:

### 1. Individuality

The system must constitute its own identity. It must be a **self-individuating** entity — its boundaries and organization must be maintained by its own processes, not imposed from outside.

This rules out most AI agents. An LLM agent's individuality is defined by its architecture, weights, and deployment configuration — all externally imposed. The agent does not maintain its own boundaries.

### 2. Interactional Asymmetry

The agent must be the **active source** of its interactions with the environment, not merely reactive. There must be an asymmetry between the agent and its environment — the agent initiates, the environment responds (and vice versa, but the initiation matters).

This is related to but distinct from the cybernetic notion of a controller. A thermostat has interactional asymmetry (it initiates heating/cooling). But the authors require more: the asymmetry must be grounded in the agent's own self-maintaining organization.

### 3. Normativity

The agent must regulate its activity according to norms that arise from its own organization. These norms are not externally defined goals or reward functions — they are **intrinsic** to the agent's way of being.

The source of intrinsic normativity is **precariousness**: a genuine agent is always at risk of disintegration. It must act to maintain itself. This creates a natural norm: actions that sustain the agent are "good" (for the agent); actions that lead to its dissolution are "bad."

## The Generative Definition

The authors don't just list conditions — they provide a **generative definition**: they describe a minimal organizational template that, when instantiated, necessarily produces a system satisfying all three conditions. This is inspired by the autopoietic definition of life.

The minimal template is:
- A self-maintaining organization (provides individuality and normativity)
- That is thermodynamically open and materially precarious (provides the basis for norms)
- That actively regulates its coupling with its environment (provides interactional asymmetry)
- And whose regulation is adaptive — it can modify its interaction patterns based on the consequences of its actions (provides genuine agency beyond mere homeostasis)

## Key Distinction: Agency vs. Mere Activity

A rock rolling down a hill is active but not an agent. A thermostat is a controller but not an agent (it lacks self-individuation and intrinsic normativity). A bacterium swimming up a sugar gradient is a genuine (minimal) agent: it is self-individuating (autopoietic), it is the active source of its movement, and its behavior is normatively regulated by its own metabolic requirements.

## Relevance to Agent Design

### The Hard Question for AI

By this definition, **no current AI system is a genuine agent**. They fail on all three conditions:
- Their individuality is externally imposed
- Their norms are externally defined (reward functions, objective functions, user instructions)
- While they may exhibit interactional asymmetry, it is not grounded in self-maintenance

This is not necessarily a problem if we are just building useful tools. But if we want to build systems with genuine autonomy, adaptability, and robust goal-pursuit, this analysis suggests we are missing something fundamental.

### What Would It Take?

To build something closer to a genuine agent, we would need:
1. A system that maintains its own organization (some form of computational autopoiesis?)
2. A system that is "precarious" — that must act to maintain itself (resource-limited agents? agents that must earn compute?)
3. A system whose goals arise from its own self-maintenance needs, not from external specification

This connects to the homeostatic AI safety work (Pihlakas) and to ideas about bounded, resource-aware agents.

### The Cybernetic Connection

The paper draws explicitly on cybernetics (especially Ashby) and develops it further:
- **Ashby's homeostat** provides a minimal model of adaptive regulation, but lacks self-individuation
- **Autopoiesis** provides self-individuation but originally lacked a clear account of agency (which is what this paper adds)
- **PCT** provides hierarchical control but with externally-defined reference levels

The paper synthesizes these traditions into a unified account.

## Intellectual Heritage

Draws on: Jonas (philosophical biology), Maturana & Varela (autopoiesis), Ashby (ultrastability), Piaget (developmental psychology), Thompson (mind in life).

## Relation to Other Notes

- Maturana & Varela autopoiesis: The biological foundation
- Ashby: Ultrastability as a component of adaptive agency
- Powers PCT: Hierarchical control without intrinsic normativity
- De Jaegher & Di Paolo (2007): Extends this individual agency to social/participatory agency
- Froese (2012): Traces the intellectual lineage this paper builds on
- Pihlakas homeostatic goals: Attempt to implement something like intrinsic normativity in AI
