# Clark (2013) — Whatever Next? Predictive Brains, Situated Agents, and the Future of Cognitive Science

## Citation

Clark, A. (2013). Whatever next? Predictive brains, situated agents, and the future of cognitive science. *Behavioral and Brain Sciences*, 36(3), 181–204. DOI: 10.1017/S0140525X12000477

Available: https://www.fil.ion.ucl.ac.uk/~karl/Whatever%20next.pdf

Over 3,100 citations. One of the foundational texts of the **predictive processing** framework.

## Core Thesis

The brain is fundamentally a prediction machine. It continuously generates top-down predictions of incoming sensory signals and updates its generative models when prediction errors arise. This is not a peripheral cognitive process — it is **the** organizing principle of cortical computation.

## Key Arguments

### 1. Hierarchical Generative Models

The brain maintains a hierarchy of generative models. Higher levels predict the activity of lower levels. When predictions fail, the resulting **prediction error** propagates upward, forcing the higher-level model to update. This is the core computational loop: predict → compare → correct.

This is directly analogous to a cybernetic feedback loop, but with a crucial difference: the "reference signal" (in PCT terms) is not fixed but is itself the output of a higher-level model. The hierarchy is nested control.

### 2. Perception as Inference

Following Helmholtz, perception is treated as **probabilistic inference** — the brain infers the most likely causes of sensory signals given its generative model. Perception is not passive reception but active hypothesis-testing. This means the agent's model of the world is not a mirror but a **constructed inference**.

Connection to Good Regulator Theorem: The brain literally must be a model of the system it regulates (its sensory environment). Clark's account provides a specific mechanism for how this model is maintained and updated.

### 3. Action as Prediction Error Minimization

Action is not a separate system. The agent can minimize prediction errors in two ways:
- **Perceptual inference**: Update the model to match the world
- **Active inference**: Change the world to match the model (act)

This unification of perception and action under a single principle (minimize prediction error) is deeply cybernetic. It echoes Powers' PCT — the agent controls its perceptions, not its outputs.

### 4. Precision Weighting (Attention)

Not all prediction errors are treated equally. The system assigns **precision** (inverse variance) to each error signal. High-precision errors demand model updates; low-precision errors are suppressed. Precision weighting is the mechanism underlying **attention** — attending to something means increasing the precision weight on its prediction errors.

This is a form of **gain control** in cybernetic terms: the system modulates its own sensitivity to different feedback channels.

### 5. The Action-Perception Cycle

Rather than perceive-then-act, the agent operates in a continuous cycle where action and perception mutually constrain each other. The agent actively samples its environment to test predictions. This is **epistemic action** — action in the service of reducing uncertainty, not just achieving goals.

## Relevance to Agent Design

### Direct Architectural Implications

1. **Hierarchical prediction as agent architecture**: Modern LLM agents could be understood as (impoverished) prediction machines. They predict next tokens based on context. But they lack the hierarchical generative model and the ability to update their model based on prediction error in real time. This is a concrete design gap.

2. **Active inference as exploration**: ReAct-style agents do something like active inference — they act to gather information. But they lack precision weighting; they treat all observations equally. An agent with precision weighting would know which observations to attend to and which to discount.

3. **Unified perception-action**: Current agent architectures often have a sharp boundary between "observation" and "action" phases. Clark's framework suggests these should be unified — the agent should be continuously predicting and acting, not alternating between distinct modes.

4. **Model updating**: Current LLM agents have frozen models. They cannot update their generative model in real time based on prediction errors. This is perhaps the most fundamental limitation when viewed through this lens.

### Connection to Other Cybernetic Concepts

- **Law of Requisite Variety**: The hierarchical generative model must have sufficient variety to match the variety of the environment it models. The depth of the hierarchy determines the complexity of patterns that can be predicted.
- **Ultrastability**: The precision-weighting mechanism is a form of meta-level control — the system adjusts its own parameters when first-order feedback fails.
- **Good Regulator Theorem**: The predictive model is literally the "model of the system" that Conant & Ashby require.

### Limitations as Agent Theory

Clark's account is primarily about biological brains. Translating it to artificial agents requires careful thought about:
- What plays the role of the generative model in an LLM agent?
- How does precision weighting map to tool selection or context management?
- Can prediction error minimization be operationalized for discrete symbolic agents, not just continuous neural ones?

## Key Quotes

- "The core function of the brain is not to process information, but to generate predictions about incoming sensory signals."
- "Action and perception are not separate but are two sides of the same coin: both serve to minimize prediction error."

## Relation to Other Notes

- Friston FEP/active inference: Clark's paper is the accessible entry point to Friston's more formal framework
- Powers PCT: Clark's hierarchy of prediction echoes Powers' hierarchy of perceptual control
- Seth (2013): Extends Clark's framework inward, to interoception
- Dreyfus (2007): Critiques representation-based AI; Clark's predictive processing may or may not count as "representation"
