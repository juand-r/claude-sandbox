# Deep Research Plan v2: Cybernetics as a Framework for Understanding and Designing AI Agents

## Why v2

The first pass was superficial — survey-level summaries from secondary sources. This round goes to primary sources: downloading and reading actual papers, taking detailed notes, extracting specific concepts, theorems, and formalisms that can serve as analytical tools for understanding modern agent design.

## Core Research Questions

1. **Can cybernetic principles serve as a unifying framework for understanding the space of AI agent designs?** (Not just "there are parallels" — can we actually use cybernetics to organize, classify, and evaluate agent architectures?)

2. **Have we been reinventing cybernetics?** (Specific, detailed comparisons: what exactly did cybernetics formalize that modern agent research rediscovers? With proofs, formalisms, not just analogies.)

3. **What does cybernetics reveal about shortcomings of current agent designs?** (Not vague "they should think more systemically" — concrete predictions about failure modes, design gaps, missing capabilities.)

4. **Can cybernetic formalisms (Ashby's variety calculus, the Good Regulator Theorem, VSM, ultrastability) be operationalized for agent design?** (Equations, architectures, design patterns — not just metaphors.)

## Research Streams (Deep Dive)

### A. Primary Cybernetics Sources (download, read, take notes)

1. **Ashby - An Introduction to Cybernetics (1956)** — The full text. Focus on: variety calculus, Law of Requisite Variety (the actual proof), regulation as information-theoretic constraint, the black box method, stability analysis. Available free online.

2. **Ashby - Design for a Brain (1952)** — Ultrastability formalism, homeostat details, multistable systems, adaptation through random search. Available free online.

3. **Conant & Ashby - "Every Good Regulator of a System Must Be a Model of That System" (1970)** — The actual theorem and proof. What does "model" formally mean here? What are the assumptions?

4. **Wiener - Cybernetics (1948)** — MIT Press open access. Focus on: formal feedback theory, information-entropy connection, the stochastic process framework.

5. **Beer - Brain of the Firm (1972) / Heart of Enterprise (1979)** — VSM in detail. The five systems, recursion, variety engineering. How it actually works, not just the diagram.

6. **Von Foerster - key papers** — Eigenforms, second-order cybernetics, the observer. Specifically: "On Self-Organizing Systems and Their Environments" (1960), "Objects: Tokens for (Eigen-)Behaviors" (1976).

7. **Maturana & Varela - Autopoiesis and Cognition (1980)** — The formal definition of autopoiesis. Operational closure vs. thermodynamic openness.

8. **Bateson - Steps to an Ecology of Mind (1972)** — Specifically: "Cybernetic Explanation" (essay), levels of learning, double bind theory as cybernetic analysis.

9. **Pask - Conversation Theory** — The formalism, not just the description. L_p and L_o languages, entailment structures.

10. **Powers - Behavior: The Control of Perception (1973)** — PCT hierarchy, perceptual control vs. output control.

### B. Modern Agent Papers (download, read, take detailed notes)

11. **Yao et al. - ReAct (2022)** — The actual paper, not summaries. Loop structure, failure modes, comparison methodology.

12. **Shinn et al. - Reflexion (2023)** — Self-correction formalism. What exactly is the "verbal reinforcement" mechanism?

13. **Wang et al. - Survey on LLM-based Autonomous Agents (2308.11432)** — The taxonomy. How does it compare to cybernetic taxonomies?

14. **Wei et al. - Chain of Thought (2022)** — What is CoT actually doing in information-theoretic terms?

15. **Yao et al. - Tree of Thoughts (2023)** — The search formalism. Connection to cybernetic exploration/exploitation.

16. **AutoGPT architecture analysis** — What specifically failed and why? Can cybernetics explain the failure modes?

17. **Anthropic MCP specification** — Tool use as variety amplification.

18. **Schick et al. - Toolformer (2023)** — Self-supervised tool learning.

### C. Bridging & Theoretical Papers

19. **Conant-Ashby theorem extensions** — Richens et al. 2025, Erdogan 2021 reinterpretation. What does "model" mean in different contexts?

20. **Friston - Free Energy Principle papers** — The actual math. Active inference as agent architecture.

21. **Control theory / RL connections** — Lewis (2012), Bertsekas. Formal parallels.

22. **Gorelkin (2025) - VSM for enterprise agentic systems** — How exactly does VSM map?

23. **Pihlakas - Homeostatic goal structures** — Formal proposal for bounded goals.

24. **Enactivism in AI/robotics** — Specific implementations, not just philosophy.

25. **Stigmergy in multi-agent systems** — Heylighen (2015), formal models.

### D. Secondary Sources (books, papers, reports, conference proceedings)

Search for and read secondary sources that provide substantive analysis (not Wikipedia-level):
- Recent books on cybernetics and AI/agent design
- Conference proceedings (AAAI, NeurIPS, ICML, AAMAS, etc.) on agent architectures
- Technical reports from AI labs on agent failure modes and design patterns
- Academic survey papers beyond Wang et al.
- Books/chapters on systems theory applied to AI

### E. Citation Chasing (recursive depth)

For each paper/book already read in notes/:
- Identify the 2-3 most important/salient references cited
- Download and read those cited papers
- Take notes on them
- Agents doing this work should launch their own sub-agents to follow the most promising citation threads deeper (sub-sub-agents)
- Goal: build a citation graph of the most important ideas, not just a flat list

### F. Question-Driven Research

Read the existing reports (report-1, report-2, report-3, SYNTHESIS.md) and generate hard, substantive questions:
- What claims are unsupported or weakly supported?
- What connections are asserted but not demonstrated?
- What counter-arguments exist?
- What's missing entirely?

Then launch sub-agents to search the literature to answer those questions. Results go in `notes/questions/`.

### G. Analysis & Synthesis

26. Build a formal concept mapping: cybernetic formalism → agent design pattern → specific papers on each side

27. Analyze ReAct/Reflexion/ToT as cybernetic feedback systems (gain, delay, stability)

28. Apply Ashby's variety calculus to tool use and agent capability

29. Map VSM onto existing multi-agent frameworks (CrewAI, LangGraph, AutoGen)

30. Identify concrete predictions: what does cybernetics predict about agent failure modes that we observe?

## Research Methodology

- **Download everything**: All papers and books (where possible) should be downloaded so agents can read the actual text, not summaries
- **Recursive agents**: Agents should launch sub-agents for citation chasing and question answering
- **Secondary sources welcome**: Books, reports, conference proceedings — anything with more substance than Wikipedia
- **Notes on everything**: Every source read gets a note in `notes/`

## Output

- `notes/` directory: detailed notes on each paper/source read
- `notes/citations/` directory: notes on papers found via citation chasing
- `notes/questions/` directory: questions generated from reports + answers found
- `notes/secondary/` directory: notes on secondary sources
- Revised, deeper reports replacing the v1 reports
- A final synthesis that is genuinely analytical, not just descriptive

## Status

- [x] Stream A: Primary cybernetics sources (notes complete for items 1-10)
- [x] Stream B: Modern agent papers (notes complete for items 11-18)
- [x] Stream C: Bridging papers (notes complete for items 19-25)
- [x] Stream D: Secondary sources (50+ sources in notes/secondary/; includes 2000-2010 bridging works: Pfeifer/Bongard 2006 embodied intelligence, Thompson 2007 enactivism, Pickering 2010 British cybernetics history, Di Paolo 2005 adaptivity deep dive, Froese/Ziemke 2009 enactive AI, Heylighen/Joslyn 2001 cybernetics encyclopedia, Seth 2007 consciousness models, Barandiaran/Moreno 2006 minimally cognitive organization, Boden 2006 cognitive science history, Wooldridge 2002 + Wooldridge/Jennings 1995 agent theory, Ferber 1999 MAS textbook, Weiss 1999 DAI textbook; plus earlier 1990s bridging works and 2007-2017 works)
- [x] Stream E: Citation chasing (27+ papers in notes/citations/ across both cybernetics and agent lineages)
- [x] Stream F: Question-driven research (32 questions generated, 8 answered in notes/questions/)
- [ ] Stream G: Analysis & synthesis
