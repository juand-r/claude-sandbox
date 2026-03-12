# Barandiaran & Moreno (2006) — On What Makes Certain Dynamical Systems Cognitive

**Full Citation:** Barandiaran, X. & Moreno, A. (2006). "On What Makes Certain Dynamical Systems Cognitive: A Minimally Cognitive Organization Program." *Adaptive Behavior*, 14(2), 171-185.

**Source:** SAGE Journals, ResearchGate (PDF), PhilArchive, Semantic Scholar, Barandiaran's website.

---

## 1. The Problem

Dynamical systems theory has given cognitive science powerful tools for modeling **how** cognitive agents work — attractors, bifurcations, coupled oscillators, state-space trajectories. But it has failed to address the more fundamental question: **what makes a system cognitive in the first place?**

Barandiaran and Moreno argue that "how it works" will never be complete without "what it is." A dynamical system that happens to produce adaptive behavior is not thereby cognitive. Something more is needed.

## 2. Against Behavioral Definitions

The paper critiques the dominant approach of defining cognition behaviorally: a system is cognitive if it behaves in certain ways (adapts, learns, solves problems, etc.). Problems with this approach:

1. **Behavioral equivalence**: Trivial systems can be behaviorally equivalent to complex cognitive systems in specific contexts. A thermostat "behaves" like a goal-directed system, but we don't call it cognitive.
2. **Observer-dependence**: Whether a behavior counts as "cognitive" depends on the observer's interpretive framework, not on properties of the system itself.
3. **No principled boundary**: Without an organizational criterion, there is no principled way to draw the line between cognitive and non-cognitive systems.

## 3. The Organizational Alternative

Instead of behavioral criteria, Barandiaran and Moreno propose **organizational** criteria. Cognition is defined not by what a system does but by how it is internally organized:

### 3.1 Definition
Cognition = **adaptive-autonomy in the embodied and situated neurodynamic domain**.

Unpacking this:
- **Adaptive**: The system actively regulates its viability (following Di Paolo 2005)
- **Autonomy**: The system's organization is operationally closed and self-maintaining
- **Embodied**: The system has a physical body coupled to an environment
- **Situated**: The system's cognition is constituted by its environmental interactions
- **Neurodynamic domain**: The organizational closure that constitutes cognition occurs specifically in the neural domain — a web of sensorimotor structures

### 3.2 The Cognitive Organization
A cognitive system has a specific organizational structure:
1. **A web of stability dependencies** between sensorimotor structures
2. These structures are **created and maintained during a historical/developmental process** (not pre-specified)
3. The system exhibits **compensatory regulation** of this web — actively maintaining its sensorimotor organization against perturbation

## 4. The Role of Emotional Embodiment

A distinctive contribution: the functional role of **emotional embodiment** in cognition.

Internal bioregulatory processes (what we loosely call "emotions") are coupled to the formation and adaptive regulation of neurodynamic autonomy. Emotions are not epiphenomenal additions to cognition but are **constitutive of it** — they provide the evaluative dimension that transforms mere information processing into sense-making.

This connects to:
- **Damasio's somatic marker hypothesis**: Emotions as bodily feedback guiding decision-making
- **Di Paolo's adaptivity**: Emotions as internal indicators of viability status
- **Seth's interoceptive inference**: Emotions as predictions about bodily state

## 5. The Minimally Cognitive Organization Program

The paper proposes a research program complementary to the existing "minimally cognitive behavior" approach (which uses evolutionary simulations to study minimal behaviors that count as cognitive):

**Minimally Cognitive Organization Program**: Study the minimal organizational requirements for a system to be genuinely cognitive. Not "what is the simplest behavior we'd call cognitive?" but "what is the simplest organization that constitutes cognition?"

This is a more rigorous foundation because:
- Organization is an intrinsic property of the system, not observer-dependent
- It provides necessary conditions, not just sufficient behaviors
- It connects to the broader theory of biological autonomy

## 6. Relevance to Agent Design

### 6.1 The Organizational Test for AI Agents
If Barandiaran and Moreno are right, the question "is this AI agent cognitive?" cannot be answered by examining its behavior alone. We must examine its organization:
- Does it have operational closure in its processing domain?
- Does it actively maintain its own organizational integrity?
- Does it have internal evaluative processes (analogous to emotions) coupled to its adaptive regulation?

By these criteria, no current AI agent is cognitive — their organization is externally designed and maintained, their evaluative criteria are externally specified, and they have no internal bioregulatory equivalent.

### 6.2 Implications for Agent Architecture
Even without claiming genuine cognition, the organizational perspective suggests design improvements:

**Web of stability dependencies:**
- Agent components should be interdependent, not modular in the traditional software sense
- A change in one component should propagate through the system, creating a need for compensatory regulation
- This argues against purely modular agent architectures and toward more tightly coupled designs

**Developmental history:**
- The agent's sensorimotor structures should be products of its own history, not pre-specified
- An agent that develops its own tools, strategies, and evaluation criteria through experience is organizationally richer than one with pre-specified capabilities
- This points toward developmental/learning-based agent architectures

**Emotional embodiment analog:**
- Agents should have internal state variables that function like emotions — evaluative signals arising from the system's own operational dynamics
- Examples: confidence levels that emerge from processing dynamics (not externally computed), urgency signals based on resource depletion, satisfaction signals based on internal coherence

### 6.3 The Agency Definition (Barandiaran, Di Paolo & Rohde, 2009)
In a later paper, Barandiaran extends this work to define agency formally:

An agent is an **autonomous organization that adaptively regulates its coupling with its environment and thereby contributes to sustaining itself as a consequence**.

Three conditions:
1. **Individuality**: The system has a distinct identity constituted by its organization
2. **Interactional asymmetry**: The system actively modulates its coupling with the environment (not passively shaped by it)
3. **Normativity**: The system's activity is regulated by norms generated by its own organization

This is the most rigorous definition of agency in the enactivist literature, and it sets a very high bar for AI systems.

## 7. Connections to Other Sources

- **Di Paolo (2005)**: Direct intellectual lineage. Barandiaran adopts Di Paolo's adaptivity and applies it to the question of what makes systems cognitive.
- **Thompson (2007)**: The life-mind continuity thesis provides the philosophical framework. Barandiaran operationalizes it.
- **Maturana & Varela**: Autopoiesis as the foundation of organizational closure.
- **Ashby**: Ultrastability as the mechanistic basis for compensatory regulation.
- **Froese & Ziemke (2009)**: Parallel conclusions about the requirements for genuine AI cognition.
- **Varela (1979)**: Organizational closure and autonomy as formal concepts.
- **Damasio**: The somatic marker hypothesis as a neuroscientific parallel to emotional embodiment.

## 8. Assessment

This paper makes a sharp and important argument: cognition is an organizational property, not a behavioral property. The implications for AI are severe — behavioral sophistication (including human-level language ability) does not establish cognition if the underlying organization is wrong.

The main weakness is the same as with most enactivist work: the organizational criteria are stated qualitatively, not formally. There is no mathematical test for "adaptive-autonomy in the neurodynamic domain." This makes it difficult to apply the criteria rigorously to artificial systems.

The paper has been influential in philosophy of cognitive science and artificial life, less so in mainstream AI — which is precisely the gap our research aims to bridge.

---

*Notes compiled 2026-03-12 from SAGE, PhilArchive, ResearchGate, and Barandiaran's website.*
