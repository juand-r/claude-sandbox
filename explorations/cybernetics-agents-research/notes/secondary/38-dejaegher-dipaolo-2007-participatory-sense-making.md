# De Jaegher & Di Paolo (2007) — Participatory Sense-Making

## Citation

De Jaegher, H., & Di Paolo, E. (2007). Participatory Sense-Making: An Enactive Approach to Social Cognition. *Phenomenology and the Cognitive Sciences*, 6(4), 485–507. DOI: 10.1007/s11097-007-9076-9

Available: https://cspeech.ucd.ie/Fred/docs/DeJaegherDiPaolo2007.pdf

Foundational text in the enactive approach to social cognition. Extended in De Jaegher, Di Paolo & Gallagher (2010).

## The Problem

Traditional accounts of social cognition assume that understanding others requires inferring their hidden mental states — either through "theory of mind" (applying folk psychological theories) or through simulation (modeling their mental processes using your own). Both approaches locate social understanding in the individual mind.

De Jaegher and Di Paolo argue this gets the problem backwards. Social understanding is not primarily an individual cognitive achievement but an **emergent property of interaction**.

## Core Thesis

Sense-making — the process by which an organism makes its world meaningful through embodied engagement — becomes **participatory** in social encounters. The interaction process itself generates meanings that neither participant could generate alone. Social cognition is not mindreading; it is **co-authoring**.

## Key Arguments

### 1. The Autonomy of the Interaction Process

When two people interact, the interaction itself can take on a form of **autonomy** — it develops its own dynamics that constrain and enable the participants. Think of a conversation that "takes on a life of its own," or a dance where neither partner is fully in control. The interaction is not reducible to the sum of individual actions.

This is directly cybernetic: the interaction is a coupled system with emergent dynamics. The behavior of the whole cannot be predicted from the behaviors of the parts.

### 2. Coordination as the Basis

Social interaction rests on **coordination** — the mutual adjustment of movements, utterances, rhythms, and postures. Coordination can be:
- **Absolute**: Synchronization, mirroring
- **Relative**: Turn-taking, complementary action
- **Breakdown and repair**: Miscoordinations followed by adjustments

Coordination is not a cognitive achievement — it happens at a bodily level, often without awareness.

### 3. Sense-Making: From Individual to Social

Individual sense-making (from Di Paolo's earlier work) is how an autonomous organism makes its environment meaningful through its own embodied engagement. In social encounters, this becomes **participatory**: each agent's sense-making is **modulated** by the other's presence and activity. The interaction generates novel meanings.

The spectrum of participation:
- **Orientation**: One agent's sense-making is influenced by another's presence (minimal)
- **Coordination**: Agents mutually adjust their behaviors
- **Joint sense-making**: Meanings emerge that require the interaction and could not arise individually (maximal)

### 4. Beyond Individual Cognition

The traditional picture: individual A observes individual B, infers B's mental state, and acts accordingly. The participatory picture: A and B engage in an interaction that generates shared meaning through their mutual coordination. Understanding the other is not something A does alone — it is something A and B do together.

### 5. Not Restricted to Humans

Participatory sense-making occurs in any sufficiently coupled autonomous agents. Wolves circle-walking to size each other up. Octopuses displaying to each other. The concept is not anthropocentric.

## Relevance to Agent Design

### Multi-Agent Systems

This framework has direct implications for multi-agent AI:

1. **Emergent coordination**: Instead of explicit communication protocols, multi-agent systems could rely on mutual behavioral adjustment — agents adapting to each other's actions in a shared environment. This is closer to stigmergy than to message-passing.

2. **The interaction as a locus of intelligence**: In current multi-agent systems, intelligence resides in the individual agents. Participatory sense-making suggests that the interaction itself can be "intelligent" — generating solutions that no individual agent could produce alone. This is already observed in swarm intelligence but not well theorized.

3. **Coordination over communication**: Current multi-agent frameworks (CrewAI, AutoGen) rely heavily on explicit communication (messages, shared state). The PSM framework suggests that implicit coordination — agents responding to the observable effects of each other's actions — may be more robust and scalable.

### Human-AI Interaction

Perhaps more importantly, PSM reframes human-AI interaction:

1. **Conversation as participatory sense-making**: When a human interacts with an AI assistant, meaning is not transmitted from one to the other — it is **co-constructed** in the interaction. The human's input shapes the AI's response, which in turn shapes the human's next input. The quality of the interaction depends on the quality of this coordination, not just the quality of either participant.

2. **The autonomy of the conversation**: Long conversations with AI systems often develop their own dynamics — topics evolve, assumptions build up, shared references emerge. This is a form of interaction autonomy, even if the AI partner lacks genuine autonomy in Barandiaran's sense.

3. **Breakdown and repair**: The most interesting moments in human-AI interaction are breakdowns — misunderstandings, hallucinations, misinterpretations. How these are repaired (or not) determines the quality of the interaction. Designing for graceful breakdown-and-repair is an underexplored design principle.

### Connection to Cybernetics

- **Coupled systems**: Two agents in interaction form a coupled dynamical system. This is basic cybernetics.
- **Circular causality**: A affects B affects A — the classic feedback loop.
- **Emergence**: The interaction generates properties that neither component has alone. Ashby's design principle: the whole system must be analyzed as a whole.
- **Coordination as regulation**: Mutual adjustment is mutual regulation. Each agent is partly regulating the other.
- **Variety matching**: Successful coordination requires that each agent can match the variety of the other's behavior — a direct application of the Law of Requisite Variety.

## Relation to Other Notes

- Barandiaran et al. (2009): Individual agency — PSM extends this to social agency
- Gallagher (2017): Uses PSM as the basis for social cognition chapter
- Froese (2012): PSM continues the second-order cybernetics tradition
- Stigmergy notes: Indirect coordination through environment modification — related mechanism
- Pask conversation theory: Formal model of conversational interaction — potential bridge
