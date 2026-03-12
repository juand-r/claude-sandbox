# Report: Primary Source Notes

**Scope:** 23 notes on core cybernetics texts and modern agent papers (notes/*.md, root level)

---

## What Was Read

### Cybernetics Side (10 sources)
- **Ashby** — *Introduction to Cybernetics* (1956), *Design for a Brain* (1952)
- **Beer** — VSM (*Brain of the Firm*, *Heart of Enterprise*)
- **Wiener** — *Cybernetics* (via secondary analysis)
- **Bateson** — *Steps to an Ecology of Mind*
- **Maturana & Varela** — autopoiesis
- **Powers** — Perceptual Control Theory
- **Pask** — Conversation Theory
- **Von Foerster** — second-order cybernetics, eigenforms
- **Friston** — Free Energy Principle, active inference
- **Conant & Ashby** — Good Regulator Theorem

### Agent Side (8 sources)
- **Yao et al.** — ReAct
- **Shinn et al.** — Reflexion
- **Yao et al.** — Tree of Thoughts
- **Wei et al.** — Chain of Thought
- **Schick et al.** — Toolformer
- **Wang et al.** — Agent survey (2308.11432)
- **AutoGPT** — failure analysis
- **MCP** — specification analysis

### Bridging (5 sources)
- **Control theory / RL bridge** (Lewis 2012, Bertsekas)
- **Gorelkin** — VSM for enterprise agents
- **Pihlakas** — homeostatic goals for agent safety
- **Enactivism in AI/robotics** (Froese, Di Paolo)
- **Stigmergy in multi-agent systems** (Heylighen)

---

## Key Findings Relevant to Cybernetics-Agent Bridge

### 1. The Agent Field Has No Feedback Theory

The Wang et al. survey — the most comprehensive taxonomy of LLM agents — treats feedback as an optional enhancement to planning ("planning with feedback" vs. "planning without feedback"). There is no comparator, no error signal, no stability analysis. The cybernetic analysis of this survey identified **ten implicit assumptions** in the field, including: goal-directedness is assumed not derived, feedback is optional, environments are passive, and there is no information-theoretic grounding. The field is engineering-driven, not theory-driven.

### 2. Ashby's Formalisms Are Directly Applicable

The primary sources on Ashby provide three formal tools ready for agent design:

- **Requisite variety** (H(E) >= H(D) - H(R)): A mathematical impossibility theorem. An agent cannot regulate any task whose variety exceeds its action variety. This is not empirical — it cannot be overturned by experiment.

- **Ultrastability**: A two-loop architecture where a fast inner loop handles routine regulation and a slow outer loop randomly reconfigures inner-loop parameters when essential variables leave bounds. This maps directly to agents that retry with modified strategies after failure.

- **Stability analysis**: Ashby defines stability as convergence of trajectories after displacement. Agent loops (ReAct, Reflexion) are dynamical systems whose convergence properties have never been formally analyzed.

### 3. The Good Regulator Theorem Is Weaker Than Cited

The primary analysis of Conant & Ashby (1970) reveals that the theorem proves only that optimal regulators are deterministic — a near-trivial result (Erdogan 2021). The stronger claim ("agents must contain world models") requires Richens et al. (2025), which proves it for multi-goal agents over multi-step horizons. Most agent literature cites the weaker theorem for the stronger claim.

### 4. ReAct Is a Loose Feedback Analogy

The ReAct notes show the thought-action-observation loop is structurally a feedback loop, but lacks all the formal properties that make feedback theory useful: no defined gain, no stability criterion, no transfer function. Calling it a "feedback loop" is descriptively accurate but analytically empty.

### 5. Reflexion Is Second-Order but Fatally Limited

Reflexion implements observation-of-observation (second-order cybernetics). But the evaluator shares the same LLM weights as the actor, meaning its variety for error detection cannot exceed the variety of errors the actor produces. Systematic errors are precisely those self-correction cannot detect. This is a direct prediction from Ashby's Law: a regulator (the evaluator) cannot have more variety than its channel capacity allows.

### 6. Toolformer Validates Variety Amplification

Toolformer shows a 6.7B model with 5 tools outperforming a 175B model without tools. This is the clearest empirical validation of Ashby's variety amplification: tools provide action variety the base model lacks. Critically, it works because selection accuracy is >97% with only 5 tools — the "variety illusion" (gap between nominal and effective variety) is small.

### 7. AutoGPT Is the Canonical Variety Failure

The AutoGPT failure analysis is the most detailed case study. The system had high nominal variety (many tools) but low effective variety (couldn't reliably select or parameterize them). The failure modes — infinite loops, error cascading, context exhaustion — are control instabilities: positive feedback, insufficient damping, unbounded delay. Nobody did the variety calculation before deployment; even a rough estimate would have predicted failure.

### 8. Homeostatic Goals Are the Most Promising Safety Contribution

Pihlakas' homeostatic goal framework replaces unbounded maximization with bounded setpoint goals. Properties: bounded behavior, settle-to-rest, natural corrigibility, multi-objective conjunctive structure. This is Ashby's homeostasis formalized in an MDP framework. It addresses the alignment problem structurally rather than through patches.

### 9. The MCP Specification Is Variety Engineering

The MCP analysis shows tool use protocols as variety engineering: schema constraints are per-tool variety attenuators, discovery mechanisms are variety filters, permissions are variety bounds. The two-stage attenuation pattern (host selects relevant servers, then LLM selects specific tool) is more efficient than single-stage.

### 10. Beer's VSM Is the Strongest Organizational Framework

The VSM provides the most concrete architectural guidance: five necessary subsystems, seven communication channels, recursive structure. The notes identify that current agent frameworks implement S1 (operations) and S3 (control) but systematically lack S2 (coordination), S3* (audit), S4 (intelligence), and algedonic channels.

---

## Assessment

The primary sources establish that cybernetics provides formal tools the agent field lacks (variety calculus, stability analysis, feedback theory) and that agent failures are predictable from cybernetic principles. The strongest contributions are quantitative (Ashby's variety, stability) rather than qualitative (autopoiesis, second-order cybernetics). The weakest links are where cybernetic concepts lack operational specificity — Beer's VSM says *what* subsystems are needed but not *how* to build them for LLM agents.
