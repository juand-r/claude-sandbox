# Variety Calculus Applied to Tool Use and Agent Capability

**Stream G, Item 28**
**Date:** 2026-03-12

---

## 1. Ashby's Variety Equation: Terms Defined for Agent-with-Tools

Ashby's Law of Requisite Variety, in its information-theoretic form (S.11/8):

> **H(E) >= H(D) - H(R)**

where the minimum of H(E) is achieved when R is a deterministic function of D.

For an agent-with-tools scenario, the terms map as follows:

| Symbol | Ashby's Meaning | Agent Interpretation |
|--------|----------------|---------------------|
| **D** | Disturbance — the set of environmental states/perturbations the regulator must handle | The **task distribution**: all distinguishable tasks, queries, or environmental states the agent may encounter. Each distinct task state is a value of D. |
| **R** | Regulator — the set of responses the controller can produce | The **action repertoire**: all distinguishable actions the agent can take. Without tools: text outputs only. With tools: text outputs x tool invocations x tool parameters. |
| **E** | Essential variable — the outcome, which must be kept within acceptable bounds (set eta) | The **task outcome quality**: success/failure, correctness, user satisfaction. The "acceptable bounds" eta are whatever constitutes adequate task completion. |
| **H(D)** | Entropy of the disturbance source | The information-theoretic complexity of the task distribution — how many bits are needed to specify which task the agent faces. |
| **H(R)** | Entropy of the regulator's responses | The effective action variety — how many bits of distinct, correctly-deployed action the agent can produce. |
| **H(E)** | Entropy of the outcome | Residual uncertainty in the outcome after the agent acts. H(E) = 0 means perfect regulation (every task handled correctly). |

The equation says: **the residual outcome uncertainty cannot be driven below H(D) - H(R)**. If the task space has 20 bits of variety and the agent's effective action space has 15 bits, at least 5 bits of outcome uncertainty remain — meaning the agent will systematically fail on a fraction of tasks proportional to 2^5 = 32 distinguishable failure categories.

### The Deterministic Coupling Condition

The minimum H(E) = H(D) - H(R) is achieved only when H_D(R) = 0 — that is, the agent's response is a deterministic function of the disturbance. In agent terms: **the agent must reliably select the correct action for each task state**. Any stochasticity, confusion, or misidentification in tool selection adds to H(E). This is the formal basis for why tool selection accuracy matters as much as tool availability.

---

## 2. Quantifying Task Domain Variety

The following estimates are rough but grounded. The goal is order-of-magnitude, not precision. I distinguish between **state variety** (how many distinguishable situations exist) and **action variety** (how many distinguishable responses are needed).

### 2.1 Coding Tasks

**State variety:**
- Programming languages in active use: ~50 (log2 ≈ 6 bits)
- Distinct task types (bug fix, feature, refactor, test, review, optimize, port, debug): ~16 (4 bits)
- Codebase size categories (single file to monorepo): ~8 (3 bits)
- Distinguishable code patterns/idioms per language: conservatively ~1,000 (10 bits)
- Error types (syntax, type, logic, runtime, concurrency, performance): ~64 (6 bits)

**Rough state variety: ~29 bits** (multiplicative independence assumed; real constraint reduces this, but constraint itself varies across contexts)

**Action variety needed:**
- File operations (create, read, edit, delete, move): ~8 (3 bits)
- Code generation granularity (line, function, class, module, project): ~8 (3 bits)
- Debugging actions (read error, set breakpoint, inspect variable, trace execution, bisect): ~16 (4 bits)
- Tool invocations (compiler, linter, test runner, search, version control): ~32 (5 bits)
- Parameter variety per tool: ~64 (6 bits)

**Rough action variety: ~21 bits**

**Variety gap: ~8 bits.** This means a coding agent will have ~2^8 = 256 distinguishable failure categories. This is consistent with empirical observation: coding agents fail on complex multi-file refactors, concurrency bugs, and architectural decisions — tasks where the state variety exceeds the action repertoire's discriminatory power.

### 2.2 Web Browsing Tasks

**State variety:**
- Distinct websites a user might visit: ~10^8 (27 bits)
- Page states per site (navigation depth, dynamic content, authentication states): ~1,000 (10 bits)
- User intent types (search, navigate, fill form, extract data, purchase, compare): ~32 (5 bits)

**Rough state variety: ~42 bits**

**Action variety needed:**
- Navigation actions (click, type, scroll, back, forward, new tab): ~16 (4 bits)
- Form field types: ~32 (5 bits)
- Selection targets per page: ~100 (7 bits)
- Query formulations: ~2^15 (15 bits, generous estimate for natural language query variety)

**Rough action variety: ~31 bits**

**Variety gap: ~11 bits.** Web browsing is harder than coding for agents, which matches empirical results. The state variety of the open web is enormous, and many states are adversarial (CAPTCHAs, anti-bot measures, dynamic rendering). Computer-use agents consistently struggle with novel website layouts.

### 2.3 File Manipulation Tasks

**State variety:**
- File types: ~200 (8 bits)
- Filesystem structures (depth, breadth, naming): ~1,000 (10 bits)
- File sizes/content variety: effectively continuous, but distinguishable categories ~100 (7 bits)
- Permission/ownership states: ~16 (4 bits)

**Rough state variety: ~29 bits**

**Action variety needed:**
- CRUD operations: ~8 (3 bits)
- Path specification: ~2^12 (12 bits for typical filesystem depth x breadth)
- Content transformation types (search/replace, format conversion, compression, encryption): ~64 (6 bits)

**Rough action variety: ~21 bits**

**Variety gap: ~8 bits.** Similar to coding. File manipulation agents work well on common operations, fail on edge cases (permissions, encodings, symlinks, large files, concurrent access).

### 2.4 Data Analysis Tasks

**State variety:**
- Data formats (CSV, JSON, SQL, Parquet, Excel, API responses, etc.): ~32 (5 bits)
- Dataset characteristics (size, dimensionality, types, missing data patterns): ~1,000 (10 bits)
- Analysis types (descriptive stats, regression, classification, clustering, visualization, time series): ~64 (6 bits)
- Domain-specific conventions (finance, biology, social science, engineering): ~100 (7 bits)
- Data quality issues (nulls, outliers, encoding errors, duplicates): ~32 (5 bits)

**Rough state variety: ~33 bits**

**Action variety needed:**
- Data loading/parsing: ~32 (5 bits)
- Transformation operations (filter, join, pivot, aggregate, impute): ~64 (6 bits)
- Statistical methods: ~128 (7 bits)
- Visualization types: ~32 (5 bits)
- Code generation for analysis: ~2^10 (10 bits)

**Rough action variety: ~33 bits**

**Variety gap: ~0 bits.** This is interesting. Data analysis is one domain where tool-augmented agents perform best empirically. The action vocabulary (pandas, SQL, matplotlib, scipy) closely matches the state variety of the problem domain. The tools were designed to match the problem. This near-zero gap predicts high success rates, which is what we observe: coding agents doing data analysis is one of the most reliable agent use cases.

### 2.5 Summary Table

| Domain | H(D) est. | H(R) est. | Gap (bits) | 2^gap (failure categories) | Empirical fit |
|--------|-----------|-----------|------------|---------------------------|---------------|
| Coding | ~29 | ~21 | ~8 | ~256 | Agents good on routine, fail on complex |
| Web browsing | ~42 | ~31 | ~11 | ~2048 | Agents struggle significantly |
| File manipulation | ~29 | ~21 | ~8 | ~256 | Similar to coding |
| Data analysis | ~33 | ~33 | ~0 | ~1 | Agents perform well |

**Caveat:** These estimates assume independence of dimensions, which overstates variety (real tasks are heavily constrained — you rarely see all combinations). The absolute numbers are not reliable. The *relative ordering* is more trustworthy: data analysis < coding ≈ file manipulation < web browsing, in terms of difficulty. This matches empirical agent performance rankings.

---

## 3. Nominal vs. Effective Variety: The Variety Illusion

### 3.1 The Distinction

Adding a tool to an agent increases **nominal variety** — the theoretical action space. But Ashby's equation uses H(R), which is the *effective* entropy of the regulator's responses. Effective variety requires that the agent can:

1. **Select** the right tool for the task (correct routing)
2. **Parameterize** the tool correctly (correct invocation)
3. **Interpret** the tool's output (correct integration)
4. **Recover** from tool errors (correct error handling)

Each of these steps has a failure probability. Let:
- p_select = probability of selecting the correct tool
- p_param = probability of correct parameterization given correct selection
- p_interpret = probability of correct interpretation given correct output
- p_recover = probability of recovery given a tool error

Then the **effective variety** per tool is:

> H_effective(tool_i) = p_select * p_param * p_interpret * H_nominal(tool_i)

where H_nominal is the full action variety the tool provides.

### 3.2 Quantifying the Gap

From the Toolformer paper, we have hard numbers on tool selection accuracy:
- Calculator selection on math tasks: 97.9%
- QA selection on fact tasks: 98.1%
- WikiSearch selection on QA tasks: 99.3%

These are *easy cases* — tasks with obvious tool-task mappings and only 5 tools. With more tools:

- ToolBench (16,464 APIs): tool selection accuracy drops significantly
- Gorilla (1,645 APIs): reports that larger API pools degrade accuracy
- Empirical rule of thumb from the literature: selection accuracy degrades roughly as O(1/log(n)) for n tools, with sharp drops when tools have overlapping descriptions

For a concrete estimate with a 500-tool agent:

| Component | 5 tools | 50 tools | 500 tools |
|-----------|---------|----------|-----------|
| p_select | 0.98 | 0.85 | 0.60 |
| p_param | 0.95 | 0.90 | 0.80 |
| p_interpret | 0.95 | 0.92 | 0.88 |
| p_effective (product) | 0.88 | 0.70 | 0.42 |

The **variety illusion** is the gap between nominal and effective:

> Variety illusion = H_nominal(R) - H_effective(R)

For a 500-tool agent where each tool provides ~6 bits of action variety:
- H_nominal = log2(500) + 6 ≈ 15 bits
- H_effective ≈ 15 * 0.42 ≈ 6.3 bits
- **Variety illusion ≈ 8.7 bits**

This means the agent's *apparent* regulatory capacity is 15 bits, but its *actual* regulatory capacity is about 6 bits. The gap is enormous — the agent appears 500x more capable than it is (2^8.7 ≈ 416).

### 3.3 Why This Matters

The variety illusion explains a recurring pattern in agent development:

1. Developer adds tools → nominal variety increases → benchmark improves on easy tasks
2. Developer deploys to harder tasks → effective variety is insufficient → failures surprise everyone
3. Post-mortem reveals: the agent couldn't reliably select/use the tools it "had"

This is precisely the AutoGPT failure pattern. AutoGPT had tools for web browsing, file I/O, code execution, and shell commands. Nominal variety was high. But effective variety was low because the agent couldn't reliably select the right tool, parameterize it correctly, or interpret the results. The variety illusion made the system appear more capable than it was.

The Toolformer result provides the counter-example: with only 5 well-matched tools and high selection accuracy (>97%), effective variety closely tracked nominal variety. The system worked because the variety illusion was small.

**Design principle:** It is better to have 5 tools at 98% selection accuracy (H_effective ≈ 4.5 bits) than 500 tools at 60% accuracy (H_effective ≈ 6.3 bits). The marginal gain from the 495 extra tools is only ~1.8 bits, while the system complexity and failure modes increase dramatically.

---

## 4. Tool Selection as Variety Attenuation

### 4.1 The Information-Theoretic Cost

When an agent faces a task and must choose from n tools, the selection process is a **variety attenuator** — it reduces the action space from all-tools to one-tool. The information-theoretic cost of this selection is:

> I_selection = H(tool space) = log2(n) bits

For n = 500: I_selection = ~9 bits. The agent must extract 9 bits of information from the task description to correctly route to one tool.

Where does this information come from? From the **mutual information between the task description and the correct tool**:

> I(task; tool) = H(tool) - H(tool | task)

If the task description fully specifies the tool (H(tool | task) = 0), then I(task; tool) = log2(n) and selection is trivial. If the task description is ambiguous (H(tool | task) > 0), the agent must supply the missing information from its training (prior knowledge) or guess.

### 4.2 The Selection Bottleneck

For an LLM selecting among tools, the selection happens through the following channel:

```
Task description → LLM processing → Tool selection
     H(D)              channel            log2(n) bits needed
```

The channel capacity is bounded by the mutual information the LLM can extract between the task and the tool descriptions. This depends on:

1. **Quality of tool descriptions:** Vague descriptions reduce I(task; tool). If two tools have similar descriptions, the conditional entropy H(tool | task) increases.
2. **LLM's discriminative ability:** The model must attend to subtle distinctions between tool descriptions. Attention capacity limits this.
3. **Context window consumption:** With 500 tools, just listing them with descriptions might consume 50K tokens. This reduces the context available for the actual task, degrading other aspects of performance.

### 4.3 The Selection-Execution Tradeoff

There is a fundamental tradeoff: the information spent on tool selection is information *not* spent on tool execution. The agent's total information processing capacity per step is bounded. If 9 bits go to selecting among 500 tools, those 9 bits are unavailable for parameterizing the selected tool.

This suggests an optimal tool set size: the point where the marginal variety gain from one more tool equals the marginal selection cost. Formally, we want to maximize:

> H_effective(R) = (H_nominal(R) - I_selection) * p_correct_selection

This is maximized at a finite n, not at n → infinity. The exact optimum depends on the task distribution and the LLM's selection accuracy curve, but the existence of a finite optimum is a theoretical prediction: **there is a number of tools beyond which adding more makes the agent worse, not better.**

### 4.4 Empirical Estimates

From the Toolformer data:
- At k=1 (strict, ~40% call rate): the model is selective — it only invokes tools when highly confident. Selection accuracy is near-perfect but coverage is low.
- At k=10 (relaxed, ~98% call rate): coverage is high but selection accuracy drops slightly.

This is the classic precision-recall tradeoff, which is a manifestation of the variety attenuation problem: aggressive attenuation (k=1) preserves accuracy but loses coverage; gentle attenuation (k=10) preserves coverage but risks misselection.

---

## 5. MCP as Variety Engineering

The Model Context Protocol is, from a variety-theoretic perspective, an engineering framework for managing the variety flow between an LLM and its tool ecosystem.

### 5.1 Composability as Variety Multiplication

MCP's client-server architecture allows composing tools from multiple servers. If server A provides n_A tools and server B provides n_B tools:

- **Nominal variety** of the composed system: n_A + n_B tools (additive in count, additive in log-variety)
- **Effective variety** depends on whether the tools can be chained: if tool outputs from A can feed as inputs to B, the composed variety is multiplicative in the relevant dimensions

MCP's sampling feature (servers requesting LLM completions that can include tool calls) enables exactly this chaining. A server can invoke the LLM, which invokes tools on another server, creating **recursive variety amplification**. The effective variety of such a system is:

> H_recursive = H(tools_layer_1) + H(tools_layer_2) + ... (up to recursion depth)

This is powerful but dangerous — each recursion level multiplies the variety illusion as well as the nominal variety. Without strong selection accuracy at each level, errors compound geometrically.

### 5.2 Discovery as Variety Attenuation

MCP's `tools/list` discovery mechanism is a variety attenuator. Instead of presenting all possible tools to the LLM at once, the protocol allows:

1. **Lazy discovery:** Tools are listed per-server, and the host decides which servers to query
2. **Dynamic listing:** The `tools/list_changed` notification allows servers to adjust available tools based on context
3. **Filtered presentation:** The host can curate which tools to expose to the LLM based on the current task

Each of these mechanisms reduces the effective n that the LLM must select from, reducing I_selection and improving selection accuracy.

The optimal MCP deployment, from a variety perspective, is one where the host performs first-stage variety attenuation (selecting relevant servers and tools) before the LLM performs second-stage attenuation (selecting the specific tool and parameters). This two-stage attenuation is more efficient than single-stage: if the host can reduce 500 tools to 20 relevant ones with 95% accuracy, the LLM only needs to discriminate among 20 (4.3 bits) rather than 500 (9 bits).

### 5.3 Permissions as Variety Bounding

MCP's security model — user consent for data access, human approval for tool invocations, filesystem roots, server isolation — is systematic variety attenuation applied to the safety dimension.

Each permission boundary reduces the variety of possible agent actions:

| Mechanism | Variety Reduction |
|-----------|------------------|
| Filesystem roots | Reduces file-addressable space from entire OS to bounded paths |
| Human approval for tool calls | Reduces action variety to human-approved subset |
| Server isolation | Prevents variety leakage between tool domains |
| Capability negotiation | Only enables variety that both parties support |

The information-theoretic effect: if the unrestricted action space has H_unrestricted bits of variety and the permission system removes k bits, then H_permitted = H_unrestricted - k. The agent can still regulate any task within the permitted space, but cannot produce actions outside it.

This is Ashby's passive blocking (S.10/7): like the tortoise's shell, permissions reduce variety without requiring active regulation. The human-in-the-loop approval is active blocking — the human actively selects which proposed actions to allow.

### 5.4 Schema Constraints as Per-Tool Attenuation

Each MCP tool's `inputSchema` (JSON Schema) constrains the parameters the LLM can provide. This is variety attenuation at the tool level:

- Without schema: the LLM can pass arbitrary JSON (effectively unlimited variety, most of which is wrong)
- With schema: the LLM must conform to specified types, ranges, and structures

If a tool's unconstrained parameter space has V_free bits and the schema constrains it to V_schema bits, the schema removes V_free - V_schema bits of irrelevant variety. This directly improves p_param (parameterization accuracy) by reducing the space of possible errors.

The `outputSchema` (optional in MCP) does the same for interpretation: constraining the output format reduces H(output | correct_usage), making it easier for the LLM to integrate results.

---

## 6. The AutoGPT Failure Through the Variety Lens

### 6.1 The Variety Budget

AutoGPT's task domain was "do anything a human can do on a computer." Rough state variety:

- Operating system states: ~2^20 (file system, processes, network)
- Web states: ~2^27 (as estimated above, and this is conservative)
- User intent variety: ~2^10 (thousands of distinguishable goals)
- Temporal dependencies: ~2^8 (task ordering constraints)

**Total task variety: ~65 bits** (with heavy double-counting, but even a conservative 40 bits is enormous)

AutoGPT's response variety:
- Tool set: ~8 tools (3 bits)
- Parameters per tool: ~2^6 (6 bits)
- Text generation variety: ~2^15 (15 bits, though constrained by prompt)
- Total nominal H(R): ~24 bits

**Variety deficit: at least 16 bits**, meaning at least 2^16 = 65,536 distinguishable failure categories. **The failure was not just predictable — it was quantitatively inevitable.**

### 6.2 The Multi-Scale Failure

Applying Siegenfeld & Bar-Yam's multi-scale requisite variety:

| Scale | Environmental complexity | AutoGPT complexity | Match? |
|-------|------------------------|-------------------|--------|
| Individual action | ~10 bits (execute one command) | ~9 bits (tool + params) | Approximately matched |
| Action sequence (5-10 steps) | ~25 bits (correct ordering, error handling) | ~12 bits (context window, no plan memory) | Deficit: ~13 bits |
| Strategy (50+ steps) | ~35 bits (goal decomposition, resource management) | ~5 bits (single system prompt) | Deficit: ~30 bits |
| Meta-strategy (recognizing failure, changing approach) | ~15 bits (failure detection, strategy switching) | ~2 bits (self-critique prompt, binary) | Deficit: ~13 bits |

The multi-scale analysis reveals that AutoGPT's variety was concentrated at the finest scale (individual actions) and essentially absent at coarser scales. This is the sum rule in action: the total complexity budget was allocated almost entirely to action-level variety, leaving nothing for coordination, strategy, or meta-cognition.

**Key prediction confirmed:** AutoGPT could execute individual steps competently (matched variety at fine scale) while failing catastrophically at multi-step tasks (deficit at coarse scales). This is exactly what was observed.

### 6.3 Could Variety Analysis Alone Have Predicted the Failure?

Yes, with qualifications.

**What variety analysis predicts correctly:**
- That the system would fail on open-ended tasks (variety deficit too large)
- That it would succeed on simple, well-defined tasks (small variety gap)
- That failure would manifest as loops, drift, and incoherence (insufficient coarse-scale variety → no strategy maintenance)
- That adding more tools without improving selection would not help (variety illusion)

**What variety analysis does NOT predict:**
- The specific failure modes (infinite loops vs. error cascading vs. hallucinated capabilities). These require knowing the system's architecture, not just its variety budget.
- The cost profile. Variety analysis says nothing about economics.
- The timeline to failure. Variety analysis is a static accounting, not a dynamical model.

**Verdict:** Variety analysis is a necessary but not sufficient diagnostic tool. It identifies the *magnitude* of the capability gap and predicts *that* failure will occur, but not *how*. For the "how," you need dynamical analysis (feedback stability, error propagation models). But even the coarse variety calculation — "65 bits of task variety, 24 bits of response variety, therefore failure" — would have been useful in March 2023. Nobody did this calculation.

---

## 7. Design Principles: Amplify or Attenuate?

### 7.1 The Fundamental Decision

Given H(E) >= H(D) - H(R), there are exactly two ways to reduce H(E) (improve outcomes):

1. **Amplify H(R):** Give the agent more tools, more capable models, more action variety
2. **Attenuate H(D):** Constrain the task domain, reduce environmental complexity, filter inputs

These are not mutually exclusive but have different cost profiles and risk characteristics.

### 7.2 When to Amplify (More Tools)

Amplification is the right strategy when:

| Condition | Why |
|-----------|-----|
| The variety gap is small (< 5 bits) | A few well-chosen tools can close it |
| Tool-task mapping is clear | High p_select means low variety illusion |
| Tools are composable | Multiplicative variety gain |
| The domain has natural tool boundaries | Tools match domain structure (e.g., calculator for math) |
| Selection accuracy remains high | Adding tools doesn't degrade existing performance |

**Example:** Toolformer adding 5 tools to GPT-J. The variety gap for math was ~10 bits. A calculator provides exactly those 10 bits. Selection accuracy was 97.9%. The result: a 6.7B model outperforms a 175B model. This is ideal variety amplification.

### 7.3 When to Attenuate (Constrain the Domain)

Attenuation is the right strategy when:

| Condition | Why |
|-----------|-----|
| The variety gap is large (> 10 bits) | No practical number of tools can close it |
| Tool selection is unreliable | Variety illusion dominates |
| The task domain is unbounded | H(D) grows faster than H(R) |
| Errors compound across steps | Multi-step tasks with error cascading |
| Safety constraints apply | Unbounded action variety is dangerous |

**Example:** Karpathy's AutoResearch. Instead of giving the agent more tools to handle arbitrary research tasks, the design constrains the domain to: one file, one metric, fixed iterations. This reduces H(D) from ~40 bits (open research) to ~15 bits (constrained experiment), which the agent's existing variety can match.

### 7.4 The Decision Framework

Given a specific agent-task pairing:

```
1. Estimate H(D) for the task domain
2. Estimate H(R) for the agent's current configuration
3. Compute gap = H(D) - H(R)

IF gap <= 0:
    Agent is sufficient. Deploy. Monitor for drift.

IF 0 < gap <= 5 bits:
    AMPLIFY: Add targeted tools that directly address the gap.
    Verify selection accuracy remains > 90%.
    Expected improvement: closing the gap to near-zero.

IF 5 < gap <= 15 bits:
    MIXED STRATEGY:
    - Attenuate the task domain (constrain scope, decompose into subtasks)
    - Amplify with tools for the constrained subtasks
    - Use human-in-the-loop for the remaining gap
    Expected improvement: reducing gap to < 5 bits per subtask.

IF gap > 15 bits:
    ATTENUATE FIRST. Do not attempt to amplify.
    The variety illusion will dominate any tool-based approach.
    Constrain the domain until gap < 15 bits, then apply mixed strategy.
    This is the AutoGPT lesson.
```

### 7.5 The Multi-Scale Version

The single-scale framework above is insufficient when tasks have multi-scale structure (most real tasks do). Apply the Siegenfeld & Bar-Yam extension:

```
For each scale s (action, sequence, strategy, meta):
    1. Estimate H_s(D) — environmental complexity at scale s
    2. Estimate H_s(R) — agent complexity at scale s
    3. Compute gap_s = H_s(D) - H_s(R)

The agent will fail at the scale with the largest gap.
Address that scale first.
```

This predicts, for example, that adding more fine-grained tools to AutoGPT would not help — the bottleneck is at the strategy scale, not the action scale. What AutoGPT needed was not more tools but more strategic variety: better planning, goal maintenance, and meta-cognition.

The practical implication: **diagnose the scale of the variety deficit before choosing amplification vs. attenuation.** Fine-scale deficits are best addressed by tools. Coarse-scale deficits are best addressed by architectural changes (better planning, human oversight, hierarchical decomposition).

### 7.6 Summary of Quantitative Predictions

| Prediction | Basis | Testable? |
|-----------|-------|-----------|
| Data analysis agents outperform web browsing agents | Variety gap ~0 vs ~11 bits | Yes — benchmark comparisons exist |
| 5 well-matched tools > 500 poorly-matched tools | Effective variety accounting | Yes — compare Toolformer vs. ToolBench performance |
| AutoGPT-style failures are inevitable for open-ended task domains | Variety deficit > 15 bits | Confirmed by empirical record |
| MCP's two-stage attenuation (host + LLM) outperforms single-stage | Information-theoretic selection cost | Testable — compare direct vs. curated tool presentation |
| Optimal tool set size exists and is finite | Selection-execution tradeoff | Testable — sweep tool count vs. task performance |
| Multi-step task failure rate is predictable from per-step variety deficit | Compound error from variety mismatch | Partially testable — compare predicted vs. actual failure rates |

---

## 8. Honest Assessment of These Estimates

The numbers in this analysis are order-of-magnitude estimates, not measurements. Specific weaknesses:

1. **Independence assumptions.** I treat variety dimensions as independent (multiplicative). In reality, task dimensions are heavily constrained (you don't see all combinations of language x task type x codebase size). Real variety is lower than the independent estimate. But the *relative* ordering of domains should be robust.

2. **Selection accuracy curves.** The p_select estimates for 50 and 500 tools are extrapolations, not measurements. Real selection accuracy depends on the specific tool distribution, description quality, and model capability. The qualitative point (accuracy degrades with tool count) is well-supported; the specific numbers are guesses.

3. **The variety illusion formula.** Treating effective variety as a simple product of probabilities is a simplification. In practice, different failure modes interact: misselection can lead to misparameterization, which compounds. The product formula underestimates the variety illusion.

4. **Multi-scale estimates.** The per-scale complexity numbers for AutoGPT are educated guesses, not derivations. The qualitative diagnosis (fine-scale matched, coarse-scale deficit) is robust; the bit-level numbers are illustrative.

5. **What's missing.** This analysis treats the agent as a single-step regulator. Real agents operate over multiple steps with memory and feedback. A full treatment would need to account for the agent's ability to iteratively reduce variety through multi-turn interaction — which partially compensates for per-step deficits. The single-step analysis is a lower bound on agent capability.

Despite these limitations, the variety framework provides something the field currently lacks: a **quantitative language for discussing agent-task match** that goes beyond "it works" or "it doesn't." Even rough variety estimates can prevent obvious mistakes (like deploying an agent with a 15-bit variety deficit) and guide architectural decisions (amplify vs. attenuate, fine-scale vs. coarse-scale).

---

## Sources

- Ashby, W.R. (1956). *An Introduction to Cybernetics.* Chapman & Hall. Sections 7, 10, 11.
- Siegenfeld, A.F. & Bar-Yam, Y. (2022). "A Formal Definition of Scale-dependent Complexity and the Multi-scale Law of Requisite Variety." arXiv:2206.04896.
- Schick, T. et al. (2023). "Toolformer: Language Models Can Teach Themselves to Use Tools." NeurIPS 2023. arXiv:2302.04761.
- Conant, R.C. & Ashby, W.R. (1970). "Every Good Regulator of a System Must Be a Model of That System." *IJSS*, 1(2), 89-97.
- Model Context Protocol Specification (2025-11-25). https://modelcontextprotocol.io/specification/2025-11-25
- AutoGPT failure analysis (project internal notes, autogpt-failure-analysis.md).
- Wang, L. et al. (2023). "A Survey on Large Language Model based Autonomous Agents." arXiv:2308.11432.
