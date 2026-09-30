# Architecture: a two-counter machine in Rule 110 without a cyclic tag system

Author: architect. Status: design document, version 3 (end of session). Section 8 lists
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
Within the lane, F's, a C1 messenger and Ebars pass through each other
with exactly predictable phases (verified, section 8). Verified with one
messenger in flight; a test with three messengers failed (`m1_multi.py`),
so several messengers need a finer incoming-class analysis.

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
state exact (section 8), and a fixed periodic stream (below).

**Zero state.** Below gap 43 the register keeps working once more (DEC
to gap 33.67). A second DEC turns the two F's into a close compound
(F_19_F, gap 19) with only Ebar-speed debris. The compound behaves as a
legitimate value 0: INC restores gap 33.67 exactly, a second INC gives
gap 43, NOP and every identity packet pass it unchanged. So the values
are 0 = compound, 1 = gap 33.67, 2 = gap 43, and so on. A 2-packet
sequence that is the identity on separated pairs splits the compound into
a separated pair at gap 24.33 (a second representation of 0), from which
INC also works. DEC applied at 0 is destructive: from the separated
zero it leaves one A moving right and only left-moving debris (the
register is gone), from the compounds it scatters. **A clean zero test
(identity at value >= 1, a readable signal at 0, register kept) was not
found**: 660 single packets and 1285 two-packet identities were tried
(section 8); synth is running the SAT version (spec Z2,
`zero_state.json`).

Fixed stream. The packets were first placed relative to T's current
position. T itself drifts, differently for INC and DEC, so a fixed
periodic stream needs balanced instructions: every instruction must drift
T by the same vector modulo the class lattice (a lattice difference only
translates later collisions by periods). INC' = INC + one lane Ebar,
DEC, and NOP = one identity pair + 7 lane Ebars are balanced; with them
slot j of the stream sits at a position that depends only on j, and 6
random 8-instruction programs ran exactly (`xstream.py`).

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
| balanced instruction set | equal marker drift for all packets | verified for INC/DEC/NOP (xstream.py) |
| zero test A | at value 0 a clean, readable signal; identity for value >= 1 | zero STATE verified; TEST not found (single and two-packet searches); SAT spec Z2 with synth |
| B-register ops | C-messenger packets that INC/DEC a register from the left | stationary C pairs do wind an F pair (cpump.py, 19 winding transitions); not assembled |
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
| counter from a fixed periodic stream | `xstream.py` | 6/6 random 8-instruction programs exact |
| census view of a counter run | `xcensus.py` | 42 E-type + 2 F (checked (36,-4)-invariant), gap = value |
| zero state (compound) and INC out of it | NOTES.md ~15:00 | exact |
| C pairs pump an F pair from the left | `cpump.py` | 19 winding transitions (stage-wise simulation) |
| no clean zero TEST among 660 packets / 1285 two-packet identities | `zc_fast.py`, `ztest3.py`, `ztest4.py` | negative, scope as stated |

## 9. Integration with the team's other counter

Collider found a second counter technology: E^n (n E gliders, moving at
-4/15) driven by a rigid G-speed stream (GB5 = INC, GB3 = DEC, GB4 = NOP)
whose DEC at zero leaves the counter intact and answers with one A
(verified by collider and scholar). It has a clean zero test, which the
F-pair counter lacks, but it is a front-only register: every G-speed
packet reacts with the first E^n it meets, and nothing crosses an E.

Can the two technologies be combined into two registers? Speed
arithmetic says not directly. An E^n (-4/15) to the right of an F pair
(-1/9) catches up with it; to its left, G packets for the E^n must pass
the F pair, and no G-speed object crosses an F (0 of 24 classes).
Ebar-speed packets never meet an E^n at all (same speed), which is why
the F-pair counter's stream would be invisible to it, but that does not
help the G packets. So two-register addressing remains the central open
problem for both technologies; the layout of section 4 is the only one I
know that is topologically consistent, and it needs the B-side gadgets
(C-pair pumps generated at the control) and a zero test.

## 10. Honest status

Shown: bidirectional transport through stored data (F lane,
order-independent); a crossing-only unbounded counter (INC/DEC/NOP)
driven by a fixed periodic stream, with a distinguished zero state; the
obstruction analysis that explains why Cook's machine is a queue; two
negative results (no winding for single crossings; no clean zero test in
the searched space).

Not shown: a zero test, a controlled branch, two registers, universality.
None of the pieces above is an emulation of a cyclic tag system, but
they are not yet a computer.

