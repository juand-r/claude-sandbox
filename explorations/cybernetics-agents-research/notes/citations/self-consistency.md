# Self-Consistency Improves Chain of Thought Reasoning in Language Models

**Citation:** Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., Chowdhery, A., & Zhou, D. (2022). "Self-Consistency Improves Chain of Thought Reasoning in Language Models." ICLR 2023. arXiv:2203.11171. Google Research, Brain Team.

**Cited in our notes:** chain-of-thought-paper.md, react-paper.md (as CoT-SC baseline and combination method)

**Date:** 2026-03-12

---

## Key Findings

### Method
Replace greedy decoding of a single chain-of-thought with:
1. Sample multiple diverse reasoning paths from the LLM (using temperature sampling)
2. Extract the final answer from each path
3. Take the majority vote across all answers

No additional training, no external models, no verifiers. Just sample-and-vote.

### Results
Substantial gains across benchmarks with PaLM-540B, GPT-3, LaMDA-137B, UL2-20B:
- GSM8K: +17.9% absolute accuracy
- SVAMP: +11.0%
- AQuA: +12.2%
- StrategyQA: +6.4%
- ARC-challenge: +3.9%

Outperforms prompt-order ensembling and multi-prompt approaches while being simpler.

---

## Relevance to Cybernetics-Agents Bridge

### Variety Amplification Through Redundancy
Self-Consistency amplifies variety by generating multiple independent reasoning paths. Each path explores a different region of the solution space. The majority vote acts as a **variety filter** — it selects the answer with the most convergent support.

This is the principle of **redundancy with voting** from fault-tolerant systems design. In reliability engineering, N-modular redundancy (NMR) achieves reliable outputs from unreliable components by majority voting. Self-Consistency is NMR applied to reasoning: N independent reasoning chains, majority vote on the output.

### Error Correction Without Feedback
Self-Consistency achieves error correction without any feedback loop — it is a **feedforward** error-correction mechanism. There is no iteration, no refinement, no loop. Just parallel generation and aggregation.

This is significant because it works where self-correction fails (Huang et al., 2023). The key difference: self-correction requires the model to evaluate its own output (which requires variety the model may lack). Self-Consistency requires only that correct reasoning paths be more probable than any single incorrect path — a weaker and more frequently satisfied condition.

### The Ashby Perspective
From Ashby's perspective, Self-Consistency increases the **effective variety** of the controller by sampling from the model's full distribution rather than taking only the greedy (mode) output. The greedy output is a single point in the space of possible responses — it has minimal variety. Sampling reveals the full distribution, and majority voting extracts the signal (consistent correct answer) from the noise (diverse incorrect answers).

### Limitation: No Inter-Chain Communication
Each reasoning chain is independent. There is no communication between chains, no ability for one chain to learn from another's approach. This means Self-Consistency cannot discover solutions that require combining insights from multiple chains. It is an ensemble, not a team.

Tree of Thoughts addresses this limitation by allowing interaction between branches — evaluation and pruning create communication channels between parallel reasoning paths.

---

## Most Important Cited References

1. **Wei et al. (2022)** — Original CoT prompting paper
2. **Cobbe et al. (2021)** — Training verifiers for math (alternative approach: learn to verify rather than vote)
3. **Brown et al. (2020)** — GPT-3 foundations
4. **Rae et al. (2021)** — Scaling language models
