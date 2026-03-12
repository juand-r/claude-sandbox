# Tree of Thoughts: Deliberate Problem Solving with Large Language Models

**Paper**: Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T.L., Cao, Y., & Narasimhan, K. (2023). arXiv:2305.10601. NeurIPS 2023.

**Date of notes**: 2026-03-12

---

## 1. Formal Framework: How ToT Generalizes CoT

### Core Idea

ToT reframes LLM inference as **search through a combinatorial problem space represented as a tree**. Each node is a partial solution state; each edge is a "thought" (a coherent language sequence serving as an intermediate reasoning step).

### Formal Notation

- **Language model**: p_theta(x) = prod_i p_theta(x[i] | x[1...i]) (standard autoregressive)
- **State**: s = [x, z_1 ... z_i] — the input x plus the sequence of thoughts generated so far
- **Thought**: z_i is a coherent language sequence (not a single token, not an entire solution — something in between)

The key insight: standard IO prompting generates the full answer in one pass; CoT generates a single chain z_1, z_2, ..., z_n sequentially; ToT generates a **tree** where each state can branch into multiple candidate thoughts.

### Generalization Hierarchy

```
IO prompting  ⊂  CoT  ⊂  CoT-SC (self-consistency)  ⊂  ToT
```

- IO: one pass, no intermediate thoughts
- CoT: one chain of thoughts, left-to-right
- CoT-SC: multiple independent chains, majority vote at the end
- ToT: tree of thoughts with evaluation and search at each step

This is a genuine generalization. CoT is the special case where the tree has branching factor 1 and no evaluation/backtracking.

### The Four Key Questions

Any ToT instantiation must answer:

1. **How to decompose the problem into thoughts?** What granularity? A thought must be small enough for the LM to generate diverse candidates, yet large enough for the LM to evaluate its promise.
2. **How to generate candidate thoughts?** G(p_theta, s, k) — generate k candidates. Two strategies:
   - *Sample*: draw i.i.d. from CoT prompt (good when thought space is rich, e.g., creative writing)
   - *Propose*: sequentially generate distinct thoughts using a "propose prompt" (good when thought space is constrained, e.g., Game of 24)
3. **How to evaluate states?** V(p_theta, S) — heuristic evaluation of how promising a state is. Two strategies:
   - *Value*: independently score each state (e.g., "sure/likely/impossible" or 1-10 scale)
   - *Vote*: compare multiple states and vote for the most promising
4. **What search algorithm to use?** BFS or DFS (see Section 2 below).

---

## 2. Search Algorithms: BFS vs DFS

### BFS (Algorithm 1)

Maintains a frontier of the **b most promising states** at each depth level, across T total steps.

```
for t = 1 to T:
    Generate candidates: S_t' = {[s, z] | s in S_{t-1}, z in G(p_theta, s, k)}
    Evaluate: V_t = V(p_theta, S_t')
    Keep top b: S_t = argmax_{|S|=b} sum of values
```

Parameters: b (beam width), k (candidates per state), T (depth).

**When appropriate**: Problems with bounded depth where you want to maintain diversity across multiple promising paths. Used for Game of 24 (T=3 steps, b=5 beams) and Creative Writing (T=2 steps, b=5).

### DFS (Algorithm 2)

Recursively explores the most promising branch first, with **pruning** based on a value threshold v_th.

```
function DFS(s, t):
    if t > T: record output, return
    for each s' in G(p_theta, s, k):
        if V(p_theta, {s'})(s') > v_th:
            DFS(s', t+1)
        # else: prune this branch (backtrack)
```

**When appropriate**: Problems with deep search trees where backtracking is natural. Used for Mini Crosswords (10 clues = depth 10). DFS is more memory-efficient and suited to problems where early mistakes can be cheaply detected and abandoned.

### Neither algorithm is novel. What is novel is using the LM itself as both the generator and the heuristic evaluator within these classical algorithms.

---

## 3. Self-Evaluation: How the LLM Evaluates Intermediate States

### Value-Based Evaluation

The LM is prompted to reason about a state and produce either:
- A **scalar value** (1-10)
- A **classification** (e.g., "sure / likely / impossible")

For Game of 24: the evaluator checks whether remaining numbers can plausibly reach 24. The prompt asks the LM to assess feasibility — a form of **lookahead simulation**. The LM reasons: "Given these remaining numbers and operations, can I reach 24?"

For Mini Crosswords: the evaluator checks letter-level constraints — do proposed words conflict with each other?

### Vote-Based Evaluation

The LM is shown multiple candidate states simultaneously and asked to vote for the most promising one. Used for Creative Writing where absolute scoring is harder than comparative judgment.

### Key Properties of Self-Evaluation

- Evaluations **do not need to be perfect** — they only need to be approximately useful for guiding search. This is analogous to heuristic functions in A* search.
- The same LM serves as both generator and evaluator. This is both a strength (no external model needed) and a limitation (evaluation quality bounded by the model's capabilities).
- The paper does not provide verbatim evaluation prompts in the main text (they are in the appendix/code), but describes the general format.

### Evidence that Evaluation Matters

Ablation on Game of 24 comparing generation vs evaluation quality:
- GPT-4 generation + GPT-4 evaluation: 74%
- GPT-4 generation + GPT-3.5 evaluation: 64%
- GPT-3.5 generation + GPT-4 evaluation: 31%
- GPT-3.5 generation + GPT-3.5 evaluation: 19%

**Conclusion**: Generation capability is the bottleneck, not evaluation. A weaker evaluator with a strong generator still works reasonably well, but a strong evaluator cannot compensate for a weak generator.

---

## 4. Experimental Results

### Game of 24

Task: Given four numbers, use +, -, *, / to reach exactly 24. 100 hard puzzles from a dataset.

| Method | Success Rate |
|--------|-------------|
| IO prompting | 7.3% |
| CoT | 4.0% |
| CoT-SC (best of 100) | 9.0% |
| ToT (b=1) | 45% |
| ToT (b=5) | 74% |

The jump from 4% to 74% is striking. Error analysis: ~60% of CoT samples made an error at the very first step, and left-to-right generation cannot recover.

Thought decomposition: 3 intermediate equations (e.g., "13 - 9 = 4 (left: 4, 4, 10)").

### Creative Writing

Task: Write a coherent 4-paragraph passage where each paragraph ends with one of 4 given random sentences. 100 tasks.

| Method | Coherency (GPT-4 scored, 1-10) |
|--------|-------------------------------|
| IO | 6.19 |
| CoT | 6.93 |
| ToT | 7.56 |

Human evaluation: ToT preferred over CoT in 41/100 comparisons; CoT preferred in only 21/100.

Thought decomposition: A writing plan/outline first, then the full passage. BFS with voting for best plan.

### Mini Crosswords (5x5)

20 test games.

| Method | Letter Accuracy | Word Accuracy | Games Solved |
|--------|----------------|---------------|-------------|
| IO | 38.7% | 14% | 0 |
| CoT | 40.6% | 15.6% | 1 |
| ToT | 78% | 60% | 4 |
| ToT (no pruning) | 65.4% | 41.5% | 5 |
| ToT (no backtracking) | 54.6% | 20% | 5 |
| Oracle best state | 82.4% | — | 7 |

Thought decomposition: individual word fills. DFS with backtracking when constraints are violated.

### Marginal Tasks (Zero-Shot ToT)

On tasks where GPT-4 is already strong:
- GSM8K: CoT 86% -> ToT 90%
- StrategyQA: CoT 82% -> ToT 83%

ToT shows diminishing returns when the base model already handles the task well. The benefit is concentrated on **hard problems where left-to-right generation systematically fails**.

---

## 5. Cost Analysis

| Task | Method | Cost/Case | Success |
|------|--------|-----------|---------|
| Game of 24 | IO (best of 100) | $0.13 | 33% |
| Game of 24 | CoT (best of 100) | $0.47 | 49% |
| Game of 24 | ToT (b=5) | $0.74 | 74% |
| Creative Writing | IO | $0.06 | — |
| Creative Writing | CoT | $0.07 | — |
| Creative Writing | ToT | $0.32 | — |

ToT uses roughly **5-100x more tokens** than standard prompting, depending on the task. For Creative Writing, ~5x. For Game of 24, the cost is ~5.7x CoT-best-of-100 but with much higher success.

Mini Crosswords: total experiment cost stayed within ~$100.

**The cost-performance tradeoff is favorable**: for Game of 24, ToT at $0.74/case achieves 74% vs CoT-best-of-100 at $0.47/case achieving only 49%. You pay ~57% more for a 51% absolute improvement.

---

## 6. Dual-Process Theory Connection (Kahneman System 1 / System 2)

The paper uses dual-process theory as **motivational analogy, not formal justification**.

Their claim: standard LLM token-level generation resembles System 1 (fast, automatic, associative). ToT augments this with deliberate search resembling System 2 (slow, effortful, planful).

### Assessment: Is This Formally Justified?

**No.** The connection is purely rhetorical. Several issues:

1. **System 1/System 2 is itself contested** in cognitive science. It is a useful heuristic, not a precise computational theory.
2. **No formal mapping** is provided between ToT operations and System 2 processes. The paper does not formalize what "deliberate" means computationally beyond "search."
3. **The real contribution is algorithmic**, not theoretical. ToT is tree search with LM-generated heuristics. The cognitive science framing adds narrative but no predictive power.
4. **More precise framing**: ToT is best understood as classical heuristic search (GBFS, beam search, DFS with pruning) where the LM serves dual roles as both the successor function and the heuristic function. This is a clean computational description that does not require appeal to cognitive science.

The dual-process framing is effective for communication but should not be mistaken for a theoretical foundation.

---

## 7. Backtracking: When and How

Backtracking occurs **only in DFS mode**. The mechanism:

1. At each node, generate k candidate thoughts.
2. Evaluate each candidate using the LM evaluator.
3. If V(p_theta, {s'}) > v_th (value threshold), recursively explore that branch.
4. If V(p_theta, {s'}) <= v_th, **prune**: do not explore, move to the next candidate.
5. If **all k candidates at a node are pruned**, backtrack to the parent node and try its next candidate.

The threshold v_th is a hyperparameter. The paper does not describe a principled method for setting it. For Mini Crosswords, the evaluation uses constraint checking (do letters conflict?), which provides a natural pruning signal.

**BFS does not backtrack.** It simply keeps the top-b states at each level and discards the rest. This is beam search, which is a form of irrevocable pruning — abandoned states cannot be revisited.

### Ablation Evidence

On Mini Crosswords, removing backtracking dropped word accuracy from 60% to 20%, demonstrating its critical importance for constraint-satisfaction problems.

---

## 8. Cybernetic Analysis

### 8a. ToT as Variety Amplification (Ashby)

Ashby's Law of Requisite Variety: a controller must have at least as much variety as the disturbances it must regulate. Standard CoT has **minimal variety** — it generates a single chain of reasoning. Even CoT-SC (self-consistency) generates independent chains with no interaction or adaptation between them.

ToT amplifies variety in two ways:
1. **Branching**: at each step, k candidates are generated, creating k^T possible paths through a tree of depth T. This is exponential variety amplification.
2. **Selective retention**: evaluation and pruning act as a **variety filter**, channeling variety toward promising regions. This is not random amplification but *directed* amplification.

The combination — generate many, evaluate, keep the best — is precisely the **generate-and-test** paradigm that Ashby identified as fundamental to adaptive systems. ToT implements this at the level of reasoning steps rather than complete solutions.

**Contrast with CoT-SC**: Self-consistency generates variety at the trajectory level (sample 100 complete chains) but has no mechanism to redirect effort based on intermediate feedback. ToT generates variety at each step and uses feedback to prune. This is a more efficient use of variety — Ashby would recognize this as a requisite variety amplifier with feedback, not just a random variety generator.

### 8b. Self-Evaluation as Feedback

Each evaluation step V(p_theta, S) functions as a **feedback signal** in the cybernetic sense:

- The evaluator compares the current state to the goal (implicitly encoded in the prompt)
- It produces an error signal: "sure" (on track), "likely" (uncertain), "impossible" (off track)
- The search algorithm uses this signal to adjust behavior: continue, explore alternatives, or backtrack

This is a negative feedback loop: deviations from the goal (bad intermediate states) are detected and corrected through branch switching. The key difference from classical control theory: the "sensor" and "actuator" are the same entity (the LM), and the feedback signal is linguistic rather than numeric.

**Limitation as feedback**: The evaluation is **open-loop within each branch**. The LM evaluator does not have access to the history of failed branches when evaluating a new one. There is no learning or adaptation across the search — each evaluation is stateless. A true cybernetic controller would update its model based on feedback history.

### 8c. Exploration/Exploitation Tradeoff and Ultrastability

Ashby's ultrastability: when a system's essential variables exceed safe limits, the system randomly reconfigures its parameters until stability is restored. This is exploration triggered by failure.

**Does ToT implement this?**

Partially. DFS with backtracking has an ultrastability-like property: when the current path fails (evaluation below threshold), the system abandons it and tries an alternative. However:

1. **The exploration is not random.** Alternatives are generated by the LM and ranked by the evaluator. This is more like directed search than random reconfiguration.
2. **There is no escalation.** In Ashby's model, if low-level adjustments fail, the system escalates to higher-level reconfiguration. ToT has a fixed search structure — it cannot change its decomposition, generation strategy, or evaluation criteria during search.
3. **The "essential variables" are implicit.** In Ashby, essential variables (survival conditions) are explicit. In ToT, the goal is implicit in the task prompt. The evaluator approximates whether essential variables are satisfied, but this approximation can be wrong.

**Verdict**: ToT implements a weak form of ultrastability — failure-triggered exploration — but lacks the hierarchical adaptation and random reconfiguration that characterize full Ashbian ultrastability. It is closer to classical heuristic search with backtracking than to genuine ultrastable regulation.

### 8d. Stability / Convergence Analysis

**Does the tree search converge?**

In the formal sense, yes: BFS terminates after T steps with b final states; DFS terminates when all branches are explored or pruned. Both have finite runtime bounded by k^T (number of possible paths).

But "convergence" in the cybernetic sense — does the system reliably reach the goal? — is not guaranteed. The paper's results show:

- Game of 24: 74% success means 26% failure even with ToT. The search does not always find a solution.
- Mini Crosswords: only 4/20 games fully solved. The oracle (best state across all explored nodes) solved 7/20, meaning the evaluator failed to identify the best path in 3 cases.

**Conditions for convergence** (informal analysis):
1. The thought decomposition must be appropriate — too fine-grained wastes computation, too coarse-grained prevents meaningful evaluation.
2. The evaluator must be better than random — it must correlate with actual solution quality. If the evaluator is anti-correlated, search will systematically move toward bad states.
3. The branching factor and depth must be manageable — k^T must be searchable within budget.
4. The problem must be decomposable — ToT assumes that intermediate states can be meaningfully evaluated. Problems where quality is only apparent in the final solution (holistic evaluation) are poorly suited.

**Feedback stability**: The system lacks the stabilizing mechanisms of classical control (integral terms, damping). The evaluator can oscillate — rating a state highly at one step and poorly at the next — with no mechanism to smooth these fluctuations. This is why the results are probabilistic rather than guaranteed.

---

## 9. Comparison to Classical AI Planning

### What is genuinely new?

**Not new:**
- Tree search (BFS, DFS): textbook algorithms since the 1960s
- Heuristic evaluation of states: core of A* (Hart, Nilsson, Raphael, 1968)
- Generate-and-test: foundational AI paradigm
- Backtracking with pruning: standard constraint satisfaction technique
- Beam search: used in NLP for decades

**Genuinely new:**
1. **The LM as a universal heuristic function.** In STRIPS/PDDL planning, heuristics are hand-crafted (delete relaxation, landmark counting) or learned from training data specific to a domain. ToT uses the LM's pretrained knowledge as a general-purpose heuristic. No domain-specific engineering is needed.
2. **The LM as a universal successor function.** In classical planning, the action space is formally defined. In ToT, the LM generates candidate next steps in natural language, defining the action space implicitly through its training distribution.
3. **Natural language as the state representation.** Classical planning uses structured state representations (sets of predicates in STRIPS, multi-valued variables in SAS+). ToT represents states as strings. This is less formal but far more flexible.

### Limitations vs Classical Planning

1. **No formal guarantees.** STRIPS/PDDL planners can prove completeness and optimality under well-defined conditions. ToT offers no such guarantees because both generation and evaluation are stochastic and approximate.
2. **No explicit world model.** Classical planners maintain a formal model of preconditions and effects. The LM's "world model" is implicit in its parameters — you cannot inspect, verify, or correct it.
3. **No admissible heuristic.** A* with an admissible heuristic guarantees optimality. The LM evaluator has no admissibility guarantee, so ToT cannot guarantee finding the best solution.
4. **Computational cost.** Each "node expansion" in ToT requires an LM forward pass (expensive). Classical planners can expand millions of nodes per second.

### The Real Contribution

ToT demonstrates that **LLMs can serve as both the domain theory and the heuristic function** for search, eliminating the need for formal domain modeling. This trades formal guarantees for generality. It is a form of **approximate planning in implicit domain models**, which is genuinely new as a practical technique even if the search algorithms are classical.

---

## 10. Limitations and Failure Modes

### Acknowledged by the Authors

1. **Computational cost**: 5-100x more tokens than standard prompting. For routine tasks where CoT works, this is wasteful.
2. **Diminishing returns on easy tasks**: GSM8K improved only 4% (86->90%). ToT is most valuable when standard inference systematically fails.
3. **No learning**: ToT does not improve the base model. Each problem is solved from scratch. The authors suggest fine-tuning on ToT traces as future work.
4. **Fixed search structure**: The decomposition, generation, and evaluation strategies are hand-designed per task. There is no automatic adaptation.

### Not Acknowledged (My Analysis)

5. **Evaluator correlation with solution quality is assumed, not verified.** If the LM systematically misjudges intermediate states (e.g., confidently rating a wrong step as "sure"), ToT will confidently pursue wrong paths. The paper shows this happens: oracle accuracy exceeds ToT accuracy on crosswords, meaning the evaluator sometimes rejects good branches.
6. **No mechanism for meta-level reasoning.** The system cannot recognize when it is stuck in a systematically wrong region of the search space and needs to change strategy (e.g., try a different decomposition). This is a single-loop controller, not a double-loop learner.
7. **Prompt sensitivity.** The evaluation prompts are hand-crafted and their quality directly determines search effectiveness. Small changes in prompt wording could significantly affect results. This fragility is not analyzed.
8. **Assumes decomposability.** Problems that are not naturally decomposable into evaluable intermediate states are poor fits. Many real-world reasoning problems have this property — you cannot tell if you are on the right track until the end.
9. **Scaling.** The paper tests on small problems (4 numbers, 5x5 crosswords, 4-paragraph essays). It is unclear how ToT scales to problems requiring hundreds or thousands of reasoning steps. The exponential branching (k^T) becomes prohibitive.
10. **Self-evaluation circularity.** The same model that generates potentially wrong reasoning is asked to evaluate that reasoning. If the model has a systematic blind spot (e.g., consistently makes a particular arithmetic error), the evaluator will share that blind spot. There is no independent verification.

---

## Summary Assessment

ToT is a clean, well-executed paper that applies classical search algorithms to LLM inference. Its main contribution is demonstrating that LLMs can serve as both generator and evaluator in tree search, eliminating the need for domain-specific heuristic engineering. The results on hard problems (Game of 24: 4% -> 74%) are compelling.

From a cybernetic perspective, ToT implements a generate-evaluate-select loop with rudimentary feedback (backtracking on failure), but lacks the adaptive, self-modifying properties of truly cybernetic systems. It is a single-level controller that cannot modify its own control strategy. The variety amplification is real but directed rather than random, and the feedback is stateless rather than cumulative.

The dual-process framing is marketing, not theory. The real theoretical connection is to classical AI search with learned heuristics, which is a well-established research direction. What ToT adds is the practical demonstration that modern LLMs are good enough to serve as general-purpose heuristics for diverse reasoning tasks.

**Key open question**: Can ToT-style search be made adaptive — learning from failed searches to improve future ones? The authors gesture toward this with "fine-tuning on ToT traces" but do not pursue it. This is where the cybernetic perspective becomes genuinely productive: what would a double-loop ToT look like, where the system modifies its decomposition, generation, and evaluation strategies based on accumulated experience?
