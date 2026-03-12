# Pickering (2010) — The Cybernetic Brain: Sketches of Another Future

**Full Citation:** Pickering, A. (2010). *The Cybernetic Brain: Sketches of Another Future*. Chicago: University of Chicago Press. 536 pp.

**Source:** U of Chicago Press catalog, Science review, Constructivist Foundations review, Computational Culture review, Goodreads, Arena PDF, Monoskop (Pickering 2002 precursor paper).

---

## 1. Core Thesis: Cybernetics as Nonmodern Ontology

British cybernetics was not primarily about computation or control in the engineering sense. It was a science of the brain — but the brain understood not as the seat of representation and thought, but as the organ of **doing**: acting, performing, adapting to the unknown.

Pickering argues that the British cybernetics tradition offers a **nonmodern ontology** — a way of understanding the world that rejects the modern scientific ambition to achieve complete knowledge and control over nature. Instead, cybernetics embraces the world as:
- **Unknowable** in its totality
- **Performative** rather than representational
- A place where **genuine novelty is always emerging**

## 2. The Six British Cyberneticians

The book is structured as professional biographies of six figures:

### 2.1 Grey Walter
Builder of the "tortoises" — autonomous electromechanical robots (1948-49) that exhibited complex behavior from simple circuits. Key contributions:
- Demonstrated that goal-directed behavior could emerge without internal representation
- The tortoises engaged performatively with their environments, not representationally
- Showed that simple feedback loops produce complex, lifelike behavior

### 2.2 Ross Ashby
Builder of the homeostat (1948). Key contributions:
- **Ultrastability** as the mechanism of adaptive behavior
- The homeostat as "ontological theater" — demonstrating how a machine adapts to an unknowable environment through random search constrained by viability criteria
- The Good Regulator Theorem (with Conant, 1970)
- Variety calculus and the Law of Requisite Variety

Pickering frames Ashby's work as fundamentally about coping with an unknowable world — the homeostat does not understand its environment, it adapts to it.

### 2.3 Gregory Bateson
The anthropologist who applied cybernetic ideas to psychiatry, ecology, and epistemology. Key contributions:
- Double bind theory (schizophrenia as a pathological feedback pattern in family systems)
- Levels of learning as a hierarchy of feedback loops
- "Cybernetic Explanation" — explanation via circular causation rather than linear causation
- Ecology of mind — mind as distributed across brain, body, and environment

### 2.4 R. D. Laing
Psychiatrist who applied cybernetic thinking to anti-psychiatry. Key contributions:
- Mental illness understood not as individual pathology but as adaptive response to pathological social systems
- The family as a cybernetic system with its own dynamics
- Therapy as changing the system dynamics, not "fixing" the individual

### 2.5 Stafford Beer
Management cybernetician. Key contributions:
- The Viable System Model (VSM) — recursive architecture for viable organizations
- Biological computing — using biological systems as computational substrates
- Project Cybersyn — real-time cybernetic management of the Chilean economy under Allende (1971-73)
- Variety engineering as the core of management science

Pickering frames Beer's work as extending Ashby's ideas to social systems: organizations, like homeostats, must cope with unknowable environments through adaptive variety management.

### 2.6 Gordon Pask
Polymath and inventor. Key contributions:
- Musicolour (1952) — a machine that collaborated with musicians to generate light shows, adapting its behavior to the musician's playing
- Conversation Theory — formal framework for learning as circular interaction between participants
- Chemical computers — self-organizing chemical systems as computational substrates
- Adaptive architecture — buildings that respond to their inhabitants

## 3. Key Concepts

### 3.1 Performance vs. Representation
The central philosophical argument. Modern science and engineering aim to represent the world accurately and then control it based on those representations. Cybernetics, as Pickering reads it, proposes an alternative: **engage performatively** with the world, adapting in real time to what happens, without pretending to have complete knowledge.

The homeostat does not model its environment — it dances with it. The tortoises do not plan paths — they feel their way. Musicolour does not represent music — it responds to it.

### 3.2 Ontological Theater
Each cybernetic machine is an "ontological theater" — a staged demonstration of how the world works at a fundamental level. The homeostat is not just an engineering curiosity; it is a demonstration of how adaptive systems cope with genuinely unknowable environments.

### 3.3 The World as Unknowable
The deepest shared conviction of the British cyberneticians: the world is not fully knowable. Genuine novelty is always emerging. No model is ever complete. The appropriate response is not better models but better **adaptive capacity**.

This connects directly to Ashby's variety argument: you cannot regulate what you cannot model, and you cannot model everything, so you need adaptive mechanisms that respond to the unexpected.

## 4. Critical Analysis

### Strengths
- The most comprehensive history of British cybernetics available
- The philosophical framing (nonmodern ontology, performance vs. representation) adds genuine intellectual depth
- The connections between the six figures reveal a coherent intellectual tradition, not just isolated thinkers
- The book rescues cybernetics from the dustbin of intellectual history and shows its continuing relevance

### Weaknesses
- Gender blindness: women appear only as wives, mothers, or patients, never as intellectual contributors
- Tension between the book's argument (nonmodern, performative) and its format (thoroughly modern academic monograph)
- The "sketches of another future" subtitle promises more than it delivers — the book is primarily historical, not prospective
- Some reviewers find the STS (Science and Technology Studies) framing occasionally intrusive

## 5. Relevance to Agent Design

### 5.1 Performance vs. Representation in AI Agents
Current LLM-based agents are heavily representational: they reason about the world through language, construct plans as text, and evaluate outcomes through verbal reflection. Pickering's reading of cybernetics suggests an alternative:
- Agents that **adapt performatively** — responding to environmental feedback without explicit world models
- This is essentially the ReAct pattern at its best: act, observe, react — not plan, execute, evaluate

### 5.2 The Homeostat Model of Agency
Ashby's homeostat, as Pickering reads it, offers a model of agency for unknowable environments:
1. The agent has essential variables (conditions of viability)
2. It acts in the world and observes the effects on its essential variables
3. When essential variables go out of bounds, it randomly searches for new parameter settings
4. Over time, it finds configurations that maintain viability

This is remarkably close to how LLM agents with self-correction work: try something, evaluate whether it worked, if not, try a different approach. But the homeostat is simpler and more principled.

### 5.3 Pask's Conversation Theory as Multi-Agent Interaction
Pask's formalization of conversation as circular interaction between participants maps directly onto multi-agent dialogue:
- Each agent has its own conceptual framework (L_p language)
- Productive conversation requires mutual understanding — each agent must model the other
- The conversation itself generates new understanding not available to either participant alone
- This is "participatory sense-making" at the engineering level

### 5.4 Beer's VSM as Agent Architecture
Beer's VSM, as Pickering presents it, is a recursive architecture for coping with environmental complexity:
- System 1: Operations (the agent's actions in the world)
- System 2: Coordination (preventing conflicts between operational units)
- System 3: Control (resource allocation and internal optimization)
- System 4: Intelligence (environmental scanning and adaptation)
- System 5: Policy (identity and purpose maintenance)

This maps directly onto multi-agent system architectures and is more principled than ad hoc agent orchestration patterns.

## 6. Connections to Other Sources in This Research

- **Ashby (1956, 1952):** Pickering provides the philosophical and historical context for Ashby's technical work. The homeostat as ontological theater enriches our reading of the variety calculus.
- **Beer VSM:** Pickering's chapter on Beer is the best historical account of how VSM emerged from Ashby's ideas.
- **Pask:** Pickering's account of Conversation Theory is the most accessible available.
- **Bateson:** The cybernetic Bateson — levels of learning, double bind — is directly relevant to agent architectures with hierarchical feedback.
- **Von Foerster:** Second-order cybernetics lurks throughout — the observer is always part of the system.
- **Thompson (2007):** The enactive approach inherits the "performance over representation" commitment from cybernetics, as Pickering documents it.

---

*Notes compiled 2026-03-12 from University of Chicago Press, reviews in Science, Constructivist Foundations, and Computational Culture, and Pickering 2002 precursor paper.*
