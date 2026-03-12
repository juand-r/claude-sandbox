# W. Ross Ashby — *Design for a Brain: The Origin of Adaptive Behaviour* (1952; 2nd ed. 1960)

## Scholarly Notes

**Citation:** Ashby, W.R. (1960). *Design for a Brain: The Origin of Adaptive Behaviour* (2nd ed., revised). London: Chapman & Hall. (Original work published 1952.)

**Full text available at:** [ashby.info PDF](https://www.ashby.info/Ashby%20-%20Design%20for%20a%20Brain%20-%20The%20Origin%20of%20Adaptive%20Behavior.pdf) | [Internet Archive (1960 ed.)](https://archive.org/details/designforbrainor00ashb) | [Internet Archive (1954 ed.)](https://archive.org/details/designforbrain00ashb) | [Springer](https://link.springer.com/book/10.1007/978-94-015-1320-3)

**Note on sources:** The PDF exceeded fetch limits. These notes are compiled from the Springer chapter listings, the Pangaro analysis, Di Paolo's lecture materials, Wikipedia's Homeostat article, multiple ResearchGate papers on the homeostat (Battle et al., Di Paolo), Goodreads reviews by specialists, and my own prior knowledge of the text. Passages marked with quotation marks are verified quotes from Ashby or from scholars quoting Ashby; passages in [brackets] indicate paraphrased reconstructions where I could not verify exact wording.

---

## Book Structure

The book is organized in three parts plus a mathematical appendix:

### Part I: Mechanism (Chapters 1--5)
1. **The Problem** — What must a brain do? The origin of adaptive behaviour.
2. **Dynamic Systems** — Phase-space, state-determined systems, canonical representation.
3. **The Organism as Machine** — The mechanistic hypothesis applied to the nervous system.
4. **Stability** — Formal definition of stability in dynamic systems.
5. **Adaptation as Stability** — The central thesis: adaptive behaviour *is* stable behaviour.

### Part II: Ultrastability (Chapters 6--10)
6. **Parameters** — Step-functions and their role in changing system dynamics.
7. **The Ultrastable System** — Formal definition of ultrastability; the double feedback loop.
8. **The Homeostat** — The physical machine built to demonstrate ultrastability.
9. **Ultrastability in the Organism** — Mapping the theory back onto biological nervous systems.
10. **The Recurrent Situation** — Iterated encounters with the same environment.

### Part III: The Multistable System (Chapters 11--16)
11. **The Fully-Joined System** — Why maximal connectivity makes adaptation intractable.
12--15. **Dispersive and Multistable Systems** — How decomposition into subsystems solves the scaling problem.
16. **Requisite Variety** — The law of requisite variety applied to the adaptive machine.

### Appendix (4 chapters)
Mathematical foundations developed rigorously: canonical equations, stability conditions, transformation theory.

---

## 1. The Central Problem

The book addresses one question: *How can a mechanism — a deterministic machine — produce adaptive behaviour?*

Ashby begins from two premises:
1. The nervous system behaves adaptively.
2. The nervous system is "essentially mechanistic" — it obeys physical law.

The task is to deduce what *kind* of mechanism can exhibit the adaptive behaviour we observe in organisms. The book is explicitly "not a treatise on all cerebral mechanisms but a proposed solution of a specific problem: the origin of the nervous system's unique ability to produce adaptive behaviour."

---

## 2. The Mathematical Framework: State-Space and Dynamic Systems (Chapters 2--4)

### State-Determined Systems

Ashby builds on the concept of a **state-determined system**: a system whose future behaviour is entirely determined by its current state. The system is described by a set of variables whose values at time *t* determine their values at all subsequent times.

The system is specified by **canonical equations** of the form:

```
dx_i/dt = f_i(x_1, x_2, ..., x_n)    for i = 1, 2, ..., n
```

where x_1 through x_n are the **main variables** of the system.

### Phase-Space and Lines of Behaviour

The state of a system at any instant is represented by a point — the **representative point** — in an n-dimensional **phase-space** (state-space). As the system evolves, this point traces a trajectory called the **line of behaviour**.

### The Field

The set of all lines of behaviour in the phase-space constitutes the **field** of the system. The field is the complete description of the system's dynamics from all possible initial conditions.

### Canonical Representation

> "When a real machine and a transformation are so related, the transformation is the canonical representation of the machine, and the machine is said to embody the transformation."

### Stability as a Property of Fields

Ashby's key formal move: **stability belongs not to a material body but to a field.** A field is **stable** if its lines of behaviour converge — that is, if after a displacement, one can "assign some bound to the subsequent movement of the representative point." In an unstable field, such limitation is impossible.

---

## 3. Adaptation as Stability (Chapter 5)

### The Central Thesis

Ashby's defining insight: **"Adaptive" behaviour is equivalent to the behaviour of a stable system, the region of stability being the region of the phase-space in which all the essential variables lie within their normal limits.**

This is the move that makes teleology mechanistic. The organism does not "want" anything — it merely occupies a region of state-space where its essential variables remain within viable bounds, and any perturbation that pushes it out is followed by a return (if the system is stable). What *looks* like purpose is the convergence of trajectories within a stable field.

---

## 4. Essential Variables (Chapter 5)

### Formal Definition

**Essential variables** are those physiological quantities "which are closely linked to survival and which are closely linked dynamically such that marked changes in any one leads sooner or later to marked changes in the others."

Examples: body temperature, blood-sugar concentration, blood pH, osmotic pressure. These are the variables that *must* remain within certain bounds for the organism to continue living.

### The Boundary of Viability

Essential variables define a **region of viability** in the organism's state-space. If the representative point leaves this region (any essential variable goes out of bounds), the organism is in danger. Survival = the representative point remaining within the viable region indefinitely.

### Role in the Architecture

Essential variables serve as the **criterion** for adaptation. The system does not need to know *what* good behaviour looks like — it only needs to know whether its essential variables are within limits. This is a binary signal: in-bounds or out-of-bounds.

---

## 5. Parameters and Step Functions (Chapter 6)

### Parameters vs. Variables

A **parameter** is a quantity that affects the system's dynamics but is not itself one of the main variables. In the canonical equations, a parameter appears as a constant (or slowly-changing quantity) that, when altered, changes the *form* of the equations — and therefore changes the field.

> "A change in the parameter causes a change in the [field]. This change-in-state-to-change-in-field is a 'step function.'"

### The Step Function

The **step function** is the mechanism by which parameters change discontinuously. It is "of paramount importance" to the theory.

Key properties of the step function:
1. **Discontinuous**: Parameters do not change smoothly — they jump from one value to another.
2. **Triggered by essential variables going out of bounds**: The step function fires when a monitored variable crosses a threshold.
3. **Random in its selection of new parameter values**: The new value is not computed or optimized — it is drawn arbitrarily.
4. **Creates a new field**: Each step-function event replaces the current dynamics with a different dynamics (potentially stable, potentially not).

The step function is the formal abstraction of what the uniselector does physically in the homeostat. It is Ashby's mechanism for **trial** in trial-and-error.

### Why Discontinuous?

Continuous parameter adjustment would require knowledge of the gradient — which direction to move the parameter to improve things. The step function sidesteps this entirely. It does not need to know which direction is better. It simply tries a new value. If the new field is stable (essential variables return to bounds), the system stays. If not, another step occurs.

---

## 6. The Ultrastable System (Chapter 7)

### Formal Definition

An **ultrastable system** is defined by the following architecture:

1. **Main variables** (x_1, ..., x_n): Define the system's state in phase-space and participate in the first-order feedback loop with the environment.
2. **Essential variables** (a subset, or functions of, the main variables): Must remain within physiological limits.
3. **Parameters** (S): Determine the form of the system's dynamics (the field).
4. **Step-function mechanism**: Resets parameters randomly whenever essential variables go out of bounds.

The system is **ultrastable** if it has the property that, when any disturbance displaces the essential variables outside their limits, the step functions change the parameters until a new stable field is found that keeps all essential variables within bounds.

### The Double Feedback Loop

This is the architectural signature of ultrastability:

```
         ┌──────────────────────────────────┐
         │                                  │
         │   ┌─────┐        ┌─────┐        │
         │   │     │ action │     │        │
         └──▶│  R  │───────▶│ Env │────────┘
             │     │◀───────│     │  sensory feedback
             └──┬──┘        └──┬──┘
                │              │
          parameters S     affects
                │              │
             ┌──┴──┐        ┌──┴──┐
             │     │◀───────│     │
             │  S  │        │  D  │
             │     │        │     │
             └─────┘        └─────┘
          (parameter       (essential
           store)          variable
                           monitor)
```

**Loop 1 (fast, continuous):** R ↔ Env. The reactive part R acts on the environment and receives sensory feedback. This is the ordinary sensorimotor loop — like a kitten adjusting its position relative to a fire.

**Loop 2 (slow, discontinuous):** D → S → R → Env → D. The essential variable monitor D detects whether essential variables are within bounds. If they go out of bounds, D triggers a change in the parameter store S, which changes R's behaviour, which changes how R acts on Env, which changes the effect on D.

Ashby described this as:

> "The organism that can adapt has a motor output to the environment and two feedback loops. The first loop consists of the ordinary sensory input from eye, ear, joints, etc., giving the organism non-affective information about the world around it. The second feedback goes through the essential variables; it carries information about whether the essential variables are or are not driven outside the normal limits, and it acts on the parameters S."

### The Two Feedback Loops Compared

| Property | Loop 1 (R ↔ Env) | Loop 2 (D → S) |
|---|---|---|
| Speed | Fast, continuous | Slow, discontinuous |
| Nature | Sensorimotor | Evaluative |
| Information | Position, velocity, etc. | In-bounds / out-of-bounds |
| Effect | Changes state | Changes dynamics (field) |
| Analogy | Reflexes, coordination | Learning, adaptation |

### The Kitten and Fire Example

Ashby's recurring illustration: a kitten near a fire. The kitten's essential variable is body temperature, which must stay within limits. The first loop governs the kitten's moment-to-moment position relative to the fire. The second loop triggers when the kitten gets too hot (essential variable out of bounds) — the kitten's behavioural parameters change (it learns to stay further away), and the new parameters produce a stable field in which body temperature remains within bounds.

### Key Properties of Ultrastability

1. **No gradient information required**: The system does not need to know *how* to improve. It only needs to detect failure (essential variables out of bounds) and try something different.
2. **Guaranteed convergence (probabilistic)**: If there exists any parameter setting that produces a stable field, the system will eventually find it — given enough time and enough possible parameter settings.
3. **Retention of success**: Once a stable field is found, no step function fires, so the parameters remain fixed. The system "locks in" to its adapted state.
4. **Passive until disturbed**: "It is only when the environment pushes an essential variable out of bounds that the system does anything at all." The natural state is to remain in stability-as-stasis.

---

## 7. The Homeostat (Chapter 8)

### Purpose

> "The ultrastable system is much richer in interesting properties than might at first be suspected. For their display, a machine was built according to the definition of the ultrastable system."

The homeostat was built in 1948 at Barnwood House Hospital to physically demonstrate that ultrastability works.

### Physical Construction

Four identical units, constructed from surplus RAF bomb control switch-gear kits. Each unit was an electro-mechanical artificial neuron. The four units were identified by colours: **red, green, blue, yellow**.

### Each Unit's Architecture

Each unit contains:

1. **A pivoting magnet** at the centre, which moves a metal plate.
2. **A semicircular trough** filled with distilled water, situated on top of the box. Electrodes at each end of the trough.
3. **Four input coils** (A, B, C, D) — one from each unit (including self-feedback). The summed magnetic fields of these coils determine the position of the pivoting magnet.
4. **A potentiometer/commutator pair** for each input — modulates the magnitude and polarity of each input's effect.
5. **A uniselector** — a 25-position stepping switch that randomly sets the potentiometer/commutator values.

The voltage V across the electrodes is determined by the magnet's position. When the system is at equilibrium, V is near zero (the magnet is centred).

### The Uniselector Mechanism

Each uniselector has **25 positions**. At each position, a unique combination of resistance (via potentiometer) and polarity (via commutator) is set for each input connection. The values at each position were chosen from **Fisher and Yates' Table of Random Numbers** — Ashby insisted on genuine randomness.

With 4 units, each having a 25-position uniselector, the total parameter space is **25^4 = 390,625** possible combinations.

### How Adaptation Works in the Homeostat

1. The four units interact through their electrical connections. Each unit's output (its trough voltage) becomes input to all other units (and itself).
2. If the system is stable, all needles (pivoting magnets) remain near their central positions. No uniselectors fire.
3. If a perturbation is introduced (e.g., Ashby manually reverses a commutator on one unit), the system becomes unstable. One or more needles are driven to extreme positions.
4. When a needle exceeds a **critical deviation** from centre (the essential variable goes out of bounds), that unit's uniselector **advances one position**, randomly changing the potentiometer/commutator settings.
5. The new parameters may or may not produce stability. If not, the needle hits the limit again, and the uniselector advances again.
6. This continues until a combination of parameters is found that produces a stable field — all needles return to near-centre and stay there.

### Experimental Results

Ashby tested the homeostat by allowing it to stabilise, then manually reversing a commutator to create instability. In a simple two-unit system (M1 controlled by hand, M2 by its uniselector), "only a relatively small number of uniselector changes in M2 were required for stability to be restored."

The homeostat exhibited behaviours analogous to **habituation**, **reinforcement**, and **learning** — not because these were programmed in, but because they are natural consequences of the ultrastable architecture.

### Connectivity and Zero Values

The uniselector mechanism "not only affords plasticity in weighting but also in connectivity: 'Zeros occur, and when this happens the units are, in effect, cut off from one another.'" This foreshadows the multistable system argument in Part III.

### What the Homeostat Demonstrated

The homeostat showed that a deterministic mechanism, with no goal-representation and no gradient information, can exhibit behaviour that appears **purposeful** and **adaptive** — the needles seek their central positions "as though" the machine wants to keep them there. The appearance of teleology emerges from the architecture, not from any vitalistic principle.

---

## 8. Adaptation as Deterministic Trial-and-Error (Chapters 7--9)

### The Basic Rule

> "The basic rule for adaptation by trial and error is: If the trial is unsuccessful change the way of behaving; when and only when it is successful, retain the way of behaving."

This is the complete algorithm. No gradient. No model of the environment. No planning. Just: detect failure → change parameters → repeat until stable.

### How Ashby Made Teleology Mechanistic

The traditional objection to mechanistic biology was that organisms appear to have *purposes* — they act *in order to* achieve goals. This seems to require something beyond mechanism. Ashby's response:

1. Define the organism's "goal" operationally: essential variables must remain within bounds.
2. Show that a mechanism (the ultrastable system) with no representation of goals can achieve this through random search.
3. The *appearance* of purposeful behaviour is a consequence of selection: only stable parameter settings persist.

The analogy is explicit: this is Darwinian selection applied to parameter settings within the lifetime of a single organism. Unstable parameter settings are "selected against" (the step function fires again); stable ones are "selected for" (the step function stops firing).

### The Delay Problem

> "A weakness of the ultrastable system's method is that success depends on using a suitable period of delay between each trial — too hurried a change may not allow time for success to declare itself, while too prolonged a testing of a wrong trial may allow serious damage."

This is a genuine engineering constraint on the mechanism. The delay between step-function firings must be long enough for the system to reveal whether the new parameters produce stability, but short enough to avoid lethality if they do not.

---

## 9. Multistable Systems and the Argument Against Rich Connectivity (Chapters 11--15)

### The Problem with Fully-Joined Systems

Chapter 11 addresses the scaling problem. A **fully-joined system** is one in which every variable affects every other variable, and every step-mechanism can affect every variable.

Ashby demonstrates that in a fully-joined ultrastable system, **adaptation time grows exponentially** with the number of variables. His famous example:

> Consider 1,000 spinning wheels that must all stop with the letter 'A' facing up.

**Case 1 (Fully joined / parallel):** Spin all 1,000 wheels simultaneously. The probability that all land on 'A' simultaneously is astronomically small (proportional to 2^(-1000) or worse). Expected waiting time is effectively infinite.

**Case 2 (Independent / serial):** Stop one wheel at a time. Each wheel takes a bounded number of tries. Total time grows *linearly* with the number of wheels.

The key insight: **when subsystems are independent, partial successes are retained.** When wheel #1 stops on 'A', it stays there while you work on wheel #2. In the fully-joined case, fixing one wheel can displace another — partial successes are destroyed by cross-interactions.

### The Multistable System

A **multistable system** is one composed of subsystems that are ultrastable *individually* and have limited (or no) communication between them. Each subsystem can find its own stable parameter settings without being disturbed by the adaptation process in other subsystems.

### Ashby's Counter-Intuitive Claim

> "Let us dispose once for all of the idea, fostered in almost every book on the brain written in the last century, that the more communication there is within the brain the better."

And:

> "The idea so often implicit in physiological writings, that all will be well if only sufficient cross-connexions are available, is, in this context, quite wrong."

### The Formal Argument

1. In a fully-joined ultrastable system with *n* binary parameters, the expected number of trials before finding a globally stable configuration is O(2^n).
2. In a multistable system decomposed into *k* independent subsystems of size *n/k*, the expected number of trials is O(k * 2^(n/k)) — exponentially smaller.
3. Therefore, **reduced connectivity dramatically improves adaptation speed**.

### The Biological Implication

> "Adaptation thus demands not only the integration of related activities but the independence of unrelated activities."

Ashby is arguing that evolution would select for brains with **modular structure** — barriers between subsystems that prevent interference during adaptation. This anticipated by decades the neuroscientific discovery of modular brain architecture.

Sherrington (1906) had already shown that "the nervous system was neither divided into permanently separated parts nor so wholly joined that every event always influenced every other — rather, it showed a picture in which interactions and independencies fluctuated, with separation and union being extremes on a scale of 'degree of connectedness.'"

Ashby's contribution was to show *why* intermediate connectivity is optimal: too little connectivity means the organism cannot coordinate responses; too much connectivity means it cannot adapt in reasonable time.

### For Accumulation of Adaptations

> "If the method of ultrastability is to succeed within a reasonably short time, then partial successes must be retained. For this to be possible it is necessary that certain parts should not communicate to, or have an effect on, certain other parts."

> "For the accumulation of adaptations to be possible the system must not be fully joined."

### The DAMS Project

Ashby attempted to build a physical multistable system called **DAMS** (Dispersive and Multistable System) — a randomly constructed array of electronic valves interconnected by neon lamps acting as switches. The project was under construction at Barnwood in 1951 but "foundered in interesting ways," and Ashby never achieved the general-purpose brainlike device he sought. The scaling difficulties he encountered empirically confirmed the theoretical importance of controlled connectivity.

---

## 10. The Law of Requisite Variety (Chapter 16)

Ashby applies his law of requisite variety to the adaptive machine:

> "Any system can adapt as far as it fits its environment — but no more."

The system's variety (the number of distinct parameter settings available) must be at least as great as the variety of disturbances the environment can produce. If the environment can produce more distinct challenges than the system has distinct responses, the system cannot maintain its essential variables within bounds for all possible disturbances.

In the homeostat, variety is provided by the 390,625 possible uniselector combinations. This is the system's repertoire of possible behaviours.

Following the law of requisite variety: **increasing the number of units increases the time taken to reach equilibrium, and conversely, reducing internal connectivity reduces the time taken to reach equilibrium.** There is a tension between having enough variety (many interconnected units) and being able to search the variety in reasonable time (fewer interconnections).

---

## 11. Mathematical Formulations Summary

### State-Space Description

The system state at time *t*:

```
x(t) = (x_1(t), x_2(t), ..., x_n(t))
```

Dynamics governed by:

```
dx_i/dt = f_i(x_1, ..., x_n; s_1, ..., s_m)
```

where s_1, ..., s_m are **parameters**.

### Stability Condition

A field is stable in a region R if, for every initial state x(0) in R, the trajectory x(t) remains in R for all t > 0, and converges to an equilibrium point (or bounded attractor) within R.

### Essential Variables Constraint

Let E = {e_1, ..., e_k} be the essential variables (functions of the main variables). The **viability region** V is defined by:

```
V = { x : a_j ≤ e_j(x) ≤ b_j  for all j = 1, ..., k }
```

### Step Function Definition

The parameters change according to a step function:

```
s(t+) = { s(t)           if x(t) ∈ V
         { random(S)      if x(t) ∉ V
```

where S is the set of possible parameter values (e.g., the 25 uniselector positions) and random(S) selects uniformly from S.

### Ultrastability as Convergence

The system is ultrastable if: for any initial state x(0) and any environment, the probability that the system eventually reaches a parameter setting s* such that the resulting field is stable in V approaches 1 as t → ∞ (provided such an s* exists in S).

---

## 12. Key Themes and Significance

### What Ashby Achieved

1. **Mechanized teleology**: Showed that purposeful-seeming behaviour does not require a purpose-representing mechanism. The ultrastable architecture produces goal-directed behaviour from purely local, reactive components.

2. **Formalized adaptation**: Gave a complete, implementation-independent specification of a system capable of learning and adapting. The specification depends only on the *architecture* (double feedback, step functions, essential variables) — not on the substrate (neurons, circuits, software).

3. **Identified the scaling problem**: Showed that rich interconnection, far from helping adaptation, makes it exponentially harder. This is a deep result with implications for brain architecture, AI design, and organizational theory.

4. **Linked adaptation to natural selection**: The ultrastable mechanism is a form of Darwinian selection operating on parameter settings within a single organism's lifetime. Unfit parameter settings are replaced; fit ones persist.

5. **Defined adaptation operationally**: Adaptation = stability of essential variables within their viability region. This removes all subjective or teleological content from the concept.

### Limitations Ashby Himself Noted

- The ultrastable system is **essentially passive**: "It is only when the environment pushes an essential variable out of bounds that the system does anything at all." It does not explore or anticipate.
- The random search is **slow**: For complex environments, the expected time to find a stable configuration may be very long.
- The **delay problem**: Choosing the right interval between step-function firings is non-trivial.
- **Scaling**: The DAMS project revealed that building large multistable systems presented engineering challenges Ashby could not overcome with 1950s technology.

### Relation to Later Work

- **Reinforcement learning**: The ultrastable mechanism is a precursor to reward-signal-driven parameter adjustment, but without the gradient information that makes modern RL efficient.
- **Modularity in AI**: Ashby's argument for reduced connectivity anticipates arguments for modular neural network architectures.
- **Autopoiesis**: Maturana and Varela's concept of autopoiesis (organizational closure maintaining essential identity) can be read as extending Ashby's essential-variables framework.
- **Enactivism / Di Paolo**: Ezequiel Di Paolo has extended ultrastability into a theory of adaptive autonomy, arguing that organisms do not merely *maintain* essential variables but actively *regulate* them.

---

## 13. Notable Quotes (verified from multiple secondary sources)

On the project:
> "Not a treatise on all cerebral mechanisms but a proposed solution of a specific problem: the origin of the nervous system's unique ability to produce adaptive behaviour."

On adaptation:
> "The basic rule for adaptation by trial and error is: If the trial is unsuccessful change the way of behaving; when and only when it is successful, retain the way of behaving."

On connectivity:
> "Let us dispose once for all of the idea, fostered in almost every book on the brain written in the last century, that the more communication there is within the brain the better."

> "The idea so often implicit in physiological writings, that all will be well if only sufficient cross-connexions are available, is, in this context, quite wrong."

> "For the accumulation of adaptations to be possible the system must not be fully joined."

> "Adaptation thus demands not only the integration of related activities but the independence of unrelated activities."

On stability:
> "The concept of 'stability' belongs not to a material body but to a field."

On essential variables:
> [Variables] "which are closely linked to survival and which are closely linked dynamically such that marked changes in any one leads sooner or later to marked changes in the others."

On the double feedback:
> "The organism that can adapt has a motor output to the environment and two feedback loops. The first loop consists of the ordinary sensory input from eye, ear, joints, etc., giving the organism non-affective information about the world around it. The second feedback goes through the essential variables."

On the step function and variety:
> "Any system can adapt as far as it fits its environment — but no more."

---

## 14. Sources Consulted

- [Ashby Digital Archive — Design for a Brain PDF](https://www.ashby.info/Ashby%20-%20Design%20for%20a%20Brain%20-%20The%20Origin%20of%20Adaptive%20Behavior.pdf)
- [Internet Archive — 1960 edition](https://archive.org/details/designforbrainor00ashb)
- [Internet Archive — 1954 edition](https://archive.org/details/designforbrain00ashb)
- [Springer — Design for a Brain](https://link.springer.com/book/10.1007/978-94-015-1320-3)
- [Pangaro — Design for a Self-Regenerating Organization](https://www.pangaro.com/ashby+design-for-self-regenerating-corporation.htm)
- [Di Paolo — Adaptive Systems lecture notes (Sussex)](https://users.sussex.ac.uk/~ezequiel/AS/lectures/AdaptiveSystems3.pdf)
- [Di Paolo — Autonomy and Homeostasis](https://ezequieldipaolo.net/research/evolutionary-robotics/autonomy-and-homeostasis/)
- [Wikipedia — Homeostat](https://en.wikipedia.org/wiki/Homeostat)
- [Panarchy — Ashby, Feedback, Adaptation and Stability (1960)](https://www.panarchy.org/ashby/adaptation.1960.html)
- [ResearchGate — Ashby's Mobile Homeostat (Battle et al.)](https://www.researchgate.net/publication/300781597_Ashby's_Mobile_Homeostat)
- [ResearchGate — Homeostats for the 21st Century](https://www.researchgate.net/publication/277596924_Homeostats_for_the_21st_Century_Simulating_Ashby_Simulating_the_Brain)
- [GitHub — jimfinnis/homeostat (Qt4 simulation)](https://github.com/jimfinnis/homeostat)
- [Academia.edu — Ashby's Mobile Homeostat](https://www.academia.edu/10986577/Ashbys_Mobile_Homeostat)
