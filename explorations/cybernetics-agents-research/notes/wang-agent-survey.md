# Scholarly Notes: "A Survey on Large Language Model based Autonomous Agents"

**Wang, L., Ma, C., Feng, X., et al. (2023/2024). arXiv:2308.11432.**
First submitted August 2023, revised through March 2025 (v7).
13 authors from Renmin University of China and collaborators.

**Notes taken**: 2026-03-12

---

## 1. Overview and Framing

The survey proposes a **unified framework** for constructing LLM-based autonomous agents,
organized around four architectural modules: **Profile, Memory, Planning, Action**.

The authors cite Franklin and Graesser's definition of autonomous agent: *"a system situated
within and a part of an environment that senses that environment and acts on it, over time, in
pursuit of its own agenda."* This is a standard AI/agent definition, notably not a cybernetic one
-- it foregrounds "agenda" (goal-directedness) rather than regulation or adaptation.

The paper distinguishes agent construction from question-answering: agents must fulfill roles
and self-evolve in dynamic environments. They frame the LLM as a kind of "brain" or "controller"
that already has extensive world knowledge from pretraining, and the architectural modules as
ways of scaffolding that brain into an agent.

**Key metaphor used**: The four modules are the agent's "hardware" (architecture), while
skills, knowledge, and learned capabilities are the "software." This is an engineering metaphor,
not a biological or cybernetic one.

### Paper Structure

1. Introduction
2. LLM-based Autonomous Agent Construction
   - 2.1 Agent Architecture Design
     - 2.1.1 Profiling Module
     - 2.1.2 Memory Module
     - 2.1.3 Planning Module
     - 2.1.4 Action Module
   - 2.2 Agent Capability Acquisition
3. LLM-based Autonomous Agent Application
   - 3.1 Social Science
   - 3.2 Natural Science
   - 3.3 Engineering
4. LLM-based Autonomous Agent Evaluation
5. Related Surveys
6. Challenges
7. Conclusion

---

## 2. The Four-Module Taxonomy

### 2.1 Profile Module

**Purpose**: Identifies and specifies the agent's role, determining behavioral characteristics.

**Three profiling strategies**:

1. **Handcrafting**: Manually written role descriptions ("you are an outgoing person"). Used in
   Generative Agents, MetaGPT, ChatDev. Flexible but labor-intensive.

2. **LLM-Generation**: Automatic profile generation. Define rules, provide seed examples, LLM
   generates the rest. RecAgent uses this. Scalable but less controllable.

3. **Dataset Alignment**: Profiles extracted from real-world datasets (e.g., demographics from
   American National Election Studies). Converts demographic data to natural language prompts.
   Accurate reflection of real populations but limited to available data.

**Profile information types**: Basic (age, gender, career), Psychological (personality traits),
Social (relationships between agents).

**What this accomplishes**: The profile module essentially sets initial conditions and constraints
on agent behavior. It answers "who is this agent?" From a cybernetic perspective, this is
analogous to setting the **reference signal** or **setpoint** for the system -- it defines what
the agent is trying to be/do, though the paper doesn't frame it this way.

### 2.2 Memory Module

**Core function**: Stores environmental perceptions and leverages recorded information to
facilitate future actions. Enables experience accumulation and behavioral consistency.

#### Memory Structures

**Unified Memory**: Only short-term memory via in-context learning. Information written directly
into prompts. Examples: RLP (conversation states), SayPlan (scene graphs), DEPS (task plans).
Constrained by LLM context window. Simple but limited.

**Hybrid Memory**: Explicitly models both:
- **Short-term**: Recent perceptions buffered in prompts (analogous to working memory)
- **Long-term**: Important information consolidated over time in vector databases
  (analogous to episodic/semantic memory)

Examples: Generative Agents, Reflexion, AgentSims, GITM.

#### Memory Formats

| Format | Example | Strengths | Weaknesses |
|--------|---------|-----------|------------|
| Natural language | Reflexion, Voyager | Flexible, semantically rich | Inefficient retrieval |
| Embeddings | MemoryBank | Fast querying | Loss of semantic richness |
| Databases (SQL) | ChatDB | Precise manipulation | Requires structured design |
| Structured lists | GITM (hierarchical tree) | Efficient, concise | Limited expressiveness |

Many systems use **hybrid formats** (e.g., GITM: embedding keys with natural language values).

#### Memory Operations

**Reading**: Extracts information relevant to current situation. The core formula:

    m* = argmax_m (alpha * s_rec(q,m) + beta * s_rel(q,m) + gamma * s_imp(m))

Where:
- `s_rec`: recency score (temporal proximity)
- `s_rel`: relevance score (query similarity)
- `s_imp`: importance score (inherent memory value)
- `alpha, beta, gamma`: weighting parameters

This is essentially a **weighted retrieval function** combining three salience dimensions.
Common configurations: relevance-only (alpha=gamma=0) or equal weighting (all = 1.0).

**Writing**: Stores perceived environmental information. Two sub-problems:
- *Memory duplication*: Handling similar information (GITM condenses N=5 similar sequences)
- *Memory overflow*: Managing storage limits (FIFO buffers, explicit deletion)

**Reflection**: Enables agents to summarize and infer abstract, high-level information from
raw memories. Process: generate questions from recent memories, query memory, produce insights.

Example: Generative Agents summarizes "Klaus Mueller writing research paper" + multiple
interaction memories into the insight "Klaus is dedicated to research." Reflection can be
**hierarchical** -- insights generated from existing insights.

ExpeL compares successful/failed trajectories within the same task to extract lessons.

#### Comparison to Cognitive Architecture Memory

The paper draws from **human cognitive science** but does NOT explicitly cite SOAR, ACT-R, or
other formal cognitive architectures. They reference the progression: sensory memory ->
short-term memory -> long-term memory.

**Key difference from cognitive architectures**:
- SOAR has explicit working memory, procedural memory (productions), and semantic/episodic
  long-term memory with specific mechanisms for chunking and learning.
- ACT-R has declarative memory (facts) vs. procedural memory (productions), with activation-
  based retrieval governed by base-level learning and spreading activation equations.
- The Wang et al. memory model is **looser** -- it borrows the STM/LTM distinction but
  implements it through prompt engineering (STM) and vector databases (LTM). There is no
  formal production system or activation calculus. The "reflection" mechanism is novel to
  LLM agents and has no direct counterpart in classical cognitive architectures -- it is
  more like a meta-cognitive summarization process.

### 2.3 Planning Module

**Purpose**: Decompose complex tasks into manageable subtasks. Analogous to human hierarchical
problem-solving.

#### Planning WITHOUT Feedback

**Single-path reasoning** (linear chain of steps):
- Chain of Thought (CoT): Include reasoning steps as prompt examples
- Zero-shot CoT: Trigger with "think step by step"
- Re-Prompting: Validate prerequisites at each step, regenerate on failure
- ReWOO: Separate plan generation from observation; generate independently then combine
- HuggingGPT: Decompose into sub-goals solved via HuggingFace tools
- SWIFTSAGE: Combine fast pattern-based responses (SWIFT) + slow LLM planning (SAGE)

**Multi-path reasoning** (tree/graph structure, multiple alternatives):
- CoT-SC (Self-Consistency): Generate multiple paths, select most frequent answer
- Tree of Thoughts (ToT): Tree structure, nodes = reasoning steps, uses BFS/DFS
- Graph of Thoughts (GoT): Generalize tree to graph
- Algorithm of Thought (AoT): Incorporate algorithmic examples
- RAP: Monte Carlo Tree Search for plan evaluation

**External planners**: When LLMs struggle with formal planning requirements:
- LLM+P: Convert to PDDL, use external planner, convert back
- LLM-DP: LLM generates PDDL representations, external planner solves
- CO-LLM: LLM for high-level plans, external planner for low-level control

#### Planning WITH Feedback

**Environmental feedback**: From objective world/virtual environments.
- ReAct: "thought-act-observation" triplets; observations influence next thoughts
- Voyager: Program execution progress, errors, verification results
- DEPS: Detailed failure reasons (not just success/fail signals)
- Inner Monologue: Three feedback types (task completion, passive descriptions, active descriptions)

**Human feedback**: Subjective signals aligning with human values.
- Inner Monologue: Agents solicit human scene descriptions, incorporate into prompts

**Model feedback**: Self-evaluation from LLMs or auxiliary models.
- Self-refine: output -> LLM feedback -> refinement cycle
- Reflexion: Evaluator generates verbal self-feedback on trajectories
- SelfCheck: Agents examine and correct their own reasoning steps
- ChatCoT: Evaluation module monitors reasoning, generates corrective feedback

**Key quote**: *"Simply following the initial plan often leads to failure"* due to
unpredictable transition dynamics, necessitating iterative feedback-based planning.

### 2.4 Action Module

**Position**: Most downstream module. Directly interacts with environment. Influenced by
all three upstream modules.

#### Action Goals

1. **Task completion**: Accomplish well-defined objectives (craft pickaxe, write code)
2. **Communication**: Share information/collaborate with agents or humans
3. **Environment exploration**: Balance exploration-exploitation; expand perception

#### Action Production

1. **Via memory recollection**: Extract relevant memories before acting (Generative Agents
   retrieves recent + relevant + important info; GITM queries for past successful experiences)
2. **Via plan following**: Execute pre-generated plans (DEPS follows plans unless failure
   signals detected)

#### Action Space

**External tools**:
- APIs (HuggingGPT, WebGPT, Gorilla, ToolFormer, RestGPT, TaskMatrix.AI)
- Databases & knowledge bases (ChatDB with SQL, MRKL with expert systems)
- External models (ViperGPT generates Python code, ChemCrow uses 17 chemistry models)

**Internal knowledge**:
- Planning capability (decomposition via LLM reasoning)
- Conversational capability (dialogue generation)
- Common sense understanding (daily life simulation, social behaviors)

#### Action Impact

1. **Changing environments**: Direct state alterations (position, inventory, construction)
2. **Altering internal states**: Memory updates, new plans, knowledge acquisition
3. **Triggering new actions**: One action initiating subsequent actions (resource gathering
   triggering building)

---

## 3. Capability Acquisition

The survey distinguishes two approaches:

### With Fine-tuning
- Human-annotated datasets (CoH, WebShop, EduChat)
- LLM-generated datasets (ToolBench: 16,464 APIs, ChatGPT generates instructions)
- Real-world datasets (MIND2WEB: 2000+ tasks from 137 websites)
- Only applicable to open-source LLMs

### Without Fine-tuning
- **Prompt engineering**: CoT, persona prompts, reasoning scaffolds
- **Mechanism engineering** (unique to agent paradigm):
  - Trial-and-error: act -> critic evaluates -> feedback incorporated
  - Crowd-sourcing: multiple agents debate toward consensus
  - Experience accumulation: store successful patterns (Voyager skill library)
  - Self-driven evolution: agent sets own goals, explores autonomously (LMA3)

---

## 4. Multi-Agent Systems

The survey mentions multi-agent scenarios primarily through application examples rather than
providing a systematic multi-agent taxonomy (this is a gap):

- **ChatDev**: Multiple roles (programmer, product manager, designer) collaborate on software
- **MetaGPT**: Predefined roles with distinct responsibilities
- **CAMEL**: Communicative agents for mind exploration
- **Debate mechanism**: Multiple agents generate responses; inconsistencies trigger iterative
  discussion until consensus

Communication appears to be **dialogue-based** (natural language), not protocol-specified.
Topology seems flexible rather than formally structured.

The paper does not deeply analyze cooperative vs. adversarial dynamics, emergent behaviors,
or communication theory aspects of multi-agent interaction.

---

## 5. Applications Surveyed

### Social Science
- **Psychology**: Simulation experiments matching human participant results; mental health support
- **Political science & economy**: Ideology detection, voting prediction, economic behavior simulation
- **Social simulation**: Virtual communities (Generative Agents, AgentSims, S3), information/emotion propagation
- **Jurisprudence**: ChatLaw (Chinese legal model), Blind Judgement (consensus via multiple judge simulations)
- **Research assistance**: Article abstracts, keyword extraction, novel inquiry identification

### Natural Science
- Documentation & data management (ChatMOF for materials, ChemCrow for chemistry)
- Experiment assistance (automated design, planning, execution)
- Education (math agents, CodeHelp for programming, EduChat for personalized dialogue)

### Engineering
- Software development (ChatDev, MetaGPT)
- Game playing (Minecraft: DEPS, GITM, Voyager; D&D: CALYPSO)
- Robotics (RoCo: multi-robot collaboration with validation checks)
- Web interaction (WebShop, MIND2WEB)
- Tool use (HuggingGPT, Gorilla, RestGPT)

---

## 6. Evaluation Approaches

### Subjective Evaluation
- Human judges rate performance on naturalness, coherence, task appropriateness
- Common in conversation and social simulation tasks

### Objective Evaluation
- **Benchmarks**: Minecraft task completion, game scores, WebShop success rates, legal judgment accuracy
- **Metrics**: Task success/failure, action efficiency (steps to completion), plan quality
- **Automated assessment**: Pre-defined critics, error detection, validation checks

The evaluation section is relatively thin compared to the architectural discussion. This is
itself significant -- the field lacks mature evaluation frameworks.

---

## 7. Challenges Identified

1. **Role-playing capability**: Maintaining consistent character personas
2. **Generalized human alignment**: Aligning with diverse human values
3. **Prompt robustness**: Sensitivity to minor prompt variations
4. **Hallucination**: Generating false information as factual
5. **Knowledge boundary**: Recognizing limits of training knowledge
6. **Efficiency**: Computational cost and latency

---

## 8. Module Interactions and Architecture

The flow described:

```
    Profile Module
        |
        v
    Memory Module  <-->  Planning Module
        \                   /
         \                 /
          v               v
         Action Module
              |
              v
         Environment
              |
              v
         (observations feed back to Memory)
```

Profiling determines agent characteristics -> influences memory retrieval priorities and planning
style. Memory provides historical context for planning. Plans guide action selection. Action
outcomes update memory through writing operations. Environment provides observations and feedback.

**Critical observation**: The feedback from environment to memory is present but **implicit**
in the architecture diagram. It is not given the same architectural weight as the forward path
from profile -> memory -> planning -> action. The feedback is discussed mainly in the Planning
module's "planning with feedback" subsection, not as a first-class architectural feature.

---

## 9. CYBERNETIC ANALYSIS

### 9.1 Mapping to Cybernetic Decomposition

A cybernetic agent (in the tradition of Ashby, Wiener, Beer) has:
- **Sensor** (perceptual apparatus): receives information from environment
- **Comparator** (error detection): compares perceived state to desired state
- **Effector** (action apparatus): acts on environment to reduce error
- **Feedback loop**: connects effector output back to sensor input
- **Variety management**: the system must have sufficient internal variety to match
  environmental variety (Ashby's Law of Requisite Variety)

**How Wang et al. maps**:

| Cybernetic Component | Wang et al. Equivalent | Notes |
|---------------------|----------------------|-------|
| Sensor | Memory module (writing operation) | Perception is modeled as memory writing, not as a distinct sensory process |
| Comparator | Planning module (with feedback) | Error detection is implicit in plan refinement, not explicit |
| Effector | Action module | Most direct mapping |
| Reference signal / setpoint | Profile module | Defines what the agent "should be" |
| Feedback loop | Partially in Planning-with-feedback | Not a first-class architectural feature |
| Variety management | **ABSENT** | No discussion whatsoever |
| Model of environment | Memory (partially) | No explicit world model distinct from memory |

### 9.2 What is MISSING from a Cybernetic Perspective

**1. No explicit feedback loop as architectural primitive.**
Feedback appears only as a *sub-type of planning* ("planning with feedback" vs "planning
without feedback"). In cybernetics, feedback is THE fundamental organizing principle, not
an optional add-on. The fact that the survey treats feedback-free planning as a legitimate
architectural option reveals the field's open-loop bias. A cybernetic analysis would say:
planning without feedback is not really planning -- it's ballistic trajectory computation.

**2. No comparator / error signal.**
There is no module whose job is to detect the discrepancy between current state and desired
state. In the Wang et al. framework, this function is diffused across modules or handled
ad hoc by the LLM's general reasoning. A cybernetician would argue this makes the system
fragile -- without explicit error detection, the agent cannot systematically correct course.

**3. No variety management.**
Ashby's Law of Requisite Variety states that a controller must have at least as much variety
as the system it controls. The survey never asks: does this agent have sufficient behavioral
variety to handle the environments it faces? The implicit assumption is that LLMs, having
been trained on vast text, have "enough" variety. This is an empirical bet, not a principled
analysis. When agents fail in novel situations, a cybernetic analysis would diagnose this as
a variety deficit.

**4. No stability analysis.**
There is no discussion of whether feedback loops in these agents are stable (convergent) or
unstable (divergent). Self-refine loops, Reflexion loops, and debate mechanisms are all
feedback systems that can oscillate, diverge, or converge -- but the survey treats them
purely as capability enhancements without analyzing their dynamic properties.

**5. No homeostasis concept.**
Cybernetic agents maintain essential variables within viable limits (Beer's viable system
model). LLM-based agents have no notion of essential variables, viability boundaries, or
the distinction between goal-seeking and regulation. Every behavior is framed as task
completion, not as maintaining conditions for continued operation.

**6. No agent-environment co-determination.**
The Wang et al. framework treats the agent and environment as separate: agent acts on
environment, environment provides feedback. In cybernetics (especially second-order
cybernetics, Maturana/Varela), the agent and environment are structurally coupled --
each determines the other. The survey's framework is closer to classical AI's agent-
environment dichotomy than to cybernetic structural coupling.

**7. Perception is undertheorized.**
There is no "sensor" module. Perception is folded into memory writing. This means there
is no analysis of what the agent can and cannot perceive, how perception is selective,
or how perceptual categories are formed. In cybernetics, the observer's categories
fundamentally determine what can be controlled (you can only regulate what you can sense).

**8. No recursion / self-reference.**
Second-order cybernetics emphasizes that the observer is part of the system observed.
LLM agents that reflect on their own performance (Reflexion, Self-refine) are engaging
in a form of self-reference, but the survey does not analyze this as recursion or connect
it to observing-system theory. The "reflection" mechanism is treated as just another
memory operation, not as a fundamentally different logical level.

### 9.3 Memory and Ashby's "Black Box"

Ashby's concept: an observer studying a "black box" must infer internal states from
input-output behavior. The past states of the system determine its future behavior --
this is the fundamental connection between memory and determinism.

The Wang et al. memory module is essentially an attempt to give the LLM agent **explicit
past states** that persist beyond the context window. Without the memory module, the LLM
agent is a (large, complex) input-output function with no history -- a memoryless system
that nonetheless appears to have memory because its weights encode training history.

The memory module adds **genuine state** to the system: the agent's behavior at time t
depends on its accumulated memories, not just on the current input. In Ashby's terms,
this transforms the agent from a trivial machine (same input -> same output) to a
non-trivial machine (same input -> different output depending on history).

**However**: The memory module as implemented is a **storage system**, not a state-transition
system. In Ashby's formalism, internal state evolves according to transition functions.
In Wang et al., memory is read and written but does not have autonomous dynamics -- it
doesn't decay naturally, consolidate automatically, or reorganize itself except when
explicitly triggered by reflection operations. This is a key limitation: the memory is
passive storage, not active state.

The **reflection mechanism** partially addresses this by allowing the agent to transform
raw memories into higher-level insights. This is closer to Ashby's idea of a system
whose internal states have their own dynamics. But reflection is triggered explicitly
(e.g., after N events), not continuously -- it is batch processing, not dynamic state
evolution.

### 9.4 The Cognitive Architecture Connection

The survey borrows from cognitive science (STM/LTM distinction) without engaging with the
formal cognitive architecture tradition:

**SOAR** (Laird, 2012):
- Working memory + procedural memory (production rules) + semantic/episodic LTM
- Learning via chunking (compiling frequently-used working memory patterns into productions)
- Impasse-driven learning: when no production fires, the system creates a subgoal
- **Key difference**: SOAR has a formal control cycle (propose-decide-apply). Wang et al.
  agents have no equivalent -- the LLM acts as a universal "decide" mechanism.

**ACT-R** (Anderson, 2007):
- Declarative memory (facts with activation levels) + procedural memory (productions)
- Activation-based retrieval: base-level learning + spreading activation
- Explicit time course of cognition (each operation takes modeled time)
- **Key parallel**: Wang et al.'s memory reading formula (recency + relevance + importance)
  is functionally similar to ACT-R's activation equation (base-level + spreading activation),
  though the Wang et al. version is ad hoc rather than psychologically grounded.

**What LLM agents add that cognitive architectures lack**: The LLM itself serves as a kind of
universal "knowledge base" + "inference engine" that cognitive architectures must laboriously
construct. This is both a strength (rich prior knowledge) and a weakness (opaque, uncontrolled
prior knowledge).

---

## 10. Implicit Assumptions of the Field

Reading this survey carefully reveals several things taken for granted:

**1. Goal-directedness is assumed, not derived.**
Agents are assumed to have goals (given by users or profiles). There is no account of how
goals emerge, compete, or are prioritized. In cybernetics, purpose is explained by feedback
structure, not assumed as a primitive.

**2. Natural language is the universal interface.**
Everything -- perception, memory, planning, action, inter-agent communication -- is mediated
by natural language. This is a strong commitment: it means the agent can only perceive,
remember, and reason about things that can be expressed in text. It excludes continuous
signals, sub-symbolic representations, and embodied cognition (except through language
descriptions of them).

**3. The LLM is a general-purpose reasoning engine.**
The entire architecture assumes the LLM can do planning, reflection, evaluation, memory
management, role-playing, and action selection -- all through prompting. The question of
whether a next-token predictor is actually capable of these functions is not deeply examined.
The survey documents what systems have been built, not whether the underlying mechanism
is appropriate.

**4. More modules = better agents.**
The progression from simple prompting to full four-module architectures is presented as
improvement. There is no discussion of diminishing returns, module interference, or the
cost of coordination. A cybernetic analysis might ask: at what point does adding modules
increase internal complexity faster than it increases effective variety?

**5. Feedback is optional.**
The planning module's division into "with feedback" and "without feedback" treats feedback
as an enhancement rather than a necessity. This is deeply un-cybernetic. It suggests the
field views agents primarily as plan-executors rather than as adaptive regulators.

**6. The environment is a passive backdrop.**
The environment provides observations and feedback but is not modeled as an active system
with its own dynamics. There is no analysis of environmental complexity, rate of change,
or the coupling between agent actions and environmental responses. The environment is
treated as a task-providing context, not as a co-evolving system.

**7. Evaluation is task-based.**
Success is measured by task completion, not by adaptive fitness, robustness, or long-term
viability. This reveals a fundamentally **engineering** (rather than scientific or cybernetic)
orientation: the question is "can it do X?" not "can it survive and adapt?"

**8. Single-agent is the default frame.**
Despite mentioning multi-agent systems, the primary framework is single-agent. Multi-agent
interaction is an application, not an architectural consideration. A cybernetic perspective
(especially Beer's Viable System Model) would make the multi-agent / organizational structure
a core design concern, not an afterthought.

**9. Anthropomorphism as design principle.**
The four modules are justified by analogy to human cognition (memory like human memory,
planning like human planning). This is borrowed from cognitive science but without the
discipline of cognitive architectures -- it's loose analogy rather than formal theory.
A cybernetic approach would not privilege human cognition as a model; it would ask about
the functional requirements of viable regulation in the relevant environment.

**10. No thermodynamic or information-theoretic grounding.**
There is no discussion of the information-theoretic costs of memory, planning, or action.
Shannon's channel capacity, Ashby's requisite variety, and thermodynamic constraints on
computation are entirely absent. The implicit assumption is that LLMs are "powerful enough"
and that computational cost is an engineering concern, not a theoretical one.

---

## Summary Assessment

This survey is an excellent **descriptive taxonomy** of the emerging LLM-agent field as of
2023-2024. It systematically catalogs architectural patterns, techniques, and applications.
Its four-module framework (Profile, Memory, Planning, Action) provides useful vocabulary for
discussing agent designs.

However, from a cybernetic/systems-theoretic perspective, it has significant blind spots:
- It describes mechanisms without analyzing dynamics (feedback stability, convergence)
- It catalogs components without analyzing their systemic interactions
- It treats feedback as optional rather than constitutive
- It has no concept of requisite variety, viability, or homeostasis
- It inherits cognitive science vocabulary without cognitive architecture rigor

The survey reveals a field that is primarily **engineering-driven** (build it and see if it
works) rather than **theory-driven** (derive the architecture from principles of viable
regulation). This is not a criticism of the survey -- it accurately reflects the state of
the field. But it identifies a significant intellectual gap: the LLM-agent community could
benefit from engaging with cybernetic and systems-theoretic frameworks that provide principled
answers to questions like "when will feedback loops converge?" and "how much internal variety
does the agent need?"

---

## Key References to Follow Up

- Franklin, S. & Graesser, A. (1997). "Is it an Agent, or just a Program?"
- Generative Agents (Park et al., 2023) -- most cited example architecture
- ReAct (Yao et al., 2022) -- thought-act-observation paradigm
- Reflexion (Shinn et al., 2023) -- verbal self-feedback
- Voyager (Wang et al., 2023) -- skill library + experience accumulation
- GITM (Zhu et al., 2023) -- hierarchical memory + planning
- MetaGPT, ChatDev -- multi-agent software development
- SOAR (Laird, 2012) and ACT-R (Anderson, 2007) for cognitive architecture comparison
- Ashby, W.R. (1956). "An Introduction to Cybernetics" -- requisite variety, black box
- Beer, S. (1972). "Brain of the Firm" -- Viable System Model
- Maturana, H. & Varela, F. (1980). "Autopoiesis and Cognition" -- structural coupling
