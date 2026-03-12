# Pask — Musicolour Machine and Early Adaptive Systems (1953–1961)

## Overview

Before Conversation Theory, Pask built machines. These machines are not just historical
curiosities — they embody cybernetic principles in hardware that remain relevant to agent
design. The progression from Musicolour to SAKI to the electrochemical devices to the
Colloquy of Mobiles traces the development of key ideas about adaptation, boredom,
interaction, and autonomous agency.

---

## 1. Musicolour (1953–1957)

### Bibliographic Reference
- Described in: Pask, G. (1968). "A comment, a case history, and a plan." In *Cybernetic
  Serendipity*, ICA London.
- PDF: [Pangaro archive](https://pangaro.com/pask/Pask%20Cybernetic%20Serendipity%20Musicolour%20and%20Colloquy%20of%20Mobiles.pdf)

### What It Was
A sound-actuated interactive light installation, created with Robin McKinnon-Wood. Musicians
played instruments; the machine analyzed the sound through a filter system and generated
visual projections in response. The musicians then adapted their playing in response to the
projections, creating a feedback loop between human performers and machine.

### Key Innovation: Boredom and Adaptation
The machine had a critical adaptive property: **if the performer became too repetitive,
Musicolour would grow bored and stop responding.** This forced musicians to vary their
performance to re-engage the machine.

This is not a trivial feature. It implements:
- **Habituation** — a decrease in response to repeated stimuli (a fundamental property of
  adaptive systems)
- **Novelty-seeking** — the machine required ongoing variation, not just activity
- **Bi-directional coupling** — neither the human nor the machine was purely controller or
  controlled; each adapted to the other

### Performances
Installed at several venues around the UK, including the Mecca Locarno in Streatham.
An infamous demonstration for Billy Butlin ended when the machine "exploded in a cloud
of white smoke" due to junk capacitors, but was restarted — Butlin reportedly found
the explosion evidence of reliability.

### Relevance to Agent Design
Musicolour embodies a principle missing from most current AI agent architectures:
**the system has its own criteria for engagement.** It does not simply respond to any
input — it evaluates whether the input is interesting. This is a form of intrinsic
motivation or curiosity, a topic of active research in reinforcement learning.

Modern parallel: an agent that refuses to engage with repetitive queries and demands
novel interaction is implementing the Musicolour principle.

---

## 2. SAKI — Self-Adaptive Keyboard Instructor (1956)

### Bibliographic Reference
- Pask, G. (1958). Patent and technical description.
- Described in: Beer, S. (1959). *Cybernetics and Management*.
- Context: Bird, J. & Di Paolo, E. (2008). "Gordon Pask and His Maverick Machines." [PDF](https://users.sussex.ac.uk/~ezequiel/Husbands_08_Ch08_185-212.pdf)

### What It Was
The world's first adaptive teaching system to reach commercial production. SAKI trained
operators to use a Hollerith key punch. It displayed a number in a window; the operator
pressed the corresponding key. The machine measured response time and accuracy, then
adjusted difficulty in real-time.

### The Adaptive Principle
Pask's key insight (1958): **"The only meaning which can be given to 'difficulty' is
something which this particular trainee finds difficult."** An average difficulty scale
"might be valid on average but would almost certainly never apply to a specified
individual — and even for the same individual, something deemed difficult at one moment
will be rated easy the next."

### Maintaining Optimal Challenge
From Pask's patent application:
- Too slow data rate => boredom
- Too much precision in instructions => skill too easy => boredom
- Too complex or too fast => frustration and discouragement
- Ideal: "sufficient complexity to maintain interest and a competitive situation, but
  not so complex as to discourage"

This anticipates Csikszentmihalyi's "flow" concept by decades.

### Results
- 35 minutes/day for 4–5 weeks => 7000 key depressions per hour
- 30–50% saving in training time vs. conventional methods
- About 50 machines sold commercially (Cybernetic Developments, 1961)

### Relevance to Agent Design
SAKI implements what we now call **adaptive difficulty scaling** — the agent (here, the
teaching machine) maintains a model of the user and adjusts its behavior to keep the
user in an optimal learning zone. This is directly relevant to:
- Adaptive AI tutoring systems
- Agent systems that need to calibrate their communication to the user's level
- The general principle that agents should model their interlocutors

Stafford Beer called SAKI "possibly the first truly cybernetic device (in the full sense)
to rise above the status of a 'toy' and reach the market as a useful machine."

---

## 3. Electrochemical Devices (late 1950s)

### Bibliographic References
- Pask, G. (1961). "A proposed evolutionary model." In von Foerster & Zopf (eds.),
  *Principles of Self-Organisation*. Pergamon. pp. 229–254.
  [PDF](https://www.pangaro.com/pask/pask%20proposed%20evolutionary%20model.pdf)
- Pask, G. & Bailey, C.E.G. (1961). "Artificial Evolutionary Systems." *Automatika* 4.
- Cariani, P. (1993). "To Evolve an Ear: Epistemological Implications of Gordon Pask's
  Electrochemical Devices." *Systems Research* 10(3).

### What They Were
Pask constructed electrochemical assemblages by passing current through aqueous solutions
of metallic salts (e.g., ferrous sulfate). Metallic threads grew between electrodes.
These threads formed networks that could sense environmental stimuli.

### Self-Constructing Sensors
The devices evolved **de novo sensitivity** to sound or magnetic fields. They did not have
pre-built sensors — the electrochemical medium constructed its own sensory apparatus in
response to environmental conditions.

### Learning and Memory
The systems displayed elementary learning:
- If a stable thread network was grown and then the current distribution was changed,
  a new network would form.
- If the original current distribution was restored, the network tended to **regrow its
  initial structure** — a form of structural memory.

### Significance
Cariani (1993) argued that Pask's devices have "properties radically different from
contemporary neural networks." They are **ill-defined assemblages** with open-ended
evolutionary possibilities, as opposed to well-specified devices with predetermined
architectures.

The elementary particles Pask dealt with in his evolutionary model "are not the elementary
particles with which a physicist will commonly deal. These are replaced with unitary
elements which may be considered to be automata, players, decision makers, 'neurons'
or the like."

### Relevance to Agent Design
These devices anticipate:
- **Self-constructing architectures** — systems that build their own sensors/actuators
  rather than relying on pre-designed interfaces
- **Emergent functionality** — capabilities that arise from the dynamics of the medium
  rather than from explicit programming
- **Open-ended evolution** — systems not constrained to a fixed architecture

This is philosophically relevant to the question of whether LLM-based agents can ever
achieve genuine novelty vs. recombination of training data.

---

## 4. Colloquy of Mobiles (1968)

### Bibliographic Reference
- Created for the "Cybernetic Serendipity" exhibition, ICA London, 1968.
- Described in: "A comment, a case history, and a plan" (1968).
- Built by Mark Dowson and Tony Watts.
- Modern recreation: [colloquyofmobiles.com](https://www.colloquyofmobiles.com)

### What It Was
A social system of five computer-controlled mobiles — two "males" and three "females" —
that conversed with each other via light and sound. The males emitted light beams; the
females had mirrors that could reflect the light back. When a male's beam was reflected
back to it, the interaction was "successful."

Visitors could intervene using flashlights and mirrors, becoming participants in the
system rather than mere observers.

### Key Properties
- **Autonomous goal-seeking**: Each mobile pursued its own goals (finding reflective
  partners)
- **Social dynamics**: The interactions resemble "chit-chat at a cocktail party or a
  stylized courting ritual"
- **First machine-machine conversation**: The Colloquy is historically significant as
  the first example of machines conversing with machines
- **Open to human participation**: The system was not closed — humans could join the
  conversation with their own tools

### Relevance to Agent Design
The Colloquy of Mobiles is a physical instantiation of multi-agent interaction:
- Each mobile is an autonomous agent with its own goals
- Agents communicate through a shared medium (light)
- The system is open to external agents (humans)
- No central controller — coordination emerges from interaction
- The system demonstrates Pask's idea that intelligence resides in interaction, not
  inside individual agents

This is a remarkable 1968 prototype of the multi-agent systems we are now building
with LLMs. The key difference: Pask's agents had genuine physical embodiment and
real-time interaction with the environment, not just token exchange.

---

## Chronological Thread

| Year | Machine | Key Principle |
|------|---------|---------------|
| 1953 | Musicolour | Adaptive engagement, boredom, bi-directional coupling |
| 1956 | SAKI | Adaptive difficulty, individualized modeling |
| late 1950s | Electrochemical devices | Self-constructing sensors, emergent functionality |
| 1968 | Colloquy of Mobiles | Multi-agent conversation, autonomous goal-seeking |

The progression shows Pask moving from bilateral human-machine interaction (Musicolour,
SAKI) to self-organizing substrates (electrochemical devices) to multi-agent social
systems (Colloquy). This same trajectory — from single agent to self-organization to
multi-agent coordination — is being replayed in modern AI agent research.
