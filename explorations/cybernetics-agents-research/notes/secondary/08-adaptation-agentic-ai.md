# Adaptation of Agentic AI

## Citation
(46+ authors led by Jiawei Han). (2025). "Adaptation of Agentic AI." arXiv:2512.16301. Institutions: UIUC, Stanford, Princeton, Harvard, UC Berkeley, Caltech, UW, UCSD, Georgia Tech, Northwestern, TAMU.

## Summary

A comprehensive survey unifying fragmented research on how LLM-based agents improve beyond pretraining. Introduces a 2×2 taxonomy along two axes: what gets optimized (agent vs. tool) and where feedback signals originate (execution-grounded vs. output-evaluated). Covers post-training (SFT, RL with verifiable rewards, preference optimization), adaptive memory, and reusable skills.

## Key Arguments & Taxonomy

**Four paradigms of adaptation:**

| | Execution-grounded signals | Output-evaluated signals |
|---|---|---|
| **Agent adaptation** | A1: Agent optimized via tool execution outcomes | A2: Agent optimized via output quality evaluation |
| **Tool adaptation** | T1: Tools trained independently of frozen agent | T2: Frozen agent supervises tool training |

1. **A1 (Tool-Execution → Agent):** Dense, causally grounded per-action feedback. E.g., Toolformer, DeepSeek-R1. Optimizes specific tool calls but may miss system-level failures.

2. **A2 (Output-Evaluation → Agent):** Episode-level rewards from answer correctness. E.g., Search-R1. Captures end-to-end performance but complicates credit assignment.

3. **T1 (Agent-Agnostic Tool):** Tools trained on broad data distributions, plug-and-play. Generalizes well across agents but can't adapt to specific agent needs.

4. **T2 (Agent-Supervised Tool):** Agent supervises tool training while remaining frozen. Can match A2 accuracy with far fewer examples (in retrieval settings).

**Key tension:** A1 offers "mechanistic precision" (per-action credit) while A2 offers "strategic flexibility" (end-to-end optimization). This maps directly onto the cybernetic tension between local and global regulation.

## Connection to Our Research

This paper doesn't use cybernetic terminology, but its framework is deeply cybernetic in structure:

- **Feedback as the core mechanism.** The entire taxonomy is organized around feedback — where it comes from, what it modifies. This is regulation in Ashby's sense.
- **A1/A2 ↔ PCT hierarchy levels.** A1 optimizes lower-level perceptual variables (specific tool calls), while A2 optimizes higher-level variables (overall answer quality). This mirrors PCT's hierarchy where higher levels set reference values for lower ones.
- **Stability concerns.** The paper explicitly discusses:
  - Catastrophic forgetting (loss of prior capabilities during adaptation) — analogous to a system losing viability when adapting
  - Co-adaptation stability (agent and tool simultaneously changing) — coupled oscillations in a cybernetic feedback system
  - Continual adaptation under non-stationary distributions — ultrastability in Ashby's sense
- **Requisite variety in adaptation.** T1 tools trained on broad distributions have more variety but less specificity. A1 methods have less variety but more precision. The framework implicitly navigates the variety-specificity tradeoff.
- **Missing cybernetic framing.** The paper would benefit from explicit cybernetic analysis — its "stability" concerns are essentially Ashby's ultrastability; its feedback taxonomy is regulation; its co-adaptation challenges are coupled control loops.

## Relevant Formalisms

- **Signal fidelity gradient**: Dense per-action feedback (A1) → sparse episode-level reward (A2)
- **Modularity tradeoff**: Tightly coupled agent-tool adaptation (A1) vs. loosely coupled modular adaptation (T1/T2)
- **Convergence/stability guarantees**: Discussed but not formally provided — identified as an open challenge

## Key References to Chase

1. **Schick, T. et al. (2024).** "Toolformer." — Pioneering work on tool-augmented LLMs (A1 paradigm).
2. **DeepSeek-AI (2025).** "DeepSeek-R1." — Key example of RL with verifiable rewards.
3. **Madaan, A. et al. (2023).** "Self-Refine." — Iterative self-improvement through feedback (connects to the IJCAI feedback survey).
