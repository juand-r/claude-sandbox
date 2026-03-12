# Formal Concept Mapping: Cybernetic Formalisms to Agent Design Patterns

**Date:** 2026-03-12
**Stream G, Item 26**

---

## Methodology

This mapping connects cybernetic formalisms to agent design patterns with specific citations. Each entry is assessed for correspondence quality:

- **TIGHT**: Formal mathematical or structural correspondence. The agent pattern instantiates the cybernetic formalism in a way that preserves the formalism's key properties and predictions.
- **MODERATE**: Structural analogy with partial formal correspondence. The mapping illuminates something real but lacks the full formal apparatus.
- **LOOSE**: Suggestive analogy only. The mapping sounds compelling but does not survive rigorous scrutiny. Included for completeness but flagged.

---

## 1. Negative Feedback Loop

| Column | Content |
|--------|---------|
| **Cybernetic Formalism** | **Negative Feedback** (Wiener, 1948; Rosenblueth, Wiener & Bigelow, 1943). The output of a system is fed back as input with inverted sign, driving the system toward a reference state. Formally: error e = r - p, output o = f(e), where r is reference and p is perception. The defining property of purposive behavior per Wiener: "behavior, purpose and teleology" are explained by feedback structure, not mental states. |
| **Agent Design Pattern** | **ReAct loop** (Yao et al., 2022, ICLR 2023). Thought-Action-Observation cycle: the agent acts, observes the result, reasons about the discrepancy between current state and goal, and adjusts. The observation functions as the feedback signal; the thought functions as the comparator computing error; the next action is the corrective output. |
| **Key Papers** | Cybernetics side: Rosenblueth, Wiener & Bigelow (1943), "Behavior, Purpose and Teleology," *Philosophy of Science* 10(1). Wiener (1948), *Cybernetics*. Agent side: Yao et al. (2022), "ReAct: Synergizing Reasoning and Acting in Language Models," arXiv:2210.03629. |
| **Correspondence** | **LOOSE.** The structural analogy is real — ReAct does feed environmental observations back to inform the next action. But a control-theoretic feedback loop has specific formal properties (gain, phase margin, stability criteria, transfer function) that ReAct lacks entirely. There is no defined gain, no stability analysis, no characterization of delay. Calling ReAct a "feedback loop" is descriptively accurate but analytically empty — it does not enable any predictions that "the agent iterates until done" does not also enable. To make this mapping tight, one would need to: define the controlled variable, specify the reference signal, characterize the gain and delay, and analyze stability conditions. Nobody has done this for ReAct. |

---

## 2. Law of Requisite Variety

| Column | Content |
|--------|---------|
| **Cybernetic Formalism** | **Ashby's Law of Requisite Variety** (Ashby, 1956, *Introduction to Cybernetics*, Ch. 11). H(E) >= H(D) - H(R), where H(E) is entropy of outcomes, H(D) is entropy of disturbances, H(R) is entropy of regulator responses. An impossibility theorem: "only variety can destroy variety." The regulator's capacity as a regulator cannot exceed its capacity as a channel of communication. Not empirical; cannot be overturned by experiment. |
| **Agent Design Pattern** | **Tool use / function calling.** An LLM with only text generation has insufficient variety (action-space entropy) for tasks requiring code execution, file manipulation, or web browsing. Adding tools amplifies the agent's response variety. This predicts: (a) text-only agents fail at real-world tasks (confirmed empirically), (b) adding indiscriminate tools can degrade performance if selection accuracy is poor (confirmed by Gorilla/ToolBench finding that tool selection degrades with tool count — Patil et al., 2023). |
| **Key Papers** | Cybernetics side: Ashby (1956), *An Introduction to Cybernetics*, S.11/7-8. Siegenfeld & Bar-Yam (2022), "An Introduction to Complex Systems Science and Its Applications," *Complexity*. Agent side: Schick et al. (2023), "Toolformer," arXiv:2302.04761. Patil et al. (2023), "Gorilla: Large Language Model Connected with Massive APIs," arXiv:2305.15334. Wang et al. (2023), survey, arXiv:2308.11432. |
| **Correspondence** | **MODERATE.** The qualitative prediction is correct: agents need tools because text generation alone has insufficient variety for complex environments. Ashby's Law predicts this as a mathematical necessity. However, the quantitative apparatus does not transfer cleanly. Computing H(D) for "the variety of tasks a user might request" and H(R) for "the variety of an LLM's response space with N tools" is not practically feasible — the state spaces are too large and too poorly defined. The law works as a design heuristic (assess the variety gap, then amplify or attenuate), not as a quantitative engineering tool in this context. |

---

## 3. Good Regulator Theorem

| Column | Content |
|--------|---------|
| **Cybernetic Formalism** | **Good Regulator Theorem** (Conant & Ashby, 1970). "Every good regulator of a system must be a model of that system." Formally: the simplest optimal regulator is a deterministic function R = h(S), a homomorphism from system states to regulator actions. CRITICAL: the "model" here is a policy (state-to-action mapping), NOT a predictive world model. Erdogan (2021) established that this is equivalent to saying the optimal policy in a single-step MDP is deterministic — "almost trivial." |
| **Agent Design Pattern** | **World models in agents / chain-of-thought as implicit model.** The theorem is frequently cited to justify model-based agent architectures. More precisely, **Richens et al. (2025, ICML)** prove the stronger claim that the original theorem does not: multi-goal agents operating over multi-step horizons necessarily encode extractable world models in their policies. This is the result people thought the Good Regulator Theorem was. |
| **Key Papers** | Cybernetics side: Conant & Ashby (1970), "Every Good Regulator of a System Must Be a Model of That System," *Int. J. Systems Science* 1(2). Francis & Wonham (1976), "The Internal Model Principle of Control Theory," *Automatica* 12. Erdogan (2021), blog. Agent side: Richens et al. (2025), "General Agents Contain World Models," ICML 2025, arXiv:2506.01622. Virgo et al. (2025), "A Good Regulator Theorem for Embodied Agents," ALIFE 2025, arXiv:2508.06326. |
| **Correspondence** | **TIGHT (with Richens et al.), LOOSE (with original theorem).** The original Conant-Ashby theorem proves only that optimal policies are deterministic — this is weak. The Francis-Wonham Internal Model Principle is the real engineering result: a robust controller must contain a dynamical copy of disturbance dynamics. Richens et al. (2025) finally proves what people thought the Good Regulator Theorem proved: general, multi-goal agents must contain world models. The mapping from cybernetic formalism to agent necessity is tight when using Richens et al., but most citations in the agent literature reference the weaker original theorem for the stronger claim, which is a category error. |

---

## 4. Viable System Model (VSM)

| Column | Content |
|--------|---------|
| **Cybernetic Formalism** | **Beer's Viable System Model** (Beer, 1972/1979/1985). Five necessary subsystems for viability: S1 (Operations), S2 (Coordination/anti-oscillation), S3 (Control/inside-and-now), S3* (Audit), S4 (Intelligence/outside-and-then), S5 (Policy/identity). Grounded in Ashby's Law: variety must balance across all interfaces. The Recursive System Theorem: any viable system contains, and is contained in, viable systems. Three axioms of management specify quantitative variety balance conditions. |
| **Agent Design Pattern** | **Hierarchical multi-agent orchestration.** S1 = specialized worker agents. S2 = shared state, conflict resolution protocols. S3 = meta-agent monitoring operations, allocating resources. S3* = independent verification agent (not the same agent self-evaluating). S4 = environmental scanning agent proposing adaptations. S5 = system prompt, constitutional constraints, human oversight. Gorelkin (2025) provides the explicit mapping; MetaGPT (Hong et al., 2023) implicitly approximates VSM structure through SOPs. |
| **Key Papers** | Cybernetics side: Beer (1972), *Brain of the Firm*. Beer (1979), *The Heart of Enterprise*. Beer (1985), *Diagnosing the System for Organisations*. Agent side: Gorelkin (2025), "Stafford Beer's VSM for Building Cost-Effective Enterprise Agentic Systems." Hong et al. (2023), "MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework," arXiv:2308.00352. Cemri et al. (2025), multi-agent failure taxonomy. |
| **Correspondence** | **MODERATE.** The VSM provides the strongest single framework for multi-agent architecture — it is a tested organizational design with 50 years of application history, and the mapping to agent roles is concrete. The limitation: VSM was developed for human organizations where components have genuine autonomy and internal motivation. Whether LLM agents, which are stateless between invocations and lack intrinsic goals, can meaningfully instantiate VSM subsystems is unproven. Gorelkin's mapping is theoretical; no production multi-agent system has been built on VSM principles and compared empirically to alternatives. The Recursive System Theorem is powerful in principle (each agent should itself be a viable system) but untested for software agents. |

---

## 5. Homeostasis / Ultrastability

| Column | Content |
|--------|---------|
| **Cybernetic Formalism** | **Homeostasis** (Cannon, 1929; Ashby, 1952/1956). Essential variables must be kept within a set eta (physiological limits). Ashby's ultrastability: a two-loop system where (1) a fast inner loop regulates environmental variables via negative feedback, and (2) a slow outer loop modifies inner-loop parameters via random search when essential variables leave bounds. Formally: survival = stability of a set; if the set of "living" states is stable under environmental transformations, the organism survives. |
| **Agent Design Pattern** | **Homeostatic goal structures for AI safety** (Pihlakas, 2024). Replace unbounded reward maximization with bounded setpoint goals. The utility curve is inverted-U-shaped: both too little and too much are bad. Properties: bounded behavior, settle-to-rest (idle when satisfied), natural corrigibility (no incentive to resist shutdown when goals are met), multi-objective conjunctive structure. Also maps to: constrained/safe RL (Berkenkamp et al., 2017) where Lyapunov stability guarantees restrict exploration to verified-safe states. |
| **Key Papers** | Cybernetics side: Ashby (1952), *Design for a Brain*. Ashby (1956), *Introduction to Cybernetics*, Ch. 10. Agent side: Pihlakas et al. (2024), "From Homeostasis to Resource Sharing," arXiv:2410.00081. Berkenkamp et al. (2017), "Safe Model-Based Reinforcement Learning with Stability Guarantees," NeurIPS. Arike et al. (2025), goal drift in LLM agents. |
| **Correspondence** | **TIGHT (for Pihlakas), MODERATE (for Berkenkamp).** Pihlakas explicitly formalizes homeostatic goals in an MDP framework, preserving Ashby's key property: bounded goals produce qualitatively different agent behavior than unbounded maximization. The mapping preserves the formal structure: setpoints, error signals, settle-to-rest. Berkenkamp's safe RL uses Lyapunov stability (a control-theoretic cousin of homeostasis) with formal guarantees — tight in the mathematical sense but the connection to Ashby is indirect (mediated through control theory). Goal drift (Arike et al., 2025) is interpretable as reference signal degradation in cybernetic terms — context pollution corrupts the agent's goal representation, which is precisely what homeostatic design aims to prevent. |

---

## 6. Second-Order Feedback / Self-Observation

| Column | Content |
|--------|---------|
| **Cybernetic Formalism** | **Second-Order Cybernetics** (von Foerster, 1960/1991/2003). "The cybernetics of observing systems" — the observer is inside the system. Self-reference produces circular causality: A implies B implies A. Formal consequence: double closure (topological torus), leading to **eigenforms** — fixed points X satisfying O(X) = X, where O is the observation operator. Objects are "tokens for eigenbehaviors" — stable outputs of recursive observer-environment interactions (Kauffman, 2003/2005). |
| **Agent Design Pattern** | **Reflexion** (Shinn et al., 2023, NeurIPS). The agent observes its own performance, generates natural-language self-critique, and modifies its approach. The self-reflection model M_sr takes the trajectory, reward, and memory as input and produces verbal diagnosis. This is second-order: the agent observes its own observations and adjusts its observation/action strategy accordingly. The convergence of iterative self-critique to stable output is structurally an eigenform — a fixed point of recursive self-evaluation. |
| **Key Papers** | Cybernetics side: von Foerster (1991/2003), "Ethics and Second-Order Cybernetics" and *Understanding Understanding*. Kauffman (2005), "Eigenforms — Objects as Tokens for Eigenbehaviors," *Kybernetes* 34(1-2). Agent side: Shinn et al. (2023), "Reflexion: Language Agents with Verbal Reinforcement Learning," NeurIPS, arXiv:2303.11366. Madaan et al. (2023), "Self-Refine," arXiv:2303.17651. |
| **Correspondence** | **MODERATE.** The structural analogy is genuine: Reflexion implements observation-of-observation, which is the definition of second-order cybernetics. The eigenform framing is illuminating — iterative self-critique does converge to stable outputs (when it converges), and this convergence is formally a fixed point. However, von Foerster's second-order cybernetics is primarily an epistemological stance (the observer is always inside), not an engineering framework. It does not provide stability conditions, convergence guarantees, or design principles for self-referential systems. The mapping is structurally sound but operationally thin. Furthermore, Huang et al. (2023) show that LLM self-correction degrades reasoning performance without external feedback — the "observer" is not independent enough to provide genuine second-order observation. The variety of the error-detection mechanism matches the variety of the error-generation mechanism (same model), so systematic errors are precisely those that self-correction cannot detect. This is a limitation Ashby would have predicted. |

---

## 7. Perceptual Control Theory (PCT)

| Column | Content |
|--------|---------|
| **Cybernetic Formalism** | **Perceptual Control Theory** (Powers, 1973). Organisms control their *perceptions*, not their *outputs*. Hierarchy of control levels (11 levels from intensity to system concept), where higher levels set reference signals for lower levels. Only the bottom level acts on the environment. Error e = r - p, output o = O(integral of e * dt). The system controls by varying behavior to maintain perceptual invariance despite disturbances. Reorganization (learning): random parameter modification driven by intrinsic error, halting when error reaches zero — directly from Ashby's ultrastability. |
| **Agent Design Pattern** | **Goal-conditioned hierarchical agents.** The PCT architecture inverts the standard agent pattern (Goal -> Plan -> Action -> Observe -> Adjust). A PCT-style agent would be organized around *what it monitors* (perceptual variables) rather than *what it does* (sub-policies). Higher-level systems set reference states for lower-level systems. This maps partially to: Voyager's (Wang et al., 2023) skill library as hierarchical control, and to the general pattern of hierarchical task decomposition where a high-level planner sets subgoals for executors. |
| **Key Papers** | Cybernetics side: Powers (1973/2005), *Behavior: The Control of Perception*. Powers, Clark & McFarland (1960), "A General Feedback Theory of Human Behavior," *Perceptual and Motor Skills* 11. Young et al. (2020), "Implementation of a Perceptual Controller for an Inverted Pendulum Robot," *J. Intelligent & Robotic Systems*. Agent side: Wang et al. (2023), "Voyager: An Open-Ended Embodied Agent with LLMs," arXiv:2305.16291. Park et al. (2023), "Generative Agents," UIST 2023. |
| **Correspondence** | **LOOSE.** This is one of the most promising but least developed mappings. No LLM agent system has been designed on PCT principles. The architectural inversion (organize around what you perceive, not what you do) generates testable predictions: PCT-organized agents should be more robust to novel disturbances than plan-organized agents. But this is untested. The hierarchical structure of PCT (reference signals flowing down, perceptual signals flowing up) has clear parallels in hierarchical agent systems, but current implementations do not preserve PCT's key property that higher levels specify *what to perceive*, not *what to do*. Voyager's curriculum system approaches this (it specifies what to explore, not how), but the correspondence is informal. |

---

## 8. Variety Engineering (Amplification + Attenuation)

| Column | Content |
|--------|---------|
| **Cybernetic Formalism** | **Variety Engineering** (Beer, 1979/1985, extending Ashby). Since the environment's variety always exceeds the organization's capacity, viability requires: **variety attenuators** (perceptual filters, exception reporting, aggregation, sampling) to reduce incoming variety, and **variety amplifiers** (tool diversification, delegation, multiple response repertoires) to increase outgoing variety. Beer's First Principle of Organisation: "Managerial, operational and environmental varieties... tend to equate; they should be designed to do so with minimum damage to people and cost." |
| **Agent Design Pattern** | **Context window management + tool expansion.** Attenuators: RAG retrieval (selects relevant documents from large corpora), summarization of long contexts, filtering of tool outputs to relevant information, structured output schemas. Amplifiers: tool libraries, code execution environments, web search, multi-agent delegation. The agent community has discovered empirically that both sides matter: too much context degrades performance (attenuation failure), and too few tools limits capability (amplification failure). |
| **Key Papers** | Cybernetics side: Beer (1979), *The Heart of Enterprise*. Beer (1985), *Diagnosing the System for Organisations*. Agent side: Lewis et al. (2020), "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," NeurIPS. Packer et al. (2023), "MemGPT: Towards LLMs as Operating Systems," arXiv:2310.08560. |
| **Correspondence** | **MODERATE.** The conceptual mapping is clean and practically useful: think of every agent design decision as either amplifying or attenuating variety, and ensure balance. RAG is a variety attenuator. Tool use is a variety amplifier. Context window management is variety attenuation. The limitation: saying "this is variety attenuation" does not tell you *how* to attenuate well. The engineering challenges of RAG (retrieval accuracy, chunk size, relevance scoring) are not illuminated by the variety framing. Beer's framework provides architectural guidance (ensure you have both amplifiers and attenuators at every interface) but not implementation guidance. |

---

## 9. Bateson's Levels of Learning

| Column | Content |
|--------|---------|
| **Cybernetic Formalism** | **Levels of Learning** (Bateson, 1964/1972, *Steps to an Ecology of Mind*). Based on Russell's Theory of Logical Types. Learning 0: fixed response. Learning I: correcting errors within a fixed set of alternatives (classical conditioning, operant learning). Learning II (deutero-learning): learning to learn — changing *how* you approach categories of problems, acquiring "habits of contextualizing." Learning III: restructuring the learning framework itself — changing the premises of Learning II. Each level is change in the process of the level below. Learning II generates self-validating premises (positive feedback loops at the character level). |
| **Agent Design Pattern** | **In-context learning (L-I) vs. meta-learning (L-II) vs. self-modifying agents (L-III).** Most current agents operate at Learning I: within-session error correction (ReAct adjusting strategy based on failed search). Reflexion approaches Learning II: learning persistent lessons that shape approach to future task categories. Learning III is the alignment frontier: agents that restructure their own objectives or evaluation frameworks. No current agent reliably achieves Learning II across sessions; Learning III is theoretical. |
| **Key Papers** | Cybernetics side: Bateson (1972), *Steps to an Ecology of Mind*, "The Logical Categories of Learning and Communication." Agent side: Yao et al. (2022), ReAct. Shinn et al. (2023), Reflexion. Brown et al. (2020), "Language Models Are Few-Shot Learners" (in-context learning). |
| **Correspondence** | **MODERATE.** Bateson's taxonomy is genuinely clarifying — it names a real gap in current agent capabilities (the absence of Learning II) and identifies a real danger (Learning III as both breakthrough and catastrophe). The mapping from Learning I to in-context error correction is clean. The mapping from Learning II to meta-learning is suggestive but imprecise: Bateson's Learning II involves persistent character change (self-validating premises), while agent meta-learning typically involves task-distribution adaptation without persistent character. Reflexion's "verbal reinforcement learning" stores reflections in memory, approaching Learning II, but only within a session — the persistence and self-validating dynamics that Bateson describes are absent. The taxonomy is essential for classifying agent learning; the formal apparatus (logical types) does not transfer to agent implementation. |

---

## 10. Autopoiesis / Operational Closure

| Column | Content |
|--------|---------|
| **Cybernetic Formalism** | **Autopoiesis** (Maturana & Varela, 1972/1980). An autopoietic system is a network of processes that produces the components which (i) regenerate the network that produced them, and (ii) constitute the system as a concrete unity by specifying its boundary. Operationally closed, thermodynamically open. Organization (abstract relations) is invariant; structure (concrete components) changes continuously. Structural coupling: the system's structure changes through interactions with the environment while organization is preserved. Di Paolo (2005) added *adaptivity*: graded evaluation of distance from viability boundaries. |
| **Agent Design Pattern** | **Self-maintaining agent systems (theoretical).** No current AI agent is autopoietic: weights require external training, code requires external developers, infrastructure requires external maintenance. The concept identifies *what genuine autonomy would mean*: an agent that maintains its own inference capability, repairs its own errors, and produces the processes it needs to operate. Partial instantiation: agents with self-healing capabilities, automatic error recovery, and self-modifying code approach operational closure without achieving it. Di Paolo's adaptivity maps to: agents that monitor their own operational health with graded signals (not just binary success/failure). |
| **Key Papers** | Cybernetics side: Maturana & Varela (1980), *Autopoiesis and Cognition*. Di Paolo (2005), "Autopoiesis, Adaptivity, Teleology, Agency," *Phenomenology and the Cognitive Sciences*. Froese & Stewart (2010), "Life After Ashby," *Cybernetics & Human Knowing*. Agent side: No direct implementation papers. Theoretical framing in: Froese & Ziemke (2009), "Enactive Artificial Intelligence," *Artificial Intelligence* 173. |
| **Correspondence** | **LOOSE.** Current AI agents fail the autopoiesis test completely. They are allopoietic (they produce something other than themselves). The concept is valuable as a framing device — it defines what "autonomous agent" would mean rigorously — but it provides no engineering guidance for current systems. The structural coupling concept (agent and environment co-adapt while preserving organization) is relevant to RLHF/fine-tuning dynamics but has not been formalized in that context. Di Paolo's adaptivity (graded viability monitoring) is the most actionable element: agents should monitor not just task success but operational health. This remains unimplemented. |

---

## 11. Conversation Theory

| Column | Content |
|--------|---------|
| **Cybernetic Formalism** | **Conversation Theory** (Pask, 1975/1976). Knowledge emerges through conversation between participants. Two language levels: Lo (object language, about the domain) and Lp (protolanguage, about how conversations work). Entailment structures: directed graphs of topics and derivation relations. The **teachback mechanism**: understanding is verified when participant B can reproduce participant A's explanation in B's own terms — and A confirms. Formally: Ap(Con(T)) => D(T), where Con(T) is the concept, Ap is concurrent execution, D(T) is the description. |
| **Agent Design Pattern** | **Multi-agent debate / verification protocols.** Pask's teachback is structurally identical to multi-agent verification: Agent A proposes a solution, Agent B restates it in different terms, Agent A confirms or corrects. This is implemented (without Pask citation) in debate-based alignment proposals and in multi-agent code review patterns. The Lo/Lp distinction maps to: task-level communication (Lo) vs. meta-communication about communication protocols (Lp). |
| **Key Papers** | Cybernetics side: Pask (1975), *Conversation, Cognition and Learning*. Pask (1976), *Conversation Theory: Applications in Education and Epistemology*. Agent side: Du et al. (2023), "Improving Factuality and Reasoning in Language Models through Multiagent Debate," arXiv:2305.14325. Battle (2023), application of Conversation Theory to LLM agents. Irving et al. (2018), "AI Safety via Debate," arXiv:1805.00899. |
| **Correspondence** | **MODERATE.** The teachback mechanism maps cleanly to multi-agent verification, and this is a genuine structural correspondence — both achieve knowledge verification through reconstruction rather than repetition. The Lo/Lp distinction is also genuinely useful: multi-agent systems need both task communication and meta-communication protocols, and confusing the two causes failures. The limitation: Pask's full formal apparatus (entailment meshes, L* languages, concurrent execution indexes) is complex and has not been mapped to agent architectures. The correspondence is at the level of the teachback mechanism, not the full theory. |

---

## 12. Stigmergy

| Column | Content |
|--------|---------|
| **Cybernetic Formalism** | **Stigmergy** (Grasse, 1959; Heylighen, 2016). Indirect coordination: the trace left by an action in a medium stimulates subsequent actions. Formally: P(action \| trace) > P(action \| no trace). Requires no planning, central control, direct communication, simultaneous presence, or mutual awareness. Coordination emerges from positive feedback (successful traces strengthen) and negative feedback (unsuccessful traces decay). The coordination state is in the environment, not in any agent's model. |
| **Agent Design Pattern** | **Shared artifact coordination in multi-agent coding.** When multiple agents work on a shared codebase, each agent's commits/changes serve as traces that guide subsequent agents' actions. Git repositories, shared documents, and task boards are stigmergic media. Also: Wikipedia-style collaborative editing, where edits by one contributor stimulate further edits by others. The pattern appears in multi-agent frameworks where agents communicate through shared state rather than direct messaging. |
| **Key Papers** | Cybernetics side: Grasse (1959), *Insectes Sociaux*. Heylighen (2016), "Stigmergy as a Universal Coordination Mechanism," *Cognitive Systems Research* 38. Agent side: No paper explicitly designs an LLM agent system on stigmergic principles. Closest: shared-workspace patterns in AutoGen, CrewAI, and the general pattern of agents communicating through shared artifacts rather than direct messages. |
| **Correspondence** | **MODERATE.** The structural mapping is clean: shared codebases and documents are stigmergic media; agent modifications are traces; subsequent agents respond to traces. The key stigmergic property — coordination without direct communication — is genuinely useful for scaling multi-agent systems beyond the point where direct inter-agent messaging becomes a bottleneck. The limitation: no LLM agent system has been explicitly designed on stigmergic principles, so the mapping is post-hoc rather than generative. The formal property P(action \| trace) > P(action \| no trace) is trivially satisfied by any shared-state system and does not discriminate good from bad designs. |

---

## 13. Active Inference / Free Energy Principle

| Column | Content |
|--------|---------|
| **Cybernetic Formalism** | **Free Energy Principle / Active Inference** (Friston, 2010; Sajid et al., 2021). Self-organizing systems minimize variational free energy F = E_q[ln q(s) - ln p(o,s)]. Decomposes into: (a) minimizing surprise (self-evidencing), (b) making beliefs accurate (approximate Bayesian inference). Active inference: the agent selects actions to minimize expected free energy, which naturally decomposes into epistemic value (exploration) and pragmatic value (exploitation). Instantiates the Good Regulator Theorem, satisfies requisite variety, unifies perception and action under one objective. Tschantz et al. (2020) established formal equivalence with RL. |
| **Agent Design Pattern** | **Exploration-exploitation in agent planning.** Active inference provides a principled solution to the exploration-exploitation tradeoff without ad-hoc mechanisms (epsilon-greedy, UCB). The epistemic/pragmatic decomposition of expected free energy maps to: agents that explore to reduce uncertainty about the environment before exploiting knowledge to achieve goals. Also maps to: agents that maintain homeostasis by minimizing surprise (staying in expected states). The self-evidencing problem (agents observe their own actions and infer preferences consistent with observed patterns) maps to accumulated context bias in LLM agents. |
| **Key Papers** | Cybernetics side: Friston (2010), "The Free-Energy Principle: A Unified Brain Theory?" *Nature Reviews Neuroscience* 11. Sajid et al. (2021), "Active Inference: Demystified and Compared," *Neural Computation* 33(3). Tschantz et al. (2020), "Reinforcement Learning Through Active Inference," arXiv:2002.12636. Agent side: No competitive active-inference LLM agent exists. Closest bridging: VERSES AI research program; Da Costa et al. (2020), "Active Inference on Discrete State-Spaces." |
| **Correspondence** | **TIGHT (mathematically), LOOSE (practically).** The formal framework is rigorous: active inference is mathematically equivalent to RL (Tschantz et al., 2020), instantiates the Good Regulator Theorem, and provides principled exploration-exploitation balance. The practical limitation is severe: active inference agents remain a research curiosity, not competitive with LLM-based agents on standard benchmarks. The gap between the mathematical elegance of the framework and its practical utility for LLM agent design is large. The self-evidencing problem (convergence to wrong eigenform) is a genuine theoretical contribution to understanding agent failure modes, but it has not been empirically validated in LLM contexts. |

---

## 14. Stability Analysis (Lyapunov / Control-Theoretic)

| Column | Content |
|--------|---------|
| **Cybernetic Formalism** | **Stability of equilibria** (Ashby, 1956; Lyapunov, 1892; modern control theory). Ashby: state a is stable under displacement D if lim(n->inf) T^n D(a) = a. Stability is always relative to a specified set of displacements. Lyapunov stability: a system is stable if a positive-definite function V(x) decreases along trajectories (dV/dt < 0). For discrete systems: V(x_{k+1}) < V(x_k). Provides formal guarantees of convergence and boundedness without solving the full dynamics. |
| **Agent Design Pattern** | **Agent loop convergence and termination.** The AutoGPT failure modes (infinite loops, error amplification, context exhaustion) are control instabilities: positive feedback (errors compounding), insufficient damping (no mechanism to reduce oscillation), and unbounded delay (context window filling without resolution). Berkenkamp et al. (2017) apply Lyapunov stability to safe RL: explore only states where stability can be verified given current model uncertainty. No LLM agent loop has been analyzed with these tools. |
| **Key Papers** | Cybernetics side: Ashby (1956), *Introduction to Cybernetics*, Ch. 5. Berkenkamp et al. (2017), "Safe Model-Based Reinforcement Learning with Stability Guarantees," NeurIPS. Agent side: No paper applies control-theoretic stability analysis to LLM agent loops. This is identified as the lowest-hanging fruit in the bridging literature. The failure mode analysis in Cemri et al. (2025) documents instabilities without formal analysis. |
| **Correspondence** | **TIGHT (in principle), ABSENT (in practice).** The mathematical tools exist and are directly applicable: model an agent loop as a discrete-time system, define a Lyapunov-like function (e.g., distance to goal + resource consumption), check whether it decreases along agent trajectories. The formal correspondence is available. The problem is that nobody has done it. This is the most actionable gap in the cybernetics-to-agents bridge. Even a crude application (gain margin analysis of a ReAct loop) would be more principled than current practice of "run it and see." |

---

## 15. McCulloch's Heterarchy / Redundancy of Potential Command

| Column | Content |
|--------|---------|
| **Cybernetic Formalism** | **Heterarchy** (McCulloch, 1945). Circular authority structures: A leads in context X, B leads in context Y, C leads in context Z, even if this creates authority cycles. **Redundancy of Potential Command** (McCulloch, 1960s): "power resides where information resides." The component with the most relevant information for the current subtask takes the lead. Leadership is emergent, not assigned. |
| **Agent Design Pattern** | **Dynamic role assignment in multi-agent systems.** Current frameworks overwhelmingly use fixed orchestration (LangGraph supervisor, CrewAI manager). McCulloch predicts this is a scaling bottleneck and robustness weakness — the orchestrator is a single point of failure, a variety bottleneck, and a latency source. The alternative: agents dynamically assume leadership based on which has the most relevant information. This appears partially in: debate frameworks where the "winning" argument shifts control, and in ensemble methods where different models lead on different subtasks. |
| **Key Papers** | Cybernetics side: McCulloch (1945), "A Heterarchy of Values Determined by the Topology of Nervous Nets," *Bulletin of Mathematical Biophysics* 7. McCulloch (1959/1965), "Redundancy of potential command" concept, various publications in *Embodiments of Mind*. Agent side: No LLM agent system explicitly implements heterarchical control. Closest: round-robin debate in Du et al. (2023); AutoGen's conversable agent pattern where different agents take turns leading. |
| **Correspondence** | **MODERATE.** The design principle is clear and actionable: build multi-agent systems where leadership shifts dynamically based on information relevance. McCulloch's formalism (circular authority determined by network topology) maps to multi-agent systems where each agent can propose actions and the group selects which proposal to follow based on competence/confidence signals. The limitation: current LLM agents lack reliable self-assessment of their own competence, making "power resides where information resides" difficult to implement — the agent with the most relevant information may not know it has the most relevant information. |

---

## 16. Structural Coupling / Co-Evolution

| Column | Content |
|--------|---------|
| **Cybernetic Formalism** | **Structural Coupling** (Maturana & Varela, 1980). When two autopoietic systems interact recurrently, each triggers structural changes in the other while both maintain their organization. The systems become structurally coupled — each adapts to the other over time. Neither "instructs" the other; perturbations are interpreted through the receiving system's own structure. Extended to social domains as "consensual coordination of actions" — the basis of language and culture. |
| **Agent Design Pattern** | **Human-AI co-adaptation / RLHF dynamics.** When a human uses an AI agent over time, they adapt to each other. The human learns what the agent is good at and routes tasks accordingly. The agent (through feedback, corrections, fine-tuning, memory) adjusts to the human's preferences. RLHF is a formalized structural coupling: human feedback triggers structural changes (weight updates) in the model, while the model's outputs shape the human's feedback behavior. Over extended use, human and agent become structurally coupled — each influencing the other's behavior patterns. |
| **Key Papers** | Cybernetics side: Maturana & Varela (1980), *Autopoiesis and Cognition*. Maturana (1978), "Biology of Language: The Epistemology of Reality." Agent side: Christiano et al. (2017), "Deep Reinforcement Learning from Human Preferences," NeurIPS. No paper explicitly models human-AI interaction as structural coupling. |
| **Correspondence** | **LOOSE.** The analogy is suggestive and identifies a real phenomenon (human-AI co-adaptation), but structural coupling requires autopoietic systems on both sides — systems that are operationally closed and self-producing. LLM agents are not autopoietic. The coupling is also asymmetric in ways Maturana's framework does not address: the human has genuine autonomy while the agent has only simulated autonomy. That said, the observation that RLHF is a form of recurrent perturbation-driven structural change is genuinely insightful — it identifies dynamics (co-evolution, deskilling, over-reliance) that current agent design treats as externalities rather than as intrinsic features of the coupled system. |

---

## 17. Ashby's Constraint and Regulation as Blocking Variety

| Column | Content |
|--------|---------|
| **Cybernetic Formalism** | **Regulation as Blocking Variety Transmission** (Ashby, 1956, Ch. 10). "An essential function of F as a regulator is that it shall block the transmission of variety from disturbance to essential variable." A good regulator prevents information about disturbances from reaching the outcome. A good pilot acts as a barrier against transmitting weather information to passengers. Formally: regulation exploits constraints (regularities) in the environment — "the organism can adapt just so far as the real world is constrained, and no further." |
| **Agent Design Pattern** | **Error isolation / graceful degradation in agent pipelines.** An agent orchestrator that shields downstream components from upstream failures is performing variety blocking. Circuit-breaker patterns (stop retrying after N failures), fallback strategies (use cached response when API fails), and error containment (catch exceptions at module boundaries) all block variety from disturbances reaching essential variables (user-facing outputs). Also: the LLM-Modulo architecture (Kambhampati et al., 2024) — LLM generates candidates, external verifier filters, user sees only verified outputs — is a variety-blocking design. |
| **Key Papers** | Cybernetics side: Ashby (1956), *Introduction to Cybernetics*, S.10/6-7. Agent side: Kambhampati et al. (2024), "Can LLMs Really Self-Correct?" and "LLM-Modulo" architecture. Madaan et al. (2023), Self-Refine (94% false-positive rate on math illustrates failure of variety blocking). |
| **Correspondence** | **MODERATE.** The framing is genuinely useful for agent architecture: think of each component as either blocking or transmitting variety from disturbances. The LLM-Modulo architecture is a clean instantiation: the external verifier blocks the variety of LLM errors from reaching the user. The 94% false-positive rate in Self-Refine's self-evaluation directly measures the failure of the variety-blocking mechanism — the evaluator cannot distinguish errors from correct outputs, so disturbance variety passes through unblocked. The limitation: "block variety" as a design principle does not specify *how* to build effective filters. |

---

## Summary Table

| # | Cybernetic Formalism | Agent Pattern | Correspondence | Key Gap |
|---|---------------------|---------------|----------------|---------|
| 1 | Negative feedback (Wiener 1948) | ReAct loop | LOOSE | No formal stability analysis of agent loops |
| 2 | Requisite variety (Ashby 1956) | Tool use / function calling | MODERATE | Quantitative variety computation infeasible at scale |
| 3 | Good Regulator (Conant-Ashby 1970) | World models in agents | TIGHT (Richens 2025) | Original theorem weaker than cited |
| 4 | VSM (Beer 1972) | Multi-agent orchestration | MODERATE | No empirical comparison with standard frameworks |
| 5 | Homeostasis / ultrastability | Homeostatic goals for safety | TIGHT (Pihlakas 2024) | Limited empirical testing |
| 6 | Second-order cybernetics (von Foerster) | Reflexion / self-critique | MODERATE | LLMs cannot genuinely self-correct reasoning |
| 7 | PCT (Powers 1973) | Hierarchical goal-conditioned agents | LOOSE | No PCT-designed LLM agent exists |
| 8 | Variety engineering (Beer 1979) | Context management + tool expansion | MODERATE | Framework guides architecture, not implementation |
| 9 | Learning levels (Bateson 1972) | In-context vs. meta-learning | MODERATE | Agents lack Learning II (persistent habits) |
| 10 | Autopoiesis (Maturana & Varela 1980) | Self-maintaining agents | LOOSE | AI agents are not autopoietic |
| 11 | Conversation Theory (Pask 1975) | Multi-agent debate / teachback | MODERATE | Full formal apparatus unmapped |
| 12 | Stigmergy (Grasse 1959) | Shared-artifact coordination | MODERATE | No explicit stigmergic agent system built |
| 13 | Active inference (Friston 2010) | Exploration-exploitation balance | TIGHT/LOOSE | Mathematically rigorous but not competitive |
| 14 | Stability analysis (Lyapunov) | Agent loop convergence | TIGHT (in principle) | Nobody has done the analysis |
| 15 | Heterarchy (McCulloch 1945) | Dynamic role assignment | MODERATE | Agents lack reliable self-competence assessment |
| 16 | Structural coupling (Maturana 1980) | Human-AI co-adaptation / RLHF | LOOSE | Requires autopoietic systems on both sides |
| 17 | Regulation as variety blocking (Ashby 1956) | Error isolation / LLM-Modulo | MODERATE | Principle clear, implementation guidance absent |

---

## Assessment

Of the 17 mappings:

- **TIGHT**: 3 (Good Regulator via Richens, homeostasis via Pihlakas, stability analysis in principle/active inference mathematically)
- **MODERATE**: 10
- **LOOSE**: 4 (ReAct as feedback loop, PCT, autopoiesis, structural coupling)

The pattern: cybernetic formalisms that come with quantitative machinery (requisite variety, stability analysis, free energy minimization) produce tighter mappings than those that are primarily qualitative or philosophical (autopoiesis, second-order cybernetics, structural coupling). The tightest correspondences occur where modern researchers have explicitly formalized the bridge (Richens extending the Good Regulator Theorem, Pihlakas implementing homeostatic goals, Tschantz connecting active inference to RL).

The most actionable gap is stability analysis (#14): the formal tools exist, the agent loops exist, but nobody has connected them. This is not a research frontier — it is straightforward engineering that the field has simply not done.

The biggest risk of overclaiming is #1 (ReAct as feedback loop). The structural analogy is trivially true and analytically empty. Calling everything a "feedback loop" without the formal apparatus of control theory adds terminology without insight.

---

## Sources

Full citations are provided inline. Key works referenced across multiple mappings:

- Ashby, W.R. (1956). *An Introduction to Cybernetics*. Chapman & Hall.
- Beer, S. (1972). *Brain of the Firm*. Allen Lane.
- Beer, S. (1979). *The Heart of Enterprise*. Wiley.
- Bateson, G. (1972). *Steps to an Ecology of Mind*. Ballantine.
- Conant, R.C. & Ashby, W.R. (1970). "Every Good Regulator of a System Must Be a Model of That System." *Int. J. Systems Science* 1(2), 89-97.
- Friston, K. (2010). "The Free-Energy Principle." *Nature Reviews Neuroscience* 11, 127-138.
- Maturana, H. & Varela, F. (1980). *Autopoiesis and Cognition*. Reidel.
- McCulloch, W.S. (1945). "A Heterarchy of Values." *Bull. Mathematical Biophysics* 7.
- Pask, G. (1976). *Conversation Theory*. Elsevier.
- Powers, W.T. (1973). *Behavior: The Control of Perception*. Aldine.
- Richens, J. et al. (2025). "General Agents Contain World Models." ICML 2025.
- Von Foerster, H. (2003). *Understanding Understanding*. Springer.
- Wiener, N. (1948). *Cybernetics*. MIT Press.
- Yao, S. et al. (2022). "ReAct." ICLR 2023.
- Shinn, N. et al. (2023). "Reflexion." NeurIPS 2023.
