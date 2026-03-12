# Russell & Norvig (2010) — Artificial Intelligence: A Modern Approach (3rd Edition)

## Citation

Russell, S. J., & Norvig, P. (2010). *Artificial Intelligence: A Modern Approach* (3rd ed.). Upper Saddle River, NJ: Prentice Hall. ISBN: 978-0-13-604259-4.

Also: 4th edition (2020) — updated but the agent framework is fundamentally the same.

The most widely used AI textbook globally. Used in 1,400+ universities. Defines the mainstream vocabulary for agent-based AI.

## Core Framework: The Rational Agent

Russell & Norvig organize all of AI around a single concept: the **rational agent**. An agent is anything that perceives its environment through sensors and acts upon it through actuators. A rational agent selects actions that are expected to maximize its performance measure, given its percept sequence and built-in knowledge.

This is Ashby's regulator in different clothing. The rational agent framework formalizes what cybernetics calls the control problem.

## PEAS: Task Environment Specification

Every agent design begins with specifying:
- **Performance measure**: How success is evaluated
- **Environment**: The world the agent operates in
- **Actuators**: How the agent acts
- **Sensors**: How the agent perceives

This is equivalent to specifying the cybernetic control loop: what is the reference signal (performance measure), what is the plant (environment), what are the effectors (actuators), and what is the feedback channel (sensors).

## Agent Architectures (Hierarchy of Increasing Sophistication)

### 1. Simple Reflex Agents
Condition-action rules: if X is perceived, do Y. No memory, no model.

Cybernetic analogue: a simple thermostat. Fixed reference level, direct feedback, no internal model.

### 2. Model-Based Reflex Agents
Maintain an internal model of the world state. Update the model based on percepts. Choose actions based on the model.

Cybernetic analogue: a controller with a model of the plant (exactly what the Good Regulator Theorem says you need).

### 3. Goal-Based Agents
Have explicit goals. Use the model to plan actions that achieve goals. Can reason about future states.

Cybernetic analogue: hierarchical control with goal-seeking behavior. The reference level is now a goal state, not a fixed value.

### 4. Utility-Based Agents
Have a utility function over states. Choose actions that maximize expected utility. Handle tradeoffs and uncertainty.

Cybernetic analogue: optimal control. The reference signal is replaced by an optimization criterion.

### 5. Learning Agents
A meta-architecture layered on top of any of the above. The agent improves its own performance by learning from experience. Components:
- **Performance element**: The current agent architecture
- **Critic**: Evaluates performance
- **Learning element**: Modifies the performance element based on critic feedback
- **Problem generator**: Suggests exploratory actions

Cybernetic analogue: ultrastability. The learning agent changes its own parameters (step function) when performance falls below threshold. The critic is the essential variable monitor. The problem generator is the source of random variation.

## Task Environment Properties

Environments are classified along dimensions:
- **Fully observable** vs. **partially observable**: Does the agent see the complete state?
- **Deterministic** vs. **stochastic**: Are outcomes of actions predictable?
- **Episodic** vs. **sequential**: Does each decision depend on previous ones?
- **Static** vs. **dynamic**: Does the environment change while the agent deliberates?
- **Discrete** vs. **continuous**: State and action spaces
- **Single-agent** vs. **multi-agent**: Competitive or cooperative?

These dimensions determine how much variety the agent must manage. Partially observable, stochastic, sequential, dynamic, continuous, multi-agent environments have maximum variety — and require maximum regulatory variety from the agent.

## Relevance to Agent Design

### 1. The Standard Vocabulary

Russell & Norvig's framework is the lingua franca of AI agent design. When people say "agent" in AI, they typically mean Russell & Norvig's definition. This makes it essential reference for any cross-disciplinary work bridging cybernetics and AI.

### 2. The Architecture Hierarchy Maps to Cybernetic Complexity

The progression from simple reflex to learning agent is a progression in regulatory sophistication:
- Simple reflex = zero-order control (no feedback, just reaction)
- Model-based = first-order control (feedback via model)
- Goal-based = hierarchical control (reference levels as goals)
- Utility-based = optimal control (reference levels as optimization criteria)
- Learning = ultrastable control (self-modifying parameters)

This mapping is not superficial — it reflects a genuine structural homology between the two frameworks.

### 3. What Russell & Norvig Misses

The rational agent framework has blind spots from a cybernetic perspective:

1. **No self-model**: The agent models the environment but not itself. It has no internal feedback about its own state. Seth's interoceptive inference addresses this gap.

2. **No autonomy in the strong sense**: The agent's goals and utility function are externally specified. Barandiaran et al.'s definition requires intrinsic normativity — the agent's norms arising from its own organization.

3. **No social dimension**: The multi-agent case is treated as a complication of the single-agent case, not as a fundamentally different mode of cognition. De Jaegher & Di Paolo's participatory sense-making is the alternative.

4. **No embodiment**: The PEAS framework treats sensors and actuators as interfaces, not as constitutive of cognition. The enactivist critique (Gallagher, Dreyfus) applies.

5. **No variety analysis**: Russell & Norvig do not ask "how much regulatory variety does this agent need?" — which is exactly what Ashby's framework provides.

### 4. LLM Agents in the RAINA Framework

Where do LLM agents fit?
- They are partly **model-based** (they have an implicit world model in their weights)
- They are partly **goal-based** (they pursue user-specified goals)
- They are **learning agents** in a limited sense (they learn within context windows but not across sessions)
- They operate in **partially observable, stochastic, sequential, dynamic** environments — the most challenging category

The gap: LLM agents have more capable perception and reasoning than the simple agents in Russell & Norvig's hierarchy, but less structured control architecture. They are powerful but poorly regulated.

## Connection to Cybernetics

The Russell & Norvig framework is cybernetics translated into the vocabulary of computer science and decision theory:

| AIMA Concept | Cybernetic Concept |
|---|---|
| Percept | Feedback signal |
| Action | Effector output |
| Performance measure | Reference level / Essential variable |
| Internal model | Model (Good Regulator Theorem) |
| Learning | Ultrastability / Parameter adaptation |
| Utility maximization | Optimal regulation |
| PEAS | Control loop specification |
| Environment properties | Disturbance characterization |

The translation is nearly one-to-one, suggesting that the two frameworks describe the same underlying structure.

## Relation to Other Notes

- Ashby: The formal variety framework that Russell & Norvig implicitly use
- Powers PCT: Hierarchical control — closely related to the agent architecture hierarchy
- Good Regulator Theorem: The model-based agent is the Good Regulator instantiated
- Beer VSM: Multi-level organizational architecture — extends Russell & Norvig's single-agent focus
- Shoham & Leyton-Brown: The multi-agent extension
- Clark (2013): Predictive processing as a specific instantiation of the model-based + learning agent
- Wang et al. agent survey: Modern LLM agents classified using Russell & Norvig's vocabulary
