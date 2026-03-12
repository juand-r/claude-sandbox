# Scholarly Notes: Chain-of-Thought Prompting Elicits Reasoning in Large Language Models

**Citation:** Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q.V., & Zhou, D. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." *NeurIPS 2022*. arXiv:2201.11903.

**Date of these notes:** 2026-03-12

---

## 1. The Core Mechanism

### What is Chain-of-Thought (CoT) Prompting?

CoT prompting augments standard few-shot prompting by including **intermediate reasoning steps** in each exemplar, rather than just input-output pairs. The prompt consists of triples: (input, chain of thought, output).

**Standard prompting:**
```
Q: Roger has 5 tennis balls. He buys 2 more cans of 3. How many does he have?
A: The answer is 11.
```

**CoT prompting:**
```
Q: Roger has 5 tennis balls. He buys 2 more cans of 3. How many does he have?
A: Roger started with 5 balls. 2 cans of 3 tennis balls each is 6. 5 + 6 = 11. The answer is 11.
```

The key insight: the chain of thought is placed **before** the final answer in the exemplar demonstrations. The model then learns to produce its own chain of thought before answering new questions. This is a **few-shot** technique -- no finetuning required, no gradient updates. Just demonstration via prompting.

### How It Differs from Standard Prompting

| Dimension | Standard Prompting | CoT Prompting |
|---|---|---|
| Exemplar format | (Q, A) pairs | (Q, reasoning, A) triples |
| Output structure | Direct answer | Reasoning steps then answer |
| Computation | Fixed (single forward pass per token) | Variable (more tokens = more computation) |
| Interpretability | Opaque | Reasoning chain is inspectable |
| Training required | None | None |

### Four Attractive Properties Identified by the Authors

1. **Decomposition:** Allows multi-step problems to be broken into intermediate steps, allocating more computation to harder problems.
2. **Interpretability:** Provides a window into the model's reasoning path (though faithfulness is an open question -- more on this below).
3. **Generality:** Applicable to math, commonsense, symbolic reasoning -- any task humans solve via sequential reasoning.
4. **Simplicity:** Requires only modifying the few-shot exemplars. No architectural changes, no finetuning, works with off-the-shelf models.

---

## 2. Experimental Setup

### Models Evaluated

Five model families, spanning a wide range of scales:

| Model Family | Sizes | Notes |
|---|---|---|
| **GPT-3** | 350M, 1.3B, 6.7B, 175B | text-ada-001 through text-davinci-002 |
| **LaMDA** | 422M, 2B, 8B, 68B, 137B | Google's dialog model |
| **PaLM** | 8B, 62B, 540B | Google's Pathways model |
| **UL2 20B** | 20B | Single size tested |
| **Codex** | code-davinci-002 | OpenAI's code model |

### Benchmarks

**Arithmetic reasoning (5 benchmarks):**
- **GSM8K** (Cobbe et al., 2021): Grade school math word problems. The hardest and most important benchmark in this paper. Multi-step.
- **SVAMP** (Patel et al., 2021): Math word problems with varying structures.
- **ASDiv** (Miao et al., 2020): Diverse math word problems.
- **AQuA** (Koncel-Kedziorski et al., 2016): Algebraic word problems. Multiple choice.
- **MAWPS** (Koncel-Kedziorski et al., 2016): Math word problem repository. Includes subsets SingleOp, SingleEq, AddSub -- mostly easy, 1-2 step problems.

**Commonsense reasoning (5 benchmarks):**
- **CSQA** (Talmor et al., 2019): CommonsenseQA -- complex semantics, prior knowledge.
- **StrategyQA** (Geva et al., 2021): Multi-hop strategy questions.
- **Date Understanding** (BIG-bench): Inferring dates from context.
- **Sports Understanding** (BIG-bench): Plausibility of sports sentences.
- **SayCan** (Ahn et al., 2022): Mapping natural language instructions to robot actions.

**Symbolic reasoning (2 tasks):**
- **Last letter concatenation:** Concatenate last letters of words in a name ("Amy Brown" -> "yn").
- **Coin flip (state tracking):** Track heads/tails after a sequence of flips/non-flips.

### Exemplar Construction

- **8 exemplars** for most arithmetic benchmarks, manually composed with chains of thought.
- For AQuA: 4 exemplars (from training set solutions).
- For commonsense: randomly selected from training sets with manually written CoT.
- For symbolic: manually composed.
- Exemplars did **not** undergo prompt engineering -- they were written straightforwardly.
- Full exemplar set given in Appendix Table 20.
- Decoding: greedy decoding for all models (though follow-up work on self-consistency uses majority voting over sampled generations).
- LaMDA: averaged over 5 random seeds with shuffled exemplar order.

---

## 3. Results Across Benchmarks

### Arithmetic Reasoning (Table 1 -- Key Numbers)

**GSM8K (the headline result):**

| Model | Standard | CoT | Improvement |
|---|---|---|---|
| UL2 20B | 4.1 | 4.4 | +0.3 |
| LaMDA 137B | 6.5 | 14.3 | +7.8 |
| GPT-3 175B | 15.6 | 46.9 | **+31.3** |
| Codex | 19.7 | 63.1 | **+43.4** |
| PaLM 540B | 17.9 | 56.9 | **+39.0** |
| Prior best (finetuned) | 55.0 | -- | -- |

PaLM 540B with CoT (56.9%) surpassed the prior SOTA of finetuned GPT-3 with a verifier (55%). This is the paper's most striking result: a prompting-only method beating a finetuned model.

**SVAMP:**
- PaLM 540B: 69.4 standard -> 79.0 CoT (+9.6)
- GPT-3 175B: 65.7 -> 68.9 (+3.2)

**MAWPS:**
- PaLM 540B: 79.2 -> 93.3 (+14.2)
- Codex: 78.7 -> 92.6 (+13.9)

**Key pattern:** CoT gains are largest on the hardest benchmarks (GSM8K) and smallest on easy ones (SingleOp subset of MAWPS). When standard prompting already achieves 90%+, there is little room for improvement.

### Commonsense Reasoning (Figure 7)

For PaLM 540B with CoT:
- **StrategyQA:** 75.6% (vs. prior SOTA 69.4%)
- **Sports Understanding:** 95.4% (vs. unaided human 84%)
- **Date Understanding:** strong gains with scale
- **CSQA:** minimal gain (already high baseline)
- **SayCan:** improvements over standard prompting

General pattern: scaling up model size improved standard prompting, and CoT led to further gains on top, with improvements largest for PaLM 540B.

### Symbolic Reasoning (Figure 8)

**In-domain (same # of steps as exemplars):**
- PaLM 540B with CoT achieves near 100% on both last letter concatenation and coin flip.
- Standard prompting fails on last letter concatenation.

**Out-of-domain (more steps than exemplars):**
- Standard prompting fails completely on both tasks.
- CoT achieves upward scaling curves with model size, demonstrating **length generalization** -- the model can generalize the reasoning pattern to longer sequences than seen in the exemplars.
- However, OOD performance is lower than in-domain, as expected.

---

## 4. Scaling Behavior: The Emergence Threshold

This is one of the paper's most important findings and arguably its most theoretically significant contribution.

### The ~100B Parameter Threshold

CoT is an **emergent ability** of model scale (Wei et al., 2022b). Specifically:

- For models **smaller than ~10B parameters**, CoT either has no effect or **hurts performance**. Small models produce "fluent but illogical chains of thought."
- Performance gains begin to appear around **~60-100B parameters**.
- The largest gains appear at **540B** (PaLM) and **175B** (GPT-3).

This is visible in Figure 4: the scaling curves for CoT are essentially flat (or negative) for small models, then shoot upward at large scale. Standard prompting scaling curves are comparatively flat throughout.

### Why Does Scale Matter?

The paper's Appendix A.1 provides a preliminary error analysis. They manually read 45 errors from PaLM 62B and categorized them:

- **Semantic understanding errors:** 20 errors (62B made them; 540B fixed 6)
- **One step missing errors:** 18 errors (62B made them; 540B fixed 12)
- **Other errors** (hallucinations, repetitions, symbol mapping): 7 errors (540B fixed 4)

The authors' interpretation: successful CoT reasoning is a **compound emergent phenomenon** that requires the simultaneous presence of multiple capabilities:
1. Semantic understanding (parsing the problem correctly)
2. Symbol mapping (connecting words to mathematical operations)
3. Arithmetic ability (performing calculations correctly)
4. Staying on topic / coherence
5. Faithfulness (the reasoning actually driving the answer)

Small models lack several of these simultaneously. Scale appears to provide all of them above a threshold. This is consistent with the "emergent abilities" framework -- these capabilities may each have their own scaling curves, and CoT requires all of them to be above some minimum level.

### Three Observations About Small Model Failure

1. Small models fail even at **symbol mapping** -- even on symbolic reasoning tasks where the logical structure is provided in the exemplars, they cannot generalize to new symbols.
2. Small models have **inherently weaker arithmetic abilities** (per Brown et al., 2020).
3. Small models often produce outputs that **cannot be parsed** -- repetitive loops, never arriving at a final answer.

---

## 5. Ablation Studies

The ablation study (Section 3.3, Figure 5) is methodologically careful and reveals what components of CoT matter.

### Ablation 1: Equation Only

Instead of natural language reasoning, the model is prompted to output only the mathematical equation.

**Result:** Equation-only helps on easy datasets (SVAMP, ASDiv, MAWPS -- one or two step problems where the equation can be directly derived from the question). But it **does not help on GSM8K**, because GSM8K problems are too semantically complex to translate directly into a single equation.

**Interpretation:** Natural language reasoning is doing something that pure symbolic translation cannot -- it allows the model to "reason about each part of the question via intermediate steps in natural language" (Appendix A.4). The natural language serves as a bridge between the problem semantics and the formal computation.

### Ablation 2: Variable Compute Only

The model outputs a sequence of dots ("...") equal in length to the equation needed, then gives the answer. This isolates the effect of "spending more tokens" from the content of those tokens.

**Result:** Performs about the same as standard prompting (no improvement).

**Interpretation:** The benefit of CoT is NOT simply "more computation." The content of the intermediate tokens matters. This rules out a purely computational explanation. (Though note: this test is somewhat crude -- the dots have no semantic content, whereas one could imagine other forms of "useful filler" that might help.)

### Ablation 3: Chain of Thought After Answer

The chain of thought is placed **after** the answer instead of before it. The model must commit to an answer first, then explain.

**Result:** Performs about the same as standard prompting.

**Interpretation:** The sequential structure matters. The reasoning must come before the answer -- the model needs to "work through" the problem before committing to a solution. The chain of thought is not merely "activating relevant knowledge" -- it is providing a sequential scaffolding that the answer then depends on.

This is a critically important ablation. It shows CoT is not just a knowledge retrieval trick. The ordering -- reasoning THEN answer -- is essential. The output tokens genuinely function as intermediate computation.

---

## 6. Robustness Analysis

### Different Annotators (Section 3.4, Figure 6)

Three co-authors independently wrote chains of thought for the same exemplars. Additionally, Annotator A wrote a concise version following the style of Cobbe et al. (2021).

**Result:** All variants outperformed standard prompting by a large margin, though there is variance among them. The coin flip task showed the most variance (99.6% for Annotator A vs. 71.4% for Annotator C).

**Interpretation:** CoT is robust to annotator style but not completely insensitive. Prompt engineering still matters for some tasks.

### Different Exemplars

Three sets of 8 exemplars randomly sampled from the GSM8K training set (which already includes reasoning chains from crowd workers).

**Result:** All three sets outperformed standard prompting and performed comparably to the manually written exemplars.

**Interpretation:** CoT does not depend on a specific set of exemplars or on machine learning expertise in writing them.

### Different Number of Exemplars (Figure 11)

Gains from CoT generally hold across varying numbers of few-shot exemplars. Increasing standard prompting exemplars from 8 to 16 did NOT close the gap with CoT prompting.

### Cross-Model Transfer

Same prompts work across LaMDA, GPT-3, and PaLM for most benchmarks. Exceptions: CSQA and StrategyQA for GPT-3. This suggests the method is somewhat model-agnostic but not perfectly so.

---

## 7. Error Analysis

### LaMDA 137B Error Analysis on GSM8K (Section 3.2)

**50 correct examples examined:** All had logically and mathematically correct chains of thought (except 2 that coincidentally arrived at the correct answer).

**50 incorrect examples examined:**
- **46% almost correct:** Minor mistakes -- calculator error, symbol mapping error, one reasoning step missing.
- **54% major errors:** Semantic understanding failures, coherence breakdowns.

### PaLM 62B Error Analysis (Appendix A.1, Figure 9)

45 errors categorized:
- **Semantic understanding:** 20 errors (540B fixes 6 of them)
- **One step missing:** 18 errors (540B fixes 12 of them)
- **Other** (hallucinations, repetitive outputs, symbol mapping): 7 errors (540B fixes 4)

Scaling from 62B to 540B fixes a substantial portion across all categories. The "one step missing" category is most responsive to scale -- the model at 540B can track longer reasoning chains.

### What Remains Even with CoT

Even with the best models and CoT:
- GSM8K solve rate is 56.9% (PaLM 540B) -- still far from perfect
- The model makes arithmetic errors, misunderstands semantics, skips steps
- Crucially: **there is no guarantee that the reasoning chain is faithful** to the model's actual computation (more on this below)

---

## 8. Information-Theoretic and Cybernetic Analysis

*[Note: This section contains my own analysis, extending beyond what the paper explicitly states.]*

### 8a. Requisite Variety (Ashby's Law)

Standard prompting constrains the model's output to a direct answer -- the response space has low variety. CoT dramatically expands the response variety: the model can produce any sequence of reasoning tokens before committing to an answer.

In Ashby's terms: the **regulator** (the model producing an answer) must have at least as much variety as the **disturbance** (the complexity of the problem). A multi-step math problem is a high-variety disturbance. Standard prompting forces a low-variety response (just the answer). CoT unlocks the variety needed to match the problem's complexity.

The ablation showing that "variable compute only" (dots) does not help is important here: it is not raw variety (more tokens) that matters, but **meaningful variety** -- tokens that carry semantic content relevant to the regulation task. Unstructured variety is useless.

### 8b. Working Memory / Scratchpad Hypothesis

CoT can be interpreted as **using output tokens as external working memory**. Transformers have limited implicit "working memory" -- their computation is bounded by depth (number of layers) and width. For problems requiring more sequential reasoning steps than the architecture can perform in a single forward pass, the model is fundamentally limited.

CoT circumvents this by externalizing intermediate results into the token sequence. Each generated token becomes part of the context for subsequent generation. The model is effectively using its own output as a **scratchpad** (Nye et al., 2021 is cited as related work on this idea).

This is analogous to how humans use pen and paper for multi-step arithmetic -- offloading working memory to an external medium. The output sequence becomes an external memory store that the attention mechanism can read from.

### 8c. Decomposition of Regulation

From a control-theoretic perspective, CoT decomposes a single complex regulation problem (question -> answer) into a cascade of simpler sub-regulations (question -> step1 -> step2 -> ... -> answer). Each step needs to regulate only a small part of the problem.

This is the principle of **hierarchical/sequential decomposition** in cybernetics. A regulator that cannot handle the full complexity of a problem in one shot can succeed by breaking it into a sequence of simpler regulations, each within its capacity.

The ablation evidence strongly supports this: equation-only prompting fails on hard problems (GSM8K) because it still requires a single-shot translation from semantics to formal expression. CoT succeeds because it allows stepwise bridging.

### 8d. Feedback Structure

**Standard prompting:** Open-loop. The model generates an answer with no opportunity to use intermediate results as feedback.

**CoT prompting:** Introduces a form of **sequential self-generated feedback**. Each intermediate token conditions the generation of the next. The model can "see" what it has reasoned so far and build upon it. This is not true closed-loop feedback (there is no external verification signal), but it creates an **internal feedforward chain** where earlier outputs constrain later outputs.

The "chain of thought after answer" ablation is the key evidence: when the reasoning comes after the answer, the feedback structure is broken. The answer cannot benefit from the reasoning if the reasoning has not yet been generated. The temporal ordering is essential because autoregressive generation is causal.

This has a cybernetic structure reminiscent of Beer's Viable System Model: the system creates its own context progressively, and each level of reasoning informs the next.

---

## 9. Connection to Bateson's Levels of Learning

### Is CoT Learning I or Learning II?

**Learning I** (Bateson): Simple conditioning -- the organism learns to respond correctly to a stimulus within a fixed context of contingency. The mapping from stimulus to response changes, but the framework for interpreting stimuli does not.

**Learning II** (Bateson): Learning to learn -- the organism learns to recognize and adapt to the *type* of contingency context it is in. Changes in the process of Learning I.

CoT as demonstrated in this paper is primarily **Learning I**. The model is given demonstrations and learns (via in-context learning) to produce a specific type of output format (reasoning chains). It is conditioning on the exemplars. The "context of contingency" is set by the human prompt designer.

However, there are hints of something deeper:

1. **OOD generalization in symbolic reasoning** suggests the model is not merely copying the exemplar structure but has learned a *transferable pattern* -- apply the reasoning template to novel inputs with more steps. This is arguably a weak form of Learning II: learning the "type of game" (step-by-step symbol manipulation) rather than just specific responses.

2. **Cross-task transfer of the CoT format** -- the same basic idea (write reasoning before answering) works across arithmetic, commonsense, and symbolic tasks. The model is not learning task-specific responses but a general *mode of responding*. This meta-pattern is Learning II-like.

3. The **emergence at scale** is interesting from a Batesonian perspective. Small models cannot do Learning I with CoT (they produce illogical chains). Large models can. This suggests that the capacity for CoT-style Learning I is itself an emergent property -- perhaps a form of Learning II that develops during pretraining at sufficient scale.

But importantly: the model is **not choosing to use CoT on its own**. It must be prompted. It does not autonomously recognize that a problem requires stepwise reasoning and switch modes. That would be Learning II proper. Zero-shot CoT ("Let's think step by step" -- Kojima et al., 2022, a follow-up paper) moves closer to this, as a single generic instruction triggers the mode shift.

---

## 10. The Faithful Reasoning Problem

### The Core Issue

The paper explicitly acknowledges: "although chain of thought emulates the thought processes of human reasoners, this does not answer whether the neural network is actually 'reasoning.'"

The generated chain of thought may not be **faithful** to the model's actual internal computation. The model might:
1. Arrive at the answer through some internal process, then generate a plausible-looking reasoning chain as post-hoc rationalization.
2. Generate correct-sounding reasoning that leads to a wrong answer.
3. Generate incorrect reasoning that coincidentally leads to a correct answer (they found 2 such cases out of 50 in their analysis).

### Evidence from the Paper

- In the error analysis, 46% of incorrect answers had chains of thought that were "almost correct" -- minor errors in an otherwise sound chain. This suggests the chains are at least somewhat functional, not purely decorative.
- The "chain of thought after answer" ablation is indirect evidence for faithfulness: if the chain were purely post-hoc, putting it after the answer should not change the answer quality. But it does -- performance drops to baseline. This suggests the chain is causally involved in producing the answer.
- However, this does not prove the chain reflects the *actual internal computation*. The model might be doing something different internally while the chain provides useful conditioning context.

### Why This Matters

This is a deep problem for interpretability and safety:
- If CoT is faithful, it provides genuine interpretability -- you can read the model's reasoning.
- If CoT is confabulatory, it is actively misleading -- it creates an illusion of transparency.
- The truth is likely somewhere in between and may vary by problem and model.

Subsequent work (Turpin et al., 2023; Lanham et al., 2023) has investigated this more thoroughly and found that CoT can be influenced by biased features in ways not reflected in the stated reasoning -- evidence of unfaithfulness.

---

## 11. How CoT Set the Stage for Subsequent Work

### Direct Descendants

1. **Self-Consistency (Wang et al., 2022a):** Instead of greedy decoding a single chain, sample multiple chains and take the majority vote on the final answer. Exploits the fact that correct reasoning paths are more likely to converge on the same answer. This is already mentioned in the paper as follow-up work.

2. **Zero-Shot CoT (Kojima et al., 2022):** "Let's think step by step" -- no exemplars needed, just an instruction. Removes the need for manually written chains of thought. Suggests the capability is latent in the model and can be triggered by simple instructions.

3. **Least-to-Most Prompting (Zhou et al., 2023):** Explicit problem decomposition before solving -- first break the problem into subproblems, then solve them sequentially.

### The ReAct Lineage

**ReAct (Yao et al., 2023):** Interleaves reasoning (Thought) with acting (Action) and observing (Observation). CoT provides the "Thought" component. The key extension: CoT is purely internal, but ReAct connects reasoning to **external tools and environments**. This is the bridge from passive reasoning to agentic behavior.

From a cybernetic perspective, ReAct adds genuine **closed-loop feedback**: the model reasons, acts, observes the result, and reasons again. CoT is open-loop sequential reasoning; ReAct closes the loop with environmental feedback.

### Reflexion (Shinn et al., 2023)

Adds **self-reflection** on previous failures. The model attempts a task, evaluates its own performance, generates reflective feedback, and tries again. This is CoT applied recursively to the model's own output history.

In Bateson's terms, this is moving toward **Learning II**: the model is not just reasoning about the problem but reasoning about *how it reasoned* about the problem.

### Tree of Thoughts (Yao et al., 2023)

Generalizes CoT from a single linear chain to a **tree of reasoning paths**. The model can explore multiple branches, evaluate them, and backtrack. This adds search and planning to the CoT framework.

From a cybernetic perspective: CoT is a sequential feedforward chain. Tree of Thoughts introduces branching and evaluation, creating a structure more like Ashby's homeostat -- the system explores multiple regulatory strategies and selects among them.

### The Broader Trajectory

CoT -> Self-Consistency -> Zero-Shot CoT -> ReAct -> Reflexion -> Tree of Thoughts represents a progression:

1. **CoT:** Externalize reasoning into tokens (open-loop sequential)
2. **Self-Consistency:** Add statistical robustness via sampling (ensemble of open loops)
3. **ReAct:** Close the loop with environmental feedback (sensing-reasoning-acting cycle)
4. **Reflexion:** Close the loop with self-evaluation (meta-reasoning)
5. **Tree of Thoughts:** Add search and planning (exploring the space of possible regulations)

Each step increases the system's **requisite variety** and its ability to regulate against increasingly complex disturbances.

---

## 12. When Does CoT Help? (Conditions for Benefit)

The paper identifies three conditions for CoT to provide maximum benefit (Appendix A.3):

1. **The task is challenging and requires multi-step reasoning.** (Not trivial one-step problems.)
2. **A large language model is used.** (>~100B parameters.)
3. **The scaling curve for standard prompting is relatively flat.** (Standard prompting is failing to improve with scale, suggesting the bottleneck is not knowledge but reasoning structure.)

Conversely, CoT provides little benefit when:
- The task is easy (standard prompting already achieves >90%)
- The model is too small (<10B)
- The task does not require sequential reasoning

---

## 13. Limitations Acknowledged by the Authors

1. **Not clear if the model is "actually reasoning"** -- faithfulness problem (see above).
2. **Annotation cost** -- manually writing chains of thought is cheap for few-shot but expensive for finetuning. (Addressed by zero-shot CoT and self-consistency in follow-up work.)
3. **No guarantee of correct reasoning paths** -- can produce correct-looking but wrong reasoning, leading to both correct and incorrect answers.
4. **Only works at large scale** -- costly to serve, not accessible for smaller deployments.
5. **The correct chain of thought is not guaranteed** -- even with CoT, the model can (and does) make errors. CoT improves the rate but does not solve the problem.

---

## 14. Key Takeaways for Cybernetics-Agents Research

1. **CoT is fundamentally a variety amplification mechanism.** It expands the model's output space to match the variety of complex problems. This is a direct application of Ashby's Law of Requisite Variety.

2. **CoT converts depth-limited computation into length-extended computation.** The transformer has fixed depth, but CoT allows it to perform sequential reasoning across many tokens. This is a form of **externalized recursion**.

3. **The content of intermediate tokens matters, not just their number.** This rules out a purely mechanical "more compute" explanation and points to the semantic content as carrying regulatory information.

4. **CoT creates a sequential feedforward structure but not true feedback.** The progression from CoT to ReAct to Reflexion is the progression from open-loop to closed-loop regulation.

5. **The emergence at scale suggests CoT requires a constellation of sub-capabilities.** It is not a single skill but a coordination of semantic understanding, arithmetic ability, coherence, and symbol mapping. This is analogous to the "requisite variety" of the regulator itself -- the model must have sufficient internal variety before it can produce useful external variety.

6. **The faithful reasoning problem is the central open question.** If CoT is not faithful, then the interpretability benefit is illusory, and we are building agentic systems on foundations we cannot inspect. This connects to cybernetic concerns about observability of the regulator's internal state.

---

## Appendix: Key Numerical Results Summary Table

| Benchmark | Model | Standard | CoT | Gain |
|---|---|---|---|---|
| GSM8K | PaLM 540B | 17.9% | 56.9% | +39.0 |
| GSM8K | GPT-3 175B | 15.6% | 46.9% | +31.3 |
| GSM8K | Codex | 19.7% | 63.1% | +43.4 |
| SVAMP | PaLM 540B | 69.4% | 79.0% | +9.6 |
| MAWPS | PaLM 540B | 79.2% | 93.3% | +14.2 |
| StrategyQA | PaLM 540B | -- | 75.6% | (vs. SOTA 69.4%) |
| Sports | PaLM 540B | -- | 95.4% | (vs. human 84%) |
| GSM8K | Prior SOTA (finetuned) | 55.0% | -- | CoT beats this |
