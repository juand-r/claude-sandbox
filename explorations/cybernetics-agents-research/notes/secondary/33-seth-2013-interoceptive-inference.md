# Seth (2013) — Interoceptive Inference, Emotion, and the Embodied Self

## Citation

Seth, A. K. (2013). Interoceptive inference, emotion, and the embodied self. *Trends in Cognitive Sciences*, 17(11), 565–573. DOI: 10.1016/j.tics.2013.09.007

Available: https://www.fil.ion.ucl.ac.uk/~karl/Interoceptive%20inference%20emotion%20and%20the%20embodied%20self..pdf

Highly cited (~1,800 citations). Extends Clark's predictive processing framework inward, to the body.

## Core Thesis

Emotional experience and embodied selfhood arise from **interoceptive inference** — the brain's predictive modeling of the causes of signals from within the body (heartbeat, gut feelings, breathing, etc.). Emotions are not reactions to external events but are the brain's best guesses about the internal physiological state of the organism.

## Key Arguments

### 1. Predictive Processing Applied to the Body

Clark (2013) showed how predictive processing works for exteroceptive perception (vision, hearing). Seth extends this to **interoception** — the perception of the body's internal state. The brain generates predictions about interoceptive signals (heart rate, respiration, visceral states) and updates these predictions when errors arise.

This means the brain doesn't just model the external world — it models **itself**. The body is another "environment" that the brain must regulate through predictive inference.

### 2. Emotion as Interoceptive Prediction Error

Emotional experience arises from the interplay between top-down interoceptive predictions and bottom-up interoceptive signals. Emotions are what it is like to have a particular pattern of interoceptive predictions and prediction errors.

This generalizes appraisal theories of emotion (which say emotions involve cognitive evaluations of physiological changes) by grounding them in a specific computational mechanism: Bayesian inference over generative models of bodily states.

### 3. Active Interoceptive Inference

Just as exteroceptive prediction errors can be minimized by acting on the world (active inference), interoceptive prediction errors can be minimized by **acting on the body** — through autonomic reflexes, hormonal regulation, etc.

The brain generates interoceptive predictions that "enslave" autonomic reflexes: sympathetic and parasympathetic outflow from the anterior insular cortex (AIC) and anterior cingulate cortex (ACC) serve as interoceptive predictions that drive the body toward predicted states. This is motor control applied inward — visceromotor control.

### 4. Precision Weighting in Interoception

As in exteroceptive processing, precision weighting modulates the balance between top-down predictions and bottom-up signals. When interoceptive precision is high, the brain is highly attentive to bodily signals (anxiety, panic). When precision is low, bodily signals are suppressed in favor of prior expectations (dissociation, depersonalization).

This provides a computational account of disorders ranging from anxiety (excessive interoceptive precision) to depersonalization (insufficient interoceptive precision).

### 5. Embodied Selfhood

The sense of being an embodied self — of owning a body, of being located within it — emerges from integrating interoceptive predictions with exteroceptive and proprioceptive predictions. The self is not a fixed entity but a **continually updated inference** about the overall state of the organism.

## The Neural Architecture

Seth proposes that interoceptive inference is implemented in a **salience network** anchored on:
- Anterior insular cortex (AIC) — interoceptive predictions
- Anterior cingulate cortex (ACC) — error monitoring and autonomic control
- Brainstem nuclei — relay of interoceptive signals and autonomic reflex arcs

## Relevance to Agent Design

### The Missing Body

Current AI agents are disembodied prediction machines. They have no body, no interoception, no visceral states. Seth's work reveals what this absence costs:

1. **No intrinsic motivation**: In biological agents, the body's homeostatic needs (hunger, fatigue, pain) generate intrinsic motivation through interoceptive inference. AI agents have no analogous drive — their "motivation" is entirely externally specified.

2. **No emotional regulation**: Emotions, on this account, are a regulatory mechanism — they modulate behavior based on the organism's internal state. AI agents have no internal state to regulate. They cannot be "anxious" about uncertainty or "confident" about well-calibrated predictions.

3. **No grounded self-model**: The sense of self arises from interoceptive inference. AI agents have no self-model in this sense — they have no continuous inference about their own operational state.

### What Could Be Borrowed

Even without a body, some architectural insights apply:

- **Internal state monitoring**: An agent could monitor its own computational state (memory usage, confidence levels, processing load) as a form of artificial interoception. Deviations from predicted internal states could serve as "meta-prediction errors" that trigger self-regulation.
- **Precision weighting for uncertainty**: When the agent is uncertain, it should up-weight incoming evidence (high precision on prediction errors). When confident, it should rely more on its model (low precision on errors). This is a concrete design pattern.
- **Homeostatic reference levels**: The agent could maintain target ranges for internal variables (response latency, token budget, confidence threshold) and regulate its behavior to stay within these ranges. This echoes the homeostatic AI safety ideas.

### Connection to Cybernetics

Seth's interoceptive inference is a specific instance of **nested control loops**: the brain controls the body's internal state just as it controls its interaction with the external world. This is hierarchical control in Powers' sense, but applied inward. The "reference level" for interoceptive control is the predicted homeostatic state.

The Good Regulator Theorem applies here too: to regulate the body effectively, the brain must be a model of the body. Seth provides the mechanism: the generative model of interoceptive causes.

## Relation to Other Notes

- Clark (2013): The exteroceptive framework that Seth extends inward
- Friston FEP: The formal mathematical framework underlying Seth's model
- Powers PCT: Hierarchical control — Seth adds the inward-facing loops
- Barandiaran et al. (2009): Normativity from precariousness — Seth provides a mechanism
- Pihlakas homeostatic goals: Practical attempt at implementing internal homeostasis in AI
