# Answer: Do LLM Self-Critique Loops Converge? Is the Eigenform Analogy Valid?

**Question**: The synthesis suggests LLM self-critique loops converge to von Foerster's eigenforms (fixed points of recursive operators). Does the evidence support this?

---

## Finding: Self-Critique Often Fails, and the Eigenform Analogy Is Misleading

### The Core Empirical Evidence

**"Large Language Models Cannot Self-Correct Reasoning Yet" (Huang et al., ICLR 2024)** -- the most cited paper on this topic -- makes a devastating case against intrinsic self-correction:

- **Without external feedback, self-correction degrades performance.** On GSM8K math problems, GPT-3.5 accuracy went from 75.9% to 74.7% after two rounds of self-correction.
- **The model changes correct answers to wrong ones more often than it fixes errors.** Among instances where the model changed its answer, it was more likely to flip from correct to incorrect than vice versa.
- **Multi-agent debate is no better than simple majority voting** with equivalent model calls. Multiple agents critiquing each other do not produce convergence to truth.
- **The apparent success of self-correction in prior papers was an artifact of poorly designed initial prompts.** When initial prompts were properly optimized, self-correction provided no benefit.

**Self-Refine (Madaan et al., 2023)** found modest improvements (5-20%) on tasks with clear criteria, but outputs became "blander and more generic" on open-ended tasks -- the model penalized distinctive phrasing as risky. This is convergence, but convergence to mediocrity, not to an optimal fixed point.

### Convergence Theory

**Liu et al. (2024)** provide a theoretical explanation: self-refinement shifts the model's internal state toward "higher-certainty regions of its training distribution." The model is not learning anything new -- it is accessing knowledge it already had but failed to retrieve initially. The review prompt effectively resamples from a better part of the distribution.

**Yang et al. (EMNLP 2025)** formalized this in "A Probabilistic Inference Scaling Theory for LLM Self-Correction," identifying conditions for convergence:

- Convergence works when the task is within the model's capability and initial quality is non-trivial.
- If the task requires reasoning the model cannot perform, the ceiling is very low.
- If initial quality is near zero, the model cannot bootstrap refinement.
- If the model is too aggressive in correction, it "fixes" correct content into incorrect content, causing **oscillation** instead of convergence.

### Parallel Sampling vs. Sequential Refinement

**Snell et al. (2024, "Scaling LLM Test-Time Compute Optimally")** provide the most rigorous empirical comparison:

- Sequential revisions outperform parallel sampling on **easier problems** where the initial response is already reasonable.
- Parallel sampling (Best-of-N) outperforms sequential refinement on **harder problems** that require fundamentally different solution approaches.
- The compute-optimal strategy allocates iterative refinement to easy problems and parallel diversity to hard ones. This achieves equivalent performance to Best-of-N with **4x less compute**.
- Critically, naive self-refinement (just prompting to fix mistakes) is "largely ineffective for reasoning tasks."

### Does the Eigenform Analogy Hold?

The synthesis claims: "When an LLM agent iteratively refines its response through self-critique, it is searching for an eigenform: a stable output that survives its own critical examination. This is mathematically identical to finding fixed points of recursive operators."

This analogy has problems:

1. **Self-critique often does not converge.** The evidence shows oscillation, degradation, and convergence to mediocrity as common outcomes. Fixed-point iteration in mathematics converges under specific conditions (contraction mappings, Lipschitz conditions). There is no evidence that LLM self-critique satisfies these conditions.

2. **The "fixed point" may not be desirable.** When convergence occurs, it often produces blander, more generic outputs -- the fixed point of the self-critique operator is the least objectionable response, not the best one. Von Foerster's eigenforms are stable because they are structurally self-consistent; LLM convergence is stable because the model stops finding things to criticize, which is a very different dynamic.

3. **The analogy ignores the key result.** The most robust finding is that external feedback (tests passing, user approval, factual verification) drives genuine improvement, while intrinsic self-critique does not. Von Foerster's eigenforms are about stable structures that emerge from recursive self-reference alone. If self-reference alone doesn't work for LLMs, the analogy breaks.

4. **The practical recommendation contradicts the analogy.** Practitioners increasingly recommend Best-of-N sampling over iterative refinement for most tasks -- "take your reflection budget and instead allocate it to generating N independent samples and picking the best." This is explicitly non-recursive and has nothing to do with eigenforms.

### Assessment

The eigenform analogy is **suggestive but misleading**. The reports present it as if self-critique naturally converges to stable, high-quality outputs through recursive self-reference. The empirical evidence shows the opposite: without external feedback, self-critique either degrades performance or converges to mediocrity. The mathematical conditions required for fixed-point convergence are not met by LLM self-critique in general.

The synthesis should either drop the eigenform analogy or qualify it heavily: "Under specific conditions (tasks within the model's capability, with clear quality criteria), iterative refinement can converge, but this convergence is better understood as resampling from a more favorable distribution than as fixed-point iteration in the mathematical sense."

## Sources

- Huang, J. et al. (2024). "Large Language Models Cannot Self-Correct Reasoning Yet." ICLR 2024. [PDF](https://proceedings.iclr.cc/paper_files/paper/2024/file/8b4add8b0aa8749d80a34ca5d941c355-Paper-Conference.pdf), [arXiv](https://arxiv.org/html/2310.01798v2)
- Snell, C. et al. (2024). "Scaling LLM Test-Time Compute Optimally Can Be More Effective than Scaling Model Parameters." [arXiv:2408.03314](https://arxiv.org/html/arXiv:2408.03314)
- Madaan, A. et al. (2023). "Self-Refine: Iterative Refinement with Self-Feedback." NeurIPS 2023.
- Kumar, A. et al. (2024). "Training Language Models to Self-Correct via Reinforcement Learning." [arXiv:2409.12917](https://arxiv.org/pdf/2409.12917)
- "The Research on LLM Self-Correction." [vadim.blog](https://vadim.blog/the-research-on-llm-self-correction)
- "Iterative review-fix loops remove LLM hallucinations." [DEV Community](https://dev.to/yannick555/iterative-review-fix-loops-remove-llm-hallucinations-and-there-is-a-formula-for-it-4ee8)
