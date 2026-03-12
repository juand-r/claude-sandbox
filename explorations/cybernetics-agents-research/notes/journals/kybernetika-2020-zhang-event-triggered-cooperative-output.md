# Event-Triggered Output Consensus for Linear Multi-Agent Systems via Adaptive Distributed Observer

**Authors:** Limin Zhang, Jian Sun, Qingkai Yang
**Journal:** Kybernetika, Vol. 56, No. 2, pp. 217-238, 2020
**DOI:** 10.14736/kyb-2020-2-0217
**URL:** https://www.kybernetika.cz/content/2020/2/217
**Keywords:** output regulation, event-triggered communication, cooperative control, multi-agent systems

## Summary

Addresses distributed event-triggered cooperative output regulation for heterogeneous linear
continuous-time multi-agent systems. Develops an event-triggered adaptive distributed observer
to reduce continuous communication requirements. Uses closed-loop estimators on each agent to
decrease triggering frequency while maintaining control performance.

## Key Contributions

1. Event-triggered adaptive distributed observer for cooperative output regulation
2. Closed-loop estimators that reduce triggering frequency (vs. open-loop alternatives)
3. Elimination of Zeno behavior (infinite triggering in finite time)
4. Handles heterogeneous agents (not all identical)

## Architecture

- Each agent has a local observer that estimates the exosystem state
- Event-triggered communication: agents only transmit when certain thresholds are exceeded
- Closed-loop estimators improve accuracy during inter-event intervals

## Relevance to Cybernetics-Agents Research

- **Cooperative regulation:** Multiple heterogeneous agents achieving coordinated output --
  this is Ashby's law of requisite variety applied to multi-agent settings
- **Adaptive observation:** Agents adapt their internal models of the environment (exosystem)
  in a distributed fashion -- a cybernetic feedback principle
- **Communication efficiency:** Event-triggered communication is a form of efficient
  information transmission -- agents only communicate when necessary
- **Output regulation = goal-directed behavior:** The agents collectively track/reject
  signals from an exosystem, a fundamental cybernetic regulation task
- **Zeno-free:** Practical guarantee that the system doesn't enter pathological states

## Connection to Other Papers in This Collection

Complements the Peng et al. 2023 paper on event-triggered optimal control (nonlinear, unknown)
and the Tu & Liang 2024 paper on distributed optimization. Together they show a spectrum
of modern cybernetic control: from cooperative linear regulation (this paper) to nonlinear
adaptive control to constrained optimization.

## Access Status

Full text accessible (open access).
