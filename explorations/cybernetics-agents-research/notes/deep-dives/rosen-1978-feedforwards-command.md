# Rosen (1978) — Feedforwards and Command Relations

**Citation:** Rosen, R. (1978). *Fundamentals of Measurement and Representation of Natural Systems*. North-Holland, New York.
**Related:** The anticipatory systems theory was developed in this period, with the full treatment appearing in the 1985 book.
**Access:** Out of print. Difficult to find. The 1985 *Anticipatory Systems* book supersedes much of this material.

## Summary

This 1978 work develops Rosen's ideas on measurement, representation, and the formal structure of natural systems. It is the conceptual precursor to *Anticipatory Systems* (1985).

The specific concepts of "feedforward" and "command relations" appear here and are developed further in the 1985 book.

## Feedforward as a Control Concept

Rosen distinguishes two fundamentally different control architectures:

### Feedback Control
- Error-driven
- Corrective
- Reactive (responds after deviation)
- Requires continuous sensing of actual state
- Classic example: thermostat

### Feedforward Control
- Model-driven
- Preventive
- Anticipatory (acts before deviation)
- Requires a predictive model, not just state sensing
- Example: organism preparing for winter before cold arrives

### Command Relations

A "command" in Rosen's framework is a signal that changes the state of a system based on model predictions rather than current errors. Command relations describe how model outputs couple to system actuators.

The distinction matters because:
- In feedback, the controller is *subordinate* to the environment (it reacts)
- In feedforward, the controller *leads* the environment (it anticipates)

## Relevance to Agent Architectures

The command relation concept maps directly to how agents translate predictions into actions:

1. **Reactive agent:** observe -> act (feedback loop)
2. **Anticipatory agent:** model -> predict -> command -> act -> observe -> update model

The "command" step is where anticipation becomes control. Without it, the agent has a world model but no way to act on predictions. This is the difference between a predictor and an agent.

Current AI agents often have both:
- Feedback loops (error correction, RLHF)
- Feedforward paths (planning, chain-of-thought reasoning about consequences)

The design challenge is getting the balance right. Too much feedback = reactive sluggishness. Too much feedforward = acting on wrong models without correction.
