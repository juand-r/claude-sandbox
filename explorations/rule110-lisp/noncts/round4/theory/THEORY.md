# Round 4 theory: the map of what is still possible

Author: theory (round 4), started 2026-10-01 22:48 UTC. Labels:
**[thm]** proved here for the model stated; **[model]** executable abstract
model with tests; **[sim]** exact Rule 110 run (collider's verified pipeline,
read-only); **[arg]** argument, not a proof; **[hyp]** hypothesis.
Every non-existence claim states its scope.

The route table is in `ROUTES.md`; this file holds the reasoning behind it.

## 1. Summary

1. **Where we stand.** Rounds 2-3 closed, inside abstract models, every design
   in which the program is a periodic stream and the memory is a set of
   counters that the stream reaches only at their outer faces: one stream
   (eventually periodic), feed-forward layouts, monotone answers, and two
   rods coupled through values (R3-T1/T2). The escapes they named (shuttle,
   crossing, gap register, pump) are all searched without success inside
   bounded widths.
2. **The common cause [arg].** Every closed design keeps the program in a
   *stream* and the data in *stores the stream cannot get through*. The
   rod is opaque, so information flows into a rod only at its outer face and
   leaves only through its inner face; a stationary C pile is transparent
   only from the right. All the no-go theorems are versions of "the
   influence graph between drift-setting states is not strongly connected".
   An escape must either (a) make the influence graph strongly connected
   (shuttle, crossing, pump, shared control point), or (b) not put the
   program in a stream at all.
3. **Route (b) has never been tried, and has an unusually clean physics
   (s.3).** In a Lindgren-Nordahl / Durand-Lose *particle Turing machine*
   the program is a fixed universal TM in the reaction table, the tape is a
   row of stationary cells, and the head is one moving packet. In Rule 110,
   if the head is a rigid packet on the A, D or B lattice, **every
   head-cell collision has exactly one class (Lemma L1 [thm])**: no timing,
   no class bookkeeping, no skew, no Cook mod-6 rules. No theorem of rounds
   2-3 applies to it. What it needs is a finite closed table of exact local
   reactions. The census (s.3.5) shows the KINDS of steps needed exist; the
   open question is whether a closed table exists, and the first hard
   sub-question is a head that crosses a cell and comes out as itself (or
   a head cycle).
4. **Route (a), near-end lane: the abort can be replaced by a class
   shift (s.4).** Round 2's near-end layout was blocked because no eater
   eats register kicks (SAT UNSAT W <= 30). The same machine (verify's
   guarded-block machine, universal) only needs the kicks to become
   *harmless* while a flag is present. A crossable flag upstream of the
   control point that shifts the class of every later packet into a
   crossing class does that. This turns an UNSAT target into a different,
   unsearched target.

## 2. The influence-graph view of the old theorems [arg]

The four no-go theorems of rounds 2-3 share one structure. Write the
machine's memory as stores S_1..S_k, each with a *drift-setting state* m_i
(what fixes how S_i changes while it is large). Draw an edge i -> j if an
event at S_i (in practice: a zero event, the only time a large store emits
anything) can change m_j.

| theorem | model | influence graph |
|---|---|---|
| R2-s3 feed-forward | stores along one stream, answers only downstream | acyclic |
| R2-s5 one counter | one store, blind stream | one node, no input |
| R3-T1 | two counters, x's mode owned | no edge y -> x |
| R3-T2 | two rods | no edge into the left rod's front |

In each case some store's mode is changed only by itself, and the proof
shows the orbit becomes eventually periodic. R2-s2 (chain machines) is
different: it has all edges but every effect is monotone.

**Loopholes, stated precisely** (each theorem's premise that fails):

- R2-s3 assumes each store is operated at its own place. It fails for the
  near-end layout (all operations at one control point; answers stationary
  there; the stream reaches the control point through the stores). Needs
  stores the stream can cross.
- R2-s5 and R3-T1 assume (A1) bounded steps: |x' - x| <= M. A multiply or
  divide in one step (row 15) violates it; so does an unbounded gap read
  by timing (row 8).
- R3-T1 assumes (Q) quiescence: no persistent process acts on both
  counters while both are large. Shuttles, pumps and guns violate it.
- R3-T2 assumes (L) no back-to-front influence in a LONG rod and (N) no
  crossing. Verify (round 4, board 23:02) showed a perturbation's
  influence cone does reach the front, at speed 3/5, but by destroying the
  rod. So (L) holds for "the rod survives" and is not a light-cone fact.
- ALL of them assume the program is a periodic *stream* acting on
  *counters*. A particle TM (s.3) has neither, so none applies.

## 3. Route 12: the phase-free particle Turing machine

### 3.1 The design (Lindgren-Nordahl 1990; Durand-Lose 2009)

- **Tape.** One stationary object (period (7,0)) per tape cell, one object
  type per tape symbol, at a large pitch. Blank cells repeat periodically
  to both sides (an ultimately periodic initial condition, the same notion
  of universality as Cook's).
- **Head.** One rigid packet. A head moving right is a set of gliders that
  all have period (3,2) (the A lattice: A, A^k, A trains, and other A-speed
  objects) or all (10,2) (the D lattice). A head moving left has period
  (4,-2) (the B lattice). Its shape encodes the TM state (and the arrival
  side).
- **Step.** h_q + c_s -> c_s' + h_q' and nothing else; h_q' is on the A/D
  lattice if the TM moves right, on the B lattice if it moves left. It next
  meets the neighbouring cell.
- **Program.** A fixed small universal TM. Durand-Lose (2009, s.3) counts,
  for the TM-to-signal-machine translation: 1 signal per symbol, 2 per
  state, at most 2 rules per table entry; for the Neary-Woods small UTMs
  this is 18 signals and <= 62 rules. Those UTMs simulate 2-tag/bi-tag
  systems, not cyclic tag systems.

### 3.2 Lemma L1 (single class) [thm]

*Statement.* Let H be a rigid packet whose gliders all have the same period
vector P_H in {(3,2), (10,2), (4,-2)}, and let S be a rigid stationary
object (period (7,0)). Then all collisions of H with S (H starting far to
the left if it moves right, far to the right if it moves left) are equal up
to a spacetime translation.

*Proof.* Every object in the ether can sit only on one coset of the ether
lattice Lambda = <(7,0), (3,2)> (index 14 in Z^2), and translating an object
by its own period vector maps its trajectory to itself. Two placements of
the pair (H, S) that differ by m*P_H for H and n*P_S for S describe the same
spacetime history (as long as H is still far from S, which holds for the
far placements considered). So the distinct collisions are indexed by
Lambda / <P_H, P_S>, of size |det(P_H, P_S)| / 14 (Cook 2004 s.3.1; verified
by scholar's class_check.py). Here det((3,2),(7,0)) = -14,
det((10,2),(7,0)) = -14, det((4,-2),(7,0)) = 14, so there is exactly one
class. The same count applies to a packet with several gliders because
P_H is a period of the whole packet and lies in Lambda
((3,2) in Lambda; (10,2) = (7,0) + (3,2); (4,-2) = (7,0) - (3,2)). ∎

*Check [sim].* Every collision run by `ptm.react` and `lnscan2.py` asserts
n_classes(P_H, (7,0)) == 1, and collider's `canonical_reps` enumerates the
classes independently and finds exactly one.

*Other single-class pairs* (|det|/14 = 1): A-B, A-D, B-E, and C with A, B,
D. Full table (classes = |det|/14) for reference:

|      | A | B | C | D | E | Ebar | F | G |
|---|---|---|---|---|---|---|---|---|
| A    | - | 1 | 1 | 1 | 3 | 6 | 6 | 9 |
| B    | 1 | - | 1 | 2 | 1 | 2 | 4 | 2 |
| C    | 1 | 1 | - | 1 | 2 | 4 | 2 | 7 |
| D    | 1 | 2 | 1 | - | 5 | 10 | 8 | 16 |

*Consequence.* In route 12 nothing depends on spacing: not the pitch, not
the head's emission point, not the order or timing of earlier steps.
Correctness reduces to a finite table of reactions, each checkable by one
simulation.

### 3.3 Lemma L2 (cells must not drift) [thm]

Each reaction moves its cell by some displacement delta(h, c) (output
position minus input position, in a fixed per-type reference). A cell
visited many times drifts by the sum of its deltas and would eventually
touch its neighbour. *Sufficient condition:* there is a potential phi on
cell types with delta(h, c) = phi(c') - phi(c) for every used reaction.
Then a cell's position is x0 + phi(current type) - phi(initial type), which
is bounded. *Necessary for arbitrary runs:* if some closed walk of symbol
rewrites c -> c' -> ... -> c that a run can repeat has nonzero total delta,
that run drifts without bound. (Proof: telescoping sums.) ∎

### 3.4 Lemma L3 (slip) [thm]

Slip (width mod 14) is conserved by every collision (Cook 2004). So
w(h) + w(c) = w(c') + w(h') (mod 14) for every step. If all cell types have
the same slip, all heads must have the same slip; in general
w(h_q) - w(h_q') = w(c_s') - w(c_s). Necessary, never sufficient; it prunes
SAT searches.

### 3.5 Census [sim]

`lnscan2.py`: every library head-lattice object (226 of them: A trains,
B trains, D pairs, unnamed A- and B-speed compounds) against library
stationary objects, one collision each (single class). Partial run (stopped
to free the CPU; resumable): 4,904 pairs. Clean steps exist of every kind
the design needs:

| kind | example | 
|---|---|
| right head reflects left, cell rewritten | A@(0,0)+A@(-1,24) + C1 -> C2 + B_2_B_4_B_2_B |
| right head continues right, cell rewritten | D2_7_D2#2 + C3 -> C2 + A_0_A_7_A |
| right D head becomes an A head (grows) | D1_17_D1 + C1 -> C2 + A^4 + A_2_A_14_A |
| left head passes, cell unchanged | v-2/4s6w29 + C1 -> C1 + B |
| left head reflects right | v-2/4s12w33 + (stationary v0/7s2w48) -> C2 + D1 |

But the outgoing head is almost never one of the incoming heads, and most
pairs are dirty. `explore.py` ran the *natural TM* (s.3.6) from every
library head on all-blank tapes of C1, C2 or C3, with and without one wall
cell: 2,502 runs, **every run ends within 2 steps** (2,343 dirty, 159
absorbed). So closed tables do not occur by accident among library objects.

### 3.6 The natural TM, and what a closed table needs

Fix the physics. Then (head shape, cell type) -> (new cell type, new head)
is a deterministic map on an infinite alphabet: the *natural TM* of Rule
110. A particle TM is a finite closed sub-table of it. Since every step is
determined, the only design freedom is the CHOICE of the head shapes and
cell types; there is no free parameter per reaction. So the search is for
a finite set closed under the map, not for individual reactions.

**Lemma L4 (passes in both directions are necessary) [thm].** A
single-head particle TM (stationary cells; head on the A or D lattice when
moving right, on the B lattice when moving left) whose step table lacks
clean R-passes (h + c -> c' + h' with h, h' both moving right), or lacks
clean L-passes, is eventually periodic or halts; so a universal one has
both.
*Proof* (wording corrected by verify, board 23:19). A right-mover can
only exit a cell on its right side and a left-mover only on its left side,
so the head gets from one side of a cell to the other only through a pass
in that direction. Without R-passes, a right-moving head in the gap
(j, j+1) can only reflect at c_(j+1); the head can never cross a cell
rightward, so the cells to the right of the current window are never
read, and every L-pass moves the window one cell left for good. The
machine is a finite automaton on a 2-cell window moving monotonically left
over an ultimately periodic tape (the cells it leaves are never read
again): eventually periodic or halting. Symmetrically without L-passes. ∎

*What it does NOT force* (verify, 23:19; my first post overstated it).
Pigeonhole forces a cycle of head types in the full walk (passes AND
reflections) with positive net crossing, not a cycle of passes. Example
of a "zig-zag ratchet": R-pass at c_(j+1), reflect at c_(j+2), reflect at
c_(j+1), R-pass at c_(j+2), back to the first head type. So pure pass
cycles (target T1) are sufficient, not necessary.

The concrete targets are therefore:

- **T1 (pass cycle)**: h_1 -> ... -> h_1 through passes only; length 1 =
  a fixpoint h + c -> c' + h. Sufficient.
- **T1' (ratchet)**: any closed walk of passes and reflections whose net
  crossing per period is nonzero, with the cell rewrites consistent.
  Necessary in the sense above.
- **T3 (binary counter)**: R + 1 -> 0 + R, R + 0 -> 1 + L, L + 0 -> 0 + L,
  L + 1 -> 1 + L, L + W -> W + R, up to renaming heads within cycles; the
  first stream-free non-periodic computation in Rule 110 if found.

### 3.7 Pass-cycle search [sim, in progress]

(filled in below as runs finish)

### 3.8 Finite seeds and the signal-machine speed theorems [arg]

Durand-Lose (CiE 2013; I read s.1-3 and 5 of the HAL version): a *rational*
signal machine with three speeds started from a *finite* configuration is
ultimately cyclic (the signals stay on a (p,q,n)-mesh that is periodic in
the region spanned by the initial signals, and nothing is created outside
it), hence not universal. Four speeds suffice (Durand-Lose 2009/2011). His
3-speed TM (stationary symbols, head moving at +-speed) is exactly route
12, and with rational positions it can only use a bounded tape; extending
the tape needs either an irrational distance or a fourth speed.

Transfer to Rule 110:
- With a periodic blank tape (route 12 as stated) the theorem's hypothesis
  "finite configuration" fails, so it says nothing.
- From a finite seed, a route-12 machine that uses only the A, 0 and B
  lattices is a 3-speed system; it needs a D head or another speed to grow
  its tape, if the transfer holds.
- The transfer is NOT automatic: Rule 110 collisions emit products at
  offsets, not at the meeting point, so a stationary product can appear
  outside the region spanned by its inputs and the mesh argument breaks.
  That loophole could let a 3-speed Rule 110 system grow. I do not claim
  either way.

## 4. Route 7, the near-end lane: abort by class shift [arg + spec]

*Background.* Round 2 (verify s.3.1) showed the near-end layout escapes
the feed-forward theorem: all register operations and zero tests happen at
one control point M; packets reach M by crossing the stores upstream of
it; a zero test's answer is born at M, stationary in the lane frame, and
every later packet meets it. Verify's guarded-block machine (GBM: two
counters, three bounded flags, "a zero DEC aborts the rest of its block",
402/402 differential tests) is universal. Gate built half of an abort (a C1
that eats neutral pairs until a gate packet removes it), but no packet that
kicks a register can be eaten (catalog + 203 compounds; SAT UNSAT W <= 30,
12 F classes, one C1 class).

*Observation [arg].* The abort does not need the kicks to be EATEN. It
needs them to have NO EFFECT between the zero event and the gate. In a
lane, a packet's effect at each marker is fixed by its collision class
there, and that class is the packet's relative position modulo the lattice
<P_packet, P_marker>. Every clean crossing displaces the packet by a fixed
vector. So a *flag*: an extra object at the control point, crossed by
every later packet, displaces all of them by the same vector v and shifts
their classes at every downstream marker by [v]. If [v] maps every kick
class to a crossing class at every downstream marker, the flag turns all
kicks into no-ops. That is an abort.

*Spec (all in the lane frame; markers T > M > P; stream from the right).*
- F1. The zero test's answer is a flag Phi created at the control point
  (upstream of every marker it must silence).
- F2. Every packet type of the program crosses Phi cleanly, in the class
  in which it arrives (it meets Phi before any shift).
- F3. For every kick type k with class c_k at marker X (in the no-flag
  stream), c_k + [v_Phi] is a clean crossing class of k at X and at every
  marker it passes.
- F4. A gate packet removes Phi (any clean products that leave).
- F5. Bookkeeping: packets that crossed Phi are displaced by v_Phi relative
  to packets that did not. Since the flag exists only between a zero event
  and the next gate, this is a bounded, program-determined correction
  (as in round 2's planner).

Why this is worth searching: it replaces "eater + kick in one packet"
(UNSAT W <= 30) by conditions on CROSSINGS, which the lane has in
abundance (Ebar pairs cross F in 7 of 12 classes). Whether some lane
object Phi shifts every kick into a crossing class is a finite catalog
question. Nobody owns route 7 in round 4; I flag it for the lead.

## 5. Rods in a line (k >= 3) [arg]

Rods R_1 .. R_k from left to right, a left stream at R_1's front and a
right stream at R_k's back, nothing crosses a rod, influence inside rods
runs left to right (R3's (L)).
- Middle rods R_2..R_(k-1) touch no stream. In the bulk (all rods long and
  the gaps quiet, (Q)) they do not change at all: their mode is trivially
  owned with drift 0.
- R_1's front is reached only by the left stream: its mode is owned.
- So, as with two rods, at least one store's drift-setting state is owned
  and no edge leads into it. I expect R3-T1's passage argument to extend
  (each owned-mode counter alternates between near and far passages), but
  I have not written the k-counter proof; with k counters the corner
  regions are products of several small counters and the passage
  bookkeeping is more involved. Status [arg]: more rods do not escape
  without a gap process or a crossing.

## 6. Other routes, briefly [arg]

- **One register with multiplication (row 15).** Minsky: a single register
  with x2, x3, /2, /3 tests is universal (registers as 2^a 3^b). A length
  can be scaled by a ratio of glider speeds (two signals leaving one event
  at speeds u, v separate at |u - v|). Rule 110's speeds give integer
  ratios, e.g. (2/3 - 0)/(0 + 1/3) = 2 (A against G) and (2/3)/(1/9) = 6
  (A against F). But every scaling construction needs *marker-preserving
  reflections* (a signal hits a marker, the marker survives, a signal goes
  back), the same primitive as route 12's bounce (T2), and residue tests
  mod 2 and 3 of an unbounded length. Route 12 needs strictly less
  geometry, so row 15 is dominated.
- **Signal-machine 2-counter (row 14)**: same primitive, also dominated.
- **Switchable gun in the gap (row 18).** A gun is a persistent process, so
  a gun that zero events can switch on and off would be a shared mode
  (violates (Q) of R3-T1). The known gun moves at -20/77 while rods move at
  -4/15 (-0.2597 vs -0.2667), so it drifts right relative to the rods by
  about one cell per 140 steps; it would need a speed-matched variant or a
  re-anchoring mechanism.
- **Intrinsic universality (row 16)**: Ollinger's open problem; requires
  blocks to exchange information both ways every simulated step, so it
  inherits every transport problem at once. Lowest priority.

## 7. Literature read for this round

- J. Durand-Lose, "Irrationality is needed to compute with signal machines
  with only three speeds", CiE 2013 (HAL hal-00807227) **[read s.1-3, 5]**:
  Lemma 1-2 (rational 3-speed machines are trapped on a periodic mesh,
  ultimately cyclic, not universal); s.5 (TM simulation with stationary
  symbol signals and a head moving at the two other speeds; tape growth is
  the obstacle).
- J. Durand-Lose, "Small Turing universal signal machines", EPTCS 1 (2009),
  arXiv:0906.3225 **[read s.2-4]**: periodic pattern generator by a
  bouncing signal; TM simulation costs (1 signal per symbol, 2 per state,
  <= 2 rules per transition; 18 signals and <= 62 rules for small
  Neary-Woods UTMs); CA simulation needs three signals per state meeting
  exactly at one point; a 6-signal semi-universal machine from Rule 110.
- Squier and Steiglitz, "Programmable parallel arithmetic in cellular
  automata using a particle model" (Complex Systems 1994) **[search
  snippet only]**: particle machines with stationary processor particles
  in a designed CA; not about Rule 110.
- Martinez, Adamatzky, McIntosh on Rule 54 glider collisions and logical
  gates (2006) **[search snippet only]**: a snippet says the gates "are
  enough to simulate a counter machine"; I did not read the paper and do
  not rely on it.
- Previous rounds' SURVEY (scholar) for Cook, Richard, Neary-Woods,
  Ollinger, Lindgren-Nordahl, Martinez et al.
