# Heinz von Foerster: Second-Order Cybernetics — Scholarly Notes

## Sources Consulted

- Von Foerster, "On Self-Organizing Systems and Their Environments" (1960), in Yovitz & Cameron (eds.), *Self-Organizing Systems*, Pergamon Press, pp. 31-50.
- Von Foerster, "Objects: Tokens for (Eigen-)Behaviors" (1976/2003), in *Understanding Understanding*, Springer.
- Von Foerster, "Ethics and Second-Order Cybernetics" (1991), lecture delivered in Paris; reprinted in *Understanding Understanding* (2003).
- Von Foerster, *Understanding Understanding: Essays on Cybernetics and Cognition* (2003), Springer.
- Glanville, "Second Order Cybernetics" (PDF at pangaro.com — binary PDF, not directly extractable; content sourced from secondary analyses).
- Kauffman, "Eigenforms — Objects as Tokens for Eigenbehaviors" (2005), *Kybernetes* 34(1-2), 129-150; also CEPA fulltext.
- Kauffman, "Eigenforms and Quantum Physics" (2011), arXiv:1109.1892.
- Kauffman, "Reflexivity and Eigenform: The Shape of Process" (2009), *Constructivist Foundations* 4(3), 121-137.
- Kauffman, "Autopoiesis and Eigenform" (2023), *Computation* 11(12), 247.
- Various secondary sources (see inline citations).

---

## 1. The Formal Distinction: First-Order vs. Second-Order Cybernetics

### The Standard Formulation

Von Foerster defined:
- **First-order cybernetics**: "the cybernetics of observed systems"
- **Second-order cybernetics**: "the cybernetics of observing systems"

This is not merely a slogan about "including the observer." The distinction has formal, logical, and mathematical content.

### What "Including the Observer" Actually Means

The shift from first-order to second-order is a shift from **linear causality** to **circular causality**, and from **external description** to **self-referential description**.

In first-order cybernetics (Wiener, Ashby), one models a system from the outside: input → black box → output. The observer is implicitly assumed to stand outside the system, unaffected by it. The descriptions are "objective" in the classical sense — the properties of the observer do not enter the description.

In second-order cybernetics, the observer is recognized as part of the system being observed. This creates a logical structure of **self-reference**: the description includes the describer. Von Foerster puts it as a logical chain:

> In the general case of circular closure: "A implies B; B implies C; C implies A."
> In the reflexive case: "A implies B, and B implies A."
> In its purest form — self-reference: "A implies A."

This is not merely philosophical hand-waving. It has consequences:

1. **Closure**: The system of observation is operationally closed. There is no external reference point.
2. **Recursion**: Descriptions are descriptions of descriptions. Computations compute computations. This leads to recursive structures of arbitrary depth.
3. **Undecidability**: Certain questions become formally undecidable within the system (see §6 below).

### The Two Circularities

Glanville (and von Foerster) identify two distinct circularities:

1. **Circularity of the observed system**: e.g., a thermostat — the sensor causes the heater to turn on/off, the heater causes the sensor to change state. Circular causality with no primary cause.
2. **Circularity of the act of observing**: the observer observes systems that include the observer. The observation changes what is observed, which changes the observer, which changes the observation...

Second-order cybernetics is specifically about recognizing and formally dealing with the second circularity. First-order cybernetics already deals with the first.

### Double Closure (Von Foerster's Formal Model)

Von Foerster formalized the structure of a cognitive/communicative system through **double closure**, which he represented topologically as a **torus**:

- **First closure**: the process of making a distinction (Spencer-Brown's mark of distinction).
- **Second closure**: the process by which the distinction itself becomes a stable, memorable entity — a concept that "remembers itself."

Communication is formally defined as "the eigenbehavior of a recursively operating system that is doubly closed onto itself."

---

## 2. Eigenforms / Eigenbehaviors: The Mathematical Concept

### The Fixed-Point Formulation

The central mathematical idea: given an operator O (representing an observer, a process, a transformation), an **eigenform** is an entity X such that:

**O(X) = X**

This is the fixed-point equation. X is invariant under the operation O. Von Foerster's claim: **objects are tokens for eigenbehaviors** — what we perceive as stable "objects" in the world are actually the fixed points of recursive processes of interaction between observer and environment.

### The Recursive Construction

How does one find such a fixed point? By **recursive iteration**:

Start with anything — call it x₀. Apply O repeatedly:

```
x₁ = O(x₀)
x₂ = O(x₁) = O(O(x₀))
x₃ = O(x₂) = O(O(O(x₀)))
...
x_∞ = O(O(O(...)))
```

If this process converges (in some appropriate sense), the limit x_∞ satisfies O(x_∞) = x_∞. The limit is the eigenform.

### Von Foerster's Canonical Example: Nested Boxes

Begin with an empty box ☐. Apply the operation "put a box around it":

```
☐ → [☐] → [[☐]] → [[[☐]]] → ...
```

The limit is an infinitely nested structure: `[[[...]]]`

This infinite nesting is **invariant** under the operation of adding one more surrounding box. Hence it is a fixed point / eigenform.

Key insight: this object does not "exist" in any naive physical sense. It requires what Kauffman calls **"imaginative completion"** — the mind posits the limit of an infinite process. The eigenform is a **cognitive construction**, not a physical entity discovered "out there."

### Mathematical Context: Fixed-Point Theorems

This is not ad hoc. It connects to deep mathematics:

1. **Banach Fixed-Point Theorem**: In a complete metric space, a contraction mapping has a unique fixed point, obtainable by iteration. Many observation processes are contractive in appropriate spaces.
2. **Brouwer Fixed-Point Theorem**: Every continuous function from a compact convex set to itself has a fixed point.
3. **Lawvere's Fixed-Point Theorem** (category theory): In any cartesian closed category, if there is a point-surjective map from an object A to the function space A^A, then every endomorphism of A has a fixed point. This is the categorical generalization underlying Gödelian self-reference, the halting problem, Cantor's theorem, and eigenforms simultaneously.

### Lambda Calculus and Self-Reference (Kauffman's Extension)

Kauffman shows that the eigenform problem O(X) = X can be solved **without** the excursion to infinity, using the lambda calculus:

In lambda calculus, define G such that G(x) = O(x(x)). Then:

**G(G) = O(G(G))**

So G(G) is a fixed point of O. This is the Church-Curry fixed-point combinator (Y-combinator). It works because the lambda calculus permits self-application: a name can act on itself.

This connects eigenforms directly to:
- Gödel's self-referential sentences
- The halting problem
- Recursive function theory
- The foundations of computation

### Eigenforms and Perception

Von Foerster's philosophical application: the "objects" of perception are not pre-given features of reality. They are the stable outcomes (fixed points) of the recursive interaction between organism and environment. There is a behavior between perceiver and perceived, and the stability that arises between them **constitutes** the object (and the perceiver).

This does not deny an underlying reality. It emphasizes the role of process and the constitutive role of the organism in producing a "map" so intertwined with the "territory" that they cannot be separated.

### Connection to Attractors in Dynamical Systems

Von Foerster's eigenforms correspond to **attractors** in the language of dynamical systems:
- Single fixed points (eigenstates)
- Periodic orbits (oscillatory eigenbehaviors)
- Strange attractors (bounded but non-repeating eigenbehaviors — "chaotic" stability)

The "order from noise" principle (§3) explains how systems reach these attractors.

---

## 3. Self-Organization: Order from Noise

### The 1960 Paper: Core Argument

In "On Self-Organizing Systems and Their Environments" (1960), von Foerster makes several formal arguments:

#### (a) No System Is Truly "Self-Organizing" in Isolation

By reductio ad absurdum: if a closed system reduces its own entropy, it violates the Second Law of Thermodynamics. Therefore, any system that appears to self-organize must be exchanging energy or information with an environment. The term "self-organizing system" is a misnomer unless understood as shorthand for "a system that organizes itself in relation to its environment."

#### (b) Redundancy as the Measure of Order

Von Foerster adopted Shannon's **redundancy** as his measure of internal order:

**R = 1 − H / H_max**

Where:
- H = Shannon entropy of the system
- H_max = maximum possible entropy (complete disorder)

When H = H_max: R = 0 (no order, maximum disorder).
When H = 0: R = 1 (perfect order — given one element, all others are determined).

Why redundancy rather than negentropy? Because negentropy always assumes finite values even for maximally disordered systems, making it a poor measure of order. Redundancy is "tailor-made" for measuring order — it is zero when there is none and unity when order is complete.

#### (c) The Self-Organization Criterion

A system is self-organizing if and only if:

**dR/dt > 0**

The redundancy (internal order) is increasing over time.

#### (d) The "Order from Noise" Principle

This is von Foerster's third principle, beyond Schrödinger's two:
- Schrödinger's "order from order" (algorithmic, crystalline)
- Schrödinger's "order from disorder" (statistical, thermodynamic)
- Von Foerster's "order from noise" (self-organizational)

The insight: random perturbations ("noise") cause a system to explore its state space more widely. This increases the probability that it will fall into the basin of a strong attractor. Paradoxically, the larger the noise, the faster the self-organization — because the system traverses more of its state space and finds attractors sooner.

Important caveat (Vallée): noise does not create order ex nihilo. It acts as a "structure displayer" — it reveals pre-existing order embedded in the system's interaction dynamics (e.g., magnetic interactions among components). The structure must already be there for noise to display it.

#### (e) The Internal and External Demons

To compute R, one must account for the coupling between system entropy and environment entropy. Von Foerster introduces:
- The **internal demon**: the agent responsible for changes in the system's entropy
- The **external demon**: the agent responsible for changes in the environment's entropy

Self-organization requires that these are coupled: the system's entropy decrease is compensated by the environment's entropy increase, satisfying the Second Law globally.

---

## 4. The Non-Trivial Machine

### Formal Definitions

#### Trivial Machine

A trivial machine is defined by a single function:

**y = f(x)**

Where x is the input and y is the output. The function f is fixed and does not change. Properties:
- **Synthetically deterministic**: given f, the output for any input is determined.
- **Analytically deterministic**: given input-output pairs, f can be deduced.
- **History-independent**: previous operations do not affect future operations.
- **Predictable**: same input always produces same output.

Number of trivial machines with n input symbols and n output symbols:

**N_T(n) = n^n**

#### Non-Trivial Machine

A non-trivial machine is defined by two functions:

**y = F(x, z)**  — the driving function (output depends on input AND internal state)
**z' = Z(x, z)** — the state function (internal state changes as a function of input and current state)

Where:
- x = input
- y = output
- z = current internal state
- z' = next internal state

Properties:
- **Synthetically deterministic**: given F, Z, and the current state z, the output is determined.
- **Analytically indeterminate**: given input-output pairs, the internal structure (F, Z, z) generally CANNOT be deduced. The problem of identification — deducing the machine's structure from its behavior — is unsolvable.
- **History-dependent**: previous inputs affect the internal state, which affects future outputs.
- **Unpredictable** (in practice and often in principle): same input can produce different outputs depending on the machine's history.

### The Transcomputational Argument

Number of non-trivial machines with n input/output symbols and z internal states:

**N_NT(n) = n^(n·z)**

Even for very small values of n, this number becomes transcomputational — exceeding the number of computations that could be performed by all the matter in the universe in all of time (Bremermann's limit: ~10^93 bits processed per second per gram).

For example, with n = 4 inputs/outputs and z = 4 internal states: N_NT = 4^16 = 4,294,967,296. But the number of possible non-trivial machines grows so fast that exhaustive analysis becomes physically impossible.

This means: **given an arbitrary non-trivial machine, there is in general no feasible procedure to determine its internal structure from observation of its input-output behavior.** The machine is analytically undecidable.

### Von Foerster's Critique of Trivialization

Von Foerster argued that Western science, education, and social systems systematically **trivialize** non-trivial machines:
- Education trivializes children by demanding predictable (correct) answers.
- Bureaucracy trivializes people by forcing them into predictable roles.
- Positivism trivializes nature by assuming it is a trivial machine.

Three responses to the existence of non-trivial machines:
1. **Ignore the problem** (pretend everything is trivial)
2. **Trivialize the world** (force non-trivial systems into trivial descriptions)
3. **Develop an epistemology of non-triviality** (what von Foerster advocates — second-order cybernetics)

Even if some systems "out there" are trivial, our cognitive system is certainly non-trivial, so everything we experience is filtered through a non-trivial machine. Triviality is an approximation — useful (like Newtonian mechanics) but fundamentally incomplete.

---

## 5. Self-Reference and Circular Causality: The Logical Structure

### Circular Causality in Cybernetic Systems

The arrangement in cybernetic systems is circular: A causes B, B causes C, C causes A. There is causality, but it is circular and has no primary cause, no ultimate origin.

This is not merely a feedback loop in the engineering sense. Von Foerster emphasizes that circular causality implies:

1. **No privileged starting point**: any node in the circuit can be taken as "the cause." The choice is a decision of the observer, not a property of the system.
2. **Self-determination**: the system's behavior is determined by its own structure, not by external inputs alone.
3. **Autonomy**: operationally closed systems generate their own laws of behavior.

### The Logical Structure of Self-Reference

Von Foerster's "purest form" — A implies A — is the structure of self-reference. But this is not a tautology. In the context of operations and processes, "A implies A" means: the operation, when applied to its own result, reproduces that result. This is precisely the eigenform equation O(X) = X.

Self-reference is productive, not vacuous. It generates:
- **Stability** (fixed points / eigenforms)
- **Paradox** (when no fixed point exists in the given domain — cf. Russell's paradox, the Liar)
- **Undecidability** (Gödel's incompleteness — self-referential sentences that can be neither proved nor disproved)

### Spencer-Brown's Laws of Form

Von Foerster was deeply influenced by G. Spencer-Brown's *Laws of Form* (1969), which provides a calculus of distinctions. The fundamental operation is **making a distinction** — drawing a boundary that separates a marked state from an unmarked state.

Spencer-Brown's calculus has two axioms:
1. **Law of Calling**: Marking a mark = the mark. (Idempotency)
2. **Law of Crossing**: Crossing a boundary twice = not crossing it. (Involution)

When Spencer-Brown allows **re-entry** — a form that re-enters its own boundary — the calculus becomes self-referential. The re-entry form is the formal model of self-reference in this framework. It produces equations like:

**f = ¬f** (a form that is its own negation)

This has no solution in classical Boolean logic (it oscillates between true and false). Spencer-Brown interprets it as **imaginary values** — analogous to √(-1) in mathematics. Varela extended this into a "calculus of self-reference" with a third value (autonomous state) beyond true and false.

### Von Foerster's Use of Self-Reference

Von Foerster applied self-referential logic to:
- **Cognition**: "I am the observed relation between myself and observing myself" (his definition of "I")
- **Knowledge**: knowledge of knowledge = understanding (the title *Understanding Understanding*)
- **Communication**: the eigenbehavior of a doubly closed recursive system
- **Ethics**: the observer who recognizes their own participation in the system cannot escape responsibility (see §6)

---

## 6. The Ethical Imperative

### Von Foerster's Statement

"**Act always so as to increase the number of choices.**"

Alongside:
- **Aesthetic Imperative**: "If you desire to see, learn how to act."
- **Therapeutic Imperative**: "If you want to be yourself, change!"

### How This Follows from Second-Order Cybernetics

The derivation is not a logical proof in the deductive sense, but a rigorous argument from the structure of second-order cybernetics:

#### Step 1: The Problem of Objectivity

First-order cybernetics claims objectivity: the observer describes the world as it is, without the observer's properties entering the description. But this reduces the observer to a "copying machine" — and with it, eliminates the concept of **responsibility**. If I am merely recording what is objectively the case, I bear no responsibility for what I report. I am compelled by the facts.

Von Foerster: "With the essence of observing removed, the observer is reduced to a copying machine, and the notion of responsibility has been successfully juggled away."

#### Step 2: Decidable vs. Undecidable Questions

Drawing on Gödel's incompleteness theorems (1931), von Foerster distinguishes:

- **Decidable questions**: already decided by the framework in which they are asked. "Is 3,396,714 divisible by 2?" — the rules of arithmetic decide this. We merely apply the algorithm.
- **Undecidable questions** (in principle): no framework, no algorithm, no set of rules can decide them. They require a **decision** by the observer/agent.

Von Foerster's "metaphysical postulate": **"Only those questions that are in principle undecidable, we can decide."** Decidable questions are decided by the framework — we merely compute. It is only when we face genuine undecidability that we exercise **choice**.

#### Step 3: Freedom and Responsibility

"We are under no compulsion, not even that of logic, when we decide upon in principle undecidable questions. There is no external necessity. We are free."

But: "The complement to necessity is not chance — it is **choice**."

And: with choice comes responsibility. We become responsible for whatever we choose, because nothing forced us to choose it. We become "metaphysicians" whenever we decide an undecidable question — we make a foundational commitment that cannot be justified by appeal to external facts or logical necessity.

#### Step 4: The Ethical Imperative

Given that:
- Second-order cybernetics reveals the observer as participant, not spectator
- Many fundamental questions are undecidable
- Undecidable questions require genuine choice
- Choice implies responsibility

The ethical imperative follows: **act so as to increase the number of choices** — both for yourself and for others. This maximizes the domain of freedom and responsibility. It is anti-authoritarian (authority reduces choices) and anti-dogmatic (dogma forecloses choices).

#### Connection to Wittgenstein

Von Foerster explicitly invokes Wittgenstein's *Tractatus*, proposition 6.421: "It is clear that ethics cannot be put into words." Ethics is not a set of propositions. Ethics cannot be articulated as a theory. Ethics must be **acted**. The ethical imperative is not a rule to follow but a principle that emerges from the structure of observation itself.

---

## 7. Constructivism: Knowledge as Construction

### The Formal Argument

Von Foerster's constructivism is not mere philosophical posturing. It follows from the formal structure of second-order cybernetics:

#### (a) The Cognitive Process as Computation

In "Cybernetics of Epistemology," von Foerster argues: if epistemology is the theory of knowledge **acquisition** (not knowledge per se), then the appropriate framework is cybernetics — the only discipline with a rigorous treatment of circular causality.

Cognitive processes are interpreted as **computational algorithms which are themselves being computed**. This leads to:
- Computations that compute computations
- Recursive structures of arbitrary depth
- The question: what are the stable outputs (eigenbehaviors) of these recursive computations?

#### (b) The Impossibility of Objective Description

Natural scientists from Einstein to Heisenberg recognized: there is no objective description of the world in which there are no subjects. This is not a philosophical preference — it follows from:
- Quantum mechanics (the measurement problem — the observer's choice of measurement apparatus determines what can be observed)
- Gödel's incompleteness (no formal system can completely describe itself)
- The logical structure of observation (the observer is part of the system being described — self-reference)

#### (c) The Constructivist Conclusion

Knowledge is not a representation of a pre-given external reality. Knowledge is a **construction** by the observer, emerging as the eigenform of recursive interactions between organism and environment.

This does not deny reality. It denies that we have access to reality independent of our processes of knowing. The map and the territory are "conjoined" — we cannot examine one without the other.

#### (d) Preparatory Cognitive Apparatus

A Kantian point formalized: preparatory cognitive apparatus must already be present to construct the meaning of incoming data. Without these constructional "devices" (analogous to Kant's transcendental categories), we cannot experience anything at all. In experience, all we experience is the subjective schemas with which we construct the world — but these schemas are themselves shaped by what they encounter (eigenform again).

---

## 8. Connections to Other Formal Systems

### 8.1 Gödel's Incompleteness Theorems

Von Foerster drew extensively on Gödel's 1931 result. The connection:

- Gödel showed that any sufficiently powerful formal system contains statements that are **true but unprovable** within the system. The proof relies on self-reference: constructing a sentence that says "I am not provable in this system."
- Von Foerster generalizes: any system that describes itself will encounter undecidable propositions. This is not a bug but a fundamental feature of self-referential systems.
- The "undecidable questions" in his ethics argument are the existential/practical analog of Gödelian undecidable propositions.
- Kauffman makes the connection explicit: Gödelian self-reference and eigenforms are instances of the same underlying structure — self-application producing fixed points (or paradoxes when no fixed point exists).

Lawvere's categorical fixed-point theorem unifies: Gödel's incompleteness, Cantor's diagonal argument, Turing's halting problem, and the eigenform construction are all instances of the same categorical structure involving self-application and fixed points in cartesian closed categories.

### 8.2 Quantum Mechanics and the Observer Problem

The parallels are deep and were recognized by von Foerster and his circle:

1. **The measurement problem**: In quantum mechanics, the act of measurement (observation) collapses the wave function. The observer's choice of measurement apparatus determines which observable is measured. The observer is not external to the system.

2. **Eigenstates as eigenforms**: In quantum mechanics, the eigenstates of an observable are those states that are unchanged by measurement of that observable. The eigenvalue equation Ĥ|ψ⟩ = E|ψ⟩ is formally identical in structure to O(X) = X. Kauffman explicitly argues that quantum eigenstates are "particular examples of eigenforms."

3. **Complementarity and undecidability**: Bohr's complementarity principle (you cannot simultaneously measure position and momentum with arbitrary precision) has a structural analog in Gödelian undecidability. Wheeler asked Gödel directly whether there was a connection between incompleteness and the uncertainty principle (Gödel reportedly threw him out of his office).

4. **Self-referential physics**: Any universal physical theory must account for the observer as part of the universe. But Gödel's theorem implies that a self-referential description is necessarily incomplete. This suggests that physics, like mathematics, faces fundamental limits — not from lack of ingenuity but from the logical structure of self-reference.

5. **The "quantum Gödelian hunch"** (Dourdent, 2020): Quantum contextuality can be interpreted as having a Liar-paradox-like logical structure, and the measurement problem can be seen as a self-referential problem analogous to Gödelian self-reference.

### 8.3 Spencer-Brown and the Calculus of Indications

Spencer-Brown's *Laws of Form* provided a formal calculus that von Foerster and Varela used extensively:

- The **mark of distinction** (☐ / ☐̄) is the primordial act of cognition — making a distinction.
- The **re-entry** of the form into itself (a form that crosses its own boundary) formalizes self-reference.
- Varela extended this to a **calculus of self-reference** with three values: marked, unmarked, and autonomous (self-referential).
- This provides a formal alternative to Boolean logic for modeling systems where the observer is part of what is described.

### 8.4 Autopoiesis (Maturana and Varela)

Von Foerster's work directly influenced Maturana and Varela's concept of **autopoiesis** — the self-production of living systems. Autopoietic systems are operationally closed: they produce the components that produce them (circular causality). An autopoietic system is itself an eigenform — a structure that reproduces itself through its own operations.

### 8.5 Gödel Agents (Contemporary Extension)

Recent work on "Gödel Agents" formalizes the idea of self-referential computational systems whose architecture embodies the limitations identified by Gödel's theorems: no agent can attain universal completeness in prediction, control, or explanation due to logical and learnability incompleteness. This is the contemporary computational embodiment of von Foerster's non-trivial machine concept.

---

## 9. Summary: The Architecture of Second-Order Cybernetics

The formal structure can be summarized as follows:

1. **Observation is operation**: To observe is to compute, to act, to transform. Not passive reception.
2. **Operations are recursive**: Observations of observations, descriptions of descriptions, computations of computations.
3. **Recursion produces stability**: The fixed points of recursive operations are eigenforms — the "objects" of our world.
4. **Stability requires closure**: Operational closure (double closure, topologically a torus) is the condition for stable eigenforms to emerge.
5. **Closure implies self-reference**: A closed system refers to itself. This is logically productive (generates eigenforms) but also generates undecidability (Gödel).
6. **Undecidability implies choice**: Where questions are undecidable, we must decide. Decision is not compulsion — it is freedom.
7. **Freedom implies responsibility**: We are responsible for our undecidable decisions because nothing compelled us.
8. **Responsibility implies ethics**: "Act always so as to increase the number of choices."

This is the chain from mathematics to ethics that constitutes second-order cybernetics as a complete intellectual framework — not merely a technical discipline, but an epistemology and an ethics grounded in the formal structure of self-reference.

---

## 10. Open Questions and Critiques

- **The ethical imperative is vague as stated.** "Increase the number of choices" for whom? In what domain? It is anti-authoritarian in spirit, but it does not address conflicts between agents whose choices are mutually exclusive. Some scholars (cf. "Undeciding the Decidable," ISSS 2021) argue that decidable decisions embedded in unjust structures must also be challenged — the imperative is necessary but not sufficient.

- **The constructivism is radical.** It risks solipsism if not carefully stated. Von Foerster avoids this by insisting that eigenforms arise from interaction with an environment — they are not purely subjective fantasies. But the formal apparatus does not clearly distinguish between stable delusions and veridical perception. The criterion is operational stability, not correspondence truth.

- **The connection to quantum mechanics is suggestive but not rigorous.** The structural parallels (eigenstates / eigenforms, measurement problem / observer inclusion) are real, but whether they reflect a deep mathematical unity or merely a surface analogy remains debated. Kauffman's work pushes this furthest, but it remains more framework than theorem.

- **Non-trivial machines are "analytically undecidable" but this needs qualification.** The transcomputational argument shows that exhaustive analysis is infeasible, not that no information can be extracted. In practice, we make useful (if incomplete) models of non-trivial machines all the time. The point is that such models are always approximations — trivializations — not the thing itself.
