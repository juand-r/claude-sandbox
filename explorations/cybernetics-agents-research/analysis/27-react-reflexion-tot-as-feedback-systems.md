# ReAct, Reflexion, and Tree of Thoughts as Cybernetic Feedback Systems

**Stream G, Item 27**
**Date:** 2026-03-12

---

## Purpose

This analysis treats three prominent LLM agent patterns — ReAct, Reflexion, and Tree of Thoughts — as feedback control systems and asks: what does the control-theoretic framing actually buy us? Not metaphor, but specifics: controlled variables, gain, delay, stability conditions, failure modes.

The honest answer, previewed: the framing is genuinely illuminating for some failure modes (ReAct loops as limit cycles, Reflexion error reinforcement as positive feedback) and merely relabeling for others. The main value is not the analogy itself but the engineering questions the framing forces you to ask — questions the agent community has mostly not asked.

---

## 1. The Three Patterns as Feedback Loops

### 1.1 ReAct (Yao et al., 2022)

**Architecture:** Thought → Action → Observation → Thought → ... The agent interleaves reasoning traces with environment interactions. Each observation feeds back into the next thought step.

| Control Element | ReAct Instantiation |
|----------------|---------------------|
| **Controlled variable** | Task progress — the distance between current state and goal completion |
| **Reference signal** | The task specification (question to answer, goal to achieve) |
| **Feedback signal** | The observation returned by the environment after each action (search results, tool outputs, error messages) |
| **Comparator** | The "Thought" step — the LLM reasons about the gap between what it has observed and what the task requires |
| **Effector** | The "Action" step — the next tool invocation or environment interaction |
| **Error signal** | Implicit in the thought: "I need X but have Y, so I should do Z" |
| **Gain** | How aggressively the agent changes strategy in response to an observation. This is **uncontrolled** — it depends entirely on the LLM's in-context reasoning. There is no gain parameter. The same model might overreact to a misleading search result (high gain) or ignore a critical error message (low gain), depending on prompt and context. |
| **Delay** | One full Thought-Action-Observation cycle per feedback iteration. In wall-clock time: 1-10 seconds per loop (LLM inference + tool execution). In information-theoretic terms: the agent receives feedback only after committing to an action, with no preview or simulation. |
| **Loop order** | **First-order.** Single feedback loop: act, observe, adjust. No meta-loop modifying how the loop itself operates. |

**Stability analysis:**

The loop converges when: (a) each observation provides information that reduces the error signal, (b) the agent's response to that information moves closer to the goal, and (c) the process terminates in finite steps.

The loop diverges when: (a) observations are uninformative or misleading (the feedback signal has low signal-to-noise ratio), (b) the agent's actions do not reduce error (the effector is poorly coupled to the controlled variable), or (c) the agent oscillates between two strategies without progress.

There is no built-in damping. The agent has no mechanism to reduce the magnitude of its corrections over time. In a well-tuned PID controller, the derivative term prevents overshoot. ReAct has no analog — the LLM may radically shift strategy on every iteration, or it may rigidly repeat the same action. Both failure modes are common.

---

### 1.2 Reflexion (Shinn et al., 2023)

**Architecture:** Two nested loops. The inner loop is a standard agent execution (which could be ReAct). The outer loop evaluates the inner loop's trajectory, generates a verbal self-reflection, stores it in memory, and re-executes with the reflection available. Formally: execute → evaluate → reflect → store → re-execute.

| Control Element | Reflexion Instantiation |
|----------------|------------------------|
| **Controlled variable** | Task performance quality (measured by an evaluator: binary success/failure, or a scalar reward) |
| **Reference signal** | Perfect task completion (evaluator returns success / maximum reward) |
| **Feedback signal** | The evaluator's judgment of the trajectory + the self-generated verbal reflection |
| **Comparator** | The evaluator function (which may be heuristic, LLM-based, or external). Computes: did the trajectory succeed? |
| **Effector** | The self-reflection model, which produces a diagnosis ("I failed because X, next time I should Y") that modifies the agent's behavior on the next trial |
| **Error signal** | The evaluator's negative judgment + the reflection's causal attribution |
| **Gain** | How much the reflection changes subsequent behavior. This depends on (a) the specificity of the reflection, (b) how prominently the reflection appears in the re-execution prompt, and (c) whether the LLM actually follows its own advice. Empirically, gain is high on early iterations and decreases as the reflection memory grows (dilution in context). |
| **Delay** | One full task execution per outer-loop iteration. This is a **long-delay** feedback loop — the agent must complete an entire attempt before receiving feedback. Delay is measured in minutes, not seconds. |
| **Loop order** | **Second-order.** The outer loop modifies the parameters of the inner loop (by changing the context/memory). This is feedback on feedback — the system observes its own performance trajectory and adjusts its strategy, not just its next action. |

**Stability analysis:**

Convergence requires: (a) the evaluator correctly identifies failures, (b) the reflection correctly diagnoses the cause, (c) the diagnosed cause, once addressed, actually fixes the problem, and (d) reflections do not accumulate contradictory advice.

Each of these is a non-trivial assumption. Huang et al. (2023) showed that LLMs cannot reliably self-correct reasoning without external feedback — which means condition (b) fails systematically when the evaluator is the same LLM. The reflection may diagnose the wrong cause, leading to a "fix" that introduces new errors.

The outer loop has no guaranteed convergence. There is no Lyapunov function decreasing along trajectories. The system can oscillate: reflection says "be more careful," next attempt is too conservative, reflection says "be more aggressive," next attempt overshoots, ad infinitum.

---

### 1.3 Tree of Thoughts (Yao et al., 2023)

**Architecture:** The agent generates multiple candidate "thoughts" (partial solutions) at each step, evaluates them, and selects the most promising for further expansion. Search strategies include BFS and DFS with backtracking. The tree structure allows exploring multiple paths and pruning unpromising branches.

| Control Element | ToT Instantiation |
|----------------|-------------------|
| **Controlled variable** | Solution quality at each node — how promising is this partial solution? |
| **Reference signal** | A correct/optimal complete solution (implicitly defined by the evaluation function) |
| **Feedback signal** | The evaluation of each candidate thought (heuristic value, LLM-judged quality, or external verification) |
| **Comparator** | The evaluation/voting function that scores candidate thoughts |
| **Effector** | The search algorithm (BFS/DFS) that selects which nodes to expand and which to prune |
| **Error signal** | Low evaluation score → prune this branch; high score → expand further |
| **Gain** | Determined by the **branching factor** (how many candidates per step) and the **pruning threshold** (how aggressively low-scoring candidates are eliminated). High branching + low pruning = low gain (explore everything). Low branching + high pruning = high gain (commit quickly). |
| **Delay** | Effectively **zero** within the evaluation loop — the agent evaluates before committing. But there is delay between tree construction and final answer: the entire tree must be built/explored before a solution is returned. |
| **Loop order** | **First-order with lookahead.** The evaluation at each node is single-loop feedback. But the tree structure provides a form of **predictive control** — the agent simulates multiple futures before committing. This is closer to Model Predictive Control (MPC) than to simple feedback. |

**Stability analysis:**

ToT is more naturally analyzed as a search problem than a feedback system. The "controlled variable" framing is somewhat forced here (see Section 6 for honest assessment).

That said: convergence depends on the evaluation function's accuracy. If the evaluator correctly identifies promising partial solutions, the tree converges toward a solution. If the evaluator is miscalibrated — systematically overvaluing certain paths — the search converges to a local optimum (premature convergence / overdamped response). If the evaluator cannot discriminate between candidates, the tree expands without pruning (combinatorial explosion / underdamped response).

The branching factor acts as an inverse damping coefficient: higher branching = less damped = more exploration but higher cost. The pruning threshold acts as a gain: aggressive pruning = high gain = fast convergence but risk of pruning the correct path.

---

## 2. Comparative Feedback Architecture

### 2.1 Loop Structure Comparison

| Property | ReAct | Reflexion | ToT |
|----------|-------|-----------|-----|
| **Loop order** | First-order | Second-order | First-order with lookahead |
| **Feedback delay** | Short (1 action cycle) | Long (1 full execution) | Near-zero (evaluate before commit) |
| **Gain control** | None (uncontrolled, LLM-dependent) | Indirect (via reflection specificity and memory prominence) | Explicit (branching factor, pruning threshold) |
| **Damping** | None built-in | Reflection memory provides some damping (past failures constrain future behavior) | Pruning provides damping |
| **State memory** | Context window only (finite, unstructured) | Explicit reflection memory (structured, persistent across trials) | Tree structure (explicit, complete history of explored paths) |
| **Environment coupling** | Tight (every action touches environment) | Loose (environment contacted only during inner-loop execution) | Minimal (evaluation may be purely internal) |
| **Closest control analog** | Bang-bang controller (full action, observe, full correction) | Iterative Learning Control (ILC) — repeat a task, learn from the trajectory | Model Predictive Control (MPC) — simulate multiple futures, select best |

### 2.2 Feedback Order and What It Means

**ReAct is first-order feedback.** It adjusts actions based on observations. It cannot adjust *how* it adjusts. If the agent's reasoning strategy is flawed, no amount of ReAct iteration will fix it — the same flawed strategy will be applied to each new observation. This is Bateson's Learning I: correction within a fixed framework.

**Reflexion is second-order feedback.** The outer loop adjusts the inner loop's behavior by modifying its context (reflection memory). This is feedback on the feedback process itself. In control theory terms, Reflexion is an adaptive controller — one that modifies its own gain and strategy based on performance history. But it is a very crude adaptive controller: the adaptation mechanism (verbal reflection) has no formal relationship to the system dynamics. A proper adaptive controller adjusts parameters that appear in a model of the plant; Reflexion adjusts natural-language advice in a prompt.

**ToT is first-order with lookahead.** It does not adjust its own strategy — the search algorithm is fixed. But the lookahead (evaluating multiple candidates before committing) provides a form of predictive control that the other two lack. The tradeoff: ToT spends computation on breadth (exploring alternatives) rather than depth (iterating on feedback). This is fundamentally different from the feedback paradigm — it is closer to open-loop planning with evaluation than to closed-loop control.

### 2.3 Damping Characteristics

In control theory, damping determines how quickly oscillations decay. The three patterns have qualitatively different damping profiles:

**ReAct: Undamped.** There is no mechanism to reduce oscillation magnitude over time. If the agent alternates between two strategies (search vs. compute, for example), nothing in the architecture reduces the amplitude of this oscillation. The only "damping" is incidental: the context window fills up, previous observations become less prominent, and the agent may settle into one strategy simply because the other has scrolled out of context. This is not damping — it is information loss masquerading as stability.

**Reflexion: Overdamped tendency.** As reflections accumulate, they increasingly constrain the agent's behavior. Each reflection adds a "don't do X" or "try Y instead" that narrows the action space. After many iterations, the agent is heavily constrained by accumulated advice, some of which may be contradictory or wrong. The system becomes sluggish — unable to try novel approaches because past reflections have foreclosed them. This is the adaptive-controller pathology of parameter drift: the adaptation mechanism itself drifts from relevance.

**ToT: Configurable damping.** The branching factor and pruning threshold are explicit damping parameters. Low branching + aggressive pruning = overdamped (converges fast but may miss correct paths). High branching + gentle pruning = underdamped (explores broadly but may never converge). This is ToT's advantage as a feedback architecture: the damping is a design parameter, not an emergent artifact.

---

## 3. Failure Modes Through the Control Theory Lens

### 3.1 ReAct Infinite Loops as Limit Cycles

**The phenomenon:** ReAct agents sometimes enter infinite loops — repeating the same sequence of actions indefinitely. This is widely documented and is the primary failure mode of ReAct-style agents.

**Control theory interpretation:** A limit cycle is a closed trajectory in state space that the system orbits without converging to a fixed point. It occurs in nonlinear systems when the feedback gain and delay combine to sustain oscillations.

For ReAct, a limit cycle occurs when:

1. Action A produces observation O₁
2. O₁ triggers the agent to try action B
3. Action B produces observation O₂
4. O₂ triggers the agent to try action A again
5. Repeat

In control terms: the open-loop gain around the cycle is exactly 1. The agent's response to O₁ always produces O₂, and vice versa. The system has a pair of fixed points in the observation-action mapping, and the feedback loop oscillates between them.

**Why this happens in ReAct specifically:** ReAct has no mechanism to detect that it is repeating. The "Thought" step should in principle notice the repetition, but in practice the LLM often does not — especially when the repeating actions are slightly different in wording but identical in effect. The absence of explicit state tracking (the agent does not maintain a set of "actions already tried") means the feedback signal does not encode cycle history.

**Control-theoretic fix:** A limit-cycle detector — track the state trajectory and detect when the system returns to a previously visited state. In control engineering, this is standard: anti-windup mechanisms prevent integrators from saturating and producing oscillations. The agent equivalent: maintain a memory of previous action-observation pairs and inject a "you have already tried this" signal when a cycle is detected. Some ReAct implementations do this ad hoc; none do it with formal analysis of which states constitute "already visited."

**Assessment: TIGHT mapping.** The limit cycle interpretation is genuinely correct — these are sustained oscillations in a nonlinear feedback system with unit loop gain. The control theory framing identifies the fix (cycle detection / anti-windup) that the agent community has arrived at empirically. The framing adds value by explaining *why* the fix works: it reduces the loop gain below 1 for repeated states.

### 3.2 Reflexion Self-Reinforcing Errors as Positive Feedback

**The phenomenon:** Reflexion sometimes makes performance worse across iterations. The agent reflects on a failure, generates an incorrect diagnosis, and the incorrect diagnosis causes a different failure on the next attempt. The new failure generates a new (also incorrect) reflection, and performance degrades steadily.

**Control theory interpretation:** This is positive feedback — the error signal is inverted. Instead of the reflection reducing the error, it amplifies it. In block-diagram terms: the sign of the feedback path has flipped from negative (corrective) to positive (reinforcing).

This happens because the reflection model and the execution model are the same LLM. When the LLM fails on a task, the failure is often caused by a systematic reasoning error. The same systematic error then corrupts the reflection: the LLM cannot correctly diagnose the failure because the diagnosis requires the same reasoning capability that failed. The reflection is not independent of the execution — it shares the same transfer function.

In control terms: the sensor (evaluator) and the controller (reflector) share the same noise characteristics as the plant (executor). The measurement noise is correlated with the process noise. This violates a fundamental assumption of feedback control: that the feedback signal is at least partially independent of the disturbance.

Huang et al. (2023) provide the empirical confirmation: "Large Language Models Cannot Self-Correct Reasoning Yet." When the feedback signal (self-evaluation) is generated by the same system that produced the error, the feedback is not informative — it is a noisy copy of the original signal, and its expected correction is zero or negative.

**When Reflexion works:** When the evaluator is external (unit tests, ground-truth comparison, human judgment). External evaluation breaks the correlation between measurement noise and process noise. The feedback signal becomes genuinely informative, and negative feedback is restored. This is why Reflexion shows strong results on coding tasks (where unit tests provide external evaluation) and weak results on reasoning tasks (where self-evaluation is the only option).

**Control-theoretic prediction:** Reflexion's performance should be strictly bounded by the quality of its evaluator's independence from the executor. If we define:

- ρ = correlation between executor errors and evaluator errors
- When ρ = 0: evaluator is fully independent → classical negative feedback → convergence
- When ρ = 1: evaluator makes the same errors as executor → zero expected correction → random walk
- When ρ > 1 (evaluator systematically agrees with executor's errors): positive feedback → divergence

This predicts a phase transition: there is a critical ρ* below which Reflexion converges and above which it diverges. The value of ρ* depends on the gain (how aggressively reflections modify behavior). Higher gain lowers ρ* — more aggressive correction requires more independent evaluation.

**Assessment: TIGHT mapping.** This is the strongest control-theoretic insight in the entire analysis. The positive feedback interpretation is not just an analogy — it is the correct causal explanation for why self-correction fails. The correlation between evaluator and executor errors is a measurable quantity. The prediction (performance bounded by evaluator independence) is testable and actionable: use external evaluators, use different models for evaluation, or reduce gain when evaluator independence is low.

### 3.3 ToT Premature Convergence as Overdamped Response

**The phenomenon:** ToT sometimes converges too quickly to a suboptimal solution. The evaluation function rates one branch highly early on, the search commits to that branch, and the correct solution (on a different branch) is pruned.

**Control theory interpretation:** Overdamping. The damping ratio ζ > 1. The system converges monotonically but slowly, and if it starts moving toward the wrong fixed point, it converges there without oscillating toward the correct one. The excessive damping (aggressive pruning) prevents the exploration that would discover the better solution.

In ToT terms: the evaluation function's confidence is too high relative to its accuracy. It assigns definitive scores to partial solutions before there is enough information to discriminate. This is analogous to a controller with high gain and high damping: it responds quickly and decisively, but it responds to noise as if it were signal.

**Fix from control theory:** Reduce damping (widen the pruning threshold) in early stages when evaluation uncertainty is high. This is exactly the exploration-exploitation tradeoff: explore when uncertain, exploit when confident. In control terms: schedule the damping ratio — start underdamped (ζ < 1, explore broadly), then increase damping as confidence grows.

**Assessment: MODERATE.** The overdamped analogy captures the qualitative phenomenon but does not provide quantitative guidance. We cannot compute ζ for a ToT search because there is no transfer function. The "reduce damping when uncertain" prescription is correct but is the standard explore-exploit insight repackaged. The control theory framing adds a useful visualization (the damping ratio spectrum) but not a new algorithm.

### 3.4 ToT Combinatorial Explosion as Underdamped Response

**The phenomenon:** With high branching factor and weak pruning, ToT generates an enormous tree that exhausts compute budget without finding a solution.

**Control theory interpretation:** Underdamping. ζ < 1. The system oscillates widely, exploring the entire state space without settling. Each evaluation step barely constrains the next — the feedback signal is too weak to focus the search.

This is less interesting than the other failure modes because it is essentially "the search space is too large and the heuristic is too weak." The control theory framing adds the observation that this is the dual of premature convergence (underdamped vs. overdamped), which is correct but not particularly illuminating.

**Assessment: LOOSE.** Calling combinatorial explosion "underdamped response" is accurate in a broad sense but adds nothing to the standard analysis. The prescriptions are the same: better heuristics, adaptive branching, beam search. The control theory language does not generate new prescriptions.

---

## 4. Toward Formal Stability Analysis

### 4.1 What Would Be Needed

A rigorous control-theoretic stability analysis of these agent patterns would require:

1. **A state space definition.** What are the state variables? For ReAct: the agent's context (all previous thoughts, actions, observations). For Reflexion: the context + the reflection memory. For ToT: the tree structure + evaluation scores. The state spaces are enormous and continuous (they live in the LLM's embedding space), making classical stability tools intractable.

2. **A dynamics model.** How does the state evolve? This requires modeling the LLM as a dynamical system: given state s_t, what is the distribution over s_{t+1}? The LLM is a deterministic function of its input (at temperature 0) or a stochastic one (at temperature > 0), but characterizing this function analytically is infeasible — it is a black-box nonlinear map with billions of parameters.

3. **An equilibrium characterization.** What are the fixed points? For ReAct: states where the agent's thought is "I am done" and no further action is needed. For Reflexion: states where the evaluator returns success. For ToT: leaf nodes with maximum evaluation score. These are well-defined in principle but intractable to enumerate.

4. **A perturbation analysis.** How does the system respond to small perturbations around equilibrium? This requires linearizing the dynamics around the fixed point, which requires computing Jacobians of the LLM's input-output function. Not feasible with current tools.

### 4.2 Lyapunov Functions: What Would They Look Like?

A Lyapunov function V(s) for an agent loop must satisfy:
- V(s) > 0 for all s ≠ s* (the goal state)
- V(s*) = 0
- V(s_{t+1}) < V(s_t) along agent trajectories (strict decrease)

**ReAct candidate:** V(s) = "distance from current state to goal completion." Concretely: the number of unanswered sub-questions, or the fraction of the task remaining. If every ReAct iteration makes progress (answers a sub-question, retrieves needed information, completes a subtask), V decreases and the system is stable.

The problem: "distance to goal" is not a computable quantity. The agent does not know how far it is from completion. Worse, the distance is not monotonically decreasing — the agent may discover that the task is harder than expected (V increases), or it may take an incorrect action that undoes progress (V increases). A Lyapunov function that can increase is not a Lyapunov function.

A weaker candidate: V(s) = remaining token budget. This is monotonically decreasing (every step consumes tokens) and reaches 0 at termination. But this proves only that the system terminates, not that it converges to the correct answer. It is a trivial Lyapunov function — it guarantees boundedness but not correctness.

**Reflexion candidate:** V(s) = evaluator's error score (e.g., number of failed test cases). If Reflexion's reflections reliably fix at least one failing test case per iteration, V decreases strictly. This is a meaningful Lyapunov function — it would guarantee convergence in at most V(s_0) iterations.

The problem: the reflections do not reliably fix failing test cases. A reflection might fix one test and break another (V stays constant — not a strict decrease). Or it might break more tests than it fixes (V increases — Lyapunov condition violated). The Lyapunov analysis reveals exactly where the guarantee breaks: the reflection's effect on the error count is not monotonically improving.

**ToT candidate:** V(s) = -max(evaluation scores across leaf nodes). As the search progresses, the best evaluation score should increase (V decreases). This requires that the evaluation function is consistent — a higher-scoring partial solution leads to a higher-scoring complete solution — which is the "admissibility" condition from A* search.

This is the tightest mapping: ToT's convergence conditions are exactly the admissibility conditions from search theory, which are themselves a form of Lyapunov stability. If the evaluation function is admissible (never overestimates the cost to completion), the search converges to the optimal solution. This is a known result; the control theory framing simply identifies it as a Lyapunov stability condition, which it formally is.

### 4.3 Gain and Phase Margin Analogs

In classical control, gain margin is how much you can increase the loop gain before the system becomes unstable. Phase margin is how much additional phase lag (delay) the system can tolerate.

**Gain margin analog for ReAct:** How much can you increase the LLM's "responsiveness" to observations before the loop becomes unstable? In practice: how much weight does the agent give to the most recent observation vs. the accumulated context? If the agent overweights the latest observation (high gain), it will oscillate between strategies based on noisy observations. If it underweights observations (low gain), it will ignore useful feedback and persist with a failing strategy.

Measurable proxy: the cosine similarity between successive action embeddings as a function of observation informativeness. If actions change dramatically in response to uninformative observations, gain is too high. If actions do not change in response to highly informative observations, gain is too low. Nobody has measured this.

**Phase margin analog for Reflexion:** How many iterations of delay between a problem occurring and the reflection correctly diagnosing it? If the reflection diagnoses the problem from iteration N in iteration N+1, the delay is 1 (good). If the correct diagnosis requires multiple failed attempts to triangulate, the delay is K > 1 (worse). The phase margin is how many iterations the system can tolerate between problem and diagnosis before it diverges.

Measurable proxy: the number of Reflexion iterations between an error first occurring and the reflection that correctly identifies it. This could be measured empirically on tasks with known failure causes.

**Phase margin analog for ToT:** How many levels of lookahead are needed for the evaluation function to discriminate correct from incorrect paths? If the evaluation function can discriminate at depth 1, the phase margin is large (good). If discrimination requires depth K, the search must expand K levels before pruning, which is expensive. The phase margin determines the minimum tree depth for stable convergence.

### 4.4 Why Nobody Has Done This

The formal analysis described above is feasible in principle but faces practical obstacles:

1. **The LLM is a black box.** Computing Jacobians, transfer functions, or gain schedules requires differentiating through the LLM, which is computationally expensive and analytically intractable for the full model.

2. **The state space is too large.** The context window is a high-dimensional sequence space. Classical stability tools (Lyapunov, Bode plots, Nyquist criteria) are designed for low-dimensional systems. Extensions to high-dimensional systems exist (Lyapunov for neural ODEs, e.g., Berkenkamp et al., 2017) but have not been applied to LLM agent loops.

3. **The payoff is uncertain.** Even if you proved a ReAct loop was stable under certain conditions, the conditions might be too restrictive to be practically useful. The agent community has addressed stability empirically (add cycle detection, limit iterations, add human-in-the-loop) without needing formal guarantees.

4. **The community doing control theory and the community doing LLM agents have essentially zero overlap.** The tools exist. The problems exist. The people are in different buildings.

---

## 5. Comparative Summary

### 5.1 As Feedback Architectures

| Dimension | ReAct | Reflexion | ToT |
|-----------|-------|-----------|-----|
| **Feedback type** | Negative (corrective) — when working | Negative (outer loop) — when evaluator is independent | Evaluative (score-based pruning) |
| **Loop order** | First | Second | First + lookahead |
| **Control analog** | Bang-bang controller | Iterative Learning Control (ILC) | Model Predictive Control (MPC) |
| **Gain** | Uncontrolled | Indirect (reflection salience) | Explicit (branching/pruning) |
| **Damping** | None | Accumulating (overdamped tendency) | Configurable |
| **Primary instability** | Limit cycles (undamped oscillation) | Positive feedback (correlated errors) | Premature convergence (overdamped) or explosion (underdamped) |
| **Stability guarantee** | None | None (empirically degrades without external evaluator) | Conditional on evaluation function admissibility |
| **Environment coupling** | Every step | Only during inner-loop execution | Minimal (may be purely internal) |

### 5.2 When Each Architecture Is Appropriate (Control-Theoretic View)

**Use ReAct when:** The environment provides fast, reliable feedback (low delay, low noise). The controlled variable is directly observable. The task is short-horizon (few steps needed). Example: question-answering with search — each search result is fast, informative feedback.

**Use Reflexion when:** The evaluator is independent of the executor (external test suite, human judgment). The task permits multiple attempts. The failure modes are diagnosable from the trajectory. Example: code generation with unit tests — the tests provide independent evaluation.

**Use ToT when:** The evaluation function can discriminate partial solutions. The task has clear decomposition into subtasks. The cost of evaluation is low relative to the cost of wrong actions. Example: constrained planning problems (Game of 24, crosswords) where partial solutions are evaluable.

### 5.3 What Each Pattern Lacks (Control-Theoretic Diagnosis)

**ReAct lacks:** Damping, gain scheduling, cycle detection, any form of adaptation. It is the crudest possible feedback architecture — a thermostat, not a PID controller.

**Reflexion lacks:** Evaluator independence guarantees, gain control (reflections accumulate without bound), convergence guarantees, any mechanism to detect when reflections are harmful rather than helpful.

**ToT lacks:** Feedback from execution (it plans but does not act and learn from acting), adaptive search depth, any mechanism to update the evaluation function based on results. It is the most "open-loop" of the three — the search is guided by a static evaluation function that does not learn.

---

## 6. Honest Assessment: Where the Control Theory Framing Helps and Where It Is Just Relabeling

### 6.1 Genuinely Illuminating

**1. Reflexion's positive feedback failure.** The control theory framing identifies the precise mechanism: correlated errors between evaluator and executor cause the feedback sign to flip. This is not just an analogy — it is the correct causal explanation, and it generates a testable prediction (performance bounded by evaluator-executor independence, quantified by ρ). This insight is genuinely useful for designing agent systems: invest in evaluator independence, not in more sophisticated self-reflection prompts. Huang et al. (2023) confirm the prediction without using the control theory framing.

**2. ReAct limit cycles.** The limit cycle interpretation correctly identifies the mechanism (unit loop gain on a cycle of observation-action pairs) and the fix (cycle detection / anti-windup). This is a real engineering insight: treat the context as a state trajectory and detect when you have returned to a previously visited state. The control theory framing provides the "why" — not just "add a check for repetition" but "the system has a limit cycle because there is no damping, and the fix must reduce loop gain for repeated states."

**3. The gain-independence tradeoff in Reflexion.** Control theory tells us that higher gain requires more independent feedback. This is quantitative and actionable: if your evaluator is only partially independent (ρ = 0.5), you must limit how aggressively reflections modify behavior (low gain). If your evaluator is fully independent (ρ ≈ 0, external test suite), you can be more aggressive (high gain). This tradeoff is not obvious from the agent perspective alone.

**4. ToT as MPC with configurable damping.** Recognizing ToT as a form of Model Predictive Control — where the branching factor and pruning threshold are damping parameters — provides useful engineering vocabulary. It connects ToT to a well-studied control paradigm with known tradeoffs (horizon length vs. computational cost, model accuracy requirements, receding horizon stability conditions). The connection to search admissibility ↔ Lyapunov stability is formally legitimate.

### 6.2 Merely Relabeling

**1. Calling ReAct a "feedback loop."** Saying ReAct has a "controlled variable," "reference signal," and "feedback signal" is technically correct but adds no insight beyond "the agent iterates." The control theory vocabulary does not enable any predictions that "loop until done" does not. Without computing gain, delay, or stability margins, the control theory framing is terminology without substance. This was already identified in Item 26.

**2. ToT's "underdamped/overdamped" failure modes.** Saying combinatorial explosion is "underdamped" and premature convergence is "overdamped" is accurate but is just mapping "too much exploration" and "too little exploration" onto control theory terms. The explore-exploit tradeoff was well understood before anyone called it damping. The relabeling does not generate new algorithms or predictions.

**3. The Lyapunov analysis (in its current state).** The Lyapunov candidates described in Section 4.2 are suggestive but not operational. We cannot verify the Lyapunov conditions because we cannot characterize the LLM's dynamics. Until someone actually constructs and verifies a Lyapunov function for an agent loop (not just proposes one), this is aspiration, not analysis.

**4. "Second-order feedback" for Reflexion.** Calling Reflexion second-order feedback is correct (it adjusts how it adjusts), but this is equivalent to saying "it learns from experience." The second-order label from cybernetics (von Foerster) adds epistemological depth but not engineering precision. The useful insight is not the label but the specific mechanism analysis (Section 3.2).

### 6.3 The Meta-Assessment

The control theory framing is most valuable when it identifies **specific, measurable quantities** that predict system behavior. The evaluator-executor correlation ρ is such a quantity. The gain margin (sensitivity of actions to observations) is potentially such a quantity, if measured. The damping ratio of ToT search is an explicit design parameter.

The framing is least valuable when it applies **generic vocabulary** to phenomena that are already understood. Calling everything a "feedback loop" or "controlled variable" produces impressive-looking block diagrams that do not constrain predictions or guide design.

The honest verdict: about 40% of this analysis is genuinely illuminating, and 60% is relabeling. The 40% is concentrated in the failure mode analysis (Section 3), particularly the positive feedback mechanism in Reflexion and the limit cycle mechanism in ReAct. The 60% is concentrated in the loop characterization tables (Section 1), which are largely definitional.

The most actionable output of this entire analysis is a single design principle: **the corrective power of any self-improving agent loop is bounded by the independence of its evaluator from its executor.** This follows directly from the positive feedback analysis, is quantifiable in principle, and applies to every self-correcting agent architecture: Self-Refine (Madaan et al., 2023), Reflexion, constitutional AI, debate, and any form of LLM self-critique.

---

## 7. Connections to Other Formalisms

**Ashby's stability (Ch. 5):** Ashby defines stability as convergence after perturbation: lim(n→∞) T^n D(a) = a. For agent loops, the question is whether repeated application of the thought-action-observation transformation T converges to a fixed point. ReAct empirically does not always converge (limit cycles). Reflexion converges under external evaluation but not under self-evaluation. ToT converges when the evaluation function is admissible. Ashby also insists that stability is always *relative to a set of displacements* — an agent may be stable for simple tasks and unstable for complex ones. This is confirmed: ReAct is reliable on simple QA and unreliable on multi-step reasoning.

**Powers' PCT (1973):** PCT frames behavior as control of perception, not control of output. Under PCT, a ReAct agent is not trying to produce the right action — it is trying to perceive the right outcome. This inversion is significant: it predicts that agents should monitor their perceptual inputs (observations) more carefully than their outputs (actions). Current agent designs do the opposite — they focus on action selection and treat observations as simple inputs. A PCT-informed ReAct agent would have explicit perceptual goals ("I need to observe X") rather than action goals ("I need to do Y").

**Wiener's feedback theory (1948):** Wiener emphasized that feedback control requires the feedback signal to have lower noise than the controlled process. For Reflexion, this means the evaluator must be more reliable than the executor — a condition that is satisfied by external test suites but violated by self-evaluation. Wiener would not be surprised by Huang et al.'s result.

**Berkenkamp et al. (2017):** Safe RL with Lyapunov stability guarantees — explore only states where a Lyapunov function can be verified given current model uncertainty. This is directly applicable to agent loops: allow the agent to take actions only when a progress metric can be verified to decrease. No one has implemented this for LLM agents, but the mathematical framework is ready.

---

## Sources

### Agent Patterns
- Yao, S. et al. (2022). "ReAct: Synergizing Reasoning and Acting in Language Models." arXiv:2210.03629. ICLR 2023.
- Shinn, N. et al. (2023). "Reflexion: Language Agents with Verbal Reinforcement Learning." arXiv:2303.11366. NeurIPS 2023.
- Yao, S. et al. (2023). "Tree of Thoughts: Deliberate Problem Solving with Large Language Models." arXiv:2305.10601. NeurIPS 2023.
- Madaan, A. et al. (2023). "Self-Refine: Iterative Refinement with Self-Feedback." arXiv:2303.17651. NeurIPS 2023.
- Huang, J. et al. (2023). "Large Language Models Cannot Self-Correct Reasoning Yet." arXiv:2310.01798. ICLR 2024.

### Cybernetics and Control Theory
- Wiener, N. (1948). *Cybernetics: or Control and Communication in the Animal and the Machine.* MIT Press.
- Ashby, W.R. (1956). *An Introduction to Cybernetics.* Chapman & Hall. Chapters 5 (stability), 11 (requisite variety).
- Powers, W.T. (1973). *Behavior: The Control of Perception.* Aldine.
- Berkenkamp, F. et al. (2017). "Safe Model-Based Reinforcement Learning with Stability Guarantees." NeurIPS 2017. arXiv:1705.08551.

### Background
- Bateson, G. (1972). *Steps to an Ecology of Mind.* Ballantine. (Learning levels and logical types.)
- Von Foerster, H. (2003). *Understanding Understanding.* Springer. (Second-order cybernetics.)
