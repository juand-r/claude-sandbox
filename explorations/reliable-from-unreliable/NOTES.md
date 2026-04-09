# Notes

## Von Neumann — "Probabilistic Logics and the Synthesis of Reliable Organisms from Unreliable Components" (1956)

### The Problem

Individual components (neurons, vacuum tubes, logic gates) fail with some probability ε.
Can you build a system that computes correctly with probability approaching 1,
even though every single piece inside it is unreliable?

Von Neumann showed: **yes**, provided ε is below a threshold.

### The Key Technique: Multiplexing (Redundant Coding + Majority Voting)

1. **Bundle representation**: Instead of carrying a signal on one wire, carry it on N wires
   simultaneously. The "value" is whatever the majority of wires say.

2. **Majority organ (NAND-majority gate)**: A restoring element that takes a bundle as input,
   performs a majority vote, and outputs a fresh bundle. This is critical — it *restores* the
   signal, beating back the accumulated errors before they overwhelm the majority.

3. **Composition**: Replace every gate in your circuit with a "multiplexed" version that
   operates on bundles and includes majority restoration stages.

### The Main Result

If each component fails independently with probability ε < some threshold ε₀
(roughly ε₀ ≈ 1/6 for his construction, though tighter bounds exist), then by using
bundles of size N, you can make the overall system error probability **exponentially small**
in N. The cost is a polynomial blowup in the number of components
(roughly O(N log N) factor).

Key equation (informal):
- After one majority vote on a bundle where each wire is correct with prob (1-δ):
  - The output bundle has per-wire error probability δ' ≈ c·δ² (for small δ)
  - This is the "error-squaring" effect — errors shrink quadratically per restoration stage
  - This is what makes the scheme work: errors contract faster than they accumulate

### The Threshold Phenomenon

Below the threshold: you can achieve arbitrary reliability with polynomial overhead.
Above the threshold: errors accumulate faster than voting can correct them; no amount
of redundancy helps.

This is directly analogous to:
- The threshold theorem in quantum error correction
- Shannon's channel coding theorem (reliable communication over noisy channels)
- The fault-tolerance threshold in distributed computing

### What Makes This Profound

1. **Universality**: Any Boolean circuit can be made reliable this way — it's a compiler
   from ideal circuits to fault-tolerant circuits.

2. **The cost is modest**: Polynomial overhead, not exponential. Reliability is "cheap"
   relative to the computation itself.

3. **It's constructive**: Not just an existence proof — he gives you the actual construction.

4. **Philosophical**: Brains are made of noisy neurons. Von Neumann was partly motivated
   by understanding how biological systems achieve reliability despite unreliable parts.

### Limitations and Caveats

- Assumes **independent failures**. Correlated failures break the analysis.
- The threshold depends on the specific voting scheme and fan-in/fan-out.
- Real systems (and LLMs) have failure modes that aren't just random bit-flips —
  they can fail *systematically* (e.g., all copies make the same mistake).

### Relevance to LLMs

The parallel to LLMs is tantalizing but imperfect:

| Von Neumann's Model | LLM Reality |
|---|---|
| Binary signal, random bit-flip errors | Rich structured output, systematic biases |
| Independent failures across copies | Same model = correlated errors |
| Majority vote is well-defined | "Majority" over natural language is fuzzy |
| Threshold is crisp | No formal error model exists for LLMs |

The key challenge for applying this to LLMs: **correlated failures** and **no clean error model**.
Calling the same LLM 5 times doesn't give you 5 independent samples —
they share training data, architecture, and biases. If the model "thinks" 2+2=5,
asking it 5 times and voting won't help.

Possible mitigations:
- Use **diverse models** (different architectures, training data) to reduce correlation
- Use **diverse prompts** (rephrasings, different chain-of-thought strategies)
- Use **verifiers** that are cheaper/more reliable than the generator
  (e.g., a code interpreter can verify code, a calculator can verify arithmetic)
- Use **structured outputs** where you CAN define majority voting cleanly
  (e.g., classification tasks, multiple-choice, yes/no)

## Open Questions for This Exploration

1. Can we formalize an error model for LLMs that's useful for reliability analysis?
2. What's the practical "threshold" — how unreliable can a component be before
   redundancy stops helping?
3. How much does diversity (model diversity, prompt diversity) actually reduce correlation?
4. For what classes of tasks can we build von Neumann-style reliability guarantees?
5. What's the right "majority organ" for LLM outputs? (Voting? LLM-as-judge? Verification?)
