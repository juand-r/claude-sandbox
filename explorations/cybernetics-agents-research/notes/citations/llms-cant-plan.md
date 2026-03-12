# LLMs Can't Plan, But Can Help Planning in LLM-Modulo Frameworks

**Citation:** Kambhampati, S., Valmeekam, K., Guan, L., Stechly, K., Verma, M., Bhambri, S., Saldyt, L., & Murthy, A. (2024). "LLMs Can't Plan, But Can Help Planning in LLM-Modulo Frameworks." arXiv:2402.01817. Arizona State University.

**Cited in our notes:** autogpt-failure-analysis.md (planning failures), wang-agent-survey.md (external planners)

**Date:** 2026-03-12

---

## Key Findings

### The Central Claim
LLMs cannot generate executable plans autonomously. Only ~12% of GPT-4 generated plans are actually executable in standard planning benchmarks. But LLMs are valuable as "universal approximate knowledge sources" when combined with external model-based verifiers.

### Three Key Negative Results

1. **LLMs cannot plan autonomously.** Performance on standard planning benchmarks is very poor. The 12% executable rate means 88% of generated plans contain errors.

2. **LLMs cannot self-verify.** When asked to critique their own solutions, models fail to detect errors reliably. This confirms Huang et al.'s finding in a different domain.

3. **Published claims are often confused.** Many papers claiming LLM planning abilities confuse "knowledge extraction" with "executable plan generation" — or test on domains with minimal subgoal interactions where sequential decomposition trivially works.

### The LLM-Modulo Solution
A generate-test-critique architecture:
1. LLM generates candidate plans (leveraging approximate knowledge)
2. External verifier checks formal correctness
3. Critique fed back to LLM for refinement
4. Repeat until verifier approves

This provides **formal correctness guarantees** while leveraging LLM knowledge. The external verifier supplies the variety the LLM lacks for self-verification.

---

## Relevance to Cybernetics-Agents Bridge

### The Good Regulator Applied to Planning
The Good Regulator Theorem (Conant-Ashby) states every good regulator must contain a model of the system it regulates. LLMs contain an *approximate* model of the world (from training data). This model is sufficient for generating plausible candidate plans but insufficient for verifying them, because:
- The model is statistical, not logical
- It captures correlations, not causal structure
- It lacks the precision needed for constraint satisfaction

The LLM-Modulo framework acknowledges this by splitting the regulatory function: LLM provides the approximate model (candidate generation), and an external verifier provides the precise model (plan verification). Together, they satisfy the Good Regulator requirement.

### Feedback Loop Architecture
The generate-test-critique loop is a proper negative feedback loop:
- **Generator:** LLM produces candidate (effector)
- **Verifier:** External model checks correctness (sensor)
- **Error signal:** Verification failure + critique (comparator output)
- **Correction:** LLM revises based on critique (controller)

The crucial insight: the verifier is **external to and independent of** the generator. This provides the independent error signal that self-correction lacks (Huang et al., 2023). The feedback loop works because the sensor (verifier) has different variety than the effector (LLM) — it has formal domain knowledge that the LLM does not.

### Implications for Agent Design
This paper supports a general principle: **LLMs should be components in feedback loops, not standalone controllers.** The LLM provides approximate knowledge and flexible generation; external mechanisms provide formal verification, stability guarantees, and independent error detection.

This is the same pattern as:
- ReAct (LLM + environment feedback)
- Toolformer (LLM + external tools)
- Berkenkamp et al. (RL + Lyapunov verification)

The common structure: approximate generator + formal verifier + feedback loop.

---

## Most Important Cited References

1. **Valmeekam et al. (2023)** — Initial results showing LLMs fail at planning benchmarks
2. **Huang et al. (2023)** — LLMs cannot self-correct (complementary result)
3. **Kambhampati (2024)** — "Can LLMs Really Reason and Plan?" (extended argument)
4. **Ghallab, Nau & Traverso (2016)** — *Automated Planning and Acting* (formal planning theory)
