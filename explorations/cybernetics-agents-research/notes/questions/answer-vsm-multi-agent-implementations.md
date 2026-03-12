# Answer: Has Anyone Actually Built a VSM-Based Multi-Agent System?

**Question**: The reports propose VSM as a blueprint for multi-agent AI. Do any implementations exist? How do they compare to standard approaches?

---

## Finding: Implementations Are Emerging, But No Rigorous Comparisons Exist

### What Exists

1. **VSM-Based Multi-Agent Code Review (Hurrell, March 2025)**: The most concrete implementation found. Eoin Hurrell built a multi-agent code review system explicitly structured according to VSM:
   - System 1: Multiple specialized reviewers examining different aspects of code
   - System 2: Prevention of contradictory or redundant feedback between reviewers
   - System 3: Prioritization of feedback based on importance and impact
   - System 4: Identification of patterns across multiple PRs for deeper improvements
   - System 5: Alignment of all feedback with project standards and priorities

   He notes that "VSM's inherent focus on autonomy and recursion makes it particularly valuable for multi-agent systems" and that the fractal structure "balances local autonomy with global coherence."

2. **Gorelkin (2025)**: Theoretical mapping of VSM onto enterprise agentic systems (referenced in the reports). This is a Medium article proposing the architecture, not an implementation with measurable results.

3. **VSM + AI Governance (MDPI Systems, 2025)**: Academic paper using VSM and Perez Rios's Taxonomy of Organizational Pathologies to develop strategies for "responsible innovation and governance in AI." This is about governing AI systems, not about building AI systems with VSM architecture.

4. **viable-systems.github.io**: Documentation mapping VSM to modern software architecture concepts, noting that "microservices mirror VSM's modular structure" and "event-driven architecture matches VSM's communication patterns."

5. **VSMod**: Software tool for organizational VSM diagnosis and design, developed for human organizations rather than AI agent systems.

### What Does Not Exist

- **No rigorous comparison** of a VSM-structured multi-agent system against LangGraph, CrewAI, AutoGen, or any other standard framework on any benchmark.
- **No quantitative evaluation** showing that VSM-structured agents perform better (or worse) on tasks like SWE-bench, WebArena, or other agent benchmarks.
- **No analysis of cost, latency, or failure mode differences** between VSM-structured and flat/graph-structured multi-agent systems.
- **No production deployment** of a VSM-based multi-agent system at enterprise scale.

### What Can Be Inferred

The VSM offers several potential advantages that have not been empirically tested:

1. **Explicit coordination layer (S2)**: Most multi-agent frameworks handle coordination implicitly through message passing. VSM's S2 provides an explicit mechanism for conflict prevention, which could reduce the well-documented problem of agents generating contradictory outputs.

2. **Separation of operational and strategic concerns (S1 vs S4)**: This could reduce cost by using cheaper models for operational tasks and expensive models only for strategic reasoning -- the "tiered intelligence" approach.

3. **Recursion**: VSM's recursive structure could naturally handle the "agents calling agents" pattern that frameworks like LangGraph support but don't architecturally enforce.

4. **System 3* (audit channel)**: Direct monitoring of operations bypassing normal channels could provide better observability for detecting agent failures.

### Why Comparisons Don't Exist Yet

1. The overlap community (people who know both VSM and LLM agent architectures) is tiny.
2. Building a proper VSM-structured multi-agent system requires significant architectural effort beyond what current frameworks provide.
3. The agent benchmarks community focuses on single-agent or simple multi-agent scenarios, not on organizational architecture of agent swarms.
4. VSM is fundamentally about organizational viability, not task performance. The benefits would show up in long-running, evolving systems, not in one-shot benchmark tasks.

### Assessment

The synthesis's recommendation of VSM for multi-agent systems is **theoretically well-motivated but empirically unvalidated**. Hurrell's code review system is the only known implementation, and it provides qualitative observations rather than quantitative comparisons.

The strongest version of the VSM argument is probably not "VSM will produce higher benchmark scores" but rather "VSM will produce more robust, maintainable, and observable multi-agent systems." This is a systems engineering claim, not a performance claim, and would require different evaluation criteria than standard benchmarks provide.

The most valuable next step would be a controlled experiment: implement the same multi-agent task (e.g., code review, report generation) using both a VSM-structured architecture and a standard LangGraph/CrewAI architecture, and compare on dimensions including task quality, cost, failure recovery, and maintainability.

## Sources

- Hurrell, E. (2025). "Building a Multi-Agent Code Review System Using the Viable System Model." [Blog](https://www.eoinhurrell.com/posts/20250306-viable-systems-ai/)
- VSM and AI Organizational Pathologies (2025). *MDPI Systems*. [MDPI](https://www.mdpi.com/2079-8954/13/9/749)
- Viable Systems Model Documentation. [GitHub](https://viable-systems.github.io/vsm-docs/overview/what-is-vsm/)
- "Viable system model." [Wikipedia](https://en.wikipedia.org/wiki/Viable_system_model)
- Gorelkin, M. (2025). "Stafford Beer's Viable System Model for Building Enterprise Agentic Systems." Medium.
