# Claude Research Notes: LLM Perception of Time

*Research compiled June 10, 2026*

---

## 1. Aging & Continuity: Keeping AI "Alive" Through Time

**Q: How can we maintain AI continuity or identity over time?**

The dominant approach is **memory-augmented agent architectures**. MemGPT (Packer et al., 2023) treats the LLM as an operating system that manages its own memory hierarchy — core memory (in-context, analogous to RAM) and archival/recall memory (external storage, analogous to disk). The LLM decides what to store, summarize, or forget via tool calls. This has evolved into the **Letta** framework (2024–present), which adds sleep-time agents that asynchronously consolidate and refine memory during idle periods. The key insight: strategic *forgetting* is a feature, not a bug — summarization and targeted deletion cut storage by ~60% and raise retrieval precision ~22%.

**Voyager** (Wang et al., 2023, NeurIPS) demonstrated lifelong learning in Minecraft: an ever-growing skill library of executable code + automatic curriculum + iterative self-verification. Skills compound over time, alleviating catastrophic forgetting. It obtained 3.3× more unique items and unlocked milestones 15.3× faster than baselines.

**Q: What about continual learning at the parameter level?**

Two comprehensive surveys cover this space: Shi et al. (ACM Computing Surveys, 2025) and Zheng et al. (ACM Computing Surveys, 2025). The core challenge is **catastrophic forgetting** — fine-tuning on new data degrades old knowledge. Strategies split into:

- **Internal knowledge**: continual pre-training, continual fine-tuning, MoE-based approaches (e.g., MoRAL — MoE Augmented LoRA for lifelong learning)
- **External knowledge**: RAG, tool-based learning that extends capabilities without modifying parameters

A newer direction is **LifelongAgentBench** (Zheng et al., 2025), which evaluates LLMs as lifelong learners in agent settings — not just knowledge retention but behavioral adaptation across tasks.

**Q: Can models consolidate experience like biological sleep?**

Two distinct but complementary lines:

1. **"LLM Sleep"** (Lee et al., CMU, May 2026): A model periodically enters a sleep phase where it performs N offline recurrent passes over accumulated context, writing information into SSM fast weights via a learned local rule. KV cache is then cleared. Result: reasoning accuracy improves from ~10% to 30%+ on hard multi-hop tasks, with no additional latency at inference time. This is about *computational* consolidation.

2. **Sleep-time Compute** (Lin & Snell et al., Letta/Stanford, April 2025): Agents use idle time to proactively process, reorganize, and rewrite their memory. Non-blocking — memory management happens asynchronously rather than during conversations. This is about *knowledge* consolidation for deployed agents.

---

## 2. Time Prediction: Can LLMs Estimate Task Duration?

**Q: Can LLMs estimate how long their own tasks take?**

**No — they are badly miscalibrated.** Garikaparthi (ICLR 2026 Workshop, "Can LLMs Perceive Time?") found:

- Pre-task duration estimates overshoot actual time by **4–7×** (p < 0.001)
- Models predict human-scale minutes for tasks completing in seconds
- Relative ordering of task durations is at or below chance (GPT-5 scored 18% on counter-intuitive pairs)
- Post-hoc recall is disconnected from reality — estimates diverge by an order of magnitude
- Errors persist in multi-step agentic settings (5–10×)
- Models have propositional knowledge about duration from training but cannot map it to their own computation

The core issue: models observe tokens, not elapsed time. Wall-clock duration depends on model size, hardware, batching, tool latency — none of which are in the prompt.

**Q: Can LLMs estimate how long *human* tasks take?**

Better, but still limited. **BRIDGE** (2026) showed that frontier LLMs (Gemini 3 Pro, GPT-5.2) can be prompted to predict human task completion times using task descriptions + calibration anchors, but the correlation with actual times is modest. LLMs as estimators for software effort work comparably to mid-tier ML baselines but worse than specialized models.

A **Frontiers survey** (Feb 2026) on LLM-aware software effort estimation finds LLMs can predict Story Points and assist backlog refinement, but face challenges in explainability, data sparsity, and integration.

LLMs also exhibit the **planning fallacy** — they underestimate completion time even when given historical evidence of overruns. A comprehensive cognitive bias evaluation (2024) found models maintain optimistic estimates despite negative evidence.

**Q: What about METR's time horizon work?**

METR's **Task-Completion Time Horizons** project (updated May 2026) measures how long (in human-expert hours) a task can be for an AI agent to complete it at 50% reliability. Key findings:

- Time horizons have been **doubling every ~7 months** since 2019
- Recently accelerated to **doubling every ~4 months** in 2024–2025
- Opus 4.6's 50% horizon is ~12 hours
- Extrapolation suggests month-long task completion by 2027–2031
- MirrorCode benchmark shows agents completing weeks-long coding tasks (16,000-line codebase reimplementation)

This is not about models *estimating* time — it's about measuring the actual time horizon of their capabilities. Relevant because it gives empirical grounding for what "time" means for agent task completion.

---

## 3. Time Perception & Introspection

**Q: Can LLMs perceive the passage of time?**

The **Token-Time Hypothesis** (Wang et al., EMNLP Findings 2025, "Discrete Minds in a Continuous World") proposes that LLMs can map discrete token counts to continuous wall-clock time. Three experiments:

1. **Dialogue duration judgment**: LLMs can roughly estimate how long a conversation lasted based on its length — validating that token count → time mapping exists
2. **Urgency adaptation**: LLMs shorten responses while maintaining accuracy when users express time pressure
3. **BombRush**: An interactive navigation game under progressive time pressure — LLMs do modify behavior under temporal constraints

Findings: LLMs possess *some* awareness of time passage, but it varies with model size and reasoning ability. Larger models are better. This is the most optimistic finding in the literature.

**Q: Are LLM agents "temporally blind" in practice?**

**Yes.** Cheng et al. (2025, "Your LLM Agents are Temporally Blind") introduced the **TicToc benchmark** — 700+ multi-turn trajectories across 34 scenarios with varying time sensitivity. Key findings:

- Without timestamps, alignment with human time-sensitive tool-calling decisions is barely above random (~60% max)
- Adding explicit timestamps helps only modestly (peak ~65%)
- Prompt-based alignment (reminders, few-shot rules) has limited effectiveness
- Models fail to decide when data is stale and needs refreshing vs. when cached context suffices
- Conclusion: **post-training alignment** is needed for temporal awareness in agents

**Q: Can LLMs be trained to be time-aware?**

The doc's own sketch — "Input → LLM → output response, note → back to LLM (train with reward model to estimate time taken)" — is essentially describing a feedback loop. Current research suggests:

- **External timestamps work partially**: simply injecting timestamps into prompts improves temporal tool-calling decisions, but not enough (TicToc results)
- **Fine-tuning on temporal data helps**: Xiong et al. (ACL 2024) showed LLMs *can* learn temporal reasoning through targeted training
- **Timeline self-reflection** (2025): Having LLMs construct explicit timelines during reasoning improves temporal ordering and duration tasks
- The **ECONET** approach (Han et al., EMNLP 2021) showed continual pre-training specifically on event temporal reasoning data improves temporal understanding

The open question from the doc — "Scope: LLM or LLM+harness?" — is critical. Pure LLMs lack time grounding; harness-augmented systems (with system clocks, timestamps, duration tracking) can be time-aware by design.

**Q: How do agents behave when commands take varying amounts of time? (Greg's questions)**

No direct published study on this exact setup exists, but the closest work is:

- **TicToc** (above) — tests whether agents adapt tool-calling based on elapsed time
- The "sleep 10000" experiment Greg proposes is novel and untested in the literature
- For timestamped logs: "Discrete Minds" shows LLMs can notice temporal gaps in text, but behavioral adaptation is inconsistent
- Greg's proposal for **controlled probing** (changing time gaps in logs, observing effects) would be a genuinely new contribution

---

## 4. Related Work From the Doc (Quick Summaries)

**Emergent Misalignment** (arXiv 2502.17424): Fine-tuning models on one behavior can cause unexpected emergence of unrelated behaviors. Relevant for data generation methodology if training time-aware models.

**TimeBench** (Chu et al., 2024): Hierarchical temporal reasoning benchmark with multiple levels: temporal knowledge, temporal NLI, event ordering, duration estimation. LLMs struggle especially with multi-hop temporal reasoning.

**RAGEN / BAGEN** (2025): Framework for training LLM reasoning agents via RL in interactive environments. BAGEN extends this to more diverse benchmarks. Relevant as infrastructure for training agents with temporal feedback loops.

---

## 5. Reading List

### CORE PAPERS — DIRECTLY RELEVANT

**"Can LLMs Perceive Time? An Empirical Investigation" — Garikaparthi (ICLR 2026 Workshop)**
https://arxiv.org/abs/2604.00010
Main contribution: Shows LLMs overshoot their own task duration estimates by 4–7×, fail relative ordering, and stay miscalibrated even after finishing tasks. Tested across 68 tasks and four model families.
Why we'd care: Directly answers whether LLMs have temporal self-awareness (they don't). Establishes the exact gap any time-aware training approach would need to close. The experimental setup is reusable for our own probing.

**"Discrete Minds in a Continuous World: Do Language Models Know Time Passes?" — Wang, Bai, Vu, Shareghi, Haffari (EMNLP Findings 2025)**
https://arxiv.org/abs/2506.05790
Main contribution: Proposes the Token-Time Hypothesis — LLMs can map discrete token counts to wall-clock time. Validates via dialogue duration judgment, urgency adaptation, and BombRush (a time-pressure navigation game).
Why we'd care: Most optimistic evidence that some time perception exists. The experimental paradigms (especially BombRush) are things we could extend. Contrasts with Garikaparthi's negative findings — the difference is about reasoning over time in text vs. estimating one's own computation time.

**"Your LLM Agents are Temporally Blind" — Cheng, Soltani Moakhar, Fan et al. (2025)**
https://arxiv.org/abs/2510.23853
Main contribution: TicToc benchmark with 700+ multi-turn trajectories across 34 scenarios. Shows agents fail to adapt tool-calling decisions based on elapsed time. Timestamps help only marginally (~60% to ~65% alignment).
Why we'd care: Directly relevant to agent time perception in practice. Their benchmark could be extended with the controlled probing experiments from our doc (e.g., varying time gaps in logs, observing behavioral changes).

**"Do Language Models Need Sleep? Offline Recurrence for Improved Online Inference" — Lee, McLeish, Goldstein, Fanti (CMU, May 2026)**
https://arxiv.org/abs/2605.26099
Main contribution: Sleep-like consolidation where the model does N offline recurrent passes over context, writing into SSM fast weights. Improves multi-hop reasoning from ~10% to 30%+ with no added inference latency.
Why we'd care: Architectural solution for the aging/continuity question. Models that consolidate experience offline could develop something like temporal continuity. Also directly relevant to the "LLM sleep" concept.

### MEMORY & CONTINUITY

**"MemGPT: Towards LLMs as Operating Systems" — Packer, Wooders, Lin, Fang, Patil, Gonzalez (2023)**
https://arxiv.org/abs/2310.08560
Main contribution: LLM-as-OS memory management with two tiers (core memory as RAM, archival/recall as disk). Self-directed memory editing via tool calling. Strategic forgetting through summarization.
Why we'd care: Foundation for persistent agents. The key idea — that the LLM itself manages what to remember and forget — is the basis for any system that maintains identity over time. Now evolved into Letta.

**"Voyager: An Open-Ended Embodied Agent with Large Language Models" — Wang et al. (NeurIPS 2023)**
https://arxiv.org/abs/2305.16291
Main contribution: First LLM-powered lifelong learning agent. Automatic curriculum + ever-growing skill library + iterative self-verification. 3.3× more unique items, 15.3× faster milestone unlocking in Minecraft.
Why we'd care: Best existing demo of an agent that "ages" by accumulating skills over time. The skill library pattern (code stored and retrieved later) is a concrete mechanism for temporal persistence.

**"Sleep-time Compute: Beyond Inference Scaling at Test-time" — Lin, Snell et al. (Letta/Stanford, April 2025)**
https://arxiv.org/abs/2504.13171
Main contribution: Agents use idle time to proactively reorganize and rewrite their memory. Non-blocking — memory management happens asynchronously rather than during conversations.
Why we'd care: Directly addresses "keeping AI alive through time." If an agent consolidates and refines its knowledge during downtime, that's a form of temporal continuity. Production-ready via Letta framework.

**"Towards Lifelong Learning of Large Language Models: A Survey" — Zheng, Qiu, Shi, Ma (ACM Computing Surveys 2025)**
https://arxiv.org/abs/2406.06391
Main contribution: Comprehensive taxonomy splitting lifelong learning into internal knowledge (continual pre-training, continual fine-tuning) and external knowledge (RAG, tool-based learning).
Why we'd care: Maps the full landscape. If we want to train models that learn over time without catastrophic forgetting, this is the reference for what's been tried and what works.

**"Continual Learning of Large Language Models: A Comprehensive Survey" — Shi et al. (ACM Computing Surveys 2025)**
https://arxiv.org/abs/2404.16789
Main contribution: Evaluation protocols, data sources, and open questions for continual learning with LLMs. Companion GitHub repo with regularly updated paper list.
Why we'd care: Complementary to the Zheng survey. More focused on evaluation methodology — useful for designing how we'd measure any time-aware training approach.

### TEMPORAL REASONING BENCHMARKS

**"TimeBench" — Chu et al. (2024)**
https://arxiv.org/abs/2311.17667
Main contribution: Hierarchical temporal reasoning benchmark covering temporal knowledge, temporal NLI, event ordering, and duration estimation. Tests Chain-of-Thought prompting.
Why we'd care: Baseline benchmark for evaluating temporal understanding. Could extend with self-estimation tasks.

**"TRAM: Benchmarking Temporal Reasoning for Large Language Models" — Wang & Zhao (ACL Findings 2024)**
Main contribution: Covers order, arithmetic, frequency, and duration aspects of temporal reasoning about events.
Why we'd care: Broadest coverage of temporal reasoning subtypes in a single benchmark.

**"TimE: A Multi-level Benchmark for Temporal Reasoning in Real-World Scenarios" — Wei et al. (NeurIPS 2025)**
https://arxiv.org/abs/2505.12891
Main contribution: Multi-level temporal reasoning benchmark grounded in real-world scenarios rather than synthetic data.
Why we'd care: More practical/applied than TimeBench. Tests whether temporal reasoning transfers to realistic settings.

**"Test of Time: A Benchmark for Evaluating LLMs on Temporal Reasoning" — Fatemi et al. (ICLR 2025)**
https://arxiv.org/abs/2406.09170
Main contribution: Synthetic temporal reasoning datasets that control for data contamination. Systematic investigation of problem structure, size, and fact order effects.
Why we'd care: Clean experimental methodology that isolates temporal reasoning from memorization. Good template for designing controlled experiments.

### TASK DURATION & EFFORT ESTIMATION

**"BRIDGE: Predicting Human Task Completion Time From Model Performance" (2026)**
https://arxiv.org/abs/2602.07267
Main contribution: Framework for predicting how long humans take on tasks, using frontier LLMs as estimators with calibration anchors.
Why we'd care: Connects AI performance to human time scales. Relevant to the Gantt-chart question — can LLMs estimate subtask durations for project planning?

**METR Task-Completion Time Horizons (2025–2026, updated regularly)**
https://metr.org/time-horizons/
Main contribution: Measures the task duration (in human-expert time) that AI agents can complete at 50% reliability. Shows exponential growth doubling every ~7 months, recently accelerating to ~4 months.
Why we'd care: Empirical grounding for what "time" means for agent capability. The meta-question: as agents handle longer tasks, temporal awareness becomes more critical. Also relevant because it shows models can't self-estimate duration but can be measured externally.

**"Leveraging LLMs for Predicting Cost and Duration in Software Engineering Projects" (2024)**
https://arxiv.org/abs/2409.09617
Main contribution: Fine-tuned GPT-3.5 for software project cost/duration estimation. Beats some ML baselines but not state-of-the-art specialized models.
Why we'd care: Shows LLMs can estimate human task duration in a specific domain even though they can't estimate their own. Useful framing for the prediction section.

**"Toward LLM-aware Software Effort Estimation: A Conceptual Framework" — Frontiers (Feb 2026)**
https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2026.1772418/full
Main contribution: Conceptual framework for effort estimation when LLMs change what "development" means — how do you estimate project time when AI tools change productivity?
Why we'd care: Forward-looking. If LLMs are doing the work, traditional time estimation breaks down. Relevant to the doc's question about whether LLMs can remember how long things took.

### AGENT FRAMEWORKS

**Letta (evolved from MemGPT)**
https://www.letta.com
Main contribution: Open-source framework for stateful agents with hierarchical memory management, sleep-time compute, and persistent agent state. Model-agnostic.
Why we'd care: Most production-ready platform for building persistent, temporally-aware agents. If we want to prototype any of the ideas in the doc, this is likely the starting infrastructure.

**"RAGEN: Understanding Self-Evolution in LLM Agents" (2025)**
https://github.com/RAGEN-AI/RAGEN
Main contribution: RL framework for training LLM reasoning agents in interactive, stochastic environments (Bandit, Sokoban, FrozenLake, WebShop).
Why we'd care: Infrastructure for training agents with temporal feedback loops. If we want to train agents that learn from how long things took, this provides the RL pipeline.

**"LifelongAgentBench: Evaluating LLM Agents as Lifelong Learners" — Zheng et al. (2025)**
Main contribution: Benchmark evaluating whether LLM agents can learn and improve across tasks over extended time horizons.
Why we'd care: Evaluates exactly the kind of temporal continuity we care about — not just knowledge retention but behavioral adaptation over a lifetime of tasks.
