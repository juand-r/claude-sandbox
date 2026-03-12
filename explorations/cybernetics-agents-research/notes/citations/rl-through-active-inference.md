# Reinforcement Learning through Active Inference

**Citation:** Tschantz, A., Millidge, B., Seth, A.K., & Buckley, C.L. (2020). "Reinforcement Learning through Active Inference." arXiv:2002.12636. University of Sussex.

**Cited in our notes:** friston-fep-active-inference.md (Section 6.5), control-theory-rl-bridge.md

**Date:** 2026-03-12

---

## Key Findings

### Core Contribution
Demonstrates how active inference concepts can enhance RL by introducing the "free energy of the expected future" as an objective function. Shows this objective naturally provides exploration-exploitation balance and works robustly across sparse, well-shaped, and absent reward structures.

### The Free Energy of the Expected Future
The key objective decomposes into:
- **Expected information gain** (exploration term) — drives the agent to seek observations that resolve uncertainty about hidden states
- **Extrinsic value** (exploitation term) — drives the agent toward preferred outcomes

This decomposition unifies exploration and exploitation under a single objective, eliminating the need for separate exploration mechanisms (epsilon-greedy, UCB, etc.).

### Formal Connections Established
The paper proves that the free energy of the expected future provides a **tractable bound** on established probabilistic RL objectives:
- Minimizing KL-divergence between expected and preferred observation distributions
- Connects to KL-control (Rawlik 2013)
- Connects to control-as-inference (Levine 2018)
- Connects to planning-as-inference (Botvinick & Toussaint 2012)

These connections show that active inference and RL are not competing frameworks but different perspectives on the same underlying mathematics.

### Experimental Results
Robust performance across reward structures:
- Sparse rewards: comparable to model-based RL baselines
- Shaped rewards: competitive performance
- **No rewards:** The agent still explores meaningfully, unlike standard RL which becomes inactive

---

## Relevance to Cybernetics-Agents Bridge

### Unifying Three Traditions
This paper sits at the intersection of three intellectual traditions:
1. **Cybernetics** (via active inference / FEP): homeostasis, good regulator theorem, requisite variety
2. **Control theory** (via control-as-inference): optimal control, stability, feedback loops
3. **Reinforcement learning** (via KL-control): reward maximization, exploration, policy learning

The formal connections established here mean that insights from any one tradition can be translated into the others. This is the mathematical bridge our research needs.

### Exploration as Cybernetic Necessity
The information-gain exploration term is the formal counterpart of a cybernetic insight: an agent that does not explore will eventually encounter disturbances it has no variety to handle. Epistemic action (information-seeking) is variety *maintenance* — keeping the agent's model up-to-date so its regulatory capacity remains adequate.

For LLM agents, the analogue is: agents should actively seek information about aspects of the task they are uncertain about, rather than proceeding with best guesses. ReAct's search actions serve this function informally; active inference provides the formal justification.

### The Reward-Free Result
The finding that active inference agents behave meaningfully without rewards connects to a deep cybernetic point: homeostatic regulation does not require external reward. A system that minimizes surprise (stays in expected states) automatically exhibits purposive-seeming behavior. Wiener, Rosenblueth & Bigelow (1943) made this point: purpose is a property of feedback structure, not of reward signals.

For LLM agent design, this suggests that well-designed feedback loops may be more important than well-designed reward functions. An agent with a robust feedback architecture can regulate effectively even with minimal reward specification.

---

## Most Important Cited References

1. **Friston et al. (2015, 2016, 2017a)** — Foundational active inference papers
2. **Levine (2018)** — "Reinforcement Learning and Control as Probabilistic Inference" (the RL-inference bridge)
3. **Kappen et al. (2012)** — KL-control framework
4. **Chua et al. (2018)** — PETS: model-based deep RL with probabilistic ensembles
5. **Rawlik (2013)** — KL-control and information-theoretic decision making
6. **Botvinick & Toussaint (2012)** — Planning as inference
