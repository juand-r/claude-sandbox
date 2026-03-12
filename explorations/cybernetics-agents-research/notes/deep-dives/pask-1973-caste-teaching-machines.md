# Pask — CASTE and Teaching Machine Systems (1956–1986)

## Bibliographic Details

### Primary Papers
- Pask, G. & Scott, B.C.E. (1973). "CASTE: A system for exhibiting learning strategies
  and regulating uncertainties." *Int J for Man-Machine Studies* 5, pp. 17–52.
  [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0020737373800082)
- Pask, G., Scott, B.C.E. & Kallikourdis, D. (1973). "A theory of conversations and
  individuals (exemplified by the learning process on CASTE)." *Int J Man-Machine Studies*
  5(4), 443–566.
- Pask, G., Kallikourdis, D. & Scott, B.C.E. (1974). "The representation of knowables."
  *Int J Man-Machine Studies* 7(1), 15–134.

### Secondary
- Scott, B.C.E. (2000). "CASTE revisited: Principles of course design in a hypertext
  environment." *Information Services & Use* 20(2-3), 117–127.
  [SAGE](https://journals.sagepub.com/doi/10.3233/ISU-2000-202-307)
- Pangaro, P. (2001). "THOUGHTSTICKER 1986." *Kybernetes*.
  [pangaro.com](https://www.pangaro.com/history-conversation-theory.html)

## The Systems

### SAKI (1956) — Self-Adaptive Keyboard Instructor
(See: pask-1953-musicolour-and-early-machines.md for details)
The first adaptive teaching machine to reach commercial production. Established the
principle that difficulty must be individualized.

### CASTE (1972) — Course Assembly System and Tutorial Environment

#### What It Was
A facility for observing and controlling human learning, developed by Pask with Bernard
Scott and Dionysus Kallikourdis. Unlike SAKI (which adapted difficulty on a single
dimension), CASTE was designed for complex, multi-dimensional subject matters where
students could adopt different learning strategies.

#### Physical Design
Three panels:
1. **Communication console** — for presenting information and receiving student responses
2. **Modeling facility** — external display where agreement between teacher and student
   could be demonstrated by reproducing public descriptions of behavior
3. **Belief sampling system** — mechanism for assessing student understanding

A digital display above the panels showed all possible concepts in the domain as nodes
linked in an entailment structure. As students learned topics and demonstrated
understanding (green light on the topic node), the display updated.

#### How Learning Worked
1. Students picked out a part of the entailment structure to learn about, in an
   **open-ended manner** — they chose their own path.
2. The machine, monitored by an observer, asked for demonstrations and explanations.
3. Understanding was assessed through **teachback**, not conventional testing.
4. The machine tracked the student's learning strategy (serialist/holist/versatile) and
   adapted its presentation accordingly.

#### Empirical Results
Tested with students from art and technical colleges learning probability theory:
- Matching students to preferred strategies using CASTE produced **significantly better
  outcomes** than mismatched instruction.
- **Teachback of ideas produced more effective learning than tests.**
- The machine could learn about the student's preferred strategy by engaging them in
  dialogue about their learning — a second-order capability.

#### Key Design Principles (from Scott 2000)
1. **Learning outcomes** — clearly defined but flexibly ordered
2. **Advance organizers** — overviews that orient the learner
3. **Content analysis** — course content analyzed as a coherent, consistent, learnable whole
4. **Tutorial strategies** — adapted to the individual
5. **Activities** — not passive reception but active engagement
6. **Formative assessment** — ongoing, through teachback
7. **Learning contracts for mastery** — explicit agreements about what constitutes understanding
8. **Summative assessment by teachback** — final evaluation through role-reversal demonstration

### THOUGHTSTICKER (1985–1986)

#### What It Was
Pask's most ambitious software implementation of CT. An adaptive, personalized information
browser built on entailment meshes — a decade before web browsers existed.

#### Key Features

**Adaptive hyperlinks:** Unlike static HTML, clicking the same link produced different
results based on individual user profiles. The link connects to "a neighborhood of
related topics" rather than a fixed destination.

**Three personalization systems:**
1. **User Profile** — learner background, preset characteristics
2. **User History** — tracked actions across sessions
3. **User Model** — preferred learning styles (serialist/holist/versatile)

**Uncertainty regulation:** ~20 overlapping measures to minimize cognitive overload.
The system controlled information complexity across multiple measurable dimensions.

**Contradiction handling:** When different users made contradictory assertions (e.g.,
"the sky is red" vs. "the sky is blue"), THOUGHTSTICKER:
1. Detected the structural conflict
2. Queried whether terms were synonymous
3. Explored contextual differences (red on Mars, blue on Earth)
4. Could accommodate both by placing them in different contexts
5. Preserved author identity and dissenting views

**Authoring tools:**
- Automatic topic suggestion via stemming
- Relationship detection between concepts
- Saturation analysis identifying underdeveloped areas
- Metadata preserving author identity across collaborative environments

#### Significance
Pangaro assessed THOUGHTSTICKER as having "all the components of modern Web browsers
plus an organizing principle for the hyperlinks — something the Web still needs."

The system was "by far the most efficient environment" compared to conventional
computer-based training or AI tutoring systems — it actively stimulated content
creators toward consistency and completeness.

### The Cognitive Reflector

The theoretical construct underlying all these systems: a virtual machine for selecting
and executing concepts/topics from an entailment mesh shared by at least a pair of
participants. Features an external modeling facility where agreement between teacher
and pupil can be shown by reproducing public descriptions of behavior.

## Relevance to Agent Architectures

### Adaptive Agents That Model Their Users
CASTE and SAKI implement what is now called "user modeling" — the agent maintains an
explicit model of the user and adapts behavior accordingly. Current LLM agents typically
do not maintain persistent user models. Pask's systems show this is both possible and
effective.

### Teachback as Evaluation Protocol
The empirical finding that teachback produces more effective learning than testing is
directly relevant to agent evaluation. Instead of testing agents with benchmarks
(the equivalent of exams), we should evaluate them through conversational interaction
where they must demonstrate understanding by teaching back or re-deriving.

### Contradiction Resolution
THOUGHTSTICKER's contradiction handling is remarkably sophisticated and directly relevant
to multi-agent systems where different agents may hold conflicting beliefs. The approach:
1. Detect conflict structurally (not just by string matching)
2. Explore whether the conflict is real or merely terminological
3. Contextualize — both views may be correct in different contexts
4. Preserve provenance — track who said what and why

This is more nuanced than most current approaches to multi-agent disagreement.

### Knowledge Organization Beyond Flat Search
THOUGHTSTICKER's entailment-mesh-based organization contrasts with modern search
(keyword matching, embedding similarity). Pask's system organized knowledge by
conceptual relationships, with adaptive presentation based on user context. This
anticipates — and exceeds — current knowledge graph approaches.

### The Missing Lp
Pangaro's key observation: modern browsers (and by extension, modern agent communication
protocols) have Lo (content, APIs, schemas) but lack Lp (the meta-protocol governing
how conversations about that content should be structured). The Web has hyperlinks but
no conversational structure governing them. Agent systems have message passing but no
formal theory of how messages should be structured into productive conversations.

## Timeline

| Year | System | Key Innovation |
|------|--------|----------------|
| 1956 | SAKI | Adaptive difficulty, individualized modeling |
| 1972 | CASTE | Multi-strategy adaptation, teachback evaluation |
| ~1975 | EXTEND | Recording learning products |
| 1985-86 | THOUGHTSTICKER | Entailment mesh browser, contradiction handling |
| 2008 | ThoughtShuffler (Pangaro) | CT principles applied to web search |
