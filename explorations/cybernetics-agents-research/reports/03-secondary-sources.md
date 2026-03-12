# Report: Secondary Sources

**Scope:** 44 books and papers providing intellectual context (notes/secondary/)

---

## What Was Read

The secondary sources span four intellectual traditions:

### Embodied/Situated AI (1987–2006) — 12 sources
- Brooks (1991) — Intelligence without representation, subsumption architecture
- Maes (1991) — Designing autonomous agents
- Steels (1993) — ALife roots of AI
- Agre & Chapman (1990) — What are plans for?
- Beer (1990) — Intelligence as adaptive behavior
- Suchman (1987) — Plans and situated actions
- Port & Van Gelder (1995) — Mind as Motion (dynamical systems)
- Clark (1997) — Being There
- Pfeifer & Scheier (1999) — Understanding Intelligence
- Pfeifer & Bongard (2006) — How the Body Shapes the Way We Think
- Holland (1995) — Hidden Order (complex adaptive systems)
- Kauffman (1993, 1995) — Origins of Order, At Home in the Universe

### Enactivism/Autopoiesis (2005–2017) — 10 sources
- Thompson (2007) — Mind in Life
- Froese & Ziemke (2009) — Enactive AI
- Froese (2012) — From second-order cybernetics to enactive cognitive science
- Di Paolo (2005) — Adaptivity deep dive
- Barandiaran & Moreno (2006) — Minimally cognitive dynamical systems
- Barandiaran, Di Paolo & Rohde (2009) — Defining agency
- De Jaegher & Di Paolo (2007) — Participatory sense-making
- Gallagher (2017) — Enactivist interventions
- Seth (2007, 2013) — Models of consciousness, interoceptive inference
- Dreyfus (2007) — Why Heideggerian AI failed

### Multi-Agent Systems Theory (1995–2009) — 6 sources
- Wooldridge (2002) — Multiagent systems textbook
- Wooldridge & Jennings (1995) — Intelligent agents
- Ferber (1999) — Multi-agent systems textbook
- Weiss (1999) — Multiagent systems: modern approach
- Shoham & Leyton-Brown (2009) — MAS game-theoretic
- Russell & Norvig (2010) — AIMA agent architectures
- Bonabeau, Dorigo & Theraulaz (1999) — Swarm intelligence

### History/Philosophy (2006–2017) — 6 sources
- Pickering (2010) — The Cybernetic Brain (history of British cybernetics)
- Boden (2006) — Mind as Machine (history of cognitive science)
- Heylighen & Joslyn (2001) — Cybernetics encyclopedia entry
- Floridi (2013) — Ethics of Information
- Dennett (2017) — From Bacteria to Bach
- Muller & Bostrom (2016) — Future Progress in AI

### Other
- Clark (2013) — Whatever Next? (predictive processing)
- Dorigo & Birattari (2010) — Swarm intelligence
- Steels (2012) — Self-organization in cultural language

---

## Key Findings

### 1. The 1990s Embodied AI Movement Already Made the Cybernetic Critique

Brooks (1991), Maes (1991), Steels (1993), and Beer (1990) all argued — 30 years ago — that classical AI's reliance on internal representations, explicit planning, and centralized control was fundamentally misguided. Their alternative: agents situated in environments, using feedback loops rather than plans, with behavior emerging from environment-agent coupling rather than internal computation.

The LLM agent community has largely not engaged with this critique. The Wang et al. agent survey's architecture (Profile → Memory → Planning → Action) is exactly the classical architecture that the situated AI movement rejected. The embodied AI critique predicts that this architecture will fail in open-ended, dynamic environments — and it does (AutoGPT).

**Relevance today:** The situated AI critique does not mean LLM agents are doomed. It means the architectural assumptions need updating. Specifically: feedback should be a first-class primitive, not an optional add-on; the environment should be treated as a co-determining partner, not a passive backdrop; and planning should be reactive and situated, not ballistic.

### 2. Enactivism Sets a Higher Bar for "Agency" Than the Agent Community Uses

Barandiaran, Di Paolo & Rohde (2009) define agency as requiring: (1) individuality (self-maintenance of identity), (2) interactional asymmetry (the agent is the source of modulation in coupling), and (3) normativity (the agent's behavior matters to itself — it has stakes). By this definition, current LLM agents are not agents at all. They lack self-maintenance (they don't persist without external infrastructure), they lack interactional asymmetry (they respond to prompts, they don't initiate), and they lack normativity (nothing matters to them).

**Relevance today:** This isn't just philosophical pedantry. The enactivist criteria identify what's missing for genuine autonomy. If you want agents that can operate without continuous human supervision, they need some form of self-maintenance (monitoring their own health), interactional asymmetry (initiating actions when needed), and normativity (caring about their own continued functioning). Homeostatic architectures (Pihlakas) address normativity; self-monitoring addresses self-maintenance; proactive environmental scanning (Beer's S4) addresses interactional asymmetry.

### 3. The MAS Textbook Tradition Has Formal Tools the LLM Community Ignores

Wooldridge (2002), Ferber (1999), and Shoham & Leyton-Brown (2009) provide decades of formal work on: agent communication languages, coordination mechanisms, negotiation protocols, organizational structures, and game-theoretic analysis of multi-agent interaction. The LLM multi-agent community (CrewAI, AutoGen, LangGraph) has largely reinvented these from scratch, poorly.

**Specific gaps:** Formal communication protocols (KQML, FIPA-ACL) have no equivalent in LLM agent frameworks — agents communicate in unstructured natural language. Organizational theory (holonic MAS, team-oriented programming) provides structural patterns that would solve known multi-agent coordination problems. Game-theoretic analysis of agent incentives is entirely absent.

### 4. Swarm Intelligence and Stigmergy Provide Scalable Coordination Models

Bonabeau, Dorigo & Theraulaz (1999) and Heylighen (2016) show that indirect coordination through environmental traces (stigmergy) scales better than direct communication. For multi-agent LLM systems, this means: agents coordinating through shared artifacts (codebases, documents, databases) rather than through direct message-passing may scale better and avoid the O(n²) communication cost problem.

### 5. Predictive Processing Provides the Deepest Theoretical Bridge

Clark (2013) — the "Whatever Next?" paper — bridges cybernetics to modern cognitive science through predictive processing. The brain as a prediction machine that minimizes prediction error is formally equivalent to Ashby's error-correcting regulator. Seth (2015) makes this explicit: the "cybernetic Bayesian brain" traces a direct lineage from Cannon (homeostasis) → Ashby (ultrastability) → Powers (PCT) → Friston (active inference). For agent design, this suggests architectures organized around prediction and error minimization rather than around planning and execution.

### 6. Dreyfus's Critique Identifies a Hard Limit

Dreyfus (2007) argues that genuine intelligence requires embodied, skillful coping that cannot be captured in rules or representations. If he's right, LLM agents will always be "competent without comprehension" (Dennett's phrase). They can manipulate symbols effectively but will never understand what they're doing. The practical consequence: LLM agents will continue to fail in situations requiring genuine understanding of physical causation, social context, or embodied know-how.

**Relevance today:** This is not an argument against building LLM agents. It is an argument for knowing their limits. Tasks requiring symbolic manipulation, text processing, and pattern matching are in scope. Tasks requiring embodied understanding, genuine creativity, or moral judgment may be permanently out of scope.

### 7. Pickering's History Shows Cybernetics Was Always About Performance, Not Representation

Pickering (2010) documents how British cybernetics (Ashby, Beer, Pask, Grey Walter) was fundamentally about *performative* engagement with the world — building machines that *do* things, not machines that *represent* things. This is directly relevant to the LLM agent debate: the cybernetic tradition would frame agent design not as "how do we build something that understands?" but as "how do we build something that performs effectively in its environment?" The performance framing avoids the philosophical quagmire of whether LLMs "really understand" and focuses on what matters: does the agent regulate its environment successfully?

---

## Assessment

The secondary sources reveal that the cybernetics-to-agents bridge has been attempted before — the 1990s embodied AI movement was explicitly cybernetic in inspiration. That movement's insights about situatedness, feedback, and environment-coupling are directly applicable today but have been largely ignored by the LLM agent community. The enactivist tradition sets a higher bar for agency that identifies specific architectural gaps. The MAS textbook tradition provides formal tools for coordination and communication that the LLM community is reinventing badly. The deepest theoretical contribution is predictive processing, which provides a formal bridge from cybernetic homeostasis through Bayesian inference to modern neural architectures.
