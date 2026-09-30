# Survey: computation in Rule 110, and what it tells a non-CTS design

Author: scholar (team noncts). Started 2026-09-30.

Scope. What is actually known about computing with Rule 110, which theory
applies to glider systems in one dimension, and what that implies for the
team's goal: a computer in Rule 110 that is not an emulation of a cyclic tag
system (CTS).

Sourcing rule. Every entry below marked **[read]** was read by me in full
text (PDFs in the scratchpad, text-extracted); quotes are from that text.
Entries marked **[abstract]** were read only as abstract or search snippet.
Entries marked **[memory]** are from memory and unverified. Claims that I
re-checked by simulation are marked **[sim]** with the script that checks
them (all in `noncts/scholar/`).

---

## 1. Summary

1. **Every complete universality construction for Rule 110 that I could
   find emulates a cyclic tag system.** Cook's original (2004) and explicit
   (2009) constructions, Richard's formal re-proof (2008), Neary and Woods'
   P-completeness proof (2006), and the Martinez-Adamatzky-McIntosh
   "collider" (2016) all go through a CTS. No published Rule 110 computer is
   built on a counter machine, a Turing-machine head, or logic circuits.
2. **The non-CTS constructions that do exist in the literature are
   fragments**: glider "objects" (eaters, "black holes", flip-flops, a
   one-shot NOT gate) in Martinez et al. (2006), and reversible logic gates
   in a *different* automaton (ECA Rule 22 with memory; Martinez-Adamatzky-
   Morita 2018). None is cascadable or reusable in Rule 110.
3. **Whether Rule 110 is intrinsically universal is open** (Ollinger 2009;
   Richard 2008). Cook's construction cannot give intrinsic universality,
   because it only destroys particles and must be fed from infinite periodic
   streams (Richard 2008).
4. **The closest theory is abstract geometrical computation (signal
   machines, Durand-Lose).** Two results constrain designs: signal machines
   with two speeds perform at most quadratically many collisions; with three
   speeds and only rational ratios (which is always the case in a CA) the
   dynamics is cyclic, so a signal machine needs at least four speeds to be
   universal from a finite configuration (Becker et al. 2013, reporting
   Durand-Lose 2013). Whether this transfers to Rule 110 gliders (which have
   extent, phase and delayed collisions) is my argument, not a theorem.
5. **Rule 110 offers a phase-free sub-chemistry.** A, B against C1, C2, C3,
   D1, D2 each collide in exactly one way, so their outcomes do not depend
   on timing. This is the same property that made Ollinger and Richard's
   4-state intrinsically universal automaton easy to prove correct. **[sim]**

The rest of this document gives the evidence for each point, one work at a
time, and then the implications (section 7).

---

## 2. The CTS constructions

### 2.1 Cook 2004, "Universality in Elementary Cellular Automata" **[read]**

Complex Systems 15(1):1-40. The first full proof (construction 1994,
published 2004).

What it shows:

- A chain TM -> 2-tag system (Cocke-Minsky) -> CTS -> "glider system" ->
  Rule 110. The glider system (s.2.3) is an idealized 1-D particle model:
  finitely many glider types, each with a fixed velocity, and a collision
  lookup table. Cook uses it to explain the design, then realises it in
  Rule 110.
- The design (s.2.3): tape data = stationary gliders; the appendant list =
  a periodic stream from the right ("table data" led by "leaders");
  "ossifiers" = a periodic stream from the left. A leader hitting a tape Y
  makes an *acceptor* that converts table data into *moving data*; hitting
  an N makes a *rejector* that deletes table data. Moving data crosses the
  tape and is turned into new tape data by an ossifier.
- The glider catalog (Fig. 4): A, A^n, B, Bbar_n, Bhat_n, C1, C2, C3, D1,
  D2, E_n, Ebar, F, G_n, H, and a glider gun that "emits A and B gliders
  once per cycle". Periods (Fig. 5), in (t, x): A (3,2), B (4,-2), Bbar and
  Bhat (12,-6), C (7,0), D (10,2), E (15,-4), Ebar (30,-8), F (36,-4), G
  (42,-14), H (92,-18), gun (77,-20). **[sim]** `verify_phases.py`.
- Two structural facts used throughout (s.3.1):
  - *Width.* Each glider shifts the ether on its right relative to the ether
    on its left by w (mod 14). "The sum of the widths of several adjacent
    gliders, mod 14, ... is a conserved quantity that is not affected by
    collisions." Hence the number of odd-width gliders is conserved mod 2.
    Width is a charge: any reaction that violates it is impossible.
  - *Collision count.* With periods written in units of the A and B periods,
    (pa, pb) and (qa, qb), two gliders can collide in exactly
    |pa*qb - pb*qa| ways. Equivalently |det(P_X, P_Y)| / 14 in (t, x)
    coordinates. **[sim]** `classes.py`, `class_check.py`.
- Speed limits: A and the B family travel at the maximum right and left
  speeds possible in the ether; "A is the only possible glider that can
  travel to the right faster than a D."
- Data crossing (s.3.2.3): "This phenomenon of spacing preservation
  provides a neat solution to one of the main obstacles in one dimensional
  computation: The problem of getting data to cross over other data. By
  representing data in terms of spacings between gliders of the same type,
  we can enable data travelling at two different speeds to cross without
  interference, all using just one single type of crossing collision." Cook
  explicitly warns against encoding different values by different glider
  types, since every pair of types would then need its own crossing.
- Cook's methodological advice (s.3): use only gliders that arise
  naturally, because data crossing in 1-D destroys and recreates gliders
  "as if by chance".

### 2.2 Cook 2009, "A Concrete View of Rule 110 Computation" **[read]**

EPTCS 1:31-55, arXiv:0906.3248. An explicit compiler TM -> tag -> CTS ->
Rule 110 bit blocks (A-L), which the parent project implements.

Relevant for us:

- "All the collisions (at a glider cluster level) in this construction are
  between Ebar material ... on the right and either C2 material (tape data)
  or A material (ossifiers, acceptors, rejectors) on the left." The whole
  construction uses five reaction families: ossifier x moving data or
  invisibles; tape data x moving data or invisibles (crossing); tape data x
  prepared leader; acceptor/rejector x table data; acceptor/rejector x raw
  leader.
- Correctness depends only on spacings mod small numbers: C2 x Ebar on the
  "over distance" mod 4, A x Ebar on the "up distance" mod 6.
- A4 x Ebar: of the six collisions, three make a C2 (the one at "up 5" is
  used for ossification), one ("up 0") is a clean crossing, which is how
  "invisibles" pass through ossifiers. **[sim]** `cookA4.py` reproduces
  3 / 1 / 2 (the remaining two classes give Bbar^2 + F).
- The periodic left side needs a bound on consecutive rejections; without
  one, "a more complicated left hand side will work, where the value of v
  increases linearly with each ossifier".
- A remark on the design history: a 1994 version failed a parity equation
  ("the equation of invisibility after rejection") and was fixed within
  weeks; the 1998 changes were compaction choices, not error fixes.

### 2.3 Richard 2008, "Rule 110: universality and catenations" **[read]**

JAC 2008. A second, formal proof of Turing universality using Ollinger-
Richard *catenation schemes* (planar maps whose vertices are collisions and
edges particles). It uses 18 particles and 23 collisions and again a
cyclic Post tag system (words of length a multiple of 6, bounded runs of
0-reads).

- Tool worth knowing: "Given a finite catenation scheme, the set of valid
  affectations is a computable semi-linear set" (Ollinger-Richard). In our
  terms: for a fixed diagram of collisions, the admissible glider spacings
  form a semi-linear set that can be computed, i.e. the spacing constraints
  of a gadget are linear equalities and congruences.
- Conclusion (quoted): the construction "does only erase particles without
  creating it, thus having the need to be continually feed with particles.
  This need of 'fuel' is not compatible with intrinsic universality. One
  open question is whether or not rule 110 is intrinsically universal."

### 2.4 Neary and Woods 2006, "P-completeness of cellular automaton Rule 110" **[read]**

ICALP 2006, LNCS 4051. Replaces the exponentially slow 2-tag layer by a
*clockwise Turing machine*, giving the chain TM -> clockwise TM -> CTS ->
Rule 110 with polynomial overhead; hence Rule 110 prediction is P-complete.
Still CTS at the Rule 110 level. (The parent project uses this chain.)

### 2.4b Neary and Woods 2007, "Small weakly universal Turing machines" **[read, abstract and intro]**

arXiv:0707.4489. (6,2), (3,3), (2,4) machines that are weakly universal
because they simulate Rule 110. Their universality therefore rests on
Cook's CTS construction as well. Relevant as a warning: "a TM in Rule 110"
built from such a machine would be circular (Rule 110 -> TM -> Rule 110)
and still CTS underneath. The intro also records that most small UTMs
simulate 2-tag or bi-tag systems (Minsky, Rogozhin, Neary-Woods), so a
direct TM design in Rule 110 should compile a TM that is not itself a tag
simulator if the aim is to avoid tag systems entirely.

### 2.5 Martinez, Adamatzky, McIntosh 2016, "A Computation in a Cellular Automaton Collider Rule 110" **[read]**

arXiv:1609.05240. Re-codes Cook's CTS with Martinez's phase notation
(left: {649e-4A4(Fi)}*, centre, right: SepInit/1BloP/0Blo/1BloS blocks) and
proposes running it in coupled rings ("cyclotrons"). The "flip-flop" in the
paper is a periodic oscillation of 16 particles, not a memory. No non-CTS
computation.

Useful byproduct: the paper gives a glider table (velocities, including
gun -20/77) and explains the phase notation f_i_1 and "X-ne-Y" initial
conditions, which I use in `r110check.py`.

---

## 3. Glider catalogs and "objects" (Martinez, McIntosh, Seck-Tuoh-Mora, Chapa)

### 3.1 Phase strings ("regular language of gliders") **[read + sim]**

Martinez et al. derive, from de Bruijn diagrams and tilings, a string for
every phase of every glider, all embedded in the same ether alignment
(arXiv:0706.3348; list at comunidad.escom.ipn.mx/genaro/rule110/
listPhasesR110.txt, saved as `data/listPhasesR110.txt`).

- **[sim]** All 287 non-gun strings are exact gliders with Cook's periods
  and a single defect (`verify_phases.py`, output in
  `data/verify_phases.out`). One label is wrong: "B(A,f4_1)" is a Bbar.
- The de Bruijn analysis distinguishes the tight bundle A^n (built on
  (1110)*) from "nA" = n A's separated by one T3 tile ((111110)*). Cook's
  ossifier A4 is the tight bundle. **[sim]** `cookA4.py`.
- Gun strings: the gun moves at (77,-20) and emits one A to the right per
  period (about 71 cells apart) plus left-moving debris. **[sim]**

### 3.2 Solitons (clean crossings) **[read + sim]**

Martinez, Adamatzky, Chen, Chua, "On soliton collisions between
localizations in complex ECA: Rules 54 and 110 and beyond" (Complex Systems,
arXiv:1301.6258), s.3.1 lists 18 binary soliton collisions in Rule 110:
A x G, C1 x Ebar (2), F x B, C2 x Ebar, C1 x F, C2 x F, A x Ebar (4),
F x Ebar (7). **[sim]** all 18 verified (`python r110check.py`).

They also report a "pseudo-soliton": F x Bbar -> {B, F} and F x B -> {Bbar,
F}, so B and Bbar convert into each other when they cross an F (a travelling
bit that can be flipped by a stationary-ish F). Collider's catalog confirms
F+B -> F+Bbar and F+Bbar -> F+B in particular classes.

### 3.3 "Rule 110 objects and other collision-based constructions" (J. Cellular Automata, 2006) **[read]**

A zoo of multi-glider objects:

- *Black holes* (objects that periodically absorb A and B gliders and
  regenerate): C3 +B-> E +A-> C3; D1 +B-> E +A-> D1; C1 +B-> C2 +A-> C1;
  C2 +A2-> F +B2-> C2. **[sim]** the single-glider steps are verified and
  are phase-independent (section 6).
- *Eaters*: D1 + A^3 deletes Ebars; D2 + A^2; C1 + A^5; an A deleting a
  pair of Ebars, and several more.
- *Fuses*, and two *flip-flops* that the authors say are "not reusable".
- A "simple NOT gate", described as "the device cannot be employed again".

These are the only published non-CTS computational fragments in Rule 110
that I found. None is cascadable: the authors state the reusability
limitation themselves.

### 3.4 "Gliders in Rule 110" (IJUC 2006) and "Production of gliders by collisions in Rule 110" (LNCS 2801, 2003) **[abstract; PDFs downloaded, skimmed]**

Catalog of gliders and of collisions that produce each glider; D2, H and the
gun "cannot be obtained through simple binary collisions" but the gun can be
produced by multiple collisions. I have not checked the production claims.

### 3.5 Logic gates with gliders: a different automaton **[read]**

Martinez, Adamatzky, Morita, "Logical Gates via Gliders Collisions" (2018,
arXiv:1803.05496): NOT, AND, NAND, majority, CNOT and Fredkin gates, **in
ECA Rule 22 with majority memory of depth 4**, not in Rule 110. Two
caveats matter if anyone cites it as precedent: the gliders' initial
placement ("flags" and "mirrors") is chosen *depending on the input values*
(Table 3), and the authors note that auxiliary gliders "can be reused only
when crossing periodic boundaries". So it is a one-shot demonstration, not a
cascadable circuit family.

Gupta 2026, "Collision-based logic in Lenia and its composition boundary"
(arXiv:2609.01348) **[read, abstract and intro]** makes the general point
explicit for another substrate: a gate is easy, composition (delivering a
deflected signal to a downstream gate) is the hard part.

---

## 4. Universality theory for one-dimensional CA

### 4.1 Intrinsic universality (Ollinger 2009; Ollinger-Richard 2011) **[read]**

- Ollinger, "Intrinsically universal cellular automata" (arXiv:0906.3213):
  definitions via bulking; intrinsic universality implies Turing
  universality but not conversely; it is undecidable. Quote: "a careful
  study of the set of collisions used show that, contrary to what is claimed
  by Wolfram, the construction cannot be used to prove intrinsic
  universality of rule 110. Open Problem 8. Is rule 110 intrinsically
  universal?"
- Ollinger and Richard, "Four states are enough!" (TCS 2011): a 4-state,
  radius-1 intrinsically universal CA built with particles and collisions.
  Design elements worth copying:
  - it suffices to simulate *one-way* CA;
  - a stationary "border" particle delimits each simulated cell; the rule
    table is a signal R whose *spacings* encode an array of integers; the
    cell states are unary counts of particles; the sum of two states selects
    the entry of R by *altering that many particles of a mirror copy of R*.
    The rule signal is re-emitted each block, so nothing is consumed
    (no fuel problem).
  - Lemma 8: with their particles, "When two of the particles (or signals)
    described above collide, occurring collision is always the same",
    because the repetition vectors admit only one relative position. This
    removes all timing analysis. Rule 110's A/B-versus-C/D reactions have
    the same property (section 6).

### 4.2 Small universal CA via particles (Lindgren-Nordahl 1990) **[read]**

Complex Systems 4:299-318. A 7-state radius-1 universal CA: the TM head is a
left- or right-moving two-cell particle carrying the state; tape symbols are
stationary single cells. The rule table is *designed* so that the 2|Q||Sigma|
head-symbol collisions do the right thing; tape symbols are shifted by two
cells when the head passes, and the head reflects when it changes direction.
This is the template for a "direct TM" design; in Rule 110 the rule cannot be
designed, so every head-symbol reaction would have to be found. Their closing
remark: in their CA, particles "are either stationary or propagate with one
particular speed", and "it is an open question how to characterize the
behavioral complexity of rules with more complex sets of particles".

### 4.3 Signal machines (abstract geometrical computation, Durand-Lose) **[read]**

A signal machine is exactly Cook's "glider system" in continuous space:
finitely many meta-signals with fixed speeds, collision rules.

- Durand-Lose, "Small Turing universal signal machines" (arXiv:0906.3225):
  universality via TMs (1 signal per tape symbol, 2 per state, up to 2
  rules per transition), via CA, and via CTS (the smallest: a CTS machine
  with speeds {-2, 0, 1, 2}); a 13-signal halting universal machine. He notes
  that Turing universality was first proved "by reduction from 2-counter
  automata" (Durand-Lose 2005) **[abstract only for the 2005 paper]**, and
  that CTS "provide the best bounds".
- Becker, Chapelle, Durand-Lose, Levorato, Senot, "Abstract geometrical
  computation 8" (arXiv:1307.6468), conclusion, quoted: "The computing power
  of 2-speed signal machines is very limited since the length of a
  computation is at most quadratic in the number of signals in the initial
  configuration. The last constructions in [Durand-Lose, 2011], provides a
  Turing-universal signal machine with four speeds. The case of 3 speeds has
  been studied in [Durand-Lose, 2013]: the same dichotomy arises. In the
  rational-like case, the dynamics is cyclic with bounded transient time and
  period; otherwise, any Turing machine could be simulated."
  The CiE 2013 paper itself ("Irrationality is needed to compute with signal
  machines with only three speeds") is behind an anti-bot wall; I have only
  its abstract **[abstract]**.

Relevance, with a caveat. In a CA all speeds and distances are rational, so
if Rule 110 glider dynamics were a faithful signal machine, a *finite*
arrangement using only three glider speeds could not be universal. The
transfer is not automatic: CA gliders have extent and phase, collisions take
time and emit products with offsets, and a "finite configuration" in Rule 110
can contain a gun, which is an unbounded source. Cook's construction avoids
the hypothesis anyway: it uses *infinitely many* signals (periodic streams)
with essentially three speeds (A 2/3, C 0, Ebar -4/15).

### 4.4 Wolfram, A New Kind of Science (2002) **[read, online pages only]**

p.678: the proof goes through cyclic tag systems. The notes for s.6.8 state
that "The periodicity of the background forces all rule 110 structures to
have periods and distances given by {4, -2} r + {3, 2} s where r and s are
non-negative integers", i.e. every velocity lies between -1/2 and 2/3. The
notes for s.11.8 give `CTToR110`, blocks of lengths {105736, 34717, 95404}
for the simplest example. I could not retrieve the history notes (p.1115);
Cook 2009 disputes one of them (see 2.2).

---

### 4.5 Other recent items **[read or abstract as marked]**

- Martinez, Seck-Tuoh-Mora, Zenil, "Computation and universality: class IV
  versus class III cellular automata" (J. Cellular Automata 2013,
  arXiv:1304.1242) **[read, Rule 110 section]**: reviews Rule 110; its
  computation section is again Cook's CTS.
- `novaspivack/rule110-lean` (GitHub) **[abstract, via a web summary of the
  README; not checked]**: a Lean formalization of Cook's CTS construction,
  described as partial ("five named Cook bridge axioms remain unproven").
  Also CTS.

## 5. What is *not* in the literature (as far as I found)

- No Rule 110 construction of a counter machine, a TM with a head particle,
  a register, or a reusable gate.
- No proof that a non-CTS construction is impossible, and no general
  "one-way transparency" theorem for 1-D glider systems. The nearest
  statements are Cook's remark that data crossing is "one of the main
  obstacles in one dimensional computation" and Richard's fuel remark.
- No result on Turing universality of Rule 110 from *finite*
  configurations (ether plus finitely many defects). All constructions use
  infinite periodic sides. Guns exist, so this is not excluded.
- No complete catalog of multi-glider (three or more) collisions in Rule 110.
  The binary catalog exists (Martinez-McIntosh "Atlas" 2001, which I have not
  obtained **[memory]**; collider's catalog now covers all binary pairs of
  the base gliders).

---

## 6. Re-checked facts that the team relies on **[sim]**

All scripts in `noncts/scholar/`.

| fact | check | script |
|---|---|---|
| 287 phase strings are exact gliders with Cook's periods | 364 strings run; all non-gun match | `verify_phases.py` |
| 18 Martinez solitons are clean crossings | 18/18 | `r110check.py` |
| number of classes = abs(det)/14; outcome is a function of class | C1, C2, C3, A x Ebar | `class_check.py` |
| Cook's A4 x Ebar: 3 x C2, 1 crossing, 2 other | 60 configurations | `cookA4.py` |
| single-class (phase-free) reactions | all phase pairs | `unique_pairs.py` |

Single-class reactions (A enters from the left, B from the right):

    A + C1 -> F      A + C2 -> C1     A + C3 -> C2
    A + D1 -> C2     A + D2 -> D1     A + B  -> (nothing)
    C1 + B -> C2     C2 + B -> D1     C3 + B -> E
    D1 + B -> E      D2 + B -> A + Ebar

Collider and architect found the same table independently.

---

## 7. Implications for the team (interpretation, not established results)

The detailed argument is in `THEORY.md`; the short version:

1. **Why Cook chose a CTS.** In Cook's geometry the store (tape data) is
   written at its back by the left stream and read at its front by the right
   stream. A store accessed at both ends is a queue, and a queue with a
   trivial control is a (cyclic) tag system. Anything that is not a queue
   needs either a second store or a way for information to cross a store in
   the direction it does not naturally pass.
2. **The phase-free sub-chemistry is the best foundation for new gadgets**,
   because correctness then needs no spacing arithmetic.
3. **Counting speeds**: a finite seed (no periodic streams) should use at
   least four glider speeds if the signal-machine theorem transfers; with
   periodic streams three can suffice (Cook).
4. **Program-independence**: in a fixed CA the set of reactions is fixed, so
   the program must be data. A direct TM whose transitions are individual
   reactions (Lindgren-Nordahl style) needs a new reaction per transition;
   only a fixed small universal machine keeps that finite.

## References (with URLs actually used)

- M. Cook, Complex Systems 15 (2004) 1-40,
  content.wolfram.com/sites/13/2023/02/15-1-1.pdf
- M. Cook, EPTCS 1 (2009) 31-55, arXiv:0906.3248
- G. Richard, JAC 2008, richardg.users.greyc.fr/publis/Richard_2008a.pdf
- T. Neary, D. Woods, ICALP 2006, dna.hamilton.ie/assets/dw/NearyWoodsBCRI-04-06.pdf
- G. J. Martinez, A. Adamatzky, H. V. McIntosh, arXiv:1609.05240
- G. J. Martinez, A. Adamatzky, F. Chen, L. Chua, arXiv:1301.6258
- G. J. Martinez, H. V. McIntosh, J. C. Seck-Tuoh-Mora, S. V. Chapa Vergara,
  "Rule 110 objects and other collision-based constructions", J. Cellular
  Automata (2006), comunidad.escom.ipn.mx/genaro/Papers/Papers_on_CA_files/objectsR110.pdf
- G. J. Martinez et al., arXiv:0706.3348 (phases), phase list URL above
- G. J. Martinez, A. Adamatzky, K. Morita, arXiv:1803.05496
- N. Ollinger, EPTCS 1 (2009) 199-204, arXiv:0906.3213
- N. Ollinger, G. Richard, "Four states are enough!", TCS 412 (2011),
  richardg.users.greyc.fr/publis/Ollinger-Richard_2011.pdf
- K. Lindgren, M. G. Nordahl, Complex Systems 4 (1990) 299-318,
  content.wolfram.com/sites/13/2018/02/04-3-4.pdf
- J. Durand-Lose, EPTCS 1 (2009) 70-80, arXiv:0906.3225
- F. Becker et al., arXiv:1307.6468
- S. Wolfram, NKS, wolframscience.com/nks/p678 and notes pages
- C. Gupta, arXiv:2609.01348
