# Architecture: a two-counter machine in Rule 110 without a cyclic tag system

Author: architect. Status: design document, version 2. Section 8 lists
exactly what is verified and what is not; everything else is design or
argument and is labelled so.

## 1. Goal and target model

The goal is a Rule 110 computer that is not an emulation of a cyclic
tag system (CTS). The target model is a Minsky two-counter machine,
universal by Minsky's theorem through Turing machines, not tag systems.
The program is supplied the way Cook supplies his table: as a periodic
stream of left-moving packets from the right. The program counter is the
next packet that is not skipped. Scholar's `scholar/csm.py` fixes the
abstract machine ("cyclic skip machine": packets `INC r`,
`DEC r (skip_zero, skip_pos)`, `NOP`, `HALT`) and compiles Minsky
programs to it, differentially tested (1212 runs, 0 failures).

## 2. What the physics offers and forbids

### 2.1 One-way transparency of single gliders

The only right-moving gliders are A (2/3, and bundles) and D1, D2 (1/5).
None crosses a stationary C: A and B act on C's as a small phase-free
chemistry instead (A: C3 -> C2 -> C1 -> F, B: C1 -> C2 -> D1, A + B ->
nothing). And no left-mover faster than Ebar crosses an Ebar. So in the
lab frame stationary data is crossed only by left-movers, and in the Ebar
frame Ebar data is crossed only by right-movers.

Consequence: with the program arriving from the right and data stored in
stationary gliders, only the frontmost store can answer. Cook's machine
fits this exactly. In the Ebar frame it is a feed-forward sweep with one
store, a queue. A second store needs information to cross stored data in
both directions.

### 2.2 F memory

F (-1/9) is crossed from its left by C1 and C2 and from its right by
Ebar (and B). Three speeds make a bidirectional memory: the stream
(Ebar, -4/15) overtakes the memory (F, -1/9), which leaves messengers
(C, 0) behind. In F's rest frame, commands move left and messengers move
right, and both pass through stored F's.

### 2.3 The wiring layer ("lane")

A crossing displaces both partners, and when three families cross
pairwise, the order of meetings depends on timing. The lane is the unique
choice (among clean crossings) in which every meeting has the same class
whatever the order: C1 x F class 1, F x Ebar class 3, C1 x Ebar class 1.
Within the lane, any number of F's, C1 messengers and Ebars pass through
each other with exactly predictable phases (verified, section 8).

### 2.4 Counting needs more than single crossings

For a register made of two markers, single clean crossings change the
marker distance by an amount that is a function of the register's phase
residue: no sequence of single crossings pumps the distance (verified for
C1, C2 and F markers, section 8).

Tight Ebar pairs break this. Their effect on an F differs from that of
two independent Ebars (8 multi-body cases among 181 F x pair collisions),
and with them the distance does wind. The **crossing counter** below uses
this.

## 3. The crossing counter (verified component)

A register is two F's, T (front) and P (back). Its value n is encoded in
their seed difference D = seed(T) - seed(P) = (0,43) + n(-24,12), i.e.
a spatial gap of 43 + 9.33n cells.

- INC = three packets: Ebar pair (-26,27), Ebar pair (-11,37), Ebar pair
  (-1,25), each placed in a given class relative to T.
- DEC = Ebar pair (-26,27), Ebar pair (-4,23), single Ebar.

Every packet crosses both F's and continues left as Ebar-speed gliders
only; after INC or DEC the register is back in the same phase residue, so
the same packets work for every value. Nothing is created or destroyed.

Verified: INC^k for k = 1..6 and then DEC^k back down, every intermediate
state exact (section 8). DEC at n = 0 destroys the pair (the F's come too
close); a clean zero test is being searched (`ztest.py`).

Caveat that matters for the full machine: the packets were placed
relative to T's current position. T itself drifts, differently for INC
and DEC (modulo the class lattice they differ by exactly one lane Ebar's
displacement), so a fixed periodic stream needs balanced instructions:
every instruction must drift every marker by the same vector modulo the
lattice. INC followed by one lane Ebar has the same T-drift as DEC.

## 4. Layout: where the registers sit

Two constraints decide the layout.

1. **Latency.** An answer from a register must reach the control point.
   If the answer has to cross another register whose size grows with its
   value, its latency is unbounded, and a periodic program cannot wait.
2. **Control before action.** A skipped instruction must be neutralised
   before it reaches the register it would act on.

Argument (not a theorem): each register's zero point must be within a
bounded distance of the control point, and each register must be reached
by its instructions only after they pass the control point. In one
dimension this leaves one layout, in F's rest frame:

    [P_A ....... T_A] [CONTROL] [T_B ....... P_B]  <== stream (Ebars)

- Register A lies downstream (left) of the control. Its operations are
  stream packets that pass the control and then cross A. Its zero point
  T_A touches the control.
- Register B lies upstream (right). Stream packets cross B as the
  identity (lane). B's operations are generated at the control as
  right-moving messengers (in the F frame: C's) that enter B from the
  left. Its zero point T_B also touches the control. Operations on B
  commute, so their latency inside B does not matter; the zero test
  follows the pending operations and its answer is quick exactly when
  the value is small. A non-zero answer is the absence of a zero answer
  within a bounded time.
- The control point holds the skip state and converts B-instructions
  into messengers.

## 5. Gadgets still needed

| gadget | what it must do | status |
|---|---|---|
| lane | transport through memory in both directions | verified |
| A-register INC/DEC | crossing counter | verified (relative placement) |
| balanced instruction set | equal marker drift for all packets | first relation found |
| zero test A | at n = 0 a clean, distinct outcome near T_A; identity for n >= 1 | searching (`ztest.py`) |
| B-register ops | C-messenger packets that INC/DEC a register from the left | not started (winding test for C packets) |
| zero test B | same, triggered by a messenger | not started |
| control: reader | stream packet + answer messenger -> skip state | not started |
| control: skip | neutralise the next k instruction packets | not started (synth lock-and-key) |
| control: B converter | B-instruction packet -> right-moving messenger | not started |

## 6. Alternatives considered and why not chosen

- **Direct Turing machine with a head packet**: needs 2|Q||Sigma|
  bespoke, program-specific reactions; no program-independent reaction
  set.
- **Pile registers** (unary units created and destroyed): counting works
  (synth: EE + F -> C3), but an answer from the deeper pile crosses the
  shallower one with unbounded latency.
- **Single register with multiplication** (FRACTRAN): no relay needed,
  but exact geometric multiplication and divisibility tests are much
  harder than INC/DEC.
- **Queue machine with finite control**: feasible with Cook-like
  machinery and F memory, but closest to what exists.
- **Boolean circuits, simulating another CA**: finite, or equivalent to
  the open intrinsic-universality question.

## 7. Relation to Cook's construction

Shared ideas: a periodic program stream from the right, data encoded in
spacings, crossings as the default interaction, and phase bookkeeping by
lattice arithmetic. Different: the store is two counters, not a queue;
data sits in F gliders (bidirectionally transparent), not in Ebars and
C's; the program has real control flow (skips chosen by zero tests), not
a fixed cyclic appendant list; and counting is done by distances pumped
by multi-body crossings, not by appending and consuming symbols.

## 8. Verified results (scripts in this directory)

| result | script | evidence |
|---|---|---|
| no right-mover crosses a C; no fast left-mover crosses an Ebar | `cat_pairs.py` + collider catalog | 718 collisions |
| F trains transparent to C2 iff gap 1 mod 28, to C1 iff 15 mod 28 | NOTES.md 03:50 | gaps 29..127; scholar reproduced |
| Ebar x F train transparency predicted by lattice arithmetic | NOTES.md ~07:00 | 7 classes |
| pairwise-clean but non-YB triple fails | `m1_robust.py` | 0/12 |
| YB lane triple | `yb3.py`, `m1_yb.py`, `m1_predict.py` | 20/20 timings; exact final seeds; census |
| no winding for single crossings | `winding.py`, `winding2.py` | 0 winding transitions |
| multi-body packets act differently and wind | `multibody.py`, `winding3.py` | 8 multi-body cases; 181 winding transitions |
| crossing counter INC/DEC | `xcounter.py long` | n = 0..6..0, F positions exact, only -4/15 debris |
