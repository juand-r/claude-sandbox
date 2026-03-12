# Toolformer: Language Models Can Teach Themselves to Use Tools

**Paper:** Schick, T., Dwivedi-Yu, J., Dessi, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N., & Scialom, T. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools.* arXiv:2302.04761. NeurIPS 2023 (Oral).

**Date of notes:** 2026-03-12

---

## 1. Core Problem and Motivation

LLMs exhibit a paradox: they can solve complex tasks from few examples or instructions, yet struggle with basic functionality where trivial programs excel -- arithmetic, factual lookup, date awareness, low-resource language understanding. Prior approaches to tool integration required either (a) large amounts of human annotation or (b) restriction to task-specific settings.

Toolformer addresses five specific LLM weaknesses:
- Inability to access up-to-date information
- Tendency to hallucinate facts
- Difficulties with low-resource languages
- Lack of mathematical skills
- Unawareness of time progression

**Key desiderata:** The approach should be (1) self-supervised (no large annotation effort), and (2) general-purpose (the model itself decides when and how to use tools, not constrained to specific tasks).

---

## 2. The Self-Supervised Tool Learning Mechanism

### 2.1 How the Model Learns WHEN to Call Tools

The model learns when to call tools through a **loss-based filtering criterion**. During training data augmentation, candidate API calls are inserted at various positions in text. An API call is retained only if it **reduces the model's loss on subsequent tokens** by at least a threshold amount. This means the model is trained on examples where tool use demonstrably helped predict what comes next -- it learns the textual contexts where tools are useful.

At **inference time**, the model generates an API-start token (`<API>`) whenever it appears among the top-k most likely next tokens (k=10 in their experiments). This is a relaxed form of greedy decoding -- the model has learned from training data that certain contexts warrant tool calls.

### 2.2 How the Model Learns WHICH Tool to Call

Each tool has its own API name (e.g., `QA`, `Calculator`, `WikiSearch`, `MT`, `Calendar`). The model learns the association between context and tool name from the filtered training examples. In practice, the model exhibits strong tool selection: on math benchmarks it uses the calculator 97.9% of the time, on fact completion it uses QA 98.1% of the time, on question answering it uses WikiSearch 99.3% of the time.

### 2.3 How the Model Learns to USE Results

The training data includes the API result inline: `<API>tool(input) -> result</API>`. The model learns to condition its subsequent token generation on the returned result. At inference time, when the model generates up to the `->` token, decoding pauses, the API is actually executed, the result is inserted, and decoding resumes.

---

## 3. The Training Pipeline: Candidate Generation, Execution, Filtering

### Step 1: Sampling Candidate API Calls

For each API tool, a **prompt** P(x) is constructed with a few demonstrations of that tool being used in text. For each position i in a text sequence x = (x_1, ..., x_n):

1. Compute the probability the model assigns to starting an API call:
   ```
   p_i = p_M(<API> | P(x), x_{1:i-1})
   ```
2. Keep positions where p_i > tau_s (sampling threshold).
3. If more than k positions qualify, keep the top k.
4. For each qualifying position, sample up to m candidate API calls by continuing generation conditioned on the prefix.

**Default hyperparameters:**
- tau_s = 0.05 (sampling threshold)
- k = 5 (max positions per text)
- m = 5 (candidates per position)

**For sparse tools** (calculator, machine translation where few positions naturally trigger calls):
- tau_s = 0.0 (consider all positions)
- k = 20
- m = 10

### Step 2: Executing API Calls

All sampled candidate API calls are executed against their respective tools to obtain text results.

### Step 3: Filtering by Loss Reduction

This is the core innovation. For each candidate API call c_i at position i:

**Define the weighted cross-entropy loss:**
```
L_i(z) = -sum_{j=i}^{n} w_{j-i} * log p_M(x_j | z, x_{1:j-1})
```

Where z is optional prefix text (the API call annotation), and the weights are:
```
w_t = w_tilde_t / sum_s(w_tilde_s)
where w_tilde_t = max(0, 1 - 0.2 * t)
```

These weights create a **linearly decaying window of 5 tokens** -- the loss focuses on the tokens immediately following the API call, where the result should be most helpful.

**Two loss instantiations are compared:**
- L_i^+ = L_i(e(c_i, r_i)) -- loss WITH the API call and its result
- L_i^- = min(L_i(epsilon), L_i(e(c_i, epsilon))) -- loss WITHOUT result (minimum of: no API call at all, or API call with empty result)

The minimum in L_i^- is important: it ensures the API call is kept only if the *result* helps, not just the act of calling (which might itself provide information via the query text).

**Filtering criterion:** Keep the API call if and only if:
```
L_i^- - L_i^+ >= tau_f
```

**Default tau_f = 1.0** for most tools. **tau_f = 0.5** for calculator and machine translation (sparse tools that need more lenient filtering).

### Step 4: Finetuning

The filtered API calls are merged into the original text to create augmented dataset C*. The model is finetuned on C* using standard language modeling objective. Crucially, the *same text* as the original dataset is used, just with API call annotations inserted. This preserves language modeling ability.

### Data Statistics (tau_f = 1.0)

| Tool | Examples with API calls |
|------|----------------------|
| Question Answering | 18,526 |
| Wikipedia Search | 60,974 |
| Calculator | 994 |
| Calendar | 20,587 |
| Machine Translation | 1,034 |

Note the extreme sparsity of calculator and translation calls -- the model learns these are rarely needed but critical when they are.

---

## 4. The Five Tools

### 4.1 Calculator
- Supports +, -, *, / (four basic operations)
- Results rounded to two decimal places
- Example: `[Calculator(18 + 12 * 3)]` -> `54`

### 4.2 Question Answering (QA)
- Based on Atlas (Izacard et al., 2022), finetuned on Natural Questions
- Takes a natural language question, returns a short answer
- Example: `[QA(Where was Knights of Columbus founded?)]` -> `New Haven, Connecticut`

### 4.3 Wikipedia Search
- BM25 retriever over Wikipedia dumps from KILT benchmark
- Takes a search term, returns relevant text snippets
- Example: `[WikiSearch(Fishing Reel Types)]` -> relevant passages

### 4.4 Machine Translation
- NLLB model (600M parameters, supports 200 languages)
- Auto-detects source language via fastText
- Always translates to English
- Example: `[MT(surete nucleaire)]` -> `nuclear safety`

### 4.5 Calendar
- Takes no input
- Returns current date as natural language string
- Example: `[Calendar()]` -> `Today is Monday, January 30, 2023`

---

## 5. API Call Format

### Linearized Representation

API calls are embedded directly in the text stream using special delimiter tokens:

- **Without result:** `<API>tool_name(input)</API>`
- **With result:** `<API>tool_name(input) -> result</API>`

### Implementation Detail

Rather than adding special tokens to the vocabulary (which would require architectural changes), the authors use existing token sequences:
- `[` for `<API>`
- `]` for `</API>`
- `->` for the result separator

### Inference Procedure

1. Model generates tokens normally via autoregressive decoding.
2. If `<API>` appears in the **top-k most likely tokens** (k=10), it is selected and API call generation begins.
3. Model generates the tool name and input.
4. When `->` is generated, **decoding pauses**.
5. The API is executed with the generated input.
6. The result text and `</API>` token are inserted.
7. Normal decoding resumes, now conditioned on the result.
8. **Constraint:** Maximum one API call per input (prevents loops).

---

## 6. Experimental Results

### Model and Setup
- **Base model:** GPT-J (6.7B parameters)
- **Training data:** Subset of CCNet
- **Training:** Batch size 128, learning rate 1e-5, linear warmup 10%
- **Baselines:** GPT-J, GPT-J finetuned on CCNet without APIs (GPT-J+CC), Toolformer with APIs disabled, OPT (66B), GPT-3 (175B)

### 6.1 Fact Retrieval (LAMA Benchmark)

| Model | SQuAD | Google-RE | T-REx |
|-------|-------|-----------|-------|
| GPT-J (6.7B) | 17.8 | 4.9 | 31.9 |
| Toolformer | **33.8** | **11.5** | **53.5** |
| OPT (66B) | 21.6 | 2.9 | 30.1 |
| GPT-3 (175B) | 26.8 | 7.0 | 39.8 |

Toolformer (6.7B) **outperforms GPT-3 (175B)** on fact retrieval by a large margin. Uses QA tool 98.1% of the time.

### 6.2 Mathematical Reasoning

| Model | ASDiv | SVAMP | MAWPS |
|-------|-------|-------|-------|
| GPT-J (6.7B) | 7.5 | 5.2 | 9.9 |
| Toolformer | **40.4** | **29.4** | **44.0** |
| OPT (66B) | 6.0 | 4.9 | 7.9 |
| GPT-3 (175B) | 14.0 | 10.0 | 19.8 |

The most dramatic improvement. A 6.7B model with a calculator **triples** GPT-3's performance on math. Uses calculator 97.9% of the time.

### 6.3 Question Answering

| Model | WebQS | NQ | TriviaQA |
|-------|-------|-------|----------|
| GPT-J (6.7B) | 18.5 | 12.8 | 43.9 |
| Toolformer | **26.3** | **17.7** | **48.8** |
| GPT-3 (175B) | 29.0 | 22.6 | 65.9 |

Substantial improvement over GPT-J but does not surpass GPT-3 on QA. Uses WikiSearch 99.3% of the time. GPT-3's parametric knowledge advantage is significant here.

### 6.4 Multilingual QA (MLQA)

Mixed results. Translation tool usage varies widely by language (7.3% to 94.9%). Some languages show improvement, others show degradation. The translation tool's helpfulness is inconsistent.

### 6.5 Temporal Reasoning

| Model | TempLAMA | Dateset |
|-------|----------|---------|
| GPT-J | 13.7 | 3.9 |
| Toolformer | **16.3** | **27.3** |
| GPT-3 (175B) | 15.5 | 0.8 |

On the Dateset benchmark, Toolformer achieves 27.3% vs GPT-3's 0.8% -- the calendar tool provides a massive advantage for date-dependent questions. Calendar used 54.8% of the time on Dateset. Interestingly, on TempLAMA, the model uses other tools instead of the calendar.

### 6.6 Language Modeling Perplexity (No Degradation)

| Model | WikiText | CCNet |
|-------|----------|-------|
| GPT-J | 9.9 | 10.6 |
| Toolformer (disabled) | 10.3 | 10.5 |

When API calls are disabled, Toolformer's perplexity is comparable to GPT-J. The finetuning does not hurt core language modeling ability.

### 6.7 Scaling Laws

- Tool use ability **emerges around 775M parameters**.
- Models below this (124M, 355M) show minimal benefit from tool access.
- The gap between with/without tools remains large even at 6.7B.
- Wikipedia search is the easiest tool to learn; others require larger models.

### 6.8 Decoding Strategy (k threshold)

For T-REx:
- k=1 (strict greedy): 40.3% call rate, 47.8% accuracy
- k=10 (relaxed): 98.1% call rate, 53.5% accuracy

At k=1, the model is **selective** -- it only calls APIs for examples it would perform poorly on. Higher k forces more tool use, which generally helps.

---

## 7. Limitations

### 7.1 No Tool Chaining
The model cannot use the output of one tool as input to another. API calls are generated independently. This prevents multi-step reasoning like "search for X, then calculate Y based on the result."

### 7.2 No Interactive Tool Use
Cannot refine queries, browse multiple search results, or iterate. One shot per tool call. This is especially limiting for search, where real users reformulate queries.

### 7.3 Prompt Sensitivity
The model is sensitive to exact wording when deciding whether to call an API. Minor rephrasing can change whether a tool is invoked.

### 7.4 Sample Inefficiency
Processing over 1 million documents yields only ~994 useful calculator calls. The filtering is extremely selective, which is good for quality but wasteful computationally.

### 7.5 No Cost Awareness
The model does not consider computational cost of API calls. It cannot weigh whether a tool call is "worth it" in terms of latency or resource consumption.

### 7.6 One Call Per Input
A hard constraint in the system. Prevents sequential reasoning patterns that would require multiple tool invocations.

### 7.7 Static Tool Set
The set of tools is fixed at training time. The model cannot discover or learn to use new tools at inference time without retraining.

---

## 8. Cybernetic Analysis

### 8.1 Tool Use as Variety Amplification (Ashby's Law of Requisite Variety)

Ashby's Law states: a controller must have at least as much variety as the system it regulates. An LLM without tools has **fixed variety** -- its responses are constrained to what it learned during pretraining. Its "variety" is bounded by its parameter count, training data, and the frozen snapshot of the world it was trained on.

Tool use is a **variety amplifier**. Each tool adds a new dimension of response capability:
- Calculator: extends variety to exact arithmetic (infinite precision within operation domain)
- WikiSearch: extends variety to the full Wikipedia corpus (dynamic, updateable)
- QA: extends variety through a specialized retrieval model
- Calendar: extends variety to temporal awareness (a single bit of information the model literally cannot know)
- Translation: extends variety across 200 languages

The results demonstrate this directly: a 6.7B model with tools **outperforms a 175B model without tools** on several benchmarks. The tools provide variety that cannot be matched by simply scaling parameters. This is a clean empirical demonstration of Ashby's Law -- the tool-augmented model has sufficient variety to regulate (predict/match) the environment, while the larger model without tools does not.

The mathematical framing: Let V(M) be the variety of a model M, and V(E) the variety of the environment (downstream tasks). For fact retrieval, V(GPT-3) < V(E) despite 175B parameters, because facts change and parametric memory is static. But V(Toolformer) >= V(E) because WikiSearch/QA provide dynamic access to facts.

### 8.2 Self-Supervised Learning as Ultrastability

Ashby's **ultrastability** describes a system that explores parameter configurations randomly and retains configurations that maintain stability (keep essential variables within viable bounds). The Toolformer training pipeline is a direct instantiation:

1. **Random exploration:** Candidate API calls are sampled at many positions with various inputs. This is the "random parameter variation" phase.
2. **Stability criterion:** The loss-based filter (L^- - L^+ >= tau_f) checks whether the new configuration (with API call) maintains or improves "stability" (lower prediction loss = better environmental model).
3. **Selection:** Only configurations that improve stability are retained in the training data.
4. **Adaptation:** The model is finetuned on the selected configurations, internalizing the stable patterns.

This is structurally identical to Ashby's homeostat:
- The homeostat has random parameter changes triggered when essential variables leave their viable range.
- Toolformer has random API call insertions filtered by whether they improve prediction (keep the "essential variable" of loss within bounds).
- Both systems explore randomly and select for stability, converging on functional configurations without explicit design of the solution.

The key difference: Ashby's homeostat operates in real time with continuous feedback. Toolformer's ultrastability operates in a **batch offline mode** -- all exploration happens during data augmentation, and selection happens before finetuning. It is ultrastability compressed into a single training cycle rather than ongoing adaptation.

### 8.3 The Good Regulator Theorem

Conant and Ashby (1970): "Every good regulator of a system must be a model of that system." A language model is literally a statistical model of language (and by extension, the world described by language). The question is: does tool access make it a *better* model?

The evidence strongly supports yes:
- On LAMA (fact completion), Toolformer achieves 53.5% vs GPT-J's 31.9% on T-REx. The tool-augmented model is a better model of the factual world.
- On math, 40.4% vs 7.5% on ASDiv. The tool-augmented model is a better model of mathematical relationships.
- On temporal tasks, 27.3% vs 3.9% on Dateset. The tool-augmented model is a better model of time.

Crucially, **perplexity does not degrade** when tools are disabled. The model has not traded general language modeling for tool use -- it has *added* modeling capacity. This means tool access provides a **strictly better regulator**: it models everything the base model does, plus domains the base model fails at.

The Good Regulator Theorem also explains *why* the self-supervised approach works: the filtering criterion (loss reduction) directly measures whether the tool makes the model a better regulator. An API call passes the filter if and only if it improves the model's ability to predict (regulate/match) the text. The training process literally optimizes for "better regulator" status.

### 8.4 Comparison to Ashby's Homeostat

| Aspect | Ashby's Homeostat | Toolformer |
|--------|------------------|------------|
| System | Electrical circuit with random parameter changes | LLM with random API call insertions |
| Essential variables | Voltages within viable range | Prediction loss within acceptable range |
| Perturbation | Random resistor changes via uniselector | Random sampling of API calls at various positions |
| Stability test | Do voltages remain in bounds? | Does L^- - L^+ >= tau_f? |
| Adaptation | Keep parameter settings that achieve stability | Keep API calls that reduce loss |
| Mechanism | Step function (uniselector changes when essential variable hits boundary) | Threshold function (filter by loss difference) |
| Timescale | Real-time continuous | Batch offline (single training cycle) |
| Coupling | Multiple homeostats can couple and co-adapt | Tools are independent (no chaining) -- a key limitation |

The lack of tool chaining in Toolformer maps to a homeostat with uncoupled subsystems. A fully cybernetic tool-using agent would allow tools to compose (coupled homeostats), which is precisely what later agentic systems (ReAct, AutoGPT, etc.) attempt.

---

## 9. Influence on the Trajectory Toward Function Calling

Toolformer (February 2023) was a catalyst in the industry's adoption of tool use as a standard LLM capability:

### Timeline of influence:
1. **Feb 2023:** Toolformer published (arXiv), demonstrating self-supervised tool learning
2. **Mar 2023:** ChatGPT plugins announced by OpenAI (tool use via curated plugin ecosystem)
3. **Jun 2023:** OpenAI launches Function Calling API -- models trained to output structured function calls with JSON arguments
4. **Nov 2023:** OpenAI upgrades from `functions` to `tools` parameter, generalizing the concept
5. **2023-2024:** Anthropic (Claude tool use), Google (Gemini function calling), and open-source models (Gorilla, ToolLLM) adopt similar patterns
6. **NeurIPS 2023:** Toolformer accepted as oral presentation, cementing its foundational status

### Key conceptual contributions that influenced the industry:

1. **API calls as inline text:** Toolformer's representation of tool calls as tokens in the text stream directly influenced the design of function calling APIs. The model generates structured output (function name + arguments) as part of its normal token generation.

2. **Model decides when to call:** The principle that the model autonomously decides tool invocation (vs. being externally prompted) became standard. OpenAI's `tool_choice: "auto"` mode is this exact paradigm.

3. **Self-supervised tool learning:** While industry implementations use RLHF and supervised finetuning on human-annotated tool use examples (rather than Toolformer's automated pipeline), the conceptual insight that models can learn tool use from training data (not just prompt engineering) was validated here.

4. **Separation of concerns:** Toolformer's architecture -- model generates call, execution happens externally, result is inserted -- became the universal pattern. No commercial API has the model execute tools directly; they all use this generate-pause-execute-resume loop.

### What the industry changed from Toolformer's design:

- **Structured output:** Industry moved from inline text tokens to JSON-structured function calls with typed arguments and schemas. More reliable for production use.
- **Tool chaining:** Modern systems support multiple sequential tool calls (addressing Toolformer's key limitation).
- **Interactive use:** Modern agents can refine tool queries based on results.
- **Human-in-the-loop training:** Industry uses human annotation and RLHF rather than self-supervised filtering.
- **Dynamic tool registration:** Users can define arbitrary tools at inference time via schemas, rather than training on a fixed set.

---

## 10. Tool Use and the Extended Mind Thesis

### 10.1 The Extended Mind Thesis (Clark & Chalmers, 1998)

Clark and Chalmers argue that cognition is not confined to the brain. When external resources (notebooks, calculators, databases) are reliably coupled to a cognitive agent and play the same functional role as internal processes, they are *constitutive* of cognition, not merely causal aids.

Their criteria for cognitive extension:
1. The external resource is **reliably available** and typically invoked
2. Information from the resource is **automatically endorsed** (not critically scrutinized each time)
3. The information is **easily accessible**
4. The information was **consciously endorsed** at some prior time

### 10.2 Toolformer as Extended Artificial Mind

Toolformer satisfies a computational analogue of the extended mind criteria:

1. **Reliably available:** Tools are available at inference time and invoked consistently (98%+ call rates on relevant tasks).
2. **Automatically endorsed:** The model integrates tool results directly into its generation without "scrutinizing" them -- the result tokens are treated as part of the context.
3. **Easily accessible:** Tool calls are part of the token generation process, accessible with the same mechanism as generating any other token.
4. **Prior endorsement:** The training process (loss-based filtering) is the "endorsement" phase -- tool results were validated as useful during training.

### 10.3 The Otto-Inga Analogy

Clark and Chalmers' famous thought experiment: Otto (Alzheimer's patient) stores beliefs in a notebook; Inga stores them in biological memory. If the notebook plays the same functional role as Inga's memory, it is part of Otto's cognitive system.

Mapping to Toolformer:
- **Inga = GPT-3 (175B):** Stores facts in parametric memory (weights). Can recall "New Haven, Connecticut" because it memorized it during training.
- **Otto = Toolformer (6.7B + QA tool):** Stores the *ability to look up* facts. Cannot recall "New Haven, Connecticut" from weights, but can call `QA("Where was Knights of Columbus founded?")` and get the answer.

Both produce the same output. If we accept Clark and Chalmers' argument, Toolformer's QA tool is *constitutive* of its "knowledge," not merely a causal aid. The 6.7B model + tool **knows** as much as (or more than) the 175B model, just via a different substrate.

### 10.4 Beyond Extension: Variety Amplification

The extended mind thesis and Ashby's Law converge here. Clark and Chalmers argue external tools extend cognition. Ashby's Law says a regulator needs sufficient variety. Tool use both *extends* the cognitive system (philosophy) and *amplifies its variety* (cybernetics). These are two vocabularies describing the same phenomenon:

- **Philosophy:** The tool becomes part of the mind.
- **Cybernetics:** The tool increases the system's requisite variety.
- **Machine learning:** The tool reduces prediction loss.

All three frameworks predict the same empirical outcome: tool-augmented systems outperform non-augmented ones when the environment requires capabilities beyond the base system's internal resources.

### 10.5 Limits of the Analogy

The extended mind thesis has a key criterion: the agent must *choose* to consult the external resource in a way that mirrors internal retrieval. Toolformer partially satisfies this -- it learns *when* to call tools, analogous to Otto deciding when to check his notebook. But it cannot:
- Decide to *stop* using a tool if it gives bad results (no meta-cognition about tool reliability)
- Choose between multiple tools for the same query adaptively
- Learn to use new tools without retraining (Otto can start a new notebook)

These limitations map to the "cognitive bloating" critique: if we say the QA system is part of Toolformer's mind, is the entire Wikipedia corpus also part of its mind? Where does the boundary stop? The same question applies to modern agentic systems with internet access.

---

## 11. Summary of Key Insights

1. **Self-supervised tool learning works.** The loss-based filtering criterion is elegant and effective: a tool call is useful if and only if the result helps predict subsequent tokens.

2. **Tools provide superlinear capability scaling.** A 6.7B model + tools > 175B model without tools, on specific benchmarks. This is more efficient than scaling parameters.

3. **The approach is fundamentally a cybernetic one.** Random exploration + stability-based selection = ultrastability. The formal structure is Ashbian.

4. **Tool use is variety amplification.** Each tool extends the model's response repertoire into domains its parameters cannot reach (dynamic facts, exact math, current time).

5. **The filtering threshold tau_f is the "essential variable boundary."** It defines what counts as "stable enough" -- analogous to the viable range in a homeostat.

6. **The key limitation is lack of coupling.** No tool chaining means no coupled homeostats. The system cannot compose tool calls into multi-step reasoning. This is precisely what the subsequent generation of agentic frameworks addresses.

7. **Emergence at scale.** Tool use only becomes learnable at ~775M parameters, suggesting a phase transition in the model's ability to represent the "when and how" of tool invocation.

8. **The extended mind reading is natural but has limits.** Toolformer's tools satisfy functional criteria for cognitive extension, but the lack of meta-cognitive oversight (no ability to evaluate tool reliability or adapt tool strategy) weakens the analogy.

---

## References

- Ashby, W.R. (1956). *An Introduction to Cybernetics.* Chapman & Hall.
- Clark, A. & Chalmers, D. (1998). "The Extended Mind." *Analysis*, 58(1), 7-19.
- Conant, R.C. & Ashby, W.R. (1970). "Every Good Regulator of a System Must Be a Model of That System." *International Journal of Systems Science*, 1(2), 89-97.
- Izacard, G. et al. (2022). "Atlas: Few-shot Learning with Retrieval Augmented Language Models."
- Parisi, A. et al. (2022). "TALM: Tool Augmented Language Models."
- Schick, T. et al. (2023). "Toolformer: Language Models Can Teach Themselves to Use Tools." NeurIPS 2023.
