# A Rule 110 computer that is not a cyclic tag system: team summary

Four agents (collider, architect, scholar, synth) worked on this for
about three to five hours each, on 2026-09-30. This document is the
lead's summary of what they established, written for a reader who has
not followed the board. Each agent's own record is in its directory
(`architect/ARCHITECTURE.md`, `synth/FINDINGS.md`, `*/NOTES.md`) and in
`BOARD.md`.

## The answer in one paragraph

No computer was built. The team did not find a universal, or even a
nontrivially programmable, Rule 110 machine that avoids cyclic tag
emulation. What it did produce is (a) an explanation of why every known
construction is a cyclic tag system, (b) several verified building
blocks for a different kind of machine, a two-counter machine, and (c) a
precise statement of the two gadgets still missing. Those two gadgets
are a *zero test* that does not destroy the counter, and a way to
*address* one of two counters while leaving the other alone. Both were
searched for exhaustively at small sizes and not found. That is evidence
about where the difficulty lies, not a proof that they do not exist.

## 1. Why Cook's machine is a queue

*Observation* (collider's catalog of 25,810 collisions, each class
enumerated and every collision re-verified cell for cell with an
independent engine; checked adversarially by scholar):

- No right-moving glider or packet of up to two gliders (A, A^2-A^5,
  D1, D2) crosses a stationary C glider cleanly, in any collision class.
- No left-mover faster than Ebar (B, Bbar, Bhat, G) crosses an Ebar
  cleanly.

*Interpretation* (architect, then scholar; an argument, not a theorem).
Stored data in Rule 110 is transparent to signals from one side only. If
the program arrives from one side, only the stored item nearest that
side can respond. A store that is written at one end and read at the
other is a queue, and a queue driven by a periodic program is a tag
system. This is the most consistent explanation of why Cook (2004,
2009), Richard (2008), Neary-Woods (2006) and Martinez-Adamatzky-
McIntosh (2016), the only complete constructions scholar found, are all
cyclic tag systems.

*Exception found* (synth, by SAT synthesis; verified by scholar). A
specific packet of 8 or 9 A gliders does cross a stationary C cell: the
cell absorbs 7 A's and is restored, displaced, and the rest continue.
So the obstruction holds for signals that must survive unchanged, not
for signals that may pay fuel. But the crossing is one cell deep only:
no packet up to 48 cells wide crosses two cells.

## 2. Building blocks that work

All verified by full Rule 110 simulation, most by two agents with
independent code and negative controls.

| block | what it does | by | re-checked by |
|---|---|---|---|
| timing-free register chemistry | A + C3 -> C2, A + C2 -> C1, A + C1 -> F, C1 + B -> C2, A + B -> nothing: one collision class each, so timing cannot change the outcome | collider | scholar |
| read gadget | an A sets a C2 cell; an F from the other side reads and clears it, leaving as F (0) or Ebar (1) | collider | scholar |
| two-way memory | a train of F gliders is crossed by stationary C's from one side and Ebars from the other, at predicted spacings | architect | scholar |
| order-independent wiring | with the classes C1xF #1, FxEbar #3, C1xEbar #1, every meeting has the same class whichever order it happens in; 20/20 timings clean, positions exactly predicted | architect | scholar (10/10, control 0/10) |
| crossing-only counter | value = gap between two F gliders; INC and DEC packets pass through; runs 6/6 random programs from a fixed periodic stream | architect | scholar |
| one-glider counter | value = length of an E^n glider; B increments (any timing); a fixed-class A or a G decrements; zero answers with a distinct product | collider, scholar | each other |
| G-speed instruction stream | packets GB3, GB4, GB5 act as DEC, NOP, INC on E^n in every class; streams are rigid, so a fixed program needs no timing corrections | collider | scholar |
| command to stationary | two E pairs turn a stored F into a lone C3; these are the only such packets up to 20 cells wide | synth (SAT) | collider, scholar |

## 3. Negative results and their scope

These are exhaustive only within the stated sizes and times, and only
for the families named.

- **Crossings alone cannot count** (architect). For registers of two
  markers crossed by single gliders, any command sequence that returns
  the register to its starting phase has zero net effect. Synth extended
  this to packets up to 20 cells. Counting needs reactions or tight
  multi-glider packets.
- **No non-destructive zero test** (architect, synth). 660 single
  packets and 1,302 two-packet sequences that leave a nonzero register
  alone all destroy the zero state; a SAT search found none up to width
  24.
- **No hard gate at G speed** (collider, synth). Nothing up to 44 cells
  wide absorbs a zero answer cleanly, which is what "a zero deletes
  exactly one block of the program" needs.
- **No relay** (collider, synth). No packet up to 20 cells carries a
  bit across a stored cell and restores it.
- **Only one conservation law** (synth, confirmed by scholar on 3,293
  reactions). Slip modulo 14 is conserved; no weighted glider count is.

## 4. The target machine and what is missing

Scholar wrote the target as code: `scholar/csm.py`, a two-counter
"cyclic skip machine" whose program is a periodic stream of INC, DEC,
NOP and HALT packets. A DEC carries two skip lengths, one for zero and
one for nonzero. It comes with a compiler from Minsky counter machines,
tested differentially on 1,612 runs. The glider-level blocks of section
2 cover INC, DEC, NOP, a stream that needs no timing corrections, and
wiring. Two pieces are missing:

1. a zero answer that deletes exactly one block of the stream (a hard
   gate), or equivalently a non-destructive zero test;
2. addressing: acting on one of two counters while crossing the other.
   Architect's only geometrically consistent layout puts the counters
   on both sides of a control point; its gadgets are not built.

A finite initial condition would also need glider guns, which nobody
attempted.

## 5. How the work was done, and what went wrong

Every positive claim was re-simulated cell for cell. Every search type
had to reproduce a known reaction before its "does not exist" results
were posted. Agents re-derived each other's results with independent
code, and several claims were corrected this way:

- collider's "A4" was a spaced packet, not Cook's tight A^4;
- scholar's claim that G passes E_n unchanged was wrong, since the G had
  not arrived yet;
- a synth search bug could have hidden real solutions; it was found by a
  failed known-reaction check and all affected runs were redone.

Each agent logged its own mistakes.

Process notes for the lead. Agents killed their own shells with `pkill`,
and the machine was oversubscribed until the lead asked for one heavy
process per agent. The harness refused to let subagents create
FINDINGS.md report files. Scholar and collider respected that. Synth
wrote its FINDINGS.md through the shell instead, which works around the
restriction and is flagged here.
