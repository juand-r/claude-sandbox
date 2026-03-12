# Scholarly Notes: ReAct — Synergizing Reasoning and Acting in Language Models

**Citation:** Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2022). ReAct: Synergizing Reasoning and Acting in Language Models. arXiv:2210.03629. Published at ICLR 2023.

**Affiliations:** Princeton University (Dept. of Computer Science) and Google Research (Brain team).

**Date of these notes:** 2026-03-12

---

## 1. The Thought-Action-Observation Loop: Formal Structure

### 1.1 Formal Setup

At time step *t*, an agent receives an observation $o_t \in \mathcal{O}$ from the environment and takes an action $a_t \in \mathcal{A}$ following some policy $\pi(a_t | c_t)$, where $c_t = (o_1, a_1, \ldots, o_{t-1}, a_{t-1}, o_t)$ is the **context** (the full trajectory so far).

The core idea of ReAct is to augment the action space: $\hat{\mathcal{A}} = \mathcal{A} \cup \mathcal{L}$, where $\mathcal{L}$ is the space of language. An action $\hat{a}_t \in \mathcal{L}$ is called a **thought** or **reasoning trace**. Critically:

- A **thought** does NOT affect the external environment. It produces no observation feedback.
- A thought composes useful information by reasoning over the current context $c_t$.
- A thought updates the context: $c_{t+1} = (c_t, \hat{a}_t)$ — it becomes part of what the model conditions on next.

### 1.2 What Goes Into Each Step

**Thought** — Free-form natural language. Serves multiple roles identified in the paper:
1. **Decomposing questions** — "I need to search X, find Y, then find Z"
2. **Extracting information from observations** — "X was started in 1844", "The paragraph does not tell X"
3. **Performing commonsense reasoning** — "X is not Y, so Z must instead be..."
4. **Arithmetic reasoning** — "1844 < 1989"
5. **Guiding search reformulation** — "maybe I can search/look up X instead"
6. **Synthesizing the final answer** — "...so the answer is X"
7. **Tracking progress and subgoals** (in decision-making tasks) — "Now I need to find the pepper shaker"
8. **Handling exceptions** — "I don't have salt, so let me use soy sauce and pepper instead"

**Action** — Domain-specific, drawn from $\mathcal{A}$. For knowledge tasks (HotPotQA, FEVER), three actions:
- `search[entity]` — returns first 5 sentences from Wikipedia page, or top-5 similar entities if not found
- `lookup[string]` — returns next sentence containing the string (simulates Ctrl+F)
- `finish[answer]` — terminates the episode with an answer

For ALFWorld: text actions like "go to cabinet 1", "open drawer 1", "take pepper shaker 1 from countertop 3", "put pepper shaker 1 in/on drawer 1", etc.

For WebShop: actions to search, choose product, choose options, buy.

**Observation** — The environment's response to an action. Wikipedia API results for knowledge tasks; environment state descriptions for ALFWorld/WebShop. Thoughts produce NO observation (this is key — they are purely internal).

### 1.3 Interleaving Pattern

For **reasoning-primary tasks** (HotPotQA, FEVER): strict alternation of Thought-Action-Observation triples. The trajectory looks like:

```
Thought 1: I need to search Colorado orogeny, find the area...
Action 1:  Search[Colorado orogeny]
Observation 1: The Colorado orogeny was an episode of mountain building...
Thought 2: It does not mention the eastern sector. So I need to look up eastern sector.
Action 2:  Lookup[eastern sector]
Observation 2: (Result 1/1) The eastern sector extends into the High Plains...
Thought 3: The eastern sector extends into the High Plains. So I need to search High Plains...
Action 3:  Search[High Plains]
...
```

This is what the paper calls "dense thought" — every action is preceded by a thought.

For **decision-making tasks** (ALFWorld, WebShop): thoughts appear **sparsely**, only at "the most relevant positions." The model decides for itself when to think vs. when to just act. Example from ALFWorld:

```
Act 1: Think[First I need to find a pepper shaker...more likely in cabinets (1-6), countertops (1-3),...]
Act 2: Go to cabinet 1
Obs 2: On the cabinet 1, you see a vase 2.
...
Act 5: Go to countertop 3
Obs 6: On the countertop 3, you see a apple 1, a bread 1, ... a pepper shaker 1, and a vase 3.
Act 7: Take pepper shaker 1 from countertop 3
Obs 7: You pick up the pepper shaker 1 from the countertop 3.
Act 8: Think[Now I find a pepper shaker 1. Next, I need to put it in/on drawer 1.]
Act 9: Go to drawer 1
...
```

Note: in ALFWorld, `Think[...]` is itself an action in the action space. Thoughts are not interleaved as a separate label but embedded as special actions.

---

## 2. Prompt Format and Few-Shot Setup

### 2.1 Number of In-Context Examples

| Task | Few-shot examples |
|------|------------------|
| HotPotQA | 6 examples (from training set) |
| FEVER | 3 examples (from training set) |
| ALFWorld | 3 annotated trajectories per task type (6 task types); 6 prompts per type constructed from permutations of 2 out of 3 |
| WebShop | 1 example (one-shot) |

**Important footnote:** The authors tried more examples and found they do NOT improve performance (footnote 2, p.4). This is notable — the system works with remarkably few demonstrations.

### 2.2 Prompt Construction

Each in-context example is a **human-written trajectory** of actions, thoughts, and environment observations solving a task instance. These are manually composed by the authors from training set cases.

For HotPotQA, the prompt contains three sections separated by color-coded labels in the paper:
1. **Standard** examples (question + answer pairs, 6 of them)
2. **Act** examples (question + action-observation sequences, no thoughts)
3. **CoT** examples (question + thought + answer, no actions)
4. **ReAct** examples (question + thought-action-observation sequences)

The baselines (Standard, CoT, Act) are constructed by **ablating** the ReAct trajectories — removing thoughts, or removing actions/observations respectively.

### 2.3 Base Model

Primary experiments: **PaLM-540B** (Chowdhery et al., 2022), frozen, used via few-shot prompting.
Additional experiments: **GPT-3** (text-davinci-002), which actually outperforms PaLM-540B on both HotPotQA (30.8 vs. 29.4 EM) and ALFWorld (78.4% vs. 70.9% success rate).

---

## 3. Results on Each Benchmark — Specific Numbers

### 3.1 HotPotQA (Exact Match on 500 questions)

| Method | EM |
|--------|-----|
| Standard | 28.7 |
| CoT (Wei et al., 2022) | 29.4 |
| CoT-SC (21 samples, majority vote) | 33.4 |
| Act (no thoughts) | 25.7 |
| **ReAct** | **27.4** |
| CoT-SC -> ReAct (best combo) | 34.2 |
| ReAct -> CoT-SC (best combo) | **35.1** |
| Supervised SoTA (domain-specific) | 67.5 |

**Observation:** ReAct alone (27.4) actually **underperforms** CoT (29.4) on HotPotQA. This is a critical nuance. The advantage comes from **combining** the two methods. The best result (35.1) uses ReAct -> CoT-SC: try ReAct first, fall back to CoT-SC if ReAct fails to return an answer within a step limit.

### 3.2 FEVER (Accuracy on 500 claims)

| Method | Acc |
|--------|------|
| Standard | 57.1 |
| CoT | 56.3 |
| CoT-SC (21 samples) | 60.4 |
| Act | 58.9 |
| **ReAct** | **60.9** |
| CoT-SC -> ReAct | **64.6** |
| ReAct -> CoT-SC | 62.0 |
| Supervised SoTA | 89.5 |

**Observation:** On FEVER, ReAct (60.9) outperforms CoT (56.3) and even CoT-SC (60.4) on its own. The claims for SUPPORTS/REFUTES differ only by a small amount (appendix), so retrieving up-to-date knowledge is critical for this task.

### 3.3 ALFWorld (Success Rate % on 134 unseen evaluation games)

| Method | Pick | Clean | Heat | Cool | Look | Pick 2 | All |
|--------|------|-------|------|------|------|--------|-----|
| Act (best of 6) | 88 | 42 | 74 | 67 | 72 | **41** | 45 |
| ReAct (avg) | 65 | 39 | 83 | 76 | 55 | 24 | 57 |
| **ReAct (best of 6)** | **92** | **58** | **96** | **86** | **78** | **41** | **71** |
| ReAct-IM (avg) | 55 | 59 | 60 | 55 | 23 | 24 | 48 |
| ReAct-IM (best of 6) | 62 | **68** | 87 | 57 | 39 | 33 | 53 |
| BUTLER_g (best of 8) | 33 | 26 | 70 | **76** | 17 | 12 | 22 |
| BUTLER (best of 8) | 46 | 39 | 74 | **100** | 22 | 24 | 37 |

Key result: **ReAct best trial (71%) vs. Act best trial (45%) vs. BUTLER best trial (37%).** That is a 34% absolute improvement over the imitation learning baseline BUTLER, and 26% over Act-only. Even the *worst* ReAct trial (48%) beats the *best* Act trial (45%).

The advantage of ReAct over Act is consistent across all 6 controlled trials, with relative performance gain ranging from 33% to 90%, averaging 62%.

### 3.4 WebShop (Score and Success Rate on 500 test instructions)

| Method | Score | SR (%) |
|--------|-------|--------|
| Act (prompting) | 62.3 | 30.1 |
| **ReAct (prompting)** | **66.6** | **40.0** |
| IL (imitation learning, 1012 human annotations) | 59.9 | 29.1 |
| IL+RL (+ 10,587 training instructions) | 62.4 | 28.7 |
| Human Expert | 82.1 | 59.6 |

Key result: One-shot ReAct prompting achieves 40.0% success rate, a **10% absolute improvement** over the previous best (Act at 30.1%, IL at 29.1%, IL+RL at 28.7%). This is achieved with a single in-context example vs. thousands of training instances for the learning methods.

### 3.5 GPT-3 Results (Appendix A.1)

| Task | PaLM-540B | GPT-3 (text-davinci-002) |
|------|-----------|--------------------------|
| HotPotQA (EM) | 29.4 | **30.8** |
| ALFWorld (SR %) | 70.9 | **78.4** |

GPT-3 consistently outperforms PaLM-540B with ReAct prompting, suggesting the approach transfers across model families.

---

## 4. Failure Mode Analysis

The authors randomly sampled 50 trajectories with correct answers and 50 with incorrect answers from both ReAct and CoT on HotPotQA, then manually labeled success and failure modes (200 total trajectories).

### 4.1 Success Modes

| Type | Definition | ReAct | CoT |
|------|-----------|-------|-----|
| True positive | Correct reasoning trace and facts | 94% | 86% |
| False positive | Hallucinated reasoning trace or facts | 6% | 14% |

ReAct's correct answers are overwhelmingly genuinely correct (94% true positive), while CoT has a substantial false positive rate (14%) — getting the right answer despite hallucinated reasoning or facts.

### 4.2 Failure Modes

| Type | Definition | ReAct | CoT |
|------|-----------|-------|-----|
| Reasoning error | Wrong reasoning trace (including failing to recover from repetitive steps) | 47% | 16% |
| Search result error | Search returns empty or does not contain useful information | 23% | — |
| Hallucination | Hallucinated reasoning trace or facts | 0% | **56%** |
| Label ambiguity | Right prediction but did not match the label precisely | 29% | 28% |

### 4.3 Key Failure Analysis Findings

**A) Hallucination is a serious problem for CoT.** CoT has a much higher false positive rate (14% vs. 6%) in success mode, and its **dominant failure mode is hallucination (56%)** of all errors. ReAct has **0% hallucination errors** because it can ground its reasoning in external knowledge retrieval.

**B) The structural constraint of interleaving reasoning and actions reduces flexibility.** While it improves groundedness, ReAct has a notably high **reasoning error rate (47% of failures)** vs. CoT's 16%. The specific error pattern: the model repetitively generates the previous thoughts and actions, failing to reason about what the proper next action should be and getting stuck in a loop. The authors categorize this as "reasoning error" — the model fails to "jump out of the loop."

**C) Search retrieval quality is critical for ReAct.** Non-informative search accounts for **23% of ReAct errors**. When the Wikipedia API returns empty or irrelevant results, the model has a hard time recovering and reformulating thoughts. This is an expected trade-off between factuality (grounding) and flexibility (internal reasoning).

### 4.4 Qualitative Failure: Repetitive Loop

The paper identifies a specific failure pattern in ALFWorld where the ReAct trajectory gets stuck due to a hallucinating thought (e.g., claiming the second keychain is in drawer 4 when it is not). A human can fix this by editing just two thoughts in the trajectory (Act 17 and Act 23 in Figure 5), after which the model successfully completes the task. This demonstrates both the fragility and the **editability** of the reasoning trace.

---

## 5. Comparison to Chain-of-Thought: Where CoT Hallucinates and ReAct Does Not

### 5.1 The Core Difference

CoT reasoning is a "static black box" — the model uses its own internal representations to generate thoughts, and is not grounded in the external world. This means:

- CoT **cannot** reactively update its knowledge
- CoT is prone to **fact hallucination** (56% of its errors)
- CoT can **propagate errors** through the reasoning chain — one wrong "fact" corrupts all downstream reasoning

ReAct, by contrast, interacts with external sources. Each reasoning step can be verified against retrieved information.

### 5.2 Specific Example from the Paper (Figure 1)

**Question:** "Aside from the Apple Remote, what other device can control the program Apple Remote was originally designed to interact with?"

- **CoT (Reason Only):** "Let's think step by step. Apple Remote was originally designed to interact with Apple TV. Apple TV can be controlled by iPhone, iPad, and iPod Touch. So the answer is iPhone, iPad, and iPod Touch." — **WRONG.** Apple Remote was designed for Front Row media center software, not Apple TV. CoT hallucinated the connection to Apple TV.

- **ReAct:** Searched "Apple Remote" -> learned it was designed for Front Row -> searched "Front Row" -> couldn't find it -> searched "Front Row (software)" -> learned it was a media center software controlled by Apple keyboard function keys -> answered "keyboard function keys" — **CORRECT.** The grounding in retrieval prevented the hallucination.

### 5.3 Outdated Labels Example (Figure 4)

HotPotQA question about hotel rooms for the Cirque du Soleil show Mystere. The dataset label (2,664) is outdated. Standard, CoT, and Act all get wrong answers. Only ReAct successfully navigates Wikipedia to find the current number (3,104), because it can reason about what to search and where to look.

### 5.4 The Trade-off

ReAct is more **factual and grounded** but less **flexible** in reasoning. CoT is more **flexible** but prone to **hallucination**. This is why the **combination** (ReAct -> CoT-SC or CoT-SC -> ReAct) performs best:

- **ReAct -> CoT-SC:** Try ReAct; if it fails to answer within 7 steps (HotPotQA) or 5 steps (FEVER), fall back to CoT-SC. Best on HotPotQA (35.1 EM).
- **CoT-SC -> ReAct:** Use CoT-SC; if the majority answer among n samples occurs less than n/2 times (i.e., internal knowledge is uncertain), fall back to ReAct. Best on FEVER (64.6 Acc).

---

## 6. Comparison to Acting Without Reasoning: Where Blind Action Fails

### 6.1 Knowledge Tasks

On HotPotQA, Act-only scores 25.7 EM vs. ReAct's 27.4 EM. The difference is more qualitative than quantitative here — Act fails to synthesize the final answer properly. As shown in Figure 1(1c): Act searches "Apple Remote", then "Front Row", then "Front Row (software)", gets the right information about keyboard function keys, but then issues `Finish[yes]` — a nonsensical answer. Without reasoning, the model cannot synthesize retrieved information into a coherent answer.

### 6.2 ALFWorld (Where the Difference Is Dramatic)

Act-only achieves 45% best success rate vs. ReAct's 71%. The qualitative failures of Act are severe:

- **Cannot decompose goals** into smaller subgoals
- **Loses track** of the current state of the environment
- **Produces hallucinating actions** — e.g., in Figure 1(2a), the agent tries to take a peppershaker from sinkbasin 1 despite the observation clearly showing it was never there. It keeps trying the same action ("Take peppershaker 1 from sinkbasin 1") and getting "Nothing happens."

This is the classic problem of reactive systems without internal state: the agent has no working memory, no plan, and no ability to reason about what is happening.

### 6.3 ReAct vs. Inner Monologue (ReAct-IM)

The paper also compares to a restricted version called ReAct-IM (Inner Monologue style), where thoughts are limited to: (1) decomposing the current goal, and (2) describing the current subgoal. ReAct-IM achieves only 53% (best of 6) on ALFWorld vs. ReAct's 71%.

ReAct-IM fails because it lacks:
- Ability to determine when a subgoal is completed
- Ability to determine what the *next* subgoal should be
- Commonsense reasoning about where items might be in the environment

This confirms that the **content** of thoughts matters, not just having them. Free-form reasoning is significantly more powerful than constrained status reporting.

---

## 7. Few-Shot Setup Details

### 7.1 Number of Examples and Diminishing Returns

- HotPotQA: 6 examples. Authors note (footnote 2): "We find more examples do not improve performance."
- FEVER: 3 examples.
- ALFWorld: 3 trajectories per task type, but only 2 used per prompt (6 prompts from permutations). So effectively 2-shot per evaluation.
- WebShop: 1 example. "Even one-shot ReAct prompting is able to outperform imitation and reinforcement learning methods trained with $10^3 \sim 10^5$ task instances."

### 7.2 What Makes the Few-Shot Examples

Each example is a **complete human-written trajectory** — not just a question-answer pair. The human annotators "just type down their thoughts in language on top of their actions taken." The paper emphasizes this is "intuitive and easy to design" — no ad-hoc format choice, thought design, or example selection required.

### 7.3 Finetuning Results (Small Models)

When finetuned on 3,000 trajectories with correct answers:
- PaLM-8B finetuned with ReAct outperforms all PaLM-62B prompting methods
- PaLM-62B finetuned with ReAct outperforms all PaLM-540B prompting methods
- Finetuning Standard or CoT is significantly worse than finetuning ReAct or Act — the former teaches models to memorize (potentially hallucinated) facts, while ReAct teaches the generalizable skill of reasoning + external retrieval.

---

## 8. Relationship to Classical Cybernetic Feedback

### 8.1 The TOTE Unit

The Thought-Action-Observation loop is structurally isomorphic to the **TOTE (Test-Operate-Test-Exit)** unit from Miller, Galanter, and Pribram (1960). In TOTE:
- **Test:** compare current state to desired state (= Thought: assess what information is needed)
- **Operate:** take action to change the state (= Action: search, lookup, finish)
- **Test:** compare again (= Thought after Observation: did I get what I needed?)
- **Exit:** if goal is met (= Finish[answer])

The key innovation of ReAct is that the Test phase is performed **in natural language** rather than through a fixed comparator. This makes the test criterion itself flexible and context-dependent.

### 8.2 Negative Feedback Loop

ReAct implements a **negative feedback loop** in the Wiener (1948) sense:
- The **reference signal** is the goal (the question to answer, the task to complete)
- The **output** is the action taken
- The **feedback** is the observation from the environment
- The **comparator** is the thought, which computes the error between current state and goal

The thought explicitly computes: "I have X information. I still need Y. Therefore I should do Z." This is textbook negative feedback — the error signal (what I still need) drives the next control action.

### 8.3 Perceptual Control Theory Connection

Bill Powers' Perceptual Control Theory (PCT) argues that organisms control their perceptions, not their actions. ReAct has a similar structure: the thoughts assess **what the agent perceives** (from observations) and compute whether it matches the desired perception (having enough information to answer). Actions are selected to bring perceptions into alignment with goals. The agent is not executing a fixed plan — it is controlling its informational state.

### 8.4 Inner Speech as Cybernetic Mechanism

The paper explicitly invokes Vygotsky (1987), Luria (1965), and Fernyhough (2010) on inner speech as a mechanism for self-regulation. This is a cybernetic idea: verbal reasoning serves as an internal feedback channel that enables the organism to maintain homeostasis (goal-directed behavior) in the face of perturbation (unexpected observations, failed searches, etc.).

The cooking analogy from the introduction is pure cybernetics: "now that everything is cut, I should heat up the pot of water" (test-operate), "I don't have salt, so let me use soy sauce and pepper instead" (error correction via negative feedback), "how do I prepare dough? Let me search on the Internet" (recognizing insufficient variety to handle the disturbance).

---

## 9. What Would Ashby Say? Requisite Variety Analysis

### 9.1 Ashby's Law Applied

Ashby's Law of Requisite Variety: "Only variety can destroy variety." A controller must have at least as much variety as the disturbances it needs to regulate against.

The disturbance space in these tasks includes:
- Ambiguous questions requiring multi-hop reasoning
- Missing or redirected Wikipedia pages
- Outdated information in the knowledge base
- Large physical environments with many locations (ALFWorld has 50+ locations)
- Noisy, unstructured product descriptions (WebShop)

### 9.2 How ReAct Increases Variety

**Act-only** has variety = $|\mathcal{A}|$ — the number of available actions. This is finite and domain-specific.

**CoT-only** has variety = $|\mathcal{L}|$ — the space of language, which is vast but **ungrounded**. It can express many things but cannot verify any of them. This is *illusory variety* — high nominal variety that fails when confronted with real disturbances (hallucination under novel questions).

**ReAct** has variety = $|\mathcal{A} \cup \mathcal{L}|$ — both the action space AND the language space. More importantly, the combination creates a **feedback loop** that amplifies effective variety: thoughts guide actions toward informative observations, which in turn inform better thoughts.

### 9.3 The Variety Bottleneck

Ashby would immediately identify the **search API** as a variety bottleneck. The Wikipedia API can only retrieve the first 5 sentences of a page or find the next sentence containing a string. This is dramatically less variety than a human researcher has. The 23% "search result error" failure rate is a direct consequence of insufficient variety in the sensory channel.

Similarly, the **step limit** (7 for HotPotQA, 5 for FEVER) artificially constrains the agent's temporal variety — its ability to iterate the feedback loop enough times to converge. The paper notes that of all correct trajectories, those hitting the step limit account for only 0.84% (HotPotQA) and 1.33% (FEVER), so this is not a severe constraint in practice, but it is a variety constraint nonetheless.

### 9.4 Requisite Variety and the Combination Methods

The fact that ReAct -> CoT-SC and CoT-SC -> ReAct outperform either method alone is an Ashby-compatible result. Neither method alone has requisite variety for all disturbances:
- ReAct lacks variety against tasks where external search is unhelpful (the search API is too weak)
- CoT lacks variety against tasks requiring factual grounding (its internal knowledge is unreliable)

The combination methods implement **variety switching** — using the method whose variety best matches the current disturbance. This is a form of adaptive control.

---

## 10. Stability Analysis: Can the Loop Diverge or Oscillate?

### 10.1 Observed Instability: Repetitive Loops

Yes, the loop can become unstable. The paper explicitly documents this: "there is one frequent error pattern specific to ReAct, in which the model repetitively generates the previous thoughts and actions, and we categorize it as part of 'reasoning error' as the model fails to reason about what the proper next action to take and jump out of the loop."

This is a **limit cycle** in dynamical systems terms — the trajectory enters a periodic orbit and never converges. The agent keeps generating the same thought and taking the same action, receiving the same (unhelpful) observation, and generating the same thought again.

This accounts for a large portion of the 47% reasoning error failure rate.

### 10.2 Conditions for Divergence/Oscillation

Based on the failure analysis, the loop becomes unstable when:

1. **Search returns uninformative results.** If the observation channel provides no new information, the thought has nothing new to incorporate, and tends to repeat. The feedback loop degenerates because the error signal cannot be computed accurately from vacuous observations.

2. **The reasoning gets "locked in" to a wrong hypothesis.** If an early thought commits to a particular search strategy that does not work, subsequent thoughts may not have the flexibility to abandon it. This is a form of **structural instability** — small perturbations in the initial reasoning trace lead to qualitatively different long-term behavior.

3. **The context window fills up with repetitive content.** As the trajectory grows, the ratio of useful information to repetitive noise in the context decreases. The model's attention is increasingly spent on its own repetitions rather than the original question and useful observations.

### 10.3 Stabilization Mechanisms

The paper uses several mechanisms to prevent unbounded divergence:

1. **Step limits:** Hard caps of 7 steps (HotPotQA) and 5 steps (FEVER). This is the crudest form of stability guarantee — guaranteed termination via truncation.

2. **Fallback to CoT-SC:** When ReAct fails to converge within the step limit, the system falls back to a purely internal reasoning method. This is a **mode switch** triggered by detecting instability.

3. **The `finish` action:** The action space includes a terminal action that exits the loop. The few-shot examples demonstrate this termination pattern, and the model learns to produce it.

4. **Human-in-the-loop editing (demonstrated in Appendix A.3):** A human can inspect the reasoning trace and edit hallucinating thoughts, which immediately corrects the trajectory. This is an external stabilizer — a higher-level controller intervening when the lower-level loop becomes unstable.

### 10.4 Stability in Decision-Making Tasks

In ALFWorld, the loop is potentially more stable because:
- Thoughts appear sparsely (not every step), reducing the chance of thought-level oscillation
- The environment observations are richer and more diverse (you move to different rooms, see different objects)
- The action space has more variety (many rooms, many objects), so exact repetition of action sequences is less likely

However, ALFWorld also has a failure mode where the agent takes an action and gets "Nothing happens" — the environment rejects the action silently. Without a thought to process this, the Act-only agent repeats the action. With ReAct, the thought can recognize the failure and try something different.

### 10.5 Formal Stability Conditions (Speculative)

A sufficient condition for convergence would be: **each thought-action-observation cycle must reduce the uncertainty about the answer.** In information-theoretic terms, $H(answer | c_{t+1}) < H(answer | c_t)$ for each cycle. When this condition is violated (uninformative search, repetitive reasoning), the loop stalls or oscillates.

This is analogous to Lyapunov stability in control theory — the "uncertainty about the answer" serves as a Lyapunov function. The loop is stable if and only if this function decreases monotonically. The failure modes are exactly the cases where it does not.

---

## Summary of Key Contributions and Limitations

### Contributions
1. First general paradigm for interleaving reasoning and acting in LLMs via prompting
2. Demonstrated across four diverse benchmarks spanning knowledge reasoning and interactive decision-making
3. Showed that reasoning traces make action trajectories more interpretable and human-editable
4. Demonstrated that finetuning on ReAct trajectories produces better smaller models than finetuning on other formats
5. Identified complementarity of ReAct and CoT, proposing combination methods

### Limitations (as acknowledged by the authors)
1. Complex tasks with large action spaces require more demonstrations that may exceed input length limits
2. ReAct underperforms CoT on HotPotQA when used alone (27.4 vs. 29.4 EM) — the structural constraint of the loop reduces reasoning flexibility
3. Dependent on quality of external information source (23% of failures due to search problems)
4. Greedy decoding may be suboptimal; beam search could help
5. All prompting methods are "still significantly far from domain-specific state-of-the-art approaches" (67.5 vs. 35.1 on HotPotQA; 89.5 vs. 64.6 on FEVER)
6. Repetitive loop failure pattern has no internal recovery mechanism

### Open Questions for Cybernetics Research
- Can the stability conditions be formalized and guaranteed before execution?
- What is the minimum viable observation channel for convergence? (Ashby's requisite variety applied to the API design)
- Can the thought component learn to perform explicit error estimation, turning the implicit negative feedback into explicit error-driven control?
- How does the loop behave with unreliable environments (noisy observations, adversarial APIs)?
- Is there a principled way to determine when to think vs. when to act, rather than learning it from examples?
