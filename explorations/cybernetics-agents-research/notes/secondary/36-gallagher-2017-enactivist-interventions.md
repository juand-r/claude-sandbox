# Gallagher (2017) — Enactivist Interventions: Rethinking the Mind

## Citation

Gallagher, S. (2017). *Enactivist Interventions: Rethinking the Mind*. Oxford University Press. ISBN: 978-0-19-879432-5.

## Core Thesis

Cognition is not in the head. It is distributed across brain, body, and environment. The mind is not a representational engine processing internal models but an embodied, enacted, situated process of making sense of the world through action and interaction. Gallagher presents the mature statement of the enactivist program and defends it against the main objections.

## Key Arguments

### 1. Five Principles of Enactivism

Gallagher distills enactivism to five core principles:

1. **Cognition is not just neural**: Cognitive processes span brain-body-environment. They cannot be reduced to brain events.
2. **The world is enacted, not pre-given**: Meaning and intentionality are not "out there" waiting to be represented but are brought forth through the organism's embodied engagement.
3. **No internal representations**: Understanding comes from embodied engagement, not from building internal models or maps. (This is the most contested principle.)
4. **Dynamical systems, not computation**: Cognitive processes are better described by dynamical systems theory (coupling, coordination, attractor dynamics) than by computational/information-processing models.
5. **Cognition is social and intersubjective**: Cognitive systems are not isolated individuals but are constitutively shaped by social interaction and cultural embedding.

### 2. Against Representation

Gallagher argues that representational accounts of cognition face a dilemma:
- If "representation" is defined strictly (isomorphic internal models), then most cognition is not representational — organisms cope with the world through action, not modeling.
- If "representation" is defined loosely (any internal state that carries information), then the concept loses explanatory power — everything becomes a representation.

The enactivist alternative: cognition is **operative intentionality** (Merleau-Ponty) — a directedness toward the world expressed in bodily action, not in mental representations.

### 3. Affordances Over Representations

Instead of representing the world and then acting, agents **perceive affordances** — action possibilities that the environment offers given the agent's embodied capacities. A door affords opening; a cup affords grasping. These affordances are not represented; they are directly perceived through the agent's bodily engagement.

### 4. The "Scaling Up" Problem

The biggest challenge for enactivism: can it explain "higher-order" cognition — abstract thought, mathematics, imagination, planning? These seem to require exactly the kind of detached, representational thinking that enactivism rejects.

Gallagher's response: even abstract cognition is grounded in affordance-based, embodied coping. Mathematical reasoning involves manipulating external symbols (on paper, on screens) — it is not purely internal. Imagination involves bodily simulation. Planning involves anticipation of action possibilities.

This is the weakest part of the argument and Gallagher acknowledges the challenge is not fully resolved.

### 5. Social Cognition: Beyond Mindreading

We understand others not primarily through "mindreading" (inferring hidden mental states) but through **direct perception** of their intentions and emotions in their bodily expressions, gestures, and actions. Social cognition is participatory — it arises in the interaction, not in the individual.

This draws directly on De Jaegher & Di Paolo's participatory sense-making.

## Relevance to Agent Design

### The Challenge to LLM Agents

Gallagher's enactivism poses a fundamental challenge:

1. **LLM agents are paradigmatically representational**: They process token sequences — discrete symbolic representations. If representations are the wrong level for understanding cognition, then LLM agents are not cognitive in the enactivist sense.

2. **LLM agents lack bodies**: No embodiment means no affordances, no operative intentionality, no grounding. The "grounding problem" is not just a technical issue but an architectural one.

3. **LLM agents lack genuine interaction**: They process input and generate output. They do not engage in the kind of dynamical coupling that enactivism requires. Their "interaction" is discrete and turn-based, not continuous and embodied.

### What Can Be Salvaged

Despite these challenges, some enactivist insights are useful for agent design:

1. **Affordance-based tool selection**: Instead of representing tools as objects with properties and methods, an agent could "perceive" tool affordances — what actions they enable given the current task context. This is closer to ready-to-hand engagement than present-at-hand analysis.

2. **Dynamical coupling with environment**: Agents that continuously monitor and respond to their environment (streaming, event-driven) are closer to the enactivist ideal than request-response agents.

3. **Social cognition for multi-agent systems**: Agents that coordinate through interaction (stigmergy, shared environments) rather than through explicit message-passing are closer to participatory sense-making.

4. **The scaling-up problem is ours too**: How do we get agents from reactive tool-use to genuine abstract reasoning? Gallagher's account suggests grounding abstract reasoning in concrete embodied practices — which for AI agents might mean grounding reasoning in tool use and environmental interaction.

### Connection to Cybernetics

Enactivism inherits from cybernetics:
- The emphasis on circular causality (perception-action loops)
- The rejection of input-output models in favor of coupled systems
- Self-organization as a fundamental principle
- The constitutive role of the observer

But it adds the phenomenological dimension that cybernetics lacks: what it is like to be an engaged, embodied agent.

## Relation to Other Notes

- Dreyfus (2007): Shares the anti-representationalist stance; Gallagher extends the argument
- De Jaegher & Di Paolo (2007): Social cognition framework that Gallagher builds on
- Froese (2012): The historical lineage from cybernetics to enactivism
- Clark (2013): Predictive processing — potentially compatible or incompatible with enactivism depending on whether prediction counts as representation
- Barandiaran et al. (2009): The formal definition of agency that enactivism requires
