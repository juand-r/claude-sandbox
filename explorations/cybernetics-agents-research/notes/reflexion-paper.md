# Reflexion: Language Agents with Verbal Reinforcement Learning

**Paper:** Shinn, N., Cassano, F., Gopinath, A., Shakhnarovich, G., & Labash, K. (2023). NeurIPS 2023. arXiv:2303.11366.

**Note:** The published NeurIPS version lists authors as: Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao. The author list changed between preprint and publication.

**Date of notes:** 2026-03-12

---

## 1. The Three Components: Actor, Evaluator, Self-Reflection

### 1.1 Actor (M_a)

- An LLM that generates actions and text conditioned on state observations.
- Formally: samples actions from policy pi_theta(a_i | s_i), where theta = {M_a, mem}.
- The policy is parameterized by BOTH the LLM weights AND the memory contents. This is the key insight: "learning" happens by changing mem, not the weights.
- Inputs: current state s_i, short-term memory (trajectory so far), long-term memory (stored reflections).
- Outputs: action a_i, which produces observation o_i from the environment.
- Can be instantiated as Chain-of-Thought, ReAct, or other prompting strategies.

### 1.2 Evaluator (M_e)

- Scores the quality of a generated trajectory.
- Formally: r_t = M_e(tau_t), producing a scalar reward for trial t.
- Instantiations vary by task:
  - **Reasoning tasks (HotPotQA):** Exact match (EM) grading — binary success/failure.
  - **Decision-making tasks (ALFWorld):** Heuristic functions detecting repeated actions, exceeding action limits, etc.
  - **Programming tasks (HumanEval):** Execute generated code against self-generated unit tests. The agent writes its OWN test suite, then runs the code against it.
  - **LLM-as-evaluator:** An LLM can also serve as evaluator for semantic judgments.
- Inputs: trajectory tau_t (the full sequence of actions and observations).
- Outputs: scalar reward r_t.

### 1.3 Self-Reflection Model (M_sr)

- Converts sparse scalar feedback into rich natural language feedback.
- Formally: sr_t = M_sr(tau_t, r_t, mem) — takes the trajectory, reward, and current memory.
- The critical capability: credit assignment through language. The agent can identify that a specific action a_i led to subsequent failures a_{i+1}, a_{i+2}, and verbally state what alternative action a_i' should have been taken.
- Inputs: failed trajectory tau_t, reward r_t, existing memory mem.
- Outputs: natural language reflection sr_t — a textual summary of what went wrong and what to do differently.

### 1.4 The Loop (Algorithm 1)

```
Initialize: Actor (M_a), Evaluator (M_e), Self-Reflection (M_sr)
Initialize: policy pi_theta, memory mem = []

LOOP:
  1. Generate trajectory tau_t by running Actor in environment
  2. Evaluate: r_t = M_e(tau_t)
  3. IF evaluator deems tau_t correct: STOP (success)
  4. Self-reflect: sr_t = M_sr(tau_t, r_t, mem)
  5. Append sr_t to mem
  6. IF trials >= max_trials: STOP (failure)
  7. Go to 1
```

---

## 2. Verbal Reinforcement: How Natural Language Substitutes for Gradients

### 2.1 The Core Claim

Traditional RL updates policy parameters via gradient descent on a loss function derived from scalar rewards. Reflexion replaces this with:

1. Scalar/binary reward --> natural language diagnosis of failure
2. Gradient update to weights --> appending reflection text to memory buffer
3. Updated policy --> same LLM, but now conditioned on richer context

The "learning" is entirely in the context window. The model weights never change. The policy pi_theta changes because theta = {M_a, mem}, and mem changes.

### 2.2 What Makes This Work

- LLMs are already capable of in-context learning. Adding a reflection to the prompt is a form of few-shot learning where the "examples" are self-generated diagnoses of past failures.
- The reflection provides a "concrete direction to improve upon" — it is directional in semantic space, analogous to how a gradient provides direction in parameter space.
- Credit assignment happens through the LLM's reasoning: it can trace back through a trajectory to identify which specific action caused failure, something that scalar rewards alone cannot convey.

### 2.3 Comparison to Traditional RL

| Aspect | Traditional RL | Reflexion |
|--------|---------------|-----------|
| Learning signal | Scalar reward | Natural language reflection |
| Parameter update | Gradient descent on weights | Append text to memory |
| Policy representation | Neural network weights | LLM + memory buffer |
| Sample efficiency | Often poor | Few trials (1-12) |
| Interpretability | Opaque | Fully interpretable |
| Requires training | Yes (fine-tuning) | No |

---

## 3. Episodic Memory

### 3.1 Architecture

Two types of memory:

- **Short-term memory:** The current trajectory history — the sequence of (action, observation) pairs within a single trial. This is essentially the conversation/execution trace.
- **Long-term memory:** The stored self-reflections from previous trials. This is the episodic memory buffer.

### 3.2 What Is Stored

Each entry in long-term memory is a natural language reflection sr_t — a textual summary produced by M_sr after a failed trial. Example content might be: "In the previous attempt, I searched for 'blue shoes' but should have searched for 'navy sneakers' because the product description uses different terminology."

### 3.3 Capacity and Retrieval

- Memory is bounded by maximum capacity Omega, typically set to 1-3 stored experiences.
- This is a hard constraint driven by LLM context window limitations.
- Retrieval is simple: ALL stored reflections are included in the prompt for the next trial. No sophisticated retrieval mechanism — just concatenation.
- When capacity is exceeded, older reflections are discarded via FIFO (first-in, first-out) truncation.
- For programming tasks: Omega = 1 (only the most recent reflection is kept).
- For decision-making/reasoning: Omega = 3 (last three reflections kept).

### 3.4 How Memory Influences Behavior

The reflections are prepended to the Actor's prompt. The LLM then conditions its next trajectory on both the task description AND the accumulated reflections. This is straightforward prompt engineering — the "learning" is literally adding text to the prompt.

This is both the strength and weakness of the approach: it is simple and interpretable, but it is fundamentally limited by context window size and the LLM's ability to follow its own advice.

---

## 4. Experimental Results

### 4.1 ALFWorld (Sequential Decision-Making)

- 134 text-based household tasks (pick & place, clean, heat, cool, examine, etc.)
- **ReAct baseline:** Converges at ~97/134 tasks (~72%) by trial 7, then stalls. 22% hallucination rate (agent believes it has items it doesn't).
- **Reflexion + ReAct:** 130/134 tasks completed (~97%) across 12 iterative trials.
- **Absolute improvement: +22%.**
- Two learning mechanisms observed:
  1. Early error identification: agent learns to recognize mistakes earlier in long trajectories.
  2. Exhaustive search: agent uses memory to systematically explore environments without repeating failed paths.

### 4.2 HotPotQA (Multi-Hop Reasoning)

**Chain-of-Thought variants (100 questions):**

| Method | Accuracy |
|--------|----------|
| CoT baseline | 60% |
| Reflexion + CoT (text-davinci-003) | 77% |
| Reflexion + CoT (gpt-3.5-turbo) | 71% |
| Reflexion + CoT (gpt-4) | 80% |

**With ground-truth context:**

| Method | Accuracy |
|--------|----------|
| CoT (GT) baseline | 68% |
| CoT (GT) + episodic memory only | ~69% |
| Reflexion + CoT (GT) | 80% |

**ReAct variants:**

| Method | Accuracy |
|--------|----------|
| ReAct baseline | 39% |
| Reflexion + ReAct | 51% |

Key finding from ablation: episodic memory alone (storing trajectories without reflection) gives only ~1% improvement. The self-reflection component adds another 8-11% on top. This demonstrates that the REFLECTION is doing the work, not just memory of past attempts.

### 4.3 HumanEval (Code Generation)

| Benchmark | Previous SOTA | GPT-4 Baseline | Reflexion |
|-----------|--------------|-----------------|-----------|
| HumanEval (Python) | 65.8% (CodeT + GPT-3.5) | 80.1% | **91.0%** |
| MBPP (Python) | 67.7% (CodeT + Codex) | 80.1% | 77.1% |
| HumanEval (Rust) | — | 60.0% | 68.0% |
| MBPP (Rust) | — | 70.9% | 75.4% |

**MBPP Python is a NEGATIVE result:** Reflexion underperforms the GPT-4 baseline (77.1% vs 80.1%). The authors attribute this to a 16.3% false positive rate in the self-generated test suite — the agent thinks its incorrect solution is correct because the tests pass.

### 4.4 LeetcodeHardGym

- 40 hard-level Leetcode problems released after October 8, 2022 (beyond GPT-4's training cutoff).
- GPT-4 baseline: 7.5%
- Reflexion: 15.0%
- 2x improvement, but absolute numbers are still low — these are genuinely hard problems.

### 4.5 WebShop (NEGATIVE RESULT)

- Task: navigate an e-commerce site to find products matching natural language descriptions.
- **Reflexion FAILS here.** After 4 trials, the agent shows no signs of improvement. Runs were terminated.
- Root cause: the task requires significant behavioral diversity and exploration. Reflexion's local optimization (reflecting on what went wrong in THIS attempt) cannot generate the kind of radical strategy shifts needed.
- The agent generates "unhelpful self-reflections" — it cannot diagnose what went wrong because the failure mode is not about specific wrong actions but about overall search strategy.

### 4.6 Test Generation Quality (HumanEval)

| Metric | Rate |
|--------|------|
| True Positives (tests pass, solution correct) | 99% |
| True Negatives (tests fail, solution incorrect) | 60% |
| False Positives (tests pass, solution WRONG) | 1% |
| False Negatives (tests fail, solution correct) | 40% |

The 1% false positive rate is low but not zero — and when it occurs, it is catastrophic because the agent terminates with a wrong answer. The 40% false negative rate is recoverable: the agent just tries again.

---

## 5. The "Semantic Gradient" Concept

### 5.1 What the Authors Claim

The self-reflective feedback "acts as a 'semantic' gradient signal by providing the agent with a concrete direction to improve upon." The scare quotes around "semantic" are the authors' own — they are aware this is an analogy, not a formal equivalence.

### 5.2 The Analogy

- In standard optimization: gradient = direction in parameter space that reduces loss.
- In Reflexion: reflection = direction in "semantic space" (the space of possible behaviors/strategies) that should improve performance.
- Both provide directional improvement signals. Both are local (they suggest incremental changes, not global optima).

### 5.3 Is It Formally Justified?

**No.** There is no formal proof that reflections function as gradients in any rigorous mathematical sense. The analogy breaks down in several ways:

1. **No guarantee of descent:** A gradient in a differentiable function guarantees local descent (for sufficiently small step size). A reflection has no such guarantee — the agent might misdiagnose the problem or suggest a worse strategy.
2. **No composability:** Gradients can be accumulated, averaged, and composed. Reflections are natural language strings with no algebraic structure.
3. **No convergence theory:** Gradient descent has well-studied convergence properties. Reflexion has none.
4. **The "step size" is undefined:** In gradient descent, you control how far to move. In Reflexion, the agent might make a tiny behavioral change or a radical one — there is no control.

The analogy is suggestive and pedagogically useful, but should not be mistaken for a formal result. It is more like a metaphor than a theorem.

---

## 6. Convergence Behavior and Iteration Count

### 6.1 How Many Iterations?

- **ALFWorld:** 12 trials. Sharp improvement in trials 1-2, then steady accumulation through trial 12. Near-complete convergence at 130/134.
- **HotPotQA:** Monotonic improvement over trials. Specific trial count not given clearly, but the paper mentions up to 3 consecutive failures as a stopping criterion.
- **HumanEval:** Not specified exactly, but the iterative test-debug-reflect loop typically converges within a few attempts.
- **WebShop:** 4 trials, then terminated due to lack of improvement.

### 6.2 Convergence Pattern

- Improvement is front-loaded: biggest gains in early trials.
- Diminishing returns set in quickly — most benefit comes from the first 1-3 reflections.
- Baseline agents (without reflection) show ZERO probabilistic improvement across trials. They are stochastic but not learning. Reflexion agents show monotonic improvement.
- The bounded memory (Omega = 1-3) means the system cannot accumulate unbounded experience. This prevents both unbounded learning and unbounded context bloat.

### 6.3 No Formal Convergence Guarantee

The authors explicitly acknowledge: "Policy optimization is a powerful approach to improve action choice through experience, but it may still succumb to non-optimal local minima solutions." There is no proof of convergence, no convergence rate, and no characterization of when the process will get stuck.

---

## 7. Failure Modes

### 7.1 When Self-Reflection Fails

1. **Hallucinated task redefinition:** After failure, the reflection step sometimes infers an entirely different function purpose and rewrites the implementation accordingly. The reflection doesn't diagnose the bug — it redefines the problem. The second attempt diverges further from the specification.

2. **Confirmation bias:** The same model generates actions, evaluates them, and produces reflections. This creates a closed loop where the agent can convince itself that a wrong approach is right.

3. **Unhelpful reflections (WebShop):** When the failure mode is strategic rather than tactical, the agent cannot generate useful reflections. It can say "I should have searched differently" but cannot specify HOW to search differently.

4. **False positive tests (MBPP):** When the self-generated test suite passes on an incorrect solution, the agent stops prematurely. This is unrecoverable — the agent believes it has succeeded.

5. **Local minima:** The agent makes small, incremental improvements but cannot escape a fundamentally wrong approach. This requires "extremely creative behavior" that reflection cannot provide.

### 7.2 When Self-Reflection Makes Things Worse

- When the reflection is confidently wrong, it can steer the agent away from a correct path.
- On MBPP Python, Reflexion actually underperforms the baseline (77.1% vs 80.1%), likely because bad reflections actively mislead.
- The unproductive loop problem: if the reflection is not "sufficiently expressive," the agent can cycle through the same mistakes.

### 7.3 Structural Limitations

- Context window bounds memory capacity. Cannot learn from more than 1-3 past experiences.
- No mechanism for forgetting BAD reflections. A wrong reflection persists in memory until pushed out by FIFO.
- Cannot handle tasks requiring fundamentally different strategies (exploration vs. exploitation).
- Non-deterministic functions, API-dependent code, hardware-dependent outputs, and concurrent code are all problematic for the test-driven evaluation.

---

## 8. Cybernetic Analysis

### 8.1 Second-Order Feedback

Reflexion is a second-order feedback system:
- **First-order loop:** Actor acts --> Environment responds --> Actor observes outcome.
- **Second-order loop:** Actor fails --> Self-Reflection analyzes the failure of the first-order loop --> Generates meta-level feedback --> Modifies Actor's future behavior.

The self-reflection is feedback ABOUT the feedback process. It is not just "I failed" (first-order) but "I failed BECAUSE I did X, and next time I should do Y" (second-order).

### 8.2 Ashby's Ultrastability

Ashby's ultrastable system (from *Design for a Brain*, 1952) has two feedback loops:
- **Primary loop:** System interacts with environment via ordinary feedback.
- **Secondary loop:** When essential variables leave acceptable bounds, the system randomly reconfigures its internal parameters until stability is restored.

**Comparison to Reflexion:**

| Aspect | Ultrastability | Reflexion |
|--------|---------------|-----------|
| Trigger for reconfiguration | Essential variables out of bounds | Evaluator returns failure |
| Reconfiguration mechanism | Random parameter change | Directed linguistic reflection |
| Search strategy | Random trial and error | Guided by LLM reasoning |
| Memory of reconfigurations | None (memoryless) | Episodic memory of reflections |
| Convergence | By chance (can be slow) | Directed but not guaranteed |

**Key difference:** Ashby's system reconfigures RANDOMLY. Reflexion reconfigures DIRECTEDLY — the reflection provides a hypothesis about what to change and why. This is a significant advance: it replaces Ashby's blind search with informed search. However, this comes at the cost of potential systematic bias (the LLM's "direction" might be consistently wrong in ways random search would not be).

**Key similarity:** Both are triggered by the same condition — the system's output leaving acceptable bounds (task failure). Both operate on a slower timescale than the primary loop. Both modify the system's internal parameters (Ashby: step functions; Reflexion: memory contents).

Reflexion could be seen as an ultrastable system where the random reconfiguration is replaced by an oracle (the LLM) that proposes directed changes. When the oracle is good, this is much faster than Ashby's random search. When the oracle is bad (hallucinated reflections, confirmation bias), it can be worse — systematically biased rather than merely slow.

### 8.3 Bateson's Learning II (Deutero-Learning)

Bateson (*Steps to an Ecology of Mind*, 1972) distinguished levels of learning:
- **Learning I:** Change in response within a fixed set of alternatives (standard conditioning).
- **Learning II:** Change in the process of Learning I — learning to learn. The organism changes how it categorizes and responds to contexts.
- **Learning III:** Change in Learning II — rare, potentially pathological.

**Reflexion as Learning II:**

The Actor's behavior within a single trial is Learning I — it responds to observations and takes actions. The Self-Reflection step is Learning II — it changes HOW the Actor will approach the next trial. The agent is not just learning the task; it is learning how to learn the task.

Evidence for this interpretation:
- The ALFWorld results show two qualitatively different learning mechanisms emerging: (1) early error detection and (2) systematic exploration. These are not specific task solutions but general STRATEGIES for approaching tasks — exactly what Bateson meant by Learning II.
- The HotPotQA ablation shows that episodic memory alone (storing trajectories = Learning I) gives minimal improvement, while reflection (analyzing WHY trajectories failed = Learning II) gives substantial improvement.

**Limitation:** Bateson noted that Learning II can produce rigidity — the organism becomes committed to a particular way of categorizing contexts, even when it's no longer appropriate. This maps directly to Reflexion's confirmation bias failure mode: once the agent has a reflection that commits it to a certain interpretation of the task, it may be unable to abandon that interpretation even when it's wrong.

### 8.4 Von Foerster's Eigenforms

Von Foerster's eigenform concept (*Observing Systems*, 1981): stable objects emerge as fixed points of recursive operations. If an operator O acts on a state x, and O(O(O(...O(x)...))) converges, the limit is an eigenform — a stable output of recursive self-reference.

**Reflexion as eigenform search:**

Each trial can be seen as applying an operator:
```
O(state) = Reflect(Evaluate(Act(state)))
```

A successful solution is an eigenform of this operator — a trajectory tau* such that evaluating it returns success, and no further reflection is needed. The system has reached a fixed point.

**The question is whether this operator contracts:**
- If O is a contraction mapping (each application brings the state closer to the fixed point), then convergence is guaranteed (Banach fixed-point theorem).
- But O is NOT a contraction mapping in general. Reflections can move the agent further from the solution (hallucinated task redefinition, confirmation bias).
- The empirical results suggest that O is "usually" contractive (performance monotonically improves in most settings) but not always (WebShop, MBPP Python).

**Eigenform instability:** Von Foerster also noted that eigenforms can be unstable — small perturbations can push the system away from the fixed point. In Reflexion, this manifests as sensitivity to the specific wording of reflections. A slightly different reflection might lead to convergence or divergence.

The eigenform framework suggests a deeper question: what determines whether Reflexion's recursive self-reference converges to a stable solution (eigenform) or oscillates/diverges? The answer likely depends on:
1. The quality of the LLM's self-model (how accurate its reflections are).
2. The complexity of the task (how many local optima exist).
3. The expressiveness of the reflection (whether language can capture the relevant distinctions).

---

## 9. Formal Convergence Guarantees

**There are none.** The authors explicitly state this as a limitation.

### 9.1 What Would Be Needed

For a formal guarantee, you would need:
1. A metric space over behavioral policies (or trajectories).
2. A proof that the Reflect-Evaluate-Act operator is a contraction in this metric.
3. Bounds on the contraction rate.

None of these exist. The "semantic space" in which reflections operate is not a metric space in any well-defined sense. The operator's behavior depends on the LLM's internals, which are not formally characterized.

### 9.2 Conditions Under Which Convergence Is More Likely

From the empirical results, convergence seems to require:
- **Diagnosable failures:** The failure mode must be identifiable from the trajectory. WebShop fails because the failures are not diagnosable.
- **Actionable reflections:** The reflection must suggest a concrete change that the Actor can implement. Vague reflections ("try harder") don't help.
- **Accurate self-evaluation:** The Evaluator must correctly identify success and failure. False positives (MBPP) break the loop.
- **Sufficiently expressive action space:** The alternative action suggested by the reflection must be feasible. If the action space is too constrained, reflection cannot help.
- **Low-dimensional error space:** Tasks where failures cluster in a small number of categories are easier to reflect on than tasks with diverse, idiosyncratic failure modes.

### 9.3 Empirical Convergence Profile

The empirical profile is: fast initial improvement, diminishing returns, eventual plateau. This is consistent with the system fixing the "easy" errors (common failure modes that reflections can diagnose) and then getting stuck on the "hard" errors (rare failure modes, fundamental capability limitations).

---

## 10. The "Experience Following Property" and Learning Bad Habits

### 10.1 The Problem

If an agent conditions on past experience, it may learn bad habits — systematic biases introduced by its own history. In Reflexion, the agent conditions on its own reflections, which are themselves products of its own (possibly flawed) reasoning.

### 10.2 How Reflexion Is Vulnerable

1. **Self-reinforcing errors:** If the first reflection misdiagnoses a failure, subsequent reflections may build on that misdiagnosis. Each trial reinforces the wrong hypothesis. The FIFO memory helps somewhat (bad reflections eventually get pushed out), but within the memory window, errors compound.

2. **Distribution shift:** The reflections change the agent's behavior, which changes the distribution of trajectories it generates, which changes the distribution of failures it observes. The reflection model was not trained on this shifted distribution. This is analogous to the off-policy problem in RL.

3. **Confirmation bias (formalized):** The same LLM generates both actions and reflections. If the LLM has a systematic bias (e.g., preferring certain solution patterns), the reflections will rationalize failures in terms of that bias rather than diagnosing the true cause.

4. **Path dependence:** The final solution depends on the ORDER of reflections. Different orderings of the same failures might lead to different (possibly suboptimal) convergence points. The system has no mechanism to detect or correct this path dependence.

### 10.3 Mitigating Factors

- The bounded memory (Omega = 1-3) limits the depth of bad-habit formation. The agent cannot accumulate an arbitrarily long history of bad reflections.
- The LLM's general reasoning capability can sometimes self-correct: a later reflection might override an earlier wrong one.
- For programming tasks (Omega = 1), only the most recent reflection is kept, which prevents compounding.

### 10.4 Connection to Cybernetics

This is precisely Bateson's warning about Learning II pathology: the agent can learn a "wrong" way of learning. In Bateson's framework, Learning II produces "character" — habitual patterns of contextualization. If Reflexion's early reflections establish a wrong pattern, the agent develops a "character" that systematically misinterprets failures. This is the cybernetic version of the experience-following problem.

Von Foerster would frame this as an unstable eigenform: the recursive self-reference converges to a fixed point, but it's the WRONG fixed point — a stable but incorrect solution. The system has no mechanism to distinguish correct eigenforms from incorrect ones; it only knows whether the evaluator returns success or failure.

---

## Summary Assessment

### Strengths
- Elegant and simple architecture. The idea of using natural language as a learning signal is genuinely novel and well-executed.
- Strong empirical results on most benchmarks. The 91% HumanEval result was state-of-the-art.
- Fully interpretable: you can read the reflections and understand what the agent "learned."
- No fine-tuning required: works with any LLM as a black box.
- The episodic memory design is appropriately minimal — bounded, FIFO, no retrieval complexity.

### Weaknesses
- No formal convergence guarantees. The "semantic gradient" metaphor is suggestive but unsubstantiated.
- Fails on tasks requiring exploration/diversity (WebShop).
- Vulnerable to hallucinated reflections and confirmation bias.
- Single-agent design means the same model's biases pervade all three components.
- Memory capacity severely limited by context window.
- The MBPP negative result shows that the approach can make things worse.

### Cybernetic Significance
Reflexion is one of the clearest implementations of second-order cybernetic principles in modern AI:
- It implements Ashby's ultrastability with directed (rather than random) reconfiguration.
- It instantiates Bateson's Learning II — learning to learn through meta-cognitive reflection.
- Its convergence behavior can be analyzed through Von Foerster's eigenform framework.
- Its failure modes map precisely to the pathologies predicted by cybernetic theory: rigid Learning II patterns (Bateson), unstable eigenforms (Von Foerster), and the fundamental limitation of self-referential systems that cannot fully model themselves (Ashby's Law of Requisite Variety — the reflection model must be at least as complex as the failure modes it diagnoses).

The paper does not cite any cybernetic literature, which is a missed opportunity. The framework would benefit from the theoretical vocabulary and analytical tools that cybernetics provides.

---

## Open Questions

1. Can the reflection model be separated from the actor model (use a different LLM) to reduce confirmation bias? This would break the single-agent closed loop.
2. What is the information-theoretic capacity of natural language reflections? How many bits of "gradient" information can a reflection convey compared to an actual gradient vector?
3. Is there a formal sense in which bounded episodic memory (Omega = 1-3) is optimal, or is it just a context-window constraint dressed up as a design choice?
4. Could Reflexion be combined with actual gradient updates (fine-tuning on successful trajectories) to get both the interpretability of verbal reflection and the formal guarantees of gradient descent?
5. The FIFO memory policy is naive. Would a selective memory (keeping the most USEFUL reflections rather than the most RECENT) improve performance?
