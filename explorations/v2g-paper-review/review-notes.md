# V2G Paper Review Notes

Paper: "Improving LM Generators via Validator-to-Generator Training"
Target venue: NeurIPS 2025
Date: 2026-03-03

---

## Overall Impression

The core idea is solid and well-motivated: LLMs validate better than they generate, so use the validation signal to improve generation. The same-prompt constraint is a clean methodological contribution that addresses a real flaw in prior work (RankAlign). The combination of ranking loss + NLL regularization + typicality correction is sensible engineering.

The draft is early-stage---most sections are TODO. Below are thoughts on Related Work and Introduction, which are the most developed sections.

---

## Related Work: What's There Now

The current related work has three sparse paragraphs:
1. **Generator-Validator Gap** - cites West et al. 2022, Li et al. 2024, Rodriguez et al. 2025
2. **Preference Learning** - cites RLHF (Ouyang 2022), DPO (Rafailov 2023)
3. **Self-Improvement** - one sentence, no citations

This needs substantial expansion. Below is a suggested structure with specific papers to discuss.

---

## Related Work: Recommended Structure

### 1. The Generator-Validator Gap (keep, expand)

**Core citations (already have):**
- West et al. 2022 (Symbolic Knowledge Distillation) - first to document the gap
- Li et al. 2024 (Benchmarking GV Consistency, ICLR) - systematic benchmarking, proposed consistency fine-tuning
- Rodriguez et al. 2025 (RankAlign) - ranking-based training to close the gap, the most direct predecessor

**Should add:**
- Gekhman et al. 2025 (Inside-Out, COLM 2025) - already in your .bib! Shows LLMs encode ~40% more factual knowledge internally than they express through generation. Directly supports the V2G premise: the model "knows" more than it can say.
- Kadavath et al. 2022 (Language Models Know What They Know) - already in .bib. Models can often assess their own correctness. Foundational for the idea that validation > generation.

**Narrative to build:** The gap is well-documented across multiple tasks and models. Prior work has measured it (West, Li, Kadavath, Gekhman) and attempted to close it (Li via consistency fine-tuning, Rodriguez via RankAlign). V2G improves on RankAlign by fixing the cross-prompt comparison issue and adding regularization.

**Key positioning question:** How does V2G differ from Li et al.'s "consistency fine-tuning"? Li et al. filter for instances where G and V agree and fine-tune on those. V2G instead uses V's rankings to construct preference pairs and does ranking-based training. This distinction should be made explicit.

### 2. Preference Optimization (keep, expand significantly)

**Core citations (already have):**
- RLHF: Ouyang et al. 2022
- DPO: Rafailov et al. 2023

**Should add:**
- Ziegler et al. 2019 and Stiennon et al. 2020 (already in .bib) - foundational RLHF work
- SLiC-HF (Zhao et al. 2023) - sequence likelihood calibration, uses ranking loss similar to V2G
- IPO (Azar et al. 2023) - Identity Policy Optimization, addresses DPO overfitting
- KTO (Ethayarajh et al. 2024) - Kahneman-Tversky Optimization, works with unpaired preferences
- ORPO (Hong et al. 2024) - Odds Ratio Preference Optimization

**Narrative:** V2G is doing preference optimization, but the preference signal comes from the model's own validator rather than from humans. This connects V2G to both the preference learning literature AND the self-improvement literature. The specific loss function (ranking + NLL) should be contextualized against these alternatives. Why ranking loss rather than DPO? This deserves explicit discussion.

### 3. Self-Improvement and Self-Play (expand significantly - currently almost empty)

**Should add:**
- Self-Rewarding Language Models (Yuan et al. 2024, ICML) - models generate their own reward signal for iterative training. Very close in spirit to V2G: the model judges its own outputs and improves from that signal. Probably the single closest existing work.
- SPIN (Chen et al. 2024, ICML) - Self-Play Fine-Tuning. Model plays against itself to improve. Related framing.
- ReST / REST^EM (Gulcehre et al. 2023; Singh et al. 2024, TMLR) - Reinforced Self-Training. Sample from model, filter by reward, fine-tune on filtered data. The generate-then-filter paradigm.
- STaR (Zelikman et al. 2022, NeurIPS) - Self-Taught Reasoner. Generate rationales, keep correct ones, fine-tune.
- V-STaR (Hosseini et al. 2024, COLM) - Trains verifiers alongside generators from self-generated data. Uses both correct and incorrect solutions to train a DPO verifier. Very directly relevant.
- Constitutional AI / RLAIF (Bai et al. 2022; Lee et al. 2023) - AI-generated feedback for alignment. Conceptually similar to using self-validation.

**Also consider:**
- Weaver / Saad-Falcon et al. 2025 - "Shrinking the Generation-Verification Gap with Weak Verifiers." Directly quantifies the gap: Llama 3.3 70B gets 82.8% pass@100 but only 42.9% on first sample. Very recent and directly relevant.
- Meta-Rewarding (Yuan et al. 2024, follow-up to Self-Rewarding) - adds meta-judging to prevent validator signal degradation over iterations. Addresses a potential failure mode of V2G-like approaches.

**Narrative:** V2G sits in a family of methods where models improve from their own signal. The distinguishing feature is that V2G specifically exploits the *validation-generation asymmetry*---it's not just self-distillation or filtering, it's leveraging a capability the model demonstrably has (validation) to improve one it demonstrably lacks (generation). This is a sharper motivation than generic "self-improvement."

### 4. Verifiers and Test-Time Compute (new section to consider)

**Papers:**
- Cobbe et al. 2021 (GSM8K / training verifiers for math)
- Lightman et al. 2023 (Process reward models, ICLR 2024)
- Math-Shepherd (Wang et al. 2024, ACL) - automated process supervision, no human step-level labels
- Snell et al. 2024 (Scaling LLM test-time compute, ICLR 2025)
- GenRM (Hossu et al. 2024) - generative verifiers via next-token prediction, blurs generator/validator line

**Narrative:** Using verifiers at inference time (best-of-N sampling with a verifier) is a well-known technique. V2G is complementary: instead of using the validator at test time (which is expensive), you *bake the validator's knowledge into the generator* at training time. This gives you the quality improvement without the inference cost. This is a strong selling point worth highlighting.

### 5. Self-Distillation (optional, brief)

**Papers:**
- Born-Again Neural Networks (Furlanello et al. 2018, ICML) - same-architecture distillation can surpass teacher
- GKD / On-Policy Distillation (Agarwal et al. 2024, ICLR) - student trains on its own outputs with teacher feedback

**Narrative:** V2G can be viewed as a form of self-distillation where the "teacher" is the model's own validation mode. Brief mention to connect to this literature.

### 5. Typicality and Pointwise Mutual Information (optional, brief)

**Papers:**
- PMI-based decoding (e.g., Holtzman et al. 2021, Li et al. 2016 on MMI decoding)

**Narrative:** The typicality correction (subtracting unconditional log prob) is essentially PMI. This has precedent in decoding strategies. Brief mention is sufficient.

---

## Introduction: Thoughts

### What's there now:
- Defines generators vs validators
- Notes the gap (cites West 2022)
- Proposes V2G training
- Three contributions: (1) methodological issues in prior work, (2) same-prompt constraint, (3) improvements on tasks

### What I'd change:

**1. Lead with a concrete example.** The abstract generator/validator distinction is clear to people in the field but a concrete example lands harder. E.g.: "Ask an LLM to name a hypernym of 'dog' and it might say 'pet.' Ask it whether 'animal' is a hypernym of 'dog' and it readily confirms. The model *knows* 'animal' is the better answer---it just doesn't *say* it."

**2. Sharpen the "why this matters" angle.** The gap is not just a curiosity---it means models are leaving performance on the table. V2G is a way to recover that performance without additional annotation (no human labels needed, just the model's own validation signal). This is a practical advantage worth emphasizing early.

**3. Reframe contribution #1 more carefully.** The current text has a parenthetical "(OK this is maybe beating up too much on RankAlign?)" --- yes, probably. Rather than framing it as "we found flaws in prior work," frame it as "we identify that same-prompt constraints are critical for valid preference learning from model self-evaluation." The contribution is the insight + the fix, not the critique.

**4. Add a contribution about the regularization / typicality correction.** Currently contributions #1 and #2 are really the same thing (identifying the issue and proposing the fix). I'd restructure:
   - (1) We show that same-prompt constraints are necessary for valid V2G training
   - (2) We propose a training objective combining ranking loss with NLL regularization and typicality correction that prevents degenerate solutions
   - (3) We demonstrate improvements on [tasks]

**5. Consider a figure.** A schematic showing the V2G pipeline (generate candidates -> validate/rank -> construct preference pairs -> train) would help readers immediately grasp the approach. First figure in the paper should convey the whole idea.

---

## Other Observations

### On the "beating up on RankAlign" concern
The paper currently positions itself as fixing RankAlign's methodology. This is delicate because Rodriguez et al. 2025 is the most direct predecessor. I'd suggest:
- Acknowledge RankAlign as the primary inspiration
- Frame the same-prompt issue as a refinement/extension, not a correction
- Show ablation: V2G without same-prompt constraint (i.e., approximately RankAlign's setup) vs. with it. Let the numbers speak.

### On the typicality correction
Using GPT-2 for the unconditional probability baseline is a somewhat arbitrary choice. Why GPT-2 specifically? Is this just a convenience/size thing? If so, acknowledge that. If different base models for typicality give different results, that's worth exploring in ablations.

### On the task selection
Hypernymy, COLLIE, and QA are reasonable but fairly narrow. For NeurIPS, reviewers will want to see breadth. Consider adding:
- A reasoning/math task (to connect with the verifier literature)
- A factual knowledge task (to connect with Gekhman et al.'s "hidden knowledge" finding)
- Something with larger models (Gemma-2-2B is small; does V2G scale?)

### On the training objective
The combined loss has three terms with two lambda hyperparameters. Ablation over these is essential. Also: why ranking loss specifically, rather than DPO or another preference optimization objective? The choice should be motivated or at least compared against.

---

## Summary of Recommendations

| Priority | Item | Section |
|----------|------|---------|
| High | Expand Related Work with self-improvement and verifier literature | Related Work |
| High | Differentiate from Li et al. 2024 (consistency fine-tuning) | Related Work |
| High | Reframe contributions to be less adversarial toward RankAlign | Intro |
| High | Add concrete example to opening | Intro |
| Medium | Position V2G as "baking in" test-time verification | Intro / Related Work |
| Medium | Add figure showing the V2G pipeline | Intro |
| Medium | Motivate choice of ranking loss vs. DPO | Method / Related Work |
| Low | Discuss PMI connection for typicality correction | Method |
| Low | Consider additional tasks for breadth | Experiments |

---

## References

Already in the paper's .bib:
- West et al. "Symbolic Knowledge Distillation." NAACL 2022.
- Li et al. "Benchmarking and Improving Generator-Validator Consistency of Language Models." ICLR 2024.
- Rodriguez et al. "RankAlign: A Ranking View of the Generator-Validator Gap in LLMs." arXiv 2025.
- Gekhman et al. "Inside-Out: Hidden Factual Knowledge in LLMs." COLM 2025.
- Kadavath et al. "Language Models (Mostly) Know What They Know." arXiv 2022.
- Ouyang et al. "Training Language Models to Follow Instructions with Human Feedback." NeurIPS 2022.
- Rafailov et al. "Direct Preference Optimization (DPO)." NeurIPS 2023.
- Ziegler et al. "Fine-Tuning Language Models from Human Preferences." arXiv 2019.
- Stiennon et al. "Learning to Summarize with Human Feedback." NeurIPS 2020.
- Hu et al. "LoRA: Low-Rank Adaptation of Large Language Models." arXiv 2021.
- Yao et al. "COLLIE: Systematic Construction of Constrained Text Generation Tasks." ICLR 2024.
- Min et al. "AmbigQA: Answering Ambiguous Open-domain Questions." EMNLP 2020.
- Gemma Team. "Gemma 2." arXiv 2024.

Suggested additions -- Generator-Validator Gap:
- Saad-Falcon et al. "Shrinking the Generation-Verification Gap with Weak Verifiers (Weaver)." arXiv 2025. Quantifies the gap: Llama 3.3 70B gets 82.8% pass@100 but 42.9% first-sample.

Suggested additions -- Preference Optimization:
- Azar et al. "A General Theoretical Paradigm to Understand Learning from Human Preferences (IPO)." AISTATS 2024. Avoids DPO overfitting via identity mapping.
- Ethayarajh et al. "KTO: Model Alignment as Prospect Theoretic Optimization." ICML 2024. Binary signal (desirable/undesirable) instead of paired preferences.
- Zhao et al. "Calibrating Sequence Likelihood Improves Conditional Language Generation (SLiC-HF)." arXiv 2023. Ranking loss for preference optimization, similar to V2G.
- Hong et al. "ORPO: Monolithic Preference Optimization Without Reference Model." arXiv 2024.
- Meng et al. "SimPO: Simple Preference Optimization with a Reference-Free Reward." NeurIPS 2024.

Suggested additions -- Self-Improvement / Self-Play:
- Yuan et al. "Self-Rewarding Language Models." ICML 2024. Model judges itself, builds preference pairs, trains with DPO, iterates. Probably the closest existing work to V2G.
- Yuan et al. "Meta-Rewarding Language Models." arXiv 2024. Follow-up; adds meta-judging to prevent validator degradation.
- Chen et al. "Self-Play Fine-Tuning (SPIN)." ICML 2024. Model discriminates own outputs from human text.
- Gulcehre et al. "Reinforced Self-Training (ReST) for Language Modeling." arXiv 2023. Generate, score, fine-tune on high-scoring.
- Singh et al. "Beyond Human Data: Scaling Self-Training for Problem-Solving (ReST^EM)." TMLR 2024. ReST cast as EM.
- Zelikman et al. "STaR: Bootstrapping Reasoning With Reasoning." NeurIPS 2022. Generate rationales, keep correct, fine-tune.
- Hosseini et al. "V-STaR: Training Verifiers for Self-Taught Reasoners." COLM 2024. Trains DPO verifier from both correct and incorrect self-generated solutions.
- Bai et al. "Constitutional AI: Harmlessness from AI Feedback." arXiv 2022.
- Lee et al. "RLAIF: Scaling Reinforcement Learning from Human Feedback with AI Feedback." arXiv 2023.

Suggested additions -- Verifiers / Test-Time Compute:
- Cobbe et al. "Training Verifiers to Solve Math Word Problems (GSM8K)." arXiv 2021.
- Lightman et al. "Let's Verify Step by Step (Process Reward Models)." ICLR 2024.
- Wang et al. "Math-Shepherd: Verify and Reinforce LLMs Step-by-Step." ACL 2024.
- Snell et al. "Scaling LLM Test-Time Compute Optimally." ICLR 2025.
- Hossu et al. "Generative Verifiers: Reward Modeling as Next-Token Prediction (GenRM)." arXiv 2024.

Suggested additions -- Self-Distillation:
- Furlanello et al. "Born-Again Neural Networks." ICML 2018. Same-architecture distillation can surpass teacher.
- Agarwal et al. "On-Policy Distillation of Language Models (GKD)." ICLR 2024. Student trains on own outputs with teacher feedback.

Suggested additions -- Typicality / PMI:
- Holtzman et al. "Surface Form Competition." EMNLP 2021. PMI-based scoring for surface form frequency.
- Li et al. "A Diversity-Promoting Objective Function for Neural Conversation Models (MMI decoding)." NAACL 2016.
