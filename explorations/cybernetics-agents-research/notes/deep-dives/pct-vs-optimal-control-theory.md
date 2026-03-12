# PCT vs. Optimal Control Theory — Comparison

## Key References
- Powers, W.T. (1973/2005). *Behavior: The Control of Perception*.
- Todorov, E. & Jordan, M.I. (2002). Optimal feedback control as a theory of motor coordination. *Nature Neuroscience*, 5, 1226-1235.
- Scott, S.H. (2012). The computational and neural basis of voluntary motor control and planning. *Trends in Cognitive Sciences*, 16(11), 541-549.
- Kennaway, R. (2025). Perceptual control theory and the free energy principle: A comparison. *Current Opinion in Behavioral Sciences*.
- Anonymous (2025). PCT vs. FEP: A comparison between reorganization theory and Bayesian inference. *MDPI*.

## The Core Distinction

### Optimal Control Theory (OCT)
**Core question:** What is the best action to take given the current state?

The system:
1. Has a **cost function** (externally defined)
2. Has a **forward model** of system dynamics
3. **Optimizes** actions to minimize cost over a time horizon
4. Computes the **optimal policy** — the best mapping from states to actions

### Perceptual Control Theory (PCT)
**Core question:** What perception should be maintained?

The system:
1. Has a **reference signal** (internally generated)
2. Has **no forward model** — only sensory feedback
3. **Controls** perceptions by varying outputs to reduce error
4. Has **no concept of optimal action** — any action that reduces error is adequate

## Detailed Comparison

| Dimension | OCT | PCT |
|-----------|-----|-----|
| **What is specified** | Cost function (what to minimize) | Reference signal (what to perceive) |
| **Who specifies it** | External (designer, experimenter) | Internal (higher-level control system) |
| **Internal model** | Required (forward model of dynamics) | Not required |
| **Computation** | Heavy (optimization, matrix operations, trajectory planning) | Light (subtraction + integration per loop) |
| **Optimality** | Central concept — finds the BEST action | No concept of optimality — any error-reducing action works |
| **Disturbance handling** | Must be modeled or estimated | Inherent — the loop rejects disturbances automatically |
| **Hierarchy** | Optional (can be flat or hierarchical) | Essential (the hierarchy IS the theory) |
| **What is controlled** | Outputs (actions, trajectories) | Inputs (perceptions) |
| **Causation model** | Often feedforward or model-predictive | Always closed-loop (circular causation) |
| **Failure mode** | Brittle when model is wrong | Degrades gracefully — continues controlling even with imperfect parameters |

## The Computational Argument

### OCT Computational Cost
To control a robot arm (6 DOF):
1. Forward dynamics model: ~$O(n^3)$ per timestep (Featherstone's algorithm)
2. Inverse kinematics: ~$O(n^3)$ per solution
3. Trajectory optimization: iterates forward model many times
4. Total: thousands of floating-point operations per control update

### PCT Computational Cost
Same robot arm:
1. Perceive current joint angles: 6 subtractions (one per joint)
2. Compare to reference: 6 subtractions
3. Compute output: 6 integrations
4. Total: ~18 operations per control update

PCT is orders of magnitude cheaper. This matters for real-time control and for scaling to large hierarchies.

## The Inverted Pendulum Test Case

Young et al. (2020) directly compared PCT and LQR (a form of optimal control) for a two-wheeled balancing robot:

| Metric | LQR | PCT |
|--------|-----|-----|
| Balance performance | Good | Comparable |
| Disturbance rejection | Good | **Superior** |
| Architecture complexity | State-space model + Riccati equation | 5 simple control loops |
| Model requirements | Full system dynamics model | None |
| Tuning | Requires careful Q/R matrix tuning | Gains set by simple rules |

The PCT controller matched or exceeded LQR performance with a drastically simpler architecture.

## PCT vs. Free Energy Principle (FEP) / Active Inference

### Structural Similarities
Both PCT and FEP:
- Treat organisms as systems that minimize a form of error
- Use hierarchical architectures
- Emphasize that action serves perception
- Reject stimulus-response models

### Key Differences
| Dimension | PCT | FEP/Active Inference |
|-----------|-----|---------------------|
| **Internal model** | Rejected — no generative model | Central — requires a generative model |
| **Learning mechanism** | Reorganization (random walk driven by intrinsic error) | Bayesian inference (belief updating) |
| **Mathematical framework** | Control theory (differential equations) | Variational Bayesian inference (free energy minimization) |
| **Prediction** | Not a central concept — the system corrects errors, doesn't predict | Central concept — the system predicts and acts to confirm predictions |
| **Formal generality** | Narrower formal framework | Broader — can be shown to subsume PCT |

### The Category Theory Result (2025)
A 2025 paper using category-theoretic tools argued that **PCT can be formally understood as a subset of the FEP framework**. This means:
- Everything PCT describes can be described in FEP terms
- FEP describes additional phenomena (model learning, prediction, Bayesian updating) that PCT does not formalize
- However, PCT's greater conceptual clarity may be an advantage for practical applications

## Relevance to Agent Architectures

### OCT-style Agents (Most Current LLM Agents)
- Plan an optimal sequence of actions (chain of thought, tool calls)
- Require a model of the environment (context window, knowledge)
- Optimize for a cost function (RLHF reward, loss function)
- Brittle when the model is wrong (hallucination, tool failures)

### PCT-style Agents (Hypothetical)
- Control perceptual variables (e.g., perceived task completion, perceived helpfulness)
- No explicit environment model needed
- Continuously reduce error between perception and reference
- Robust to disturbances (unexpected inputs, tool failures) because the feedback loop compensates

### The Hybrid Possibility
The FEP result suggests a possible hybrid: use PCT's simple control loops for real-time disturbance rejection and FEP's generative models for learning and prediction. The control loops provide robustness; the models provide adaptability.

This maps to an agent architecture where:
- **Fast inner loop (PCT):** Continuously controls perception in real-time. Simple, cheap, robust.
- **Slow outer loop (FEP/Bayesian):** Updates the models and reference signals based on accumulated experience. Complex, expensive, but runs infrequently.

This is structurally similar to Ashby's ultrastability and Powers' reorganization — the fast loop handles disturbances, the slow loop restructures the fast loop when it fails.
