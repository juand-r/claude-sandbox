# How Researchers Use LLMs: Datasets, Evidence, and Replication Strategies

**Date:** 2026-08-29

## Overview

This report synthesizes findings from six primary-source deep-dives into how scientists and CS researchers use LLMs in practice. It covers three questions: (1) what researchers are actually doing with AI — which models, agents, and workflows — based on empirical data; (2) whether anyone has replicated research workflows with Claude specifically, and what the most productive elicitation strategies are; (3) budget-conscious advice on whether to focus on ideation-only with expensive models or run a full pipeline with cheap ones.

The evidence base spans ~108K scientific papers, ~94K real-world use cases, ~128K GitHub projects, conversation logs from millions of users, and several controlled experiments. Sources are cited inline; full bibliographic details appear at the end.

---

## Part 1: What Are Researchers Actually Doing with AI?

### 1.1 Which Models Do Scientists Use?

The most direct evidence comes from Trišović (2026), who tracked 62 LLM variants across 108K citing papers from 2018–2025. The study classified every citation as either background reference or active adoption (using or extending the model's weights), with Bayesian error correction to handle the asymmetric false-positive risk inherent in rare-event classification.

**Key findings on model adoption:**

The study does not publish a simple "top N most-adopted models" ranking — its contribution is about lifecycle dynamics, not market share. What it does establish:

- Scientific adoption follows an **inverted-U trajectory**: usage rises after release, peaks, and declines as newer models appear. The aggregate peak across the 2019–2022 cohorts is at **3.58 years** (95% CI: 3.30–3.87) post-release.
- This lifecycle is **compressing rapidly**. Each successive release year is associated with a 27% shorter time-to-peak (p < 0.001) and a 23% shorter lifespan (p < 0.001). Concretely:

| Release cohort | Peak adoption (years) | Peak (months) |
|---|---|---|
| 2019 | 4.0 | 48 |
| 2020 | 3.4 | 40 |
| 2021 | 2.9 | 35 |
| 2022 | 2.0 | 24 |
| 2023 | 1.5 | 18 |

- **Release timing dominates model-level attributes** as a predictor of lifecycle dynamics. A decoder-only model and an encoder-decoder from the same year have more similar lifecycles than two decoder-only models released three years apart. Architecture, openness, and scale have little independent predictive power for time-to-peak or lifespan once release year is controlled.
- For **adoption volume** (as opposed to lifecycle shape), model size and API accessibility do matter: larger models and API-accessible models accumulate more total adoptions. Fine-tuned models accumulate fewer — they serve narrower communities.
- The ten pre-2022 models with highest **retention** (2025 adoption as fraction of their peak) are: RoBERTa Large (0.79), GPT-2 1.5B (0.78), DeBERTa (0.72), CodeT5 Base (0.67), XLM-RoBERTa (0.66), T5-3B (0.59), T5-11B (0.56), mT5-XXL (0.54), SciBERT (0.52), Transformer-XL (0.47). All are base/pretrained models spanning all three architecture classes.
- GPT-4 is classified as "still rising" (not yet peaked), so it's excluded from time-to-peak estimation.

**What the study does not answer:** which specific models are #1, #2, #3 by total adoption count, and whether adoption patterns differ by scientific field. The author cites a companion paper (Trišović et al., arXiv:2511.21739) and Pramanick et al. (2026) as sources for cross-field breakdowns.

**Implication for choosing a model today:** The compression trend means any model you adopt for a research workflow will likely be displaced within 1–2 years by something newer. This argues for building workflows that are **model-agnostic** — i.e., structured around the pipeline stages and prompt strategies rather than tightly coupled to one model's API quirks.

### 1.2 What Do Researchers Use LLMs For?

The REALM dataset (Cheng et al., ACL 2025 Findings) provides the most granular answer. It contains 94K curated real-world LLM use cases from Reddit (~15K) and news articles (~79K), spanning June 2020 through December 2024, annotated with a 14-category use-case taxonomy and 14 occupation groups.

**Use-case distribution** (share of use-case × occupation links):

| Category | News (%) | Reddit (%) |
|---|---|---|
| Content Synthesis (summarize, integrate) | 22.4 | 25.0 |
| Content Creation (generate text, code, data) | 17.9 | 23.8 |
| Process Automation | 14.9 | 14.8 |
| Decision Making | 14.9 | 11.6 |
| Digital Assistance | 9.1 | 11.5 |
| Everything else combined | 20.8 | 13.3 |

**Content Creation and Content Synthesis together account for ~40% of all LLM use** across both sources. This is consistent with writing assistance, summarization, and code generation being the dominant real-world applications.

**Scientists specifically** (the Life, Physical, and Social Science occupation group) are disproportionately linked to **Discovery**-type use cases — finding/uncovering new insights, exploratory analysis — which distinguishes them from Business/Management users (Decision Making, Process Automation) and Arts/Media users (Content Creation). The paper states: "professionals in Computer Science, Mathematics, Physical Sciences, and Social Sciences are notably involved in discovery-oriented tasks, highlighting the potential of LLMs to advance scientific research."

However, scientists represent a modest share of overall LLM discourse: ~4.8% of news links and ~4.3% of Reddit links. Computer & Mathematical occupations are much larger (17.3% news, 28.3% Reddit). After normalizing for each occupation's baseline share of media attention, Education, Healthcare, and Art & Media show the highest "exposure rates" — meaning LLM-related content is a disproportionately large fraction of what gets said about those fields.

**What REALM does not contain:** per-model usage breakdowns. Model names were used only as search keywords to filter the initial corpus, not analyzed as an output variable.

### 1.3 Coding Agents: Adoption and Usage Patterns

Two large-scale studies cover this territory in detail.

**GitHub-wide adoption (Robbes et al., 2026):** Analyzed 128,018 projects for coding agent adoption markers (config files like CLAUDE.md/.cursorrules/AGENTS.md, and commit-message signatures). Key numbers:

- **Overall adoption rate: 22–29%** of projects show evidence of coding-agent use as of February 2026 — reached in roughly one year from when full-fledged agents appeared.
- **Market share** by adopting-project count:

| Tool | Projects |
|---|---|
| Copilot | 13,890 |
| Claude Code | 12,053 |
| Generic/AGENTS.md (likely mostly Codex) | 5,325 |
| Cursor | 4,416 |
| Codex (explicit) | 2,965 |
| Gemini | 2,147 |

- **What agents do** (classification of 790 Claude Code commits): 35.7% new features, 29.9% bug fixes, 10.9% docs, 9.9% refactoring, 5.4% tests, 7.1% chores. Roughly double the feature-commit share of human-authored commits.
- **AI-assisted commits are substantially larger**: median 31 added lines (AI) vs. 11 (human). Commits touching 20+ files are ~30% more frequent for AI-assisted work.
- **Youngest projects adopt most**: 26.4% file-level adoption for projects ≤1 year old vs. 8.0% for projects >10 years old. Larger/more active projects adopt broadly but shallowly; smaller projects that adopt tend to go deep.

**Microsoft internal study (Murphy-Hill et al., 2026):** Studied Claude Code and GitHub Copilot CLI adoption among tens of thousands of engineers over ~4 months (Jan–Apr 2026).

- **Productivity lift: +24% merged PRs/engineer/day** (95% CI: +14.5%, +33.7%), with no decay over 4 months. Dose-response is monotone: +15% at 3 tool-use days/week, +50% at 5+ days/week.
- **Social exposure is the strongest adoption predictor**: +216% higher odds of trying the tool when >25% of skip-level peers already used it.
- **Neither study measures code quality directly.** Both explicitly flag this as the critical open question. The GitHub study found increased churn/complexity; a related Cursor study found increasing static-analysis warnings over time. The throughput gains are real, but whether they translate into better software is unresolved.

### 1.4 LLM-Based Scientific Agent Systems

The survey by Ren et al. (2025) catalogs 120+ LLM-based scientific agent systems. The most documented ones:

| System | Domain | Pipeline stages covered | Models used | Cost per paper |
|---|---|---|---|---|
| **AI Scientist v1** (Sakana, 2024) | ML/CS | Full: idea → code → experiments → paper → review | GPT-4-class / Claude 3.5 Sonnet | ~$15 |
| **AI Scientist v2** (Sakana, 2025) | ML/CS | Same + agentic tree search, VLM figure feedback | Claude 3.5 Sonnet | ~$20–25 |
| **Agent Laboratory** (Schmidgall, 2025) | ML research | Lit review → plan → data prep → experiments → report | GPT-4o / o1-mini / o1-preview | **$2.33** (GPT-4o) to $13.10 (o1-preview) |
| **ChemCrow** (2024) | Chemistry | Reasoning + 18 chemoinformatics tools | GPT-4 | Not reported |
| **Coscientist** (2023) | Chemistry | Lit search → planning → robotic synthesis | GPT-4 | Not reported |
| **ResearchAgent** (2024) | General | Lit-grounded ideation + multi-agent peer review | Various | Not reported |

**The typical automated pipeline** (from Agent Laboratory, the best-documented system):
1. Literature Review — agent queries arXiv, iteratively builds a curated paper set
2. Plan Formulation — "PhD" and "Postdoc" agents dialogue to consensus
3. Data Preparation — code generation for data loading (HuggingFace datasets)
4. Experiments — iterative code generation with LLM-reward scoring and self-reflection
5. Results Interpretation — joint interpretation by multiple agents
6. Report Writing — LaTeX scaffold, arXiv-grounded editing, automated NeurIPS-style review

**Which stages work vs. which don't:**
- **Most automatable**: code generation/debugging (objective compiler/test feedback), literature retrieval, data preparation, simulator-checkable steps.
- **Least automatable**: scientific idea novelty/significance judgment, safety-critical decisions, and (surprisingly) the literature review *execution* itself — Agent Laboratory's lit review phase failed 60–80% of the time depending on backend.
- **Human-in-the-loop raises quality but not significance**: Agent Laboratory's co-pilot mode raised human-rated quality/clarity/soundness, but significance scores barely moved (+0.03/10). Human oversight fixes presentation, not scientific substance.

**Quality reality check:** Agent Laboratory papers scored **3.5–4.0/10** on human-rated NeurIPS-style reviews (autonomous mode), vs. the NeurIPS 2024 acceptance average of **5.85–5.9/10**. Co-pilot mode reached 4.38/10 — still 1.45 points below the acceptance bar. The automated reviewer overestimated quality by 2.3 points. One AI Scientist v2 paper was accepted at an ICLR workshop (scores 6/7/6), but this is a single anecdote at a workshop, not the main conference.

### 1.5 The Prompt Dataset Landscape

Zhang et al. (EMNLP 2026 Findings) cataloged 129 LLM prompt datasets (>1.22 TB, >673M instances) into a structured taxonomy. Of these:

- **62.8% were created by LLM researchers** (for fine-tuning/benchmarking), 22.5% by end users, and only **14.7% by domain scientists**.
- The 19 domain-scientist datasets are overwhelmingly **math/science reasoning** corpora (SciInstruct, DeepMath, NuminaMath, PubMedQA, etc.) — i.e., they capture the *kind* of questions scientists ask LLMs, but they are not logs of scientists' actual LLM usage sessions.
- **Critical gap the authors identify**: no dataset in their catalogue contains actual researcher/scientist chat logs during real research work. Commercial assistant traffic (ChatGPT, Claude) is entirely absent. This is the biggest hole if your goal is studying research workflows specifically.

For actual conversation data, the best public resources remain **WildChat-4.8M** (Allen AI; 4.8M real ChatGPT conversations with metadata, through July 2025) and **LMSYS-Chat-1M** (1M conversations across 25 LLMs from Chatbot Arena). Neither is scientist-specific, but both can be filtered by topic.

---

## Part 2: Replicating Research Workflows with Claude

### 2.1 Has Anyone Done This?

Yes, on multiple fronts.

**Anthropic's own push (Claude Science, launched June 2026):**
- Jérôme Lecoq (Allen Institute, neuroscience) built a multi-agent "computational review template" with ~20 custom skills: sub-agents read thousands of papers, extract claims/quantitative findings into an evidence database, then co-write a long-form review section by section — a task previously taking up to two years.
- Biomni (Stanford) — a Claude-powered biomedical agent that completed a GWAS in 20 minutes (vs. months normally).
- Lundberg Lab (Stanford) — uses Claude for hypothesis generation in gene screening, testing whether Claude-generated candidate genes outperform human expert picks.
- Cheeseman Lab (MIT) — PhD student built "MozzareLLM" to automate CRISPR knockout screen interpretation.

**Independent replication studies:**
- **"Read the Paper, Write the Code"** (arXiv 2604.21965) — gives coding agents only a paper's methods section plus original data, has them reimplement the analysis from scratch. A Claude-Code-based configuration scored 93.4% task-level / 78.0% paper-level accuracy vs. 62.1%/35.8% for Codex-based approaches (numbers from search snippets, not verified against full paper).
- **"Coding-agents can replicate scientific ML papers"** (arXiv 2607.02134) — 12 workspaces, 158 recorded targets, all matched with report coverage across four ML papers.
- **Andy Hall** (political scientist) — Claude Code produced "a full empirical polisci study in an hour": downloaded original repo, translated Stata to Python, pulled updated data, reran analyses, generated tables/figures, did a literature review, and wrote a paper draft.
- **Scott Cunningham** (economist, Baylor) — running an ongoing public series "Claude Code for Economists" on Substack, including a coding audit that reimplements diff-in-diff pipelines across Python/R/Stata and a collaborative paper written end-to-end with Claude Code.
- **pedrohcgs/claude-code-my-workflow** on GitHub — a ready-made academic Claude Code template for LaTeX/Beamer + R work, with multi-agent review, quality gates, adversarial QA, and replication protocols baked in as skills.

### 2.2 Five Elicitation Strategies That Give the Most Coverage

Based on the ideation literature (Si et al., ICLR 2025; Chain-of-Ideas, EMNLP 2025; the 61-study synthesis by arXiv 2503.00946; and the IdeaBench/AI Idea Bench benchmarks):

**Strategy 1: Literature-Trajectory Prompting (Chain-of-Ideas style)**

Organize relevant papers into a chronological chain anchored on one seed paper — backward to its references, forward to its citations and follow-up work. Feed this trajectory to the LLM so it sees a *research arc*, not an unstructured pile. Then prompt for ideas that extend the trajectory's direction, fill gaps it reveals, or combine insights from different points along it. This is the closest to how researchers actually think about "what comes next" after reading a body of work.

*Coverage:* Best for incremental/extension ideas in a well-established area. Matches the Discovery use-case pattern identified in REALM for scientific occupations.

**Strategy 2: Multi-Persona Brainstorming (PersonaFlow style)**

Assign the LLM multiple expert personas (e.g., "domain expert in X," "methodologist in Y," "skeptic who worries about Z") and have it generate ideas from each perspective, then cross-pollinate. This directly targets the diversity problem: Si et al. (ICLR 2025) found LLM-generated ideas scored higher on novelty than expert human ideas but suffered from repetitiveness across generations. Multiple personas force divergent thinking.

*Coverage:* Best for cross-disciplinary or unconventional ideas. Addresses the main weakness of single-pass LLM ideation.

**Strategy 3: Generate-Then-Judge (Two-Pass)**

First pass: generate a large batch (20–50) of candidate ideas without any quality filter — maximize volume and variety. Second pass: score each idea on explicit criteria (novelty, feasibility, significance, testability) using a separate prompt or a different model. This mirrors classic brainstorming theory and is recommended by both the HBR analysis of LLM ideation and the Wharton "Ideas are Dimes a Dozen" study, which found GPT-4's *best* outputs from a large batch beat human best-effort, even when its median was comparable.

*Coverage:* Best overall general-purpose strategy. The most robust to model choice since even weaker models can contribute useful ideas to a big batch that a strong judge later filters.

**Strategy 4: Actor-Critic with Iterative Refinement (ResearchAgent / Anthropic pattern)**

Use two agents: one generates a research proposal, the other reviews it as a simulated peer reviewer (with explicit review criteria: novelty, soundness, significance, clarity). Iterate 2–3 rounds. This is the pattern Anthropic's own Claude Science team uses (actor-critic agent pairs), and it directly addresses the finding that LLMs are poor at self-evaluating their own ideas (Si et al.) by separating generation from judgment.

*Coverage:* Best for producing polished, defensible proposals rather than raw idea lists. Most closely simulates the actual peer-review loop.

**Strategy 5: Structured Proposal Elicitation**

Prompt the LLM to produce not just an idea but a structured research proposal with explicit sections: problem statement, hypothesis, proposed method, expected contributions, key experiments, anticipated results, limitations, and related work. This forces the model to think through feasibility (the weakest dimension in benchmarks — consistently below 0.5 on IdeaBench) and produces output that's immediately usable as a working document rather than requiring separate elaboration.

*Coverage:* Best for the "ideation-only" workflow — produces a document you can evaluate, share, and act on without running experiments. This is the strategy most aligned with what REALM data shows scientists actually do: Discovery-oriented tasks where the LLM helps formulate and structure what to investigate.

**Combining strategies:** Strategies 1–3 are complementary (trajectory context → diverse generation → quality filtering). Strategy 4 takes the best outputs from 3 and polishes them. Strategy 5 is the output format for the final deliverable. A complete ideation workflow would chain: 1 → 2 → 3 → 4 → 5.

---

## Part 3: Budget Advice

### 3.1 The Cost Landscape

| Approach | Documented cost | Quality (human-rated) |
|---|---|---|
| AI Scientist v1, full pipeline, GPT-4o | ~$15/paper | Not formally scored |
| AI Scientist v2, full pipeline, Claude 3.5 Sonnet | ~$20–25/paper | One ICLR workshop acceptance (6.33/10) |
| Agent Laboratory, full pipeline, GPT-4o | $2.33/paper | 3.5–4.0/10 (NeurIPS reviewer scale) |
| Agent Laboratory, full pipeline, o1-preview | $13.10/paper | 3.5–4.0/10 (same — marginal quality gain over GPT-4o) |
| Agent Laboratory, co-pilot mode (human-in-loop) | Same compute + human time | 4.38/10 (still 1.45 pts below NeurIPS acceptance) |

**Per-phase cost breakdown** (Agent Laboratory, GPT-4o): Literature Review $0.12, Plan $0.03, Data Prep $0.09, **Report Writing $1.73** (74% of total cost). The writing phase dominates regardless of backend — $9.58 for o1-preview. Experimentation cost is not separately reported but is implicit in the total minus the other phases.

### 3.2 The Critical Tradeoff

No study has run a head-to-head comparison of "ideation-only with expensive model" vs. "full pipeline with cheap models" on research-quality outcomes. This is an open gap. But the evidence points strongly in one direction:

**The case for ideation-only with the best model available:**

1. **Feasibility degrades more than novelty with cheaper models.** IdeaBench testing found small models (Llama 3.1 8B) scored well on novelty but poorly on feasibility, generating "large amounts of irrelevant or incoherent text." The novelty/feasibility gap is a robust finding across benchmarks: LLMs commonly score above 0.6 on novelty but below 0.5 on feasibility.

2. **The full pipeline doesn't produce publishable work anyway.** Agent Laboratory's best configuration (o1-preview + human-in-the-loop) scored 4.38/10, vs. the NeurIPS acceptance bar of ~5.85/10. You're not going to get a paper out of the cheap pipeline alone. The value of the full pipeline is as a *draft* or *prototype* that a human researcher then substantially reworks — and at that point, you're doing most of the real work yourself regardless.

3. **Self-evaluation is unreliable at every scale.** The automated reviewer overestimated quality by 2.3 points (6.1 vs. 3.8 human score). If even a strong model can't reliably judge its own output, a cheap-model pipeline (where both generation *and* judging are weak) compounds the unreliability. You need a human in the judgment loop, and at that point you might as well invest the compute budget in the stage where model quality matters most: ideation.

4. **The literature review phase is the most failure-prone.** Agent Laboratory's lit review failed 60–80% of the time. This is the stage that requires the most world knowledge and reasoning — exactly where model quality matters and where cheap models will fail worst.

5. **Report writing dominates pipeline cost.** At $1.73 of $2.33 (GPT-4o), writing is 74% of the total. If you skip report writing (because you'll write the actual paper yourself), the remaining pipeline stages cost ~$0.60. At that price point, the "full pipeline with cheap models" savings are negligible — you might as well use the best model for the ~$0.60 worth of ideation/planning and skip the automated writing entirely.

**The case for the full pipeline with cheap models (weaker, but real):**

1. **FrugalGPT-style cascading** (cheap model first, escalate when uncertain) can match GPT-4 accuracy at up to 98% cost reduction on general LLM tasks. If you built a smart router, you could potentially run most of the mechanical stages (data prep, boilerplate code, formatting) with a cheap model and reserve the expensive model for ideation and judgment.

2. **The full pipeline produces artifacts** — code, data, preliminary results — that inform the ideation process. Ideas generated without any experimental grounding tend to be more novel but less feasible. Running even rough experiments can surface practical constraints that reshape the research direction productively.

3. **GPT-4o already costs only $2.33/paper** in Agent Laboratory. "Cheap models" might save you $1–2 per paper at the cost of substantially worse output. The absolute dollars are already low enough that the cost difference is unlikely to matter unless you're running hundreds of papers.

### 3.3 My Recommendation

**Do ideation-only with the best model, but structure it carefully.**

Here's why: The full pipeline's output quality (3.5–4.0/10) is too far below the publishability bar (~5.85/10) to be useful as-is. You'd have to rework it so extensively that you lose the time savings. Meanwhile, the ideation stage is where model quality matters most (feasibility, coherence, world knowledge) and where the absolute compute cost is lowest (~$0.12–$0.60 per run).

**Concrete workflow I'd suggest:**

1. **Seed with literature trajectories** (Strategy 1): Feed 5–10 key papers into Claude as a research trajectory. Use the extended context window.
2. **Multi-persona brainstorm** (Strategy 2): Generate 20–30 candidate ideas across 3–4 expert personas.
3. **Filter with a separate judge pass** (Strategy 3): Score each idea on novelty, feasibility, significance, testability. Keep the top 5.
4. **Refine via actor-critic** (Strategy 4): Take the top 5 and run 2–3 rounds of proposal → review → revision.
5. **Produce structured proposals** (Strategy 5): Final output is a full research proposal for each surviving idea: problem statement, hypothesis, method, expected contributions, experiments, related work, abstract.

**What this gives you:** A portfolio of 3–5 fully elaborated research proposals, each grounded in real literature, stress-tested against reviewer objections, and structured enough to evaluate or hand to a collaborator. Total compute cost: probably $1–5 depending on context length and iteration count.

**What you lose vs. the full pipeline:** Preliminary experimental results, code prototypes, and the "reality check" of running experiments. You can partially compensate by asking Claude to write *pseudocode* or *experimental plans* with expected failure modes, without actually executing them.

**If you do want to run some experiments cheaply:** Use Claude for ideation (the first 5 steps above), then use a cheap model (GPT-4o-mini, Haiku, or an open model via Ollama) for the mechanical parts: data loading code, boilerplate, simple analysis scripts. Keep Claude for interpreting results and revising the proposal based on findings. This hybrid approach follows the FrugalGPT principle: expensive model where judgment matters, cheap model where it's just code execution.

---

## Key Datasets and Resources

### For studying how people use LLMs
| Dataset | Size | What it captures | Link |
|---|---|---|---|
| WildChat-4.8M | 4.8M conversations | Real ChatGPT conversations with metadata (geo, language, model) | [HuggingFace](https://huggingface.co/datasets/allenai/WildChat-4.8M) |
| LMSYS-Chat-1M | 1M conversations | Conversations across 25 LLMs, with model names | [HuggingFace](https://huggingface.co/datasets/lmsys/lmsys-chat-1m) |
| REALM | 94K use cases | Use-case taxonomy × occupation, from Reddit + news | [arXiv](https://arxiv.org/abs/2503.18792), [Dashboard](https://realm-e7682.web.app/) |
| Prompt Dataset Survey | Catalog of 129 datasets | Taxonomy of 673M+ prompt instances | [arXiv](https://arxiv.org/abs/2510.09316), [GitHub](https://github.com/ymzhang-cs/prompt-dataset-analysis) |

### For studying scientific model adoption
| Resource | What it covers |
|---|---|
| Trišović (2026), arXiv:2604.07530 | 62 LLMs × 108K papers, adoption lifecycles |
| Trišović et al. (2025), arXiv:2511.21739 | Companion paper, may have per-field breakdown |
| Pramanick et al. (2026), PLoS One | Cross-field LLM adoption beyond CS |

### For studying coding agents
| Resource | What it covers |
|---|---|
| Robbes et al. (2026), arXiv:2601.18341 | 128K GitHub projects, agent adoption rates/patterns |
| Murphy-Hill et al. (2026), arXiv:2607.01418 | Microsoft internal, Claude Code vs. Copilot CLI |

### For ideation benchmarks
| Resource | What it measures |
|---|---|
| Si et al. (ICLR 2025), arXiv:2409.04109 | LLM vs. human idea novelty/feasibility with 100+ NLP researchers |
| IdeaBench, arXiv:2411.02429 | 2,374 biomedical papers, idea quality scoring |
| AI Idea Bench 2025, arXiv:2504.14191 | 3,495 AI-conference papers, guards against training leakage |

### For Claude-specific research workflows
| Resource | Description |
|---|---|
| Claude Science (Anthropic, June 2026) | [anthropic.com/news/claude-science-ai-workbench](https://www.anthropic.com/news/claude-science-ai-workbench) |
| pedrohcgs/claude-code-my-workflow | Academic Claude Code template with review/replication skills |
| Read the Paper, Write the Code (arXiv 2604.21965) | Agentic reproduction of social-science results |
| Scott Cunningham's Claude Code series | [causalinf.substack.com/s/claude-code](https://causalinf.substack.com/s/claude-code) |

---

## Sources

1. Trišović, A. "The Shrinking Lifespan of LLMs in Science." arXiv:2604.07530v2, June 2026.
2. Cheng, J. et al. "REALM: A Dataset of Real-World LLM Use Cases." ACL 2025 Findings. arXiv:2503.18792.
3. Zhang, Y. et al. "A Survey of LLM Prompt Datasets: Taxonomy, Linguistic Patterns, and Practical Uses." EMNLP 2026 Findings. arXiv:2510.09316.
4. Ren, J. et al. "Towards Scientific Intelligence: A Survey of LLM-based Scientific Agents." arXiv:2503.24047, 2025.
5. Schmidgall, S. et al. "Agent Laboratory: Using LLM Agents as Research Assistants." arXiv:2501.04227, 2025.
6. Robbes, R. et al. "Agentic Much? Adoption of Coding Agents on GitHub." arXiv:2601.18341v2, April 2026.
7. Murphy-Hill, E. et al. "Adoption and Impact of Command-Line AI Coding Agents." arXiv:2607.01418, July 2026.
8. Si, C. et al. "Can LLMs Generate Novel Research Ideas?" ICLR 2025. arXiv:2409.04109.
9. Li, S. et al. "Chain of Ideas: Revolutionizing Research Via Novel Idea Development." EMNLP 2025 Findings. arXiv:2410.13185.
10. Gilon, D. et al. "A Review of LLM-Assisted Ideation." arXiv:2503.00946, 2025.
11. Lu, C. et al. "The AI Scientist." Sakana AI, 2024. sakana.ai/ai-scientist
12. Yamada, T. et al. "AI Scientist v2." arXiv:2504.08066, 2025. 
13. Chen, L. et al. "FrugalGPT." arXiv:2305.05176, 2023.
14. "Read the Paper, Write the Code." arXiv:2604.21965, 2026.
15. "Coding-agents can replicate scientific ML papers." arXiv:2607.02134, 2026.
