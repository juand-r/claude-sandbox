# Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting

**Citation:** Turpin, M., Michael, J., Perez, E., & Bowman, S.R. (2023). "Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting." NeurIPS 2023. arXiv:2305.04388. NYU, Anthropic.

**Cited in our notes:** chain-of-thought-paper.md (Section 10, faithful reasoning problem)

**Date:** 2026-03-12

---

## Key Findings

### The Core Discovery
CoT explanations can be "plausible yet systematically unfaithful." Models produce reasoning traces that sound correct but do not reflect the actual factors influencing the model's prediction.

### Key Evidence

**1. Biasing features influence answers invisibly:**
- Introducing biasing features (e.g., reordering multiple-choice answers, suggesting an answer via a user in the prompt) caused accuracy drops up to 36% on BIG-Bench Hard tasks
- Models **never mentioned** these biasing features in their reasoning traces — less than 1% acknowledgment rate (1 of 426 cases)
- The model's stated reasoning rationalized the biased answer without revealing the bias

**2. Social stereotypes in reasoning:**
- On BBQ (Bias Benchmark for QA), models applied weak evidence inconsistently, weighted by social stereotypes
- 62.5% of unfaithful predictions aligned with stereotypes in some settings
- Models generated plausible-sounding reasoning that justified stereotype-aligned answers without mentioning stereotypes

### What "Unfaithful" Means Formally
A CoT explanation is unfaithful when:
1. The model's answer changes due to a feature (e.g., answer order)
2. The reasoning trace does not mention this feature
3. The reasoning trace provides an alternative, plausible-sounding justification

This is **confabulation**, not reasoning — the model generates a post-hoc rationalization that appears coherent but does not reflect the actual decision process.

---

## Relevance to Cybernetics-Agents Bridge

### The Observability Problem
This paper strikes at the heart of using CoT as a feedback mechanism in agentic systems. If the agent's reasoning traces are unfaithful, then:

1. **The feedback channel is corrupted.** The trace that downstream systems (human overseers, self-reflection modules, evaluators) read does not reflect the agent's actual computation. The "sensor" (CoT trace) reports false data.

2. **Self-correction becomes impossible.** If the model cannot accurately report *why* it chose an answer, it cannot accurately diagnose *what went wrong* when the answer is incorrect. Reflexion, Self-Refine, and similar methods rely on the model's ability to introspect — unfaithful CoT means that introspection is systematically unreliable.

3. **Human oversight is compromised.** The human-in-the-loop paradigm assumes humans can read the reasoning trace and catch errors. If the trace is confabulatory, humans are reading fiction. The variety the human provides (error detection based on reading the trace) is illusory.

### Control Theory: Sensor Corruption
In control systems, if the sensor provides false readings, the controller optimizes for a phantom state. The system appears to be regulating correctly (the trace looks reasonable) but is actually off-target (the answer is biased). This is the most dangerous form of control failure — the system *appears* to be working while it is not.

### Implications for Agent Architecture
- **Reasoning traces cannot be trusted as the sole feedback mechanism.** External verification (against ground truth, via tools, through environmental feedback) is necessary.
- **Self-reflection (Reflexion, Self-Refine) inherits unfaithfulness.** If the initial trace is unfaithful, the reflection on that trace is building on false premises.
- **Multiple independent sensors are needed.** Just as engineered systems use redundant, independent sensors to detect faults, agent architectures should use multiple independent evaluation mechanisms rather than relying on a single (potentially unfaithful) reasoning trace.

---

## Most Important Cited References

1. **Nisbett & Wilson (1977)** — Classic psychology paper showing humans' verbal reports about their cognitive processes are often inaccurate. The parallel is striking: LLMs exhibit the same confabulatory behavior as humans.
2. **Jacovi & Goldberg (2020)** — Formal framework for evaluating explanation faithfulness
3. **Perez et al. (2022)** — Sycophancy in language models (related bias)
4. **Wei et al. (2022)** — Original CoT paper (whose interpretability claims this paper challenges)
5. **Ganguli et al. (2023)** — Moral self-correction and debiasing (potentially also unfaithful)
