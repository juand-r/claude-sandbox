# Rosen (1985) — Anticipatory Systems

**Citation:** Rosen, R. (1985). *Anticipatory Systems: Philosophical, Mathematical & Methodological Foundations*. Pergamon Press, Oxford. (2nd ed. 2012, Springer, with Prolegomena by M. Nadin.)
**Access:** 2nd edition available from Springer (DOI: 10.1007/978-1-4614-1269-4), paywalled. Amazon has copies.

## Summary

The first detailed study of systems containing internal predictive models of themselves and/or their environments, whose predictions are utilized for purposes of present control. This book established Anticipatory Systems Theory (AST).

## Core Definition

> "An anticipatory system is a system containing a predictive model of itself and/or its environment, which allows it to change state at an instant in accord with the model's predictions pertaining to a latter instant."

## Feedforward vs. Feedback — The Central Distinction

This is the most directly relevant concept for agent design.

### Feedback (Reactive)
- Error-actuated: the stimulus to corrective action is the *discrepancy* between actual present state and desired state
- The system must already be departing from nominal behavior before control kicks in
- Reactive by definition: responds to what *has happened*
- Classic cybernetic loop: sense -> compare -> act

### Feedforward (Anticipatory)
- Model-actuated: the stimulus to action is a *predicted* future state from an internal model
- The system acts *before* deviation occurs
- Proactive: responds to what the model says *will happen*
- Anticipatory loop: model -> predict -> act -> sense (to update model)

### Key Insight
Feedforward is NOT prediction alone. Having a model of the future is not enough. **An anticipatory system must also make use of the prediction to change the present, so that a possibly different future from the one originally predicted may result.**

This means anticipation is inherently about *control*, not just *forecasting*.

## The Predictive Model

Critical properties:
1. **Runs faster than real time** — the model must produce predictions about future states before those states actually arrive
2. **Not certainty** — the model's predictions are assertions, not knowledge of the actual future
3. **Can be wrong** — and the system must handle model failure
4. **Must be updated** — the model needs feedback from reality to stay calibrated

## The Modeling Relation

Rosen's formal framework connecting a natural system S to a formal system F:

```
Natural System S  <--encoding-->  Formal System F
     |                                  |
  causality                          inference
     |                                  |
     v                                  v
  S(t+1)        <--decoding-->      F(t+1)
```

The encoding maps real-world states into formal objects. Inference in the formal system corresponds to causation in the natural system. Decoding maps predictions back to expected real states.

If this diagram commutes (encoding-then-inference gives the same result as causation-then-decoding), then F is a valid model of S.

## All Living Organisms Are Anticipatory Systems

This is Rosen's strong claim: anticipation is not an optional feature but a **fundamental component of all life.** An active form of the modeling relation is built into every organism.

Examples:
- DNA as a model of protein structure (encodes future states)
- Immune system anticipating pathogens (model of pathogen space)
- Neural predictions of sensory consequences of motor actions
- Circadian rhythms anticipating day/night cycles

## Relevance to Agent Architectures

### Reactive vs. Anticipatory Agents

| Feature | Reactive Agent | Anticipatory Agent |
|---------|---------------|-------------------|
| Control basis | Current state | Predicted future state |
| Response timing | After deviation | Before deviation |
| Internal model | None or implicit | Explicit predictive model |
| Error handling | Corrective | Preventive |
| Time horizon | Present only | Present + modeled future |

### Direct Applications

1. **Chain-of-thought as anticipation:** When an LLM-based agent "thinks ahead" about consequences of actions before taking them, it is implementing feedforward control via an internal model.

2. **Planning as faster-than-real-time simulation:** An agent that simulates outcomes of candidate actions before choosing one is running Rosen's predictive model.

3. **World models in RL:** Learned environment models (e.g., Dreamer, MuZero) are explicit realizations of Rosen's modeling relation.

4. **The model-action gap:** Rosen emphasizes that having a model is necessary but not sufficient. The agent must *act on* the model's predictions. Many current agents have good models but poor model-to-action coupling.

### Design Implications

- An agent that only uses feedback (react to errors) will always lag behind the environment
- An agent with an internal model that runs faster than real time can anticipate and preempt problems
- The quality of the model directly determines the quality of anticipatory behavior
- Model failure modes must be designed for: what happens when the model is wrong?
