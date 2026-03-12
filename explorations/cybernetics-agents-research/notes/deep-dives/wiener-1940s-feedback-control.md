# Wiener's Work on Feedback and Control (1940s-1950s)

## The Anti-Aircraft Predictor (1940-1943)

### Origin

In early November 1940, Wiener suggested to servo-engineers at MIT that networks
with frequency responses of a certain kind, into which positional data of an
airplane's flight trajectory is fed, might predict future locations and assist
anti-aircraft fire. This was of tremendous military importance due to German
air superiority over England.

### The Key Insight: Gunner-Pilot Feedback Loop

When tracking a flying aircraft you observe to predict its future position.
But Wiener realized: in war, the *gunner's actions* must be part of the
prediction too. The pilot changes course in response to enemy fire; the gunner
adjusts in turn. This creates a cycle of adjustments and re-adjustments —
a feedback loop involving two agents.

This is arguably the first formalization of a **multi-agent feedback system**
where both agents are modeled as stochastic processes.

### From Predictor to Cybernetics

Peter Galison documented how Wiener gradually came to see the predictor "not
only as a model of the mind of an inaccessible Axis opponent but of the vast
array of human proprioceptive and electrophysiological feedback systems."

The anti-aircraft predictor was the concrete engineering problem that led Wiener
to the general theory of cybernetics.

---

## The Fire Control Report (1942, classified)

This is the precursor to the "Yellow Peril." The classified report detailed:
- Statistical prediction of aircraft trajectories from noisy radar data
- Optimal linear filtering theory
- The connection between communication engineering and control

(See wiener-1949-yellow-peril.md for the declassified version)

---

## Key Concepts in Wiener's Control Theory

### Negative Feedback

Central claim from Rosenblueth-Wiener-Bigelow (1943): "all purposeful behavior
may be considered to require negative feedback." The output is compared to the
desired state; the difference (error) drives corrective action.

### Servomechanisms as Information Processors

Wiener's radical move: he severed control from its origins in power engineering
and brought it into communication theory. A servo is not fundamentally about
force — it is about information flow. The controller receives information
(sensor data), processes it (computation), and transmits it (actuator commands).

### Control as Communication

The wide applicability of self-correcting systems was not lost on Wiener, who
was more drawn to the underlying theory than military applications. He grew
convinced that the study of complexity should focus not on traditional physics
concepts (mass, energy) but on concepts like **feedback** and **information
processing**.

### Stability and Oscillation

Wiener understood that feedback systems can be unstable — positive feedback
or delayed negative feedback leads to oscillation or divergence. This maps
directly to:
- Purpose tremor in neurological disorders (from the 1943 paper)
- Hunting in servomechanisms
- Instability in control systems (Nyquist, Bode criteria)

---

## The Macy Conferences (1946-1953)

Wiener was a central participant in the Macy Conferences on cybernetics, held
in New York City and Princeton. These conferences brought together:
- Mathematicians (Wiener, von Neumann)
- Neurophysiologists (McCulloch, Pitts, Rosenblueth)
- Anthropologists (Bateson, Mead)
- Psychologists and psychiatrists
- Engineers

The conferences were crucial for cross-pollinating feedback/control ideas
across disciplines.

---

## Post-War Ethical Stance on Control Technology

After the war, Wiener refused to participate in military research. He was
very concerned about mechanizing the military and openly urged other scientists
to refuse as well. This was deeply unpopular during the Cold War.

---

## Relevance to AI Agent Architectures

- **The agent-environment feedback loop** is directly descended from Wiener's
  servo-mechanism model
- **Multi-agent adversarial dynamics** — the gunner-pilot model is the
  ancestor of game-theoretic multi-agent RL
- **Information-theoretic view of control** — Wiener showed control IS
  communication, which maps to modern information-theoretic approaches
  to control (e.g., rate-distortion theory for control)
- **Stability analysis** — essential for any agent that uses feedback
  (prevents reward hacking via oscillation, ensures convergence)
