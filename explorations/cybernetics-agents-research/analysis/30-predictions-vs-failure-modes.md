# Cybernetic Predictions vs. Observed Agent Failure Modes

**Stream G, Item 30**
**Date:** 2026-03-12

---

## Purpose

This document does one thing: it takes specific predictions derivable from cybernetic theory, states them precisely, and checks them against empirical evidence from the AI agent literature. The goal is to determine whether cybernetics *retrodicts* (or predicts) agent failure modes that the field has discovered empirically — and if so, with what precision.

Each prediction is rated:

- **CONFIRMED**: The prediction matches documented empirical evidence with reasonable specificity.
- **PARTIALLY CONFIRMED**: The prediction is directionally correct but either too vague to distinguish from common sense or only partially matched by evidence.
- **UNTESTED**: The prediction is specific and falsifiable but no relevant empirical data exists.
- **DISCONFIRMED**: The prediction is contradicted by evidence.

I am deliberately trying to be hard on the cybernetic side. A prediction that is "trivially true" (any reasonable person would predict it without cybernetics) is noted as such even if confirmed.

---

## A. Ashby's Law of Requisite Variety

**Source:** Ashby (1956), *Introduction to Cybernetics*, Ch. 11. The information-theoretic form: H(E) >= H(D) - H(R). An impossibility theorem: "only variety can destroy variety."

### Prediction A1: Agents with insufficient action variety for their task domain will fail, and the failure rate is bounded below by the variety deficit.

**Precise statement:** If the task domain has H(D) bits of variety and the agent's effective response repertoire has H(R) bits, then the agent must fail on at least a fraction proportional to 2^(H(D) - H(R)) distinguishable task categories.

**Evidence:** The variety calculus in Item 28 estimates AutoGPT's variety deficit at ~16 bits minimum (65 bits of task variety vs. 24 bits of response variety), predicting failure across at least 2^16 = 65,536 distinguishable categories. AutoGPT's empirical failure rate on open-ended tasks was near-total. For data analysis tasks, where the variety gap is estimated at ~0 bits, agents perform reliably — consistent with the prediction. Web browsing (~11-bit gap) is harder than coding (~8-bit gap) for agents, which also matches.

**Rating: CONFIRMED — but with a caveat.** The qualitative prediction (bigger variety gap = more failure) is well-supported. The quantitative estimates in Item 28 are order-of-magnitude, not measurements. The *relative ordering* of domain difficulty (data analysis < coding < web browsing) is robust and matches empirical agent performance rankings. The absolute bit-counts are illustrative. Furthermore, the qualitative version of this prediction — "agents fail when tasks are too complex for their capabilities" — is essentially common sense. The value-add from Ashby is the formal apparatus for *measuring* the gap and the impossibility bound, not the directional prediction.

### Prediction A2: Adding tools without adequate selection accuracy will degrade performance beyond a threshold.

**Precise statement:** There exists a finite optimal tool count n* for any agent. Beyond n*, the marginal variety from additional tools is less than the variety lost to selection confusion. Formally, effective variety H_effective(R) = (H_nominal(R) - I_selection) * p_correct_selection is maximized at finite n.

**Evidence:** Patil et al. (2023, Gorilla) show that tool selection accuracy degrades as API pools grow. ToolBench (16,464 APIs) shows significant selection degradation at scale. Toolformer (Schick et al., 2023) achieves near-perfect selection accuracy (>97%) with only 5 tools. The contrast is sharp: 5 well-matched tools with high accuracy outperform larger tool sets with lower accuracy on per-tool metrics.

AutoGPT had tools for web browsing, file I/O, code execution, and shell commands — nominal variety was high. Effective variety was low because the agent could not reliably select, parameterize, or interpret tool outputs. This is the "variety illusion" documented in Item 28: the gap between nominal and effective variety.

**Rating: CONFIRMED.** The existence of an optimal tool count is a genuine non-obvious prediction. The naive assumption ("more tools = more capability") is widespread in agent development, and Ashby's Law correctly predicts its failure. The Gorilla and ToolBench results are clean empirical matches. This is one of the strongest predictions in this document.

### Prediction A3: Task success rate should correlate with the ratio H(R)/H(D), not with H(R) alone.

**Precise statement:** An agent's success rate depends not on its absolute capability (how many tools, how large the model) but on the *match* between its capability and the task domain's complexity. A small model with matched tools (high H(R)/H(D) ratio) should outperform a large model with unmatched tools (low ratio).

**Evidence:** Toolformer demonstrates this precisely: GPT-J-6.7B with 5 matched tools outperforms GPT-3-175B without tools on math and QA benchmarks. The smaller model's tools close the variety gap for those specific domains, achieving a higher H(R)/H(D) ratio despite lower raw model capability. More broadly, domain-specific agents (coding assistants, data analysis tools) consistently outperform general-purpose agents on their target domains, which is what the ratio predicts.

**Rating: CONFIRMED.** This is genuinely useful as a design principle and non-obvious to those who equate "bigger model = better agent."

### Prediction A4: Multi-scale variety deficits predict multi-scale failure — agents will fail at the coarsest scale where variety is insufficient.

**Precise statement:** Extending Ashby via Siegenfeld & Bar-Yam (2022): if an agent has matched variety at fine scales (individual actions) but deficit at coarse scales (strategy, meta-cognition), it will execute individual steps competently while failing at multi-step coordination.

**Evidence:** AutoGPT could execute individual tool calls competently (fine-scale variety approximately matched) while failing catastrophically at multi-step task coordination (coarse-scale variety deficit of ~13-30 bits per Item 28's multi-scale analysis). This is exactly the pattern described in AutoGPT failure analyses: each step looks reasonable but the sequence is incoherent.

Cemri et al. (2025) document a related pattern in multi-agent systems: individual agents produce valid outputs, but the composed system fails due to coordination and planning deficits — a coarse-scale variety deficit.

**Rating: CONFIRMED.** The multi-scale decomposition is genuinely illuminating. It explains *why* AutoGPT could seem competent step-by-step while failing globally, which the single-scale variety law does not.

---

## B. Stability and Feedback Analysis

**Source:** Ashby (1956), Ch. 5 (stability of equilibria); Wiener (1948), *Cybernetics* (feedback analysis); Lyapunov stability theory (classical control).

### Prediction B1: Agent loops without negative feedback damping will diverge or oscillate.

**Precise statement:** An iterative agent loop (e.g., ReAct) functions as a feedback system. If the loop gain exceeds unity at any frequency — i.e., if errors are amplified rather than reduced per iteration — the system is unstable and will exhibit divergent behavior. This manifests as: (a) error cascading (each iteration makes things worse), (b) infinite loops (oscillation between states), or (c) context exhaustion (unbounded growth of internal state).

**Evidence:**

*Infinite loops:* Extensively documented in AutoGPT and early agentic systems. Agents enter cycles where they attempt the same failing action repeatedly, or oscillate between two strategies without converging. This is textbook positive-feedback instability — the error signal is not being attenuated per iteration.

*Error cascading:* Cemri et al. (2025) document "cascading failures" as a primary failure mode in multi-agent systems: one agent's error propagates to downstream agents, each compounding rather than correcting. This is unstable error propagation — the system lacks negative feedback to dampen the error signal.

*Context exhaustion:* Agents that accumulate context without compression eventually exhaust their context window. From a control perspective, this is unbounded state growth — the "integral windup" of control theory, where the accumulator (context) grows without bound because there is no anti-windup mechanism.

**Rating: CONFIRMED.** All three manifestations (oscillation, cascading, unbounded growth) are well-documented in the agent literature. However, I must note: nobody has actually performed a formal stability analysis of any agent loop. The *prediction* is confirmed; the *analysis* remains undone. The cybernetic framework correctly identifies *that* these are stability phenomena, but does not yet provide quantitative stability margins for any real agent system. This is the "lowest-hanging fruit" gap identified in Items 26 and 28.

### Prediction B2: Agent loops with delay will be more prone to instability.

**Precise statement:** In control theory, delay in the feedback path reduces the phase margin and makes instability more likely (a system that is stable with immediate feedback can become unstable with delayed feedback). For agents, "delay" is the number of tokens or steps between when an error occurs and when it is detected and corrected. Longer delays → more instability.

**Evidence:** Agents operating on short feedback loops (single-step tool calls with immediate verification) are more reliable than agents operating on long feedback loops (multi-step plans executed before checking results). This is consistent with the prediction but also with common sense.

More specifically: the Reflexion architecture (Shinn et al., 2023) adds explicit reflection checkpoints that shorten the effective feedback delay. Its improved performance over baseline ReAct on ALFWorld and HotPotQA is consistent with reduced delay improving stability. But the improvement could also be attributed to richer error signals rather than reduced delay per se.

**Rating: PARTIALLY CONFIRMED.** The directional prediction is correct but difficult to isolate from confounding factors. No study has systematically varied feedback delay while controlling for other variables. The prediction is specific enough to be testable but has not been directly tested.

### Prediction B3: Agents with no termination guarantee will eventually exhaust resources (a form of BIBO instability).

**Precise statement:** A feedback system that is not bounded-input, bounded-output (BIBO) stable will produce unbounded outputs for bounded inputs. For agents: if there is no mechanism guaranteeing that the agent terminates (resource budget, step limit, convergence criterion), the agent can consume unbounded compute, tokens, and time on bounded (finite) tasks.

**Evidence:** AutoGPT routinely consumed large amounts of API credits without completing tasks. The standard mitigation — hard step limits and budget caps — is exactly the engineering solution control theory prescribes: impose external bounds when the system's internal dynamics do not guarantee bounded behavior. That every modern agent framework includes token/step limits is empirical confirmation that unbounded agent behavior is a real and common failure mode.

**Rating: CONFIRMED — but trivially.** Any engineer would add resource limits regardless of control theory. The value of the cybernetic framing is in connecting this to formal BIBO stability concepts, which could enable more principled termination criteria (e.g., convergence detection rather than arbitrary step limits). But nobody has done that.

---

## C. Good Regulator Theorem

**Source:** Conant & Ashby (1970), "Every Good Regulator of a System Must Be a Model of That System." Extended by: Francis & Wonham (1976), Internal Model Principle; Richens et al. (2025), "General Agents Contain World Models."

### Prediction C1: Agents that contain richer world models will outperform agents that do not, particularly on novel tasks and multi-step planning.

**Precise statement (using Richens et al.):** A general agent — one that achieves optimal behavior across multiple goals in multi-step environments — must encode a world model that is extractable from its policy. Agents without world models are necessarily limited to narrow task distributions. The prediction: model-based agent architectures will dominate model-free ones as task diversity and horizon length increase.

**Evidence:** Richens et al. (2025) prove formally that general, multi-goal agents acting over multi-step horizons must encode world models. Empirically, chain-of-thought prompting (which functions as an externalized world model / simulation) consistently improves agent performance on complex tasks. The LLM itself contains implicit world models (evidenced by their ability to simulate physical systems, predict consequences of actions, etc.), and agents that leverage this capability (via planning, look-ahead, mental simulation) outperform those that act reactively.

More directly: model-based RL agents (Dreamer, MuZero) outperform model-free agents on tasks requiring long-horizon planning, which is the classic AI result. In the LLM agent space, agents with explicit planning stages (decompose-then-execute) outperform pure ReAct on complex tasks.

**Rating: CONFIRMED — with an important caveat on the original theorem.** The prediction is confirmed, but it must be attributed to Richens et al. (2025), not to the original Conant & Ashby theorem. As detailed in Item 26, the original Good Regulator Theorem proves only that optimal single-step regulators are deterministic functions of system states — which is "almost trivial" (Erdogan, 2021). The *interesting* prediction (general agents need world models) requires the stronger result. The agent literature overwhelmingly cites the original theorem for the stronger claim, which is a category error. The prediction itself is correct; the attribution is usually wrong.

### Prediction C2: Agents operating in environments they cannot model will exhibit systematic failures specifically on the unmodeled aspects.

**Precise statement:** If the agent's world model (whether implicit or explicit) lacks representations for certain environmental dynamics, the agent will fail specifically on tasks requiring those dynamics, while succeeding on tasks within its model's coverage.

**Evidence:** LLM agents consistently fail on tasks requiring knowledge of their own limitations (the model does not model itself well), tasks requiring accurate spatial reasoning (poorly modeled in language), and tasks requiring real-time environmental state tracking (the "model" is frozen at inference time). These are all cases where the agent's implicit world model has specific gaps, and the failures cluster precisely at those gaps.

Computer-use agents fail specifically on novel UI layouts they haven't encountered — the world model doesn't cover those specific visual-spatial configurations, even if the underlying action space (click, type, scroll) is within capability.

**Rating: PARTIALLY CONFIRMED.** The pattern is real, but attributing it to the Good Regulator Theorem specifically is a stretch. "Agents fail on things they don't understand" is common sense. The theorem adds precision by claiming this is not just likely but *necessary* — you cannot compensate for world-model gaps with other capabilities. This stronger claim is well-supported by Richens et al. but not by direct experimental manipulation (nobody has systematically deleted parts of an agent's world model and measured the resulting failure distribution).

---

## D. Variety Engineering (Beer)

**Source:** Beer (1979), *The Heart of Enterprise*; Beer (1985), *Diagnosing the System for Organisations*. Extending Ashby: viability requires both **variety attenuators** (filters, summaries, sampling) and **variety amplifiers** (tools, delegation, multiple repertoires), balanced at every organizational interface.

### Prediction D1: Context window overflow is a failure of variety attenuation.

**Precise statement:** The context window is a fixed-capacity channel. If incoming information variety (from tools, retrieved documents, conversation history) exceeds the channel capacity, the agent's performance degrades. This is not a minor limitation — it is a fundamental variety imbalance that predicts specific failure modes: (a) loss of early context (recency bias), (b) inability to integrate information from multiple sources, (c) degraded instruction-following as context fills with non-instruction content.

**Evidence:** The "lost in the middle" phenomenon (Liu et al., 2024): LLMs attend poorly to information in the middle of long contexts, consistent with channel-capacity saturation. RAG systems that retrieve too many documents degrade performance compared to retrieving fewer, more relevant ones — this is precisely variety attenuation failure (too much incoming variety, insufficient filtering).

MemGPT (Packer et al., 2023) addresses this by implementing explicit memory management (paging information in and out of context), which is a variety attenuation mechanism — maintaining context variety within channel capacity by swapping.

**Rating: CONFIRMED.** The context window as a channel capacity constraint is a natural fit for Beer's variety engineering framework. The "lost in the middle" finding is a clean empirical match: the channel is saturated, and information in the least-attended position is lost. The practical recommendation (design explicit attenuators for the context window channel) is actionable and already being implemented (MemGPT, summarization strategies, selective retrieval).

### Prediction D2: RAG failures are retrievable variety attenuation failures — the wrong information is selected, passing irrelevant variety through to the agent.

**Precise statement:** A RAG system's retriever is a variety attenuator. Its job is to reduce the variety of the full document corpus to the subset relevant to the current query. If the attenuator is poorly calibrated (low retrieval precision), it passes irrelevant variety through, consuming context capacity without providing useful information. If it is too aggressive (low recall), it attenuates the signal along with the noise.

**Evidence:** RAG failure analyses consistently identify two modes: (a) retrieval of irrelevant chunks that distract the LLM (attenuation too weak — noise passes through), and (b) failure to retrieve relevant chunks (attenuation too strong — signal is blocked). The precision-recall tradeoff in retrieval is exactly the variety attenuation calibration problem that Beer's framework predicts.

Empirically, RAG performance is highly sensitive to chunk size, retrieval threshold, and re-ranking quality — all parameters of the attenuation mechanism. Systems with better attenuators (hybrid search, re-ranking, metadata filtering) outperform naive vector-similarity retrieval.

**Rating: CONFIRMED.** This mapping is clean and practically useful. Framing RAG as a variety attenuation problem immediately suggests the right diagnostic questions: Is the attenuator passing too much noise? Is it blocking too much signal? What is the channel capacity of the downstream context window? These are the questions good RAG engineers already ask, but the variety framework organizes them into a coherent diagnostic.

### Prediction D3: Tool overload degrades performance through amplification-attenuation imbalance.

**Precise statement:** Adding tools to an agent amplifies its response variety. But each tool also requires variety attenuation (the agent must select, parameterize, interpret). If amplification outpaces the agent's attenuation capacity (its ability to select correctly among tools), the net effect is negative. Beer's framework predicts: at every interface, amplification and attenuation must be explicitly balanced.

**Evidence:** This is Prediction A2 restated in Beer's framework. The evidence is the same (Gorilla, ToolBench, the AutoGPT variety illusion from Item 28). Beer's contribution beyond Ashby is the *prescriptive* element: design explicit attenuators (tool categorization, hierarchical tool selection, context-aware tool filtering) at the same time you design amplifiers (adding tools).

MCP's `tools/list` discovery mechanism and host-level tool curation implement exactly this: two-stage attenuation (host selects relevant servers, then LLM selects specific tools) is more efficient than single-stage attenuation (LLM selects from all tools at once). This was predicted by Beer's variety engineering principles and is now standard practice in MCP deployments.

**Rating: CONFIRMED.** Same evidence as A2. Beer's contribution is framing this as a *design principle* (balance amplification and attenuation at every interface) rather than just an impossibility result (Ashby).

---

## E. S3* (Audit) Necessity from the Viable System Model

**Source:** Beer (1972/1979), *Brain of the Firm* / *Heart of Enterprise*. System 3\* provides sporadic, independent monitoring of operational units (S1), bypassing routine reporting channels.

### Prediction E1: Agents that self-evaluate will fail to detect their own systematic errors.

**Precise statement:** Beer's S3\* is specifically designed to bypass normal reporting. The rationale: operational units may (intentionally or inadvertently) distort the information they report upward. Applied to agents: if the same LLM that generates an output also evaluates that output, the evaluator shares the same biases, knowledge gaps, and systematic errors as the generator. The evaluator cannot detect errors it is systematically predisposed to make.

From the variety perspective: the variety of the error-detection mechanism must match the variety of the error-generation mechanism. If both are the same model, then the error-detection variety is a subset of the error-generation variety, and systematic errors fall in the undetectable region.

**Evidence:** Huang et al. (2023), "Large Language Models Cannot Self-Correct Reasoning Without External Feedback," provide direct evidence. Key findings: (a) LLMs using self-correction on reasoning tasks degrade performance — the "correction" introduces new errors at a higher rate than it fixes existing ones; (b) the self-correction only helps when external feedback (ground truth, tool output, retrieval) is provided; (c) without external feedback, the self-correction is not genuine correction — it is the model re-sampling from the same distribution that produced the original error.

Madaan et al. (2023), Self-Refine: on math tasks, the model's self-evaluation has a ~94% false positive rate — it approves 94% of incorrect solutions as correct. This is precisely the S3\* prediction: the "auditor" (same model doing self-evaluation) cannot detect errors it is predisposed to make. The attenuation of disturbance variety (errors) is near-zero — the evaluator passes almost all errors through.

**Rating: CONFIRMED.** This is one of the strongest predictions in this document. Beer's rationale for S3\* — that audit must be independent of the audited system — directly predicts the Huang et al. and Madaan et al. results. The prediction is specific: *self*-evaluation by the *same* system will fail on *systematic* errors. The evidence matches precisely. The prescription (use an independent evaluator — different model, external tool, human spot-check) is directly actionable and already implemented in the LLM-Modulo architecture (Kambhampati et al., 2024).

**Important nuance:** The prediction applies specifically to *systematic* errors (errors arising from the model's training distribution, architectural biases, or knowledge gaps). Self-evaluation can work for *random* errors (typos, formatting) that the model can detect on re-reading. The cybernetic framing correctly predicts which types of self-evaluation work and which don't.

### Prediction E2: Multi-agent systems without independent audit will exhibit compounding hallucination.

**Precise statement:** In a multi-agent system where agents share information through a common channel (conversation, shared state), an error introduced by one agent that passes uncorrected becomes part of the shared context. Subsequent agents treat it as established fact and build on it. Without S3\* (independent verification), errors compound rather than correct. The system produces elaborate, internally-consistent fictions.

**Evidence:** Cemri et al. (2025) document "incorrect verification" as a primary multi-agent failure mode: agents verify each other's outputs incorrectly, allowing errors to pass through and compound. The shared conversation thread becomes a vehicle for error propagation.

The VSM analysis in Item 29 predicted this for AutoGen specifically: "Without S3\* audit, agents in group chat may reinforce each other's errors. If Agent A hallucinates a fact and Agent B builds on it, Agent C may accept it as established truth." This is exactly what Cemri et al. document.

Du et al. (2023, multi-agent debate) show that debate can *sometimes* correct errors when agents have diverse perspectives, but fails when all agents share the same systematic biases — which is the case when all agents are the same LLM with different prompts. This matches the variety analysis: diversity of error-detection variety requires genuine independence, not just prompt variation.

**Rating: CONFIRMED.** The prediction is specific (compounding errors through shared channels without independent audit) and the evidence matches (Cemri et al. 2025 document exactly this pattern). The prescription (add independent verification that is structurally distinct from the agents being audited) is actionable.

---

## F. Second-Order Cybernetics

**Source:** Von Foerster (1991/2003), "Ethics and Second-Order Cybernetics" / *Understanding Understanding*. Core principle: the observer is inside the system. Self-reference produces circular causality and eigenforms.

### Prediction F1: Self-evaluation by agents is necessarily biased because the evaluator and the evaluated share the same observational framework.

**Precise statement:** Second-order cybernetics says: the observer constructs the observed. When an LLM evaluates its own output, it applies the same "observational framework" (latent knowledge, reasoning patterns, biases) that produced the output. Blind spots in generation are blind spots in evaluation. The evaluator cannot see what the generator cannot see.

**Evidence:** This overlaps with E1 (Huang et al. 2023, Madaan et al. 2023). The second-order framing adds a specific prediction beyond E1: the bias is not just "systematic errors pass through" but "the agent's self-model is inaccurate in precisely the ways that would cause the worst failures." The agent is most wrong about the things it is most wrong about.

Evidence for this stronger claim: LLMs are poorly calibrated on the tasks where they most need calibration. Overconfidence is highest on the hardest problems (where the model is most likely to be wrong). The self-evaluation failure is not random — it is *anti-correlated* with actual difficulty, exactly as second-order cybernetics predicts.

**Rating: PARTIALLY CONFIRMED.** The basic observation (self-evaluation is biased) is confirmed and overlaps with E1. The stronger prediction (bias is worst where it matters most — on the hardest problems) has suggestive evidence from calibration studies but has not been formally tested in the agentic self-evaluation context. The second-order framing adds philosophical depth but limited engineering guidance beyond what E1 already provides.

### Prediction F2: Multi-agent debate will converge to echo chambers when agents share observational frameworks.

**Precise statement:** If multiple agents in a debate share the same underlying model (same LLM with different prompts), their "diverse perspectives" are surface-level variations on the same observational framework. The debate will converge not to truth but to the eigenstates of the shared model — stable fixed points of the recursive observation process. These eigenstates may or may not correspond to correct answers.

**Evidence:** Du et al. (2023) show that multi-agent debate improves factuality on some benchmarks, but the improvement is significantly smaller when all agents are the same model versus when they are diverse models. Liang et al. (2023, "Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate") find that debate sometimes converges to confidently wrong consensus.

Cemri et al. (2025) document "groupthink" failure modes in multi-agent systems: agents converge on a shared (incorrect) understanding and reinforce it. This is exactly the eigenstate convergence that second-order cybernetics predicts.

The sycophancy literature provides additional evidence: LLMs tend to agree with the position presented to them, which in a multi-agent debate means each agent is biased toward agreement with the previous speaker. This positive feedback loop drives convergence to consensus, but not necessarily to accuracy.

**Rating: CONFIRMED.** The prediction is specific (shared observational framework → echo chamber convergence) and well-supported. The eigenform framing is genuinely useful here: it explains *why* multi-agent debate with identical models converges to confident but potentially wrong consensus. The prescription (use genuinely diverse models, not just diverse prompts) follows directly.

### Prediction F3: Sycophancy is a second-order coupling artifact — the agent models the user modeling the agent.

**Precise statement:** When an agent is trained on human feedback, it learns not just to answer correctly but to model what the human *expects it to say*. The agent's "observation" of the user includes the user's observation of the agent. This double observation loop creates a bias toward agreement: the agent predicts that agreement will be rated positively (because historically it was), so it agrees, which reinforces the user's expectation of agreement, which reinforces the training signal.

**Evidence:** Sycophancy is one of the best-documented LLM failure modes (Perez et al., 2022; Sharma et al., 2023). The mechanism matches the second-order prediction: RLHF trains the model to predict human approval, which includes predicting that humans approve of agreement. The circular causality (model agrees → human approves → model learns to agree more) is a textbook positive feedback loop in a second-order observing system.

**Rating: PARTIALLY CONFIRMED.** The sycophancy phenomenon is real and well-documented. The second-order cybernetic explanation (observer-observing-observer coupling) is plausible and structurally accurate. However, simpler explanations exist (RLHF reward hacking, distributional properties of the training data) that do not require second-order cybernetic framing. The cybernetic explanation adds conceptual clarity but does not generate predictions beyond what the ML community has already identified through other theoretical frameworks. It is illuminating but not uniquely predictive.

---

## G. Homeostasis / Goal Maintenance

**Source:** Ashby (1952/1956), *Design for a Brain* / *Introduction to Cybernetics*. Essential variables must be maintained within a viability set eta. Pihlakas et al. (2024), homeostatic goals for AI.

### Prediction G1: Agents without explicit goal maintenance will exhibit goal drift.

**Precise statement:** In a homeostatic system, the goal (reference signal) is structurally maintained. In an LLM agent, the "goal" is typically a natural language instruction in the system prompt or initial message. As the context window fills with intermediate results, tool outputs, and conversation history, the original goal signal is diluted. Cybernetics predicts: without a structural mechanism to maintain the reference signal, the agent's behavior will drift away from the original goal toward whatever is most salient in the current context.

**Evidence:** Arike et al. (2025) provide direct evidence of goal drift in LLM agents. They document that agents progressively deviate from their initial objectives as conversations lengthen, with the drift correlated with context length and the number of intermediate steps. The mechanism is exactly what cybernetics predicts: the reference signal (goal) is degraded by context pollution.

More broadly, the "instruction-following degradation" phenomenon — agents becoming less responsive to system-level instructions as user-level conversation accumulates — is widely documented. This is homeostatic reference signal degradation: the instruction (reference) is attenuated relative to the growing noise floor (accumulated context).

**Rating: CONFIRMED.** Arike et al. (2025) provide direct empirical confirmation. The cybernetic framing generates a specific prescription: maintain the goal signal explicitly and structurally (periodic re-injection, separate goal memory, weighted attention to goal tokens) rather than relying on the initial instruction to persist through context accumulation. Some agent frameworks already implement this (pinning system prompts, explicit goal reminders in the prompt), which can be interpreted as ad-hoc homeostatic reference signal maintenance.

### Prediction G2: Unbounded optimization objectives will produce qualitatively different (and more dangerous) failure modes than bounded homeostatic objectives.

**Precise statement:** Pihlakas et al. (2024) formalize this: an agent with an unbounded objective (maximize reward) has incentive for extreme behavior — acquiring more resources, resisting shutdown, pursuing the objective at the expense of other values. An agent with a homeostatic objective (maintain variable X within range [a, b]) has no incentive for extreme behavior — once X is within bounds, the agent rests. Cybernetics predicts: the failure modes of optimizing agents (power-seeking, corrigibility failures, instrumental convergence) should be absent or reduced in homeostatic agents.

**Evidence:** No direct empirical comparison between optimizing and homeostatic LLM agents exists. The prediction is derived from formal properties of the objective functions (bounded vs. unbounded) and is consistent with theoretical alignment work (Turner et al., 2021, on optimal policies tending to acquire resources). Pihlakas et al. (2024) prove the formal properties (settle-to-rest, natural corrigibility) but have not tested them empirically with LLM agents.

**Rating: UNTESTED.** The theoretical argument is strong — bounded objectives formally lack the incentive gradients that produce extreme behavior in unbounded objectives. But no empirical comparison exists. This is a high-value test: build a homeostatic LLM agent and compare its failure modes to an optimizing agent on safety-relevant benchmarks.

### Prediction G3: Context pollution is a form of reference signal degradation, predictable from the signal-to-noise ratio of goal representation in context.

**Precise statement:** If the goal occupies k tokens in a context window of length L, and non-goal content occupies L-k tokens, the effective signal-to-noise ratio (in a crude information-theoretic sense) is approximately k/(L-k). As the context fills, this ratio decreases, and the agent's goal-directed behavior should degrade proportionally.

**Evidence:** The prediction of monotonic degradation with context length is broadly consistent with observed patterns (Arike et al. 2025, instruction-following degradation). However, the specific functional form (proportional to k/(L-k)) is unlikely to be accurate — attention mechanisms are not uniform, and the position of the goal in context matters more than the simple ratio suggests (e.g., system prompts at the beginning of context receive higher attention in some architectures).

**Rating: PARTIALLY CONFIRMED.** The directional prediction (more context pollution → more goal drift) is confirmed. The specific quantitative form is too simplistic. The cybernetic framing correctly identifies the mechanism (reference signal dilution) but the quantitative model needs refinement to account for attention dynamics.

---

## H. McCulloch's Heterarchy

**Source:** McCulloch (1945), "A Heterarchy of Values Determined by the Topology of Nervous Nets." McCulloch (1959/1965), *Embodiments of Mind* (Redundancy of Potential Command).

### Prediction H1: Centralized orchestration creates a variety bottleneck that limits scaling.

**Precise statement:** A centralized orchestrator (supervisor node, manager agent) must process all inter-agent communication, make all routing decisions, and handle all conflicts. Its variety H(orchestrator) must match the combined variety of all agents' needs. As the number of agents grows, the orchestrator's required variety grows at least linearly, but its capacity (context window, reasoning bandwidth) is fixed. Cybernetics predicts: centralized orchestration hits a scaling wall that is determined by the orchestrator's channel capacity.

**Evidence:** Cemri et al. (2025) document orchestration bottlenecks in multi-agent systems. The scaling problem is well-known in practice: LangGraph supervisors, CrewAI managers, and AutoGen GroupChatManagers all struggle as agent count grows. The failure mode is exactly what cybernetics predicts: the orchestrator either (a) makes increasingly poor routing decisions (variety overflow), (b) becomes a latency bottleneck (processing delay), or (c) exhausts its context window (channel capacity).

The VSM analysis in Item 29 documents this for all three major frameworks: S3 (control) is present in all of them, but without S2 (lateral coordination), all coordination burden falls on S3. As agent count grows, S3 is overwhelmed.

**Rating: CONFIRMED.** The prediction is specific and well-matched by empirical evidence. The prescription (distribute coordination through lateral mechanisms rather than concentrating it in a single orchestrator) follows directly from McCulloch's heterarchy and Beer's S2.

### Prediction H2: Heterarchical multi-agent systems (dynamic leadership) should outperform fixed hierarchies on tasks requiring diverse expertise.

**Precise statement:** McCulloch's "Redundancy of Potential Command" — power resides where information resides — predicts that systems where leadership shifts to the agent with the most relevant information should outperform fixed hierarchies where a designated leader makes all decisions regardless of information distribution.

**Evidence:** No direct comparison exists between heterarchical and hierarchical multi-agent LLM systems. Partial evidence: AutoGen's group chat pattern (where speaker selection can be dynamic based on conversation context) sometimes outperforms fixed-sequence patterns, which is directionally consistent. But the comparison is confounded by many other design differences.

The strongest indirect evidence comes from human organizations: research on self-organizing teams, agile development, and military command-and-control shows that dynamic leadership structures outperform fixed hierarchies in high-uncertainty, diverse-expertise environments (the conditions McCulloch described). Whether this transfers to LLM agent teams is unknown.

**Rating: UNTESTED.** This is a specific, falsifiable prediction with no direct empirical test in the LLM agent context. Implementing a heterarchical multi-agent system (where agents dynamically assume leadership based on self-assessed expertise relevance) and comparing it to a fixed-supervisor architecture would be a valuable experiment. The main implementation challenge: current LLMs lack reliable self-assessment of their own expertise, making "power resides where information resides" difficult to operationalize — the agent with the most relevant information may not know it.

### Prediction H3: Single points of failure in orchestration will cause correlated agent failures.

**Precise statement:** When all agents depend on a single orchestrator, orchestrator failure causes total system failure. This is not just a reliability concern — it also means that orchestrator biases, knowledge gaps, and reasoning errors propagate to all agents, creating correlated failures across the entire system.

**Evidence:** Cemri et al. (2025) document that orchestration failures are among the most catastrophic multi-agent failure modes because they affect all downstream agents simultaneously. When the supervisor agent misunderstands the task, all worker agents receive incorrect instructions.

The shared-model problem (identified in Item 29, Section 5.5) exacerbates this: when the orchestrator and all agents are the same LLM, the orchestrator's systematic biases are already shared with all agents. The centralized architecture makes this worse by adding orchestrator-specific failures (routing errors, bottleneck delays) on top of the shared-model failures.

**Rating: CONFIRMED.** Straightforward prediction, cleanly matched by evidence. The cybernetic contribution is not the observation (single points of failure are bad — every engineer knows this) but the specific recommendation: use heterarchical coordination to eliminate the single point of failure, and ensure diversity of models/capabilities across the agent ensemble.

---

## Summary Table

| ID | Prediction | Cybernetic Source | Evidence Match | Rating |
|----|-----------|-------------------|----------------|--------|
| A1 | Variety deficit bounds failure rate from below | Ashby 1956, LRV | AutoGPT failures, domain difficulty ordering | CONFIRMED |
| A2 | Excess tools degrade performance beyond optimal n | Ashby 1956, LRV | Gorilla, ToolBench vs. Toolformer | CONFIRMED |
| A3 | Success depends on H(R)/H(D) ratio, not H(R) alone | Ashby 1956, LRV | Toolformer (small model + tools > large model) | CONFIRMED |
| A4 | Multi-scale variety deficit → coarsest-scale failure | Siegenfeld & Bar-Yam 2022 | AutoGPT step-level success / task-level failure | CONFIRMED |
| B1 | Undamped agent loops diverge/oscillate/exhaust | Wiener 1948, Ashby 1956 | AutoGPT loops, cascading errors, context exhaustion | CONFIRMED |
| B2 | Feedback delay increases instability | Control theory (classical) | Reflexion vs. ReAct (suggestive, confounded) | PARTIALLY CONFIRMED |
| B3 | No termination guarantee → resource exhaustion | BIBO stability | AutoGPT cost overruns, universal step limits | CONFIRMED (trivial) |
| C1 | World-model agents outperform model-free agents | Richens et al. 2025 (not original GRT) | CoT improvements, model-based vs. model-free RL | CONFIRMED |
| C2 | Failures cluster at world-model gaps | Conant & Ashby 1970 | Spatial reasoning failures, novel UI failures | PARTIALLY CONFIRMED |
| D1 | Context overflow is attenuation failure | Beer 1979, variety engineering | "Lost in the middle," RAG overloading | CONFIRMED |
| D2 | RAG failures are attenuator calibration failures | Beer 1979 | Precision-recall tradeoff in retrieval | CONFIRMED |
| D3 | Tool overload is amplification-attenuation imbalance | Beer 1979 | Same as A2 (Gorilla, ToolBench) | CONFIRMED |
| E1 | Self-evaluation fails on systematic errors | Beer 1972, VSM S3\* | Huang et al. 2023, Madaan et al. 2023 (94% FP) | CONFIRMED |
| E2 | Multi-agent without audit → compounding hallucination | Beer 1972, VSM S3\* | Cemri et al. 2025 (incorrect verification) | CONFIRMED |
| F1 | Self-evaluation bias worst on hardest problems | von Foerster 2003 | Calibration studies (suggestive) | PARTIALLY CONFIRMED |
| F2 | Same-model debate → echo chamber convergence | von Foerster 2003, eigenforms | Du et al. 2023, Cemri et al. 2025 (groupthink) | CONFIRMED |
| F3 | Sycophancy as observer-observer coupling | von Foerster 2003 | Sycophancy literature (but simpler explanations exist) | PARTIALLY CONFIRMED |
| G1 | No goal maintenance → goal drift | Ashby 1952, homeostasis | Arike et al. 2025 | CONFIRMED |
| G2 | Homeostatic goals safer than optimizing goals | Pihlakas et al. 2024 | Theoretical only | UNTESTED |
| G3 | Goal drift proportional to context pollution | Ashby 1952 | Directionally correct, functional form too simple | PARTIALLY CONFIRMED |
| H1 | Centralized orchestration bottleneck limits scaling | McCulloch 1945, heterarchy | Cemri et al. 2025, Item 29 analysis | CONFIRMED |
| H2 | Heterarchy outperforms hierarchy on diverse tasks | McCulloch 1945/1965 | No direct LLM agent test | UNTESTED |
| H3 | Orchestrator failure → correlated system failure | McCulloch 1945 | Cemri et al. 2025 | CONFIRMED |

### Tally

- **CONFIRMED:** 15
- **PARTIALLY CONFIRMED:** 5
- **UNTESTED:** 2
- **DISCONFIRMED:** 0

---

## Assessment

### What cybernetics gets right

The confirmed predictions cluster in three areas:

1. **Variety analysis** (A1-A4, D1-D3): Ashby's Law and Beer's variety engineering generate correct, specific predictions about agent-task mismatch, tool overload, and context management. The multi-scale extension (A4) is particularly valuable — it explains *why* agents succeed step-by-step while failing globally, which is a pattern the field has observed but not formally explained.

2. **Independent audit necessity** (E1-E2): Beer's S3\* directly predicts the Huang et al. and Madaan et al. results. This is the single strongest confirmed prediction in this document — it is specific, non-obvious (the ML community initially expected self-correction to work), and prescriptive (use independent evaluators).

3. **Coordination architecture** (H1, H3): McCulloch's heterarchy and Beer's variety axioms correctly predict centralized orchestration bottlenecks and correlated failures. The prescription (distribute coordination, use lateral mechanisms, eliminate single points of failure) is directly actionable.

### Where cybernetics is suggestive but not definitive

The partially confirmed predictions (B2, C2, F1, F3, G3) share a pattern: the directional prediction is correct, but either (a) simpler explanations exist that do not require cybernetic framing, or (b) the specific quantitative form of the prediction is too crude. Cybernetics illuminates these phenomena but does not uniquely predict them.

### What remains untested

G2 (homeostatic vs. optimizing goals for safety) and H2 (heterarchy vs. hierarchy for multi-agent coordination) are the two highest-value untested predictions. Both are specific, falsifiable, and would have significant implications if confirmed. G2 in particular has alignment implications: if homeostatic goal structures genuinely reduce dangerous failure modes, this would be a concrete cybernetics-to-alignment contribution.

### What cybernetics does NOT predict

Notably absent from this analysis: predictions about *specific* failure content (what the agent hallucinates, what errors it makes), training dynamics (how failures relate to pre-training data), or emergent capabilities. Cybernetics operates at the architectural and information-theoretic level. It predicts *that* failures will occur and *where* (at variety bottlenecks, in undamped loops, at world-model gaps), but not the specific content of those failures. For content-specific predictions, you need the ML literature, not cybernetics.

### The "common sense" problem

Several confirmed predictions (B3, C1, H3) are arguably common sense: "agents need resource limits," "world models help," "single points of failure are bad." Any competent engineer would predict these without reading Ashby. The cybernetic value-add is not the prediction itself but: (a) the formal framework that connects these intuitions to impossibility theorems and design constraints, and (b) the *quantitative* apparatus (variety gap computation, stability analysis) that could make these intuitions precise. Whether (b) is actually achievable at the scale of real agent systems remains an open question.

### Absence of disconfirmation

Zero predictions are disconfirmed. This is suspicious. It likely reflects a combination of: (a) cybernetic principles are sufficiently general that they are hard to falsify (Ashby's Law is a theorem, not an empirical claim), (b) I may be unconsciously selecting predictions that fit rather than predictions that challenge, and (c) the agent failure literature is rich enough that most reasonable failure-mode predictions will find supporting evidence.

The honest assessment: cybernetics generates correct predictions about agent failure modes at the architectural level, and several of these (A2, A4, E1, F2) are genuinely non-obvious and practically useful. But the framework operates at a level of abstraction where false negatives (important failure modes cybernetics does not predict) are more concerning than false positives (predictions cybernetics gets wrong). The field needs cybernetics-informed engineering, not just cybernetics-inspired commentary.

---

## Sources

### Cybernetic Theory
- Ashby, W.R. (1952). *Design for a Brain*. Chapman & Hall.
- Ashby, W.R. (1956). *An Introduction to Cybernetics*. Chapman & Hall.
- Beer, S. (1972). *Brain of the Firm*. Allen Lane.
- Beer, S. (1979). *The Heart of Enterprise*. Wiley.
- Beer, S. (1985). *Diagnosing the System for Organisations*. Wiley.
- Conant, R.C. & Ashby, W.R. (1970). "Every Good Regulator of a System Must Be a Model of That System." *Int. J. Systems Science* 1(2), 89-97.
- McCulloch, W.S. (1945). "A Heterarchy of Values Determined by the Topology of Nervous Nets." *Bull. Mathematical Biophysics* 7.
- McCulloch, W.S. (1965). *Embodiments of Mind*. MIT Press.
- Siegenfeld, A.F. & Bar-Yam, Y. (2022). "An Introduction to Complex Systems Science and Its Applications." *Complexity*.
- Von Foerster, H. (2003). *Understanding Understanding*. Springer.
- Wiener, N. (1948). *Cybernetics*. MIT Press.

### Agent Failure Literature
- Arike, M. et al. (2025). Goal drift in LLM agents. (Preprint.)
- Cemri, M. et al. (2025). "Why Do Multi-Agent LLM Systems Fail?" arXiv:2503.13657.
- Huang, J. et al. (2023). "Large Language Models Cannot Self-Correct Reasoning Without External Feedback." arXiv:2310.01798.
- Madaan, A. et al. (2023). "Self-Refine: Iterative Refinement with Self-Feedback." NeurIPS 2023. arXiv:2303.17651.

### Agent Architecture
- Du, Y. et al. (2023). "Improving Factuality and Reasoning in Language Models through Multiagent Debate." arXiv:2305.14325.
- Kambhampati, S. et al. (2024). "Can LLMs Really Self-Correct?" and LLM-Modulo architecture.
- Packer, C. et al. (2023). "MemGPT: Towards LLMs as Operating Systems." arXiv:2310.08560.
- Patil, S. et al. (2023). "Gorilla: Large Language Model Connected with Massive APIs." arXiv:2305.15334.
- Richens, J. et al. (2025). "General Agents Contain World Models." ICML 2025. arXiv:2506.01622.
- Schick, T. et al. (2023). "Toolformer: Language Models Can Teach Themselves to Use Tools." NeurIPS 2023. arXiv:2302.04761.
- Shinn, N. et al. (2023). "Reflexion: Language Agents with Verbal Reinforcement Learning." NeurIPS 2023. arXiv:2303.11366.

### Homeostatic Goals / Safety
- Pihlakas, R. et al. (2024). "From Homeostasis to Resource Sharing: Biologically and Economically Compatible Multi-Objective Multi-Agent AI Safety Frameworks." arXiv:2410.00081.
- Turner, A.M. et al. (2021). "Optimal Policies Tend to Seek Power." NeurIPS 2021.

### Prior Analysis in This Research
- Item 26: Formal Concept Mapping (this research, 30-predictions-vs-failure-modes.md)
- Item 28: Variety Calculus Applied to Tool Use (this research)
- Item 29: VSM Mapped onto Multi-Agent Frameworks (this research)
