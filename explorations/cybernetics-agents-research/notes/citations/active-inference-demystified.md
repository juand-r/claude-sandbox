# Active Inference: Demystified and Compared

**Citation:** Sajid, N., Ball, P.J., Parr, T., & Friston, K.J. (2021). "Active Inference: Demystified and Compared." *Neural Computation*, 33(3), 674-712. arXiv:1909.10863. University College London.

**Cited in our notes:** friston-fep-active-inference.md, control-theory-rl-bridge.md

**Date:** 2026-03-12

---

## Key Findings

### Core Comparison: Active Inference vs. RL

**Fundamental difference:**
- RL: Maximizes expected cumulative reward
- Active inference: Minimizes expected free energy

**What active inference adds over RL:**

1. **No explicit reward required.** Active inference agents generate meaningful behavior (structured exploration) even without reward signals, through information-seeking (epistemic value). Standard RL becomes inactive without rewards.

2. **Natural exploration-exploitation balance.** The expected free energy decomposes into epistemic value (exploration) + pragmatic value (exploitation). No need for epsilon-greedy, UCB, or other bolted-on exploration mechanisms. The balance emerges from the objective function itself.

3. **Preference learning.** Active inference agents can learn their own outcome preferences from interaction — treating reward as "just another observation we have a preference over" rather than an environmental signal.

4. **Belief-space operation.** Active inference operates in belief space (distributions over states), naturally handling uncertainty. Standard RL often operates directly on states.

### Formal Connections
- Expected free energy provides a tractable bound on established probabilistic RL objectives
- The KL-divergence between expected and preferred observations connects to KL-control
- Active inference relates to control-as-inference (Levine 2018) and planning-as-inference frameworks

### Experimental Comparison (FrozenLake)
- **Stationary environments:** All methods (active inference, Q-learning, Bayesian RL) achieve >80% success
- **Non-stationary environments:** Active inference recovers from goal-location switches within 1-2 episodes; Bayesian RL requires ~40 episodes
- **Reward-free learning:** Active inference agents explore meaningfully; Q-learning becomes inactive

### Self-Evidencing Behavior
A striking finding: active inference agents exhibit "self-evidencing" — they observe their own actions and infer preferences consistent with observed patterns. An agent that finds itself repeatedly in holes learns to *prefer* holes. This appears reward-minimizing from an RL perspective but is Bayes-optimal under learned preferences.

---

## Relevance to Cybernetics-Agents Bridge

### The Most Direct Bridge
This paper is arguably the most direct formal bridge between cybernetics and modern agent design. Active inference:
- Formalizes **homeostasis** (minimizing surprise = staying in expected states)
- Instantiates the **Good Regulator Theorem** (agent must be a model of its environment)
- Satisfies **requisite variety** (generative model must match environmental complexity)
- Unifies **perception and action** under one objective (Wiener's original insight that sensing and acting are coupled)

### Feedback Loop Structure
Active inference implements a complete cybernetic feedback loop:
- **Sensor:** Observations from environment
- **Comparator:** Free energy computation (difference between predicted and actual observations)
- **Controller:** Policy selection (minimize expected free energy)
- **Effector:** Actions that change future observations
- **Reference signal:** Prior preferences (encoded as preferred observations in the generative model)

Unlike LLM-based agents where feedback is ad hoc (sometimes present, sometimes absent), active inference makes the feedback loop **constitutive** — it IS the agent.

### Multi-Timescale Control
The paper identifies two timescales:
- **Fast:** State estimation under each policy (perception)
- **Slow:** Parameter learning and preference updating (learning)

This maps to hierarchical control with inner and outer loops — a fundamental pattern in control engineering that LLM agents currently lack. LLM agents operate at a single timescale (the prompt-response cycle), which limits their adaptive capacity.

### The Self-Evidencing Problem
The self-evidencing phenomenon (learning to prefer holes) highlights a risk for any Bayesian agent: the agent may converge to a stable but pathological policy by adapting its preferences to match its behavior rather than adapting its behavior to match desired outcomes. This is a form of **eigenform instability** (Von Foerster) — convergence to the wrong fixed point.

For LLM agents, this maps to: an agent that repeatedly fails at a task may "learn" (through accumulated context) that failure is the expected outcome and stop trying. This is the cybernetic equivalent of learned helplessness.

---

## Most Important Cited References

1. **Friston et al. (2017a, 2017b)** — Foundational active inference formulations
2. **Friston et al. (2014)** — Expected free energy derivation
3. **Sutton & Barto (2018)** — RL framework (comparison target)
4. **Parr & Friston (2017, 2019)** — Epistemic exploration and generalised free energy
5. **Botvinick & Toussaint (2012)** — Planning as inference connections
6. **Levine (2018)** — Control as inference (RL perspective)
