# Fields and Ideas for Building Reliable Systems from Unreliable Components

## The Core Question

You have a component (an LLM) that works well most of the time but sometimes fails.
You want to build a *system* around it that is more reliable than the component itself.
What existing theory and practice can you draw on?

There is a LOT. This is arguably one of the central problems of engineering.

---

## 1. Von Neumann — Reliable Organisms from Unreliable Components (1956)

Already covered in NOTES.md. The headline:

- **Multiplexing + majority voting** achieves arbitrary reliability with polynomial overhead.
- **Error-squaring effect**: restoration stages shrink errors quadratically.
- **Threshold theorem**: works only if per-component error rate is below a threshold.
- **Assumes independent failures** — this is the big problem for LLMs.

**Transfer to LLMs**: Partial. Works well for tasks with verifiable, discrete outputs
(classification, yes/no, multiple-choice). Breaks down for open-ended generation
and when failures are correlated (same model = same biases).

---

## 2. Shannon — Coding Theory / Reliable Communication (1948)

Shannon showed you can communicate reliably over a noisy channel, up to a
**channel capacity** limit, by adding structured redundancy (error-correcting codes).

Key ideas:
- **Channel capacity**: There's a fundamental limit to how much reliable information
  you can push through a noisy channel. Below capacity, error can be made arbitrarily
  small. Above it, impossible.
- **Separation principle**: You can separate the problem of source coding (compression)
  from channel coding (error correction). This modularity is powerful.
- **Structured redundancy >> naive repetition**: Repeating a message 3x is wasteful.
  Cleverly designed codes (Hamming, Reed-Solomon, LDPC, turbo codes) achieve near-capacity
  performance with much less overhead.

**Transfer to LLMs**: The "channel" analogy is suggestive. The LLM is a noisy channel
between your intent and the output. Can we design "codes" — structured prompting
strategies, output formats, verification steps — that approach some capacity limit?

The separation principle is also relevant: you might separate the "what to compute"
(the task specification) from the "how to make it reliable" (the redundancy/verification
layer). This is essentially what tool-use architectures do: the LLM handles the
hard/fuzzy part, and deterministic code handles the reliable part.

---

## 3. Fault-Tolerant Distributed Systems

A huge body of work on making systems reliable when individual nodes can crash
or even behave maliciously.

### 3a. Consensus (Paxos, Raft, PBFT)
- **Problem**: N nodes must agree on a value even if some fail.
- **Result**: Tolerate f crash failures with 2f+1 nodes (Paxos/Raft).
  Tolerate f Byzantine (arbitrary) failures with 3f+1 nodes (PBFT).
- **Key insight**: Agreement requires *quorums* — overlapping subsets that guarantee
  at least one correct node participates in every decision.

**Transfer to LLMs**: Byzantine fault tolerance is interesting because LLMs don't just
crash — they confidently produce wrong answers (Byzantine behavior). If you model each
LLM call as a potentially Byzantine node, you need 3f+1 calls to tolerate f bad ones.
But: this assumes failures are independent across nodes, which doesn't hold for copies
of the same model.

### 3b. State Machine Replication
- Run the same deterministic computation on multiple nodes.
- As long as they agree on the order of inputs, they produce the same outputs.
- Non-determinism is the enemy.

**Transfer to LLMs**: LLMs are inherently non-deterministic (even at temperature 0,
due to floating point and batching). You can't just replicate — you must *reconcile*.

### 3c. Quorum Systems
- Not every node needs to participate in every operation.
- You just need enough overlap between read-quorums and write-quorums.
- Generalizes to *weighted* quorums — not all nodes equally trusted.

**Transfer to LLMs**: Weighted voting where better models or more reliable approaches
get more weight. This is essentially ensemble weighting.

---

## 4. N-Version Programming and Recovery Blocks

### N-Version Programming (Avizienis, 1977)
- Build N independent implementations of the same spec.
- Run all N, take majority vote.
- Idea: independent development → independent failure modes.

**The dirty secret**: In practice, independence is hard to achieve. Knight & Leveson (1986)
showed that independently developed programs have *correlated* failures — they tend to
fail on the same hard inputs. Sounds familiar?

**Transfer to LLMs**: This is directly analogous to using diverse models. But just as
Knight & Leveson found, different LLMs may share failure modes due to similar training
data, architectures, or RLHF-induced biases. Diversity helps but doesn't guarantee
independence.

### Recovery Blocks (Randell, 1975)
- Try the primary approach.
- Run an **acceptance test** on the result.
- If it fails, try an alternative approach.
- Repeat until one passes or all alternatives are exhausted.

**Key insight**: Separates *generation* from *checking*. The acceptance test can be
much simpler and more reliable than the computation itself.

**Transfer to LLMs**: This transfers beautifully. Generate with an LLM, check with
a verifier (another LLM, a type checker, a test suite, a constraint solver, a human).
This exploits the **generation-verification asymmetry**: for many problems, checking
a solution is much easier than producing one. This is perhaps the single most important
principle for LLM reliability.

---

## 5. Control Theory

### Feedback Control
- You don't need a perfect model of the plant.
- You need a sensor (observation), a controller, and a feedback loop.
- Feedback corrects for model errors, disturbances, and component drift.
- **PID controllers** work remarkably well despite knowing almost nothing about
  the system they're controlling.

**Key concepts**:
- **Stability**: Does the system stay bounded or diverge?
- **Robustness**: How much can the plant deviate from the model before stability breaks?
- **Gain margin / phase margin**: Quantitative measures of robustness.

**Transfer to LLMs**: An LLM agent with tool use and a feedback loop (execute → observe
result → correct) is essentially a control system. The "plant" is the world/codebase/API,
the "controller" is the LLM, and "sensors" are the outputs of tool calls. The reliability
comes not from the LLM being perfect but from the **closed-loop** structure.

This is why agentic LLM systems (that can run code, see errors, iterate) are much more
reliable than single-shot prompting — they're closed-loop vs. open-loop.

### Robust Control (H∞)
- Design controllers that work well across a *set* of possible plants, not just one.
- Worst-case optimization rather than average-case.

**Transfer to LLMs**: Design prompting/scaffolding strategies that are robust across
a range of model behaviors, not tuned to one model's quirks.

---

## 6. Ensemble Methods in Machine Learning

### Bagging (Breiman, 1996)
- Train multiple models on bootstrap samples of the data.
- Average their predictions.
- Reduces **variance** without increasing bias (much).
- Works because averaging reduces the variance of uncorrelated errors.

### Boosting (Freund & Schapire, 1997)
- Train models sequentially, each focusing on the errors of the previous.
- Reduces **bias** — the ensemble can learn things no individual model can.
- More aggressive but also more prone to overfitting.

### Mixture of Experts
- Route different inputs to different specialized models.
- Not every model sees every input.
- Sparse activation = efficiency.

**Transfer to LLMs**:
- **Bagging analog**: Call multiple models/prompts, aggregate. Standard "sample and vote."
- **Boosting analog**: Use the first LLM's output as context for a second LLM that
  critiques/refines. Chain-of-thought refinement. Self-critique loops.
- **MoE analog**: Route tasks to specialized models or prompts. Use a fast model for
  easy tasks, expensive model for hard ones. Confidence-based routing.

---

## 7. Cybernetics and Systems Theory

### Ashby's Law of Requisite Variety (1956)
- A controller must have at least as much variety (possible states) as the system
  it's trying to control.
- **You can't control what you can't match in complexity.**

**Transfer to LLMs**: If your task has high variety (many possible failure modes),
your reliability mechanism needs correspondingly high variety. A simple "retry 3 times"
won't cut it if there are many different ways to fail. You need diverse strategies.

### Ashby's Ultrastability
- Systems that reorganize their own structure in response to disturbance.
- Not just feedback on the output — feedback on the *strategy*.

**Transfer to LLMs**: Meta-learning / prompt adaptation. If a prompting strategy
keeps failing on a class of inputs, the system should detect this and switch strategies.
Not just retry — restructure.

---

## 8. The Generation-Verification Gap (Complexity Theory)

This isn't a "field" per se, but a fundamental structural property:

- **NP**: Solutions are hard to find but easy to verify.
- **Interactive proofs / probabilistically checkable proofs**: Even stronger — you can
  verify complex computations by checking a tiny random subset.

**Transfer to LLMs**: For tasks where verification is cheap (code that can be tested,
math that can be checked, facts that can be looked up, formats that can be validated),
you can achieve high reliability by:
1. Generate many candidates
2. Verify each cheaply
3. Return the first that passes

The reliability comes from the verifier, not the generator. The generator just needs
to succeed *often enough* that the expected number of attempts is reasonable.

This is probably the most underappreciated framework for LLM reliability. It shifts
the question from "how do I make the LLM reliable" to "how do I make the task verifiable."

---

## 9. Safety Engineering and Redundancy Design

### Fail-Safe vs. Fail-Operational
- **Fail-safe**: When a component fails, the system enters a safe state (e.g., traffic
  light goes to all-red).
- **Fail-operational**: When a component fails, the system continues operating
  (possibly degraded).

**Transfer to LLMs**: What's the "safe state" for an LLM system? Refusing to answer?
Returning a cached/default response? Escalating to a human? This is under-discussed.

### Swiss Cheese Model (Reason, 1990)
- Each layer of defense has holes (like Swiss cheese slices).
- Accidents happen when holes align across all layers.
- **Defense in depth**: Multiple independent layers make alignment of holes unlikely.

**Transfer to LLMs**: Stack multiple defenses:
1. Good prompting (layer 1)
2. Output validation / parsing (layer 2)
3. LLM self-critique (layer 3)
4. Deterministic checks (layer 4)
5. Human review for high-stakes decisions (layer 5)

No single layer is reliable. The stack is.

---

## 10. Biological Reliability

Living systems are spectacularly reliable despite unreliable parts:

- **DNA repair mechanisms**: Multiple overlapping repair pathways.
- **Immune system**: Diverse, redundant, adaptive.
- **Neural coding**: Population coding in the brain — signals represented across
  many neurons, not one. Basically von Neumann's multiplexing.
- **Homeostasis**: Feedback loops maintaining stable internal state despite external
  perturbations. Body temperature, blood pH, etc.
- **Apoptosis**: Cells that detect they're malfunctioning *kill themselves*. Better to
  lose a cell than to have it go rogue. (Analogy: circuit breakers, timeouts.)

**Transfer to LLMs**: The immune system analogy is interesting — a system that
*learns* to detect and respond to new failure modes, rather than having them all
pre-programmed.

---

## 11. Quantum Error Correction

- Qubits decohere rapidly — they're extremely unreliable.
- Quantum error correction encodes logical qubits across many physical qubits.
- **Threshold theorem**: If per-gate error is below ~1%, you can compute arbitrarily
  long quantum computations reliably. (Direct analog of von Neumann's result.)
- Uses **syndrome measurements** — you can detect errors without collapsing the
  quantum state, then correct them.

**Transfer to LLMs**: The syndrome measurement idea is relevant — you want to detect
that something has gone wrong *without having to know the correct answer*. For LLMs:
consistency checks, self-contradiction detection, confidence calibration.

---

## Summary: What Transfers Best to LLMs?

### Transfers well:
1. **Generation-verification gap** (§8): For verifiable tasks, generate-and-check is
   powerful and principled.
2. **Recovery blocks** (§4): Try, check, retry with different strategy. Simple and effective.
3. **Closed-loop control** (§5): Agentic systems with feedback. This is why agents
   work so much better than single-shot.
4. **Defense in depth / Swiss cheese** (§9): Stack multiple unreliable checks.
5. **Fail-safe design** (§9): Know what to do when everything fails.
6. **Ensemble/voting for discrete tasks** (§1, §6): Works when outputs are enumerable.

### Transfers partially:
7. **Diversity for independence** (§4, N-version programming): Helps but doesn't
   guarantee independence (Knight & Leveson).
8. **Quorum/weighted voting** (§3c): Works for structured outputs.
9. **Boosting as iterative refinement** (§6): Self-critique, chain of refinement.

### Doesn't transfer cleanly:
10. **Von Neumann multiplexing for free-form text**: No clean majority operation.
11. **State machine replication** (§3b): LLMs are non-deterministic.
12. **Shannon coding** (§2): No formal channel model for LLMs (yet).

### The key structural issue:
Von Neumann, Shannon, and distributed systems all assume you can characterize the
**noise/failure model**. For LLMs, we don't have this. LLM failures are:
- **Systematic** (not random)
- **Input-dependent** (some prompts are harder)
- **Correlated** across copies of the same model
- **Hard to predict** without running the model
- **Sometimes catastrophically wrong** with high confidence

Building a proper theory of LLM reliability may require developing a new error model
that captures these properties. That's an open research problem.

---

## On the Circuit-Level Approach (Merrill → Boolean → Redundancy → Back)

The idea: take a transformer, compile it to a Boolean circuit (per Merrill's work on
circuit complexity of transformers), apply von Neumann-style redundancy to the circuit,
then map back to a neural network.

This is a cool idea but there are some issues:

1. **Scale**: A transformer with billions of parameters would yield an astronomical
   Boolean circuit. The polynomial blowup from von Neumann redundancy on top of that
   is impractical.

2. **Wrong level of abstraction**: LLM failures aren't random gate failures. A gate
   in the circuit doesn't flip randomly — the entire circuit computes a coherent but
   wrong function because the *weights are wrong for this input* (not the gates).
   Von Neumann redundancy protects against transient hardware faults, not against
   the circuit implementing the wrong function.

3. **The error model mismatch**: Von Neumann's scheme assumes each gate fails
   independently with probability ε. In a neural network, "errors" are systematic —
   the weights encode incorrect generalizations. Making each gate more reliable
   doesn't fix a fundamentally wrong computation.

4. **Mapping back**: There's no clean inverse map from a redundant Boolean circuit
   back to an efficient neural network. You'd likely end up with something much larger
   and slower with no practical benefit.

**However**: The idea has merit at a *different* level. Instead of adding redundancy
at the gate level, add it at the **component level** — treat the whole LLM as one
(unreliable) gate, and build reliability at the system level. That's what most of the
other approaches in this survey do.

The circuit-theoretic view is still useful for *understanding* what transformers can
and can't compute (Merrill's actual contribution), which informs where they'll be
unreliable. But the fix is architectural (system-level redundancy), not surgical
(gate-level redundancy).
