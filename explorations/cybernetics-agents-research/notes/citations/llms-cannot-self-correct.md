# Large Language Models Cannot Self-Correct Reasoning Yet

**Citation:** Huang, J., Chen, X., Mishra, S., Zheng, H.S., Yu, A.W., Song, X., & Zhou, D. (2023). "Large Language Models Cannot Self-Correct Reasoning Yet." ICLR 2024. arXiv:2310.01798. Google DeepMind.

**Cited in our notes:** chain-of-thought-paper.md (faithfulness problem), reflexion-paper.md (self-reflection limitations), autogpt-failure-analysis.md (self-criticism failures)

**Date:** 2026-03-12

---

## Key Findings

### Central Claim
LLMs struggle to self-correct their responses without external feedback. Performance often **degrades** after self-correction attempts. The paper focuses on "intrinsic self-correction" — improvement using only the model's own capabilities, with no external oracle, tools, or ground truth.

### When Self-Correction Fails
- **Reasoning tasks:** Self-correction consistently *reduces* accuracy on GSM8K, CommonSenseQA, HotpotQA
- **Correct -> Incorrect conversion:** Models frequently change correct answers to incorrect ones during revision
- **Oracle dependence exposed:** Prior work claiming self-correction benefits relied on ground-truth labels to guide corrections — not genuine self-improvement
- **Random baseline match:** On CommonSenseQA, randomly selecting answers in subsequent rounds matched self-correction performance

### When Self-Correction Works
- Style modifications and safety alignment (where the feedback introduces new criteria)
- Tasks where feedback provides instructions *absent from the initial prompt*
- Scenarios with external tools (calculators, code executors, search engines)

### Critical Distinctions
**Pre-hoc vs. Post-hoc prompting:** Self-correction can be viewed as adding a better prompt after the fact. When improvements occur, they often result from the initial prompt being poorly designed — the "feedback" prompt supplies the missing instructions. The fix is better initial prompting, not self-correction.

**Multi-agent debate vs. Self-Consistency:** Debate shows no meaningful advantage over simple majority voting with equivalent model calls. Improvements come from redundancy (more samples), not from correction.

### The Fundamental Mechanism
"If the model is well-aligned and paired with a thoughtfully designed initial prompt, the initial response should already be optimal given the decoding parameters." Additional feedback biases responses *away* from this optimum rather than toward correctness.

---

## Relevance to Cybernetics-Agents Bridge

### The Central Cybernetic Problem: Self-Regulation Limits
This paper is perhaps the most important citation for the cybernetics-agents bridge because it empirically demonstrates a **fundamental limit of self-regulation**.

Ashby's Law of Requisite Variety applied to self-correction: for an agent to correct its own errors, its error-detection mechanism must have at least as much variety as the errors it needs to detect. But the error-detection mechanism (the same LLM generating critique) has **exactly the same variety** as the error-generating mechanism — it is the same model. Therefore, the errors that the model systematically makes are precisely the ones its self-correction mechanism cannot detect.

This is not a contingent engineering limitation. It is a **structural** limitation predicted by cybernetics: a system cannot fully model itself (Ashby's theorem about self-regulation), and therefore cannot fully correct itself.

### The Feedback Loop That Degrades
When self-correction makes things worse, it implements a **positive feedback loop**: the model generates an answer, generates a critique biased by the same errors, revises the answer to align with the (erroneous) critique, producing a worse answer that is now more consistent with its systematic biases. The correction amplifies rather than dampens the error.

### External Feedback as Necessary Variety
The finding that self-correction works with external tools (calculators, search engines) is precisely Ashby's prediction: external tools provide **additional variety** that the model lacks internally. The calculator has variety in the domain of arithmetic that the LLM does not. Search engines have variety in the domain of current facts. These external sources restore the requisite variety for error correction.

### Implications for Agent Architecture
This paper argues against architectures that rely on the same LLM for both action and evaluation (like AutoGPT's self-criticism). It supports architectures with:
- Independent evaluation mechanisms (different model, external verifier, human review)
- External grounding (tools, databases, environments that provide independent feedback)
- Redundancy-based error correction (Self-Consistency, ensemble) rather than self-correction

---

## Most Important Cited References

1. **Shinn et al. (2023).** Reflexion — provides external evaluator (test execution), which is why it works
2. **Madaan et al. (2023).** Self-Refine — works for style but not reasoning
3. **Wang et al. (2022).** Self-Consistency — the right baseline for comparison
4. **Du et al. (2023).** Multi-agent debate — shown equivalent to majority voting
5. **Kim et al. (2023).** Self-correction with oracle feedback — what looks like self-correction is actually oracle guidance
