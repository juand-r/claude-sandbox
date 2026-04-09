# Reliable Systems from Unreliable Components

Building systems with reliability guarantees out of components that individually fail —
with a focus on LLMs as a concrete example of an unreliable component.

## Scope

- Theory: redundancy, voting, error-correcting codes, reliability math
- Von Neumann's foundational work on reliable organisms from unreliable components
- Practical software patterns: retries, circuit breakers, bulkheads, hedged requests
- Distributed systems: consensus, replication, quorums
- Application to LLMs: how to build dependable systems on top of stochastic models
- Simulation: demonstrate these principles in code

## How to run

```bash
cd explorations/reliable-from-unreliable
python <script>.py
```
