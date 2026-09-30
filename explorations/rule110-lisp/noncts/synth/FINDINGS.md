# synth: automated synthesis for a non-CTS computer in Rule 110

Final report of the "synth" agent (2026-09-30). Everything here is either
(a) a SAT answer that was re-simulated with ../../engine.py, or (b) an
UNSAT answer for an exactly stated search space. Outside the stated
bounds nothing is claimed. Working log and all mistakes: NOTES.md.

## Summary

The team's goal was a Rule 110 computer that does not emulate a cyclic
tag system. My job was to find glider reactions that nobody had
designed, by encoding pieces of spacetime as SAT problems. The main
outcomes:

1. **A reusable synthesizer** (r110sat.py, react.py, scene.py): free
   stationary objects, free moving trains of any period, fixed library
   gliders, placed at exact spacetime positions, several scenes sharing
   unknowns, region constraints ("this region is item X somewhere", "this
   region is any train of period (p,d)", "ether"), and a moving window
   that makes slow reactions (relative speed 1/15) affordable.
2. **Positive results used by the team.** The command packet for
   architect's "spec F" (an E pair turns an F glider into a lone C3);
   fuel-paying A-packets that cross a stationary C cell (the one known
   way for a right-mover to pass stored data); three B reflectors.
3. **A theorem-like data result.** Slip mod 14 is the only linear
   conservation law of glider collisions (Smith normal form of the whole
   verified catalog).
4. **About twenty bounded non-existence results** for the gadgets the
   architecture needed (relay, perfect mirror, multi-cell crossing,
   transport through counters, hard gate, zero test, pumping). Each is
   exact within its bounds, and each came with a positive control on the
   same code. Together they locate where the construction is hard: every
   "clean absorption" or "clean pass-through with state" gadget asked for
   was absent at the widths I could search.

The computer is not finished (see architect's ARCHITECTURE.md s.10 for
the team's status). My results narrow which gadgets can exist at small
sizes; none of them shows impossibility in general.

## 1. Method

### 1.1 Encoding

Cell (t, x) is a Boolean variable; Rule 110 is five clauses per cell
(new = (c or r) and not (l and c and r)). A problem is a set of scenes.
Each scene's row at t = 0 is assembled from pieces: library gliders
(collider's gliders.json), free stationary objects (period (7,0)
enforced in their own 7-row spacetime), or free trains of period (p, d)
(e.g. (30,-8) for Ebar-speed packets), all embedded in ether with
consistent phases. Outside the light cone of the unknown cells every
cell is an ether constant. Constraints at a later time T2 describe the
required outcome exactly: which regions hold which items (at any
position and time phase, by an indicator disjunction), which regions are
ether, which are periodic. Solver: CaDiCaL 1.5.3 via python-sat.

Phase convention: ether with my-phase p is cell(t, x) = ETHER[(x + 4t + p)
mod 14] (checked: one step shifts the tile by 4).

### 1.2 Verification discipline

- Every SAT answer: the decoded t = 0 row is simulated independently
  with ../../engine.py; the SAT spacetime must equal the simulation cell
  for cell, and the claimed outcome must persist for >= 400 more steps.
- Every new scene type got a POSITIVE control (a known reaction that must
  come out SAT, and the known wrong classes UNSAT) before any UNSAT was
  reported. Controls are listed with each result.
- Collision classes: for fixed items I enumerate one placement per class
  (classes.py: offsets modulo the lattice of the two period vectors,
  count |det|/14). For FREE trains the class index is not an anchor (the
  solver can shift the train inside its window), so free-train results
  cover all classes whenever the train is narrower than its window by the
  class spacing.

### 1.3 Bugs found by the verification, and their consequences

Four harness bugs were caught; none survives in a reported result.
1. O' region not isolated from outgoing gliders (walls.py): caught by
   simulation (a SAT "mirror" whose O' later emitted a glider). Fixed with
   14-cell ether bands.
2. Relay pre-roll sign error: caught by a positive control; fixed before
   any result was used.
3. Seam debris in verify_reaction (pad too small): false "verification
   failed" alarms; fixed.
4. is_item demanded the whole light cone of long-period items fit inside
   the region -> possible FALSE UNSAT for Ebar- and F-speed items. Found
   by a failed control (03:55). All affected runs were repeated after the
   fix (relay: same answer); the others were discarded (trash/).

## 2. Positive results

### 2.1 Spec F: a command packet that turns a stored F into a messenger

Question (architect): a left-moving packet P at -4/15 hitting an F glider
(the top of an F store) that leaves only stationary messengers.

Search: free (30,-8)-packets <= 20 cells wide, all 14 slips x 12
placements (168 instances), T2 = 300, outcome = ether | nonempty period-7
object | ether.

Observation: exactly two packets exist, both E pairs (collider's names
E@(0,0)+E@(-13,15) and E@(0,0)+E@(-5,11), slip 4), and the messenger is
always C3 (13 + 4 = 17 = 3 mod 14). For the first pair this happens in
exactly one of its six classes against F. Neither pair crosses F cleanly
in any class (F turns them into B^3/B^2/Ebar).

Interpretation: a destructive read of an F store exists and is unique at
this size; "decrement one store while crossing another" (addressing by
phase) does not exist with packets <= 20 wide. Independently verified by
scholar (check_specf.py) and collider (catalog).

### 2.2 Right-moving A-packets that cross a stationary cell

Question: does any right-mover pass a stationary C cell (the one-way
transparency obstruction says single gliders cannot)?

Observation (cross.py, verified; scholar re-embedded and confirmed):
| cell | packet in (slip) | cell displacement | out |
|---|---|---|---|
| C2 | 9 A's (2) | dx = -6, dt = 2 mod 7 | A^2 |
| C2 | 8 A's (8) | dx = -12, dt = 5 mod 7 | A |
| C1 | 9 A's (2) | dx = -6 | A^2 |
| C1 | 8 A's (8) | dx = -6 | A |
| C3 | 8 A's = A^3 + A^5 (8) | dx = -6 | A |
(A-trains <= 24 wide; the 8-A packet 111110111011101110111011 crosses all
three C types.)

Interpretation: the cell absorbs exactly one slip cycle (7 A's, 7 x 8 = 0
mod 14) and restores itself; the rest of the packet passes. This is a
genuine exception to the obstruction for packets, at a fuel cost of 7 A's
per crossed cell.

Boundary (all UNSAT): no A-train re-emerges identical (width <= 24 for
C1-C3, <= 36 for C2); no two-cell version (packet <= 48 whose remainder
<= 28 crosses a second C2); D-speed trains never cross (<= 20). So the
fuel-paying crossing is one cell deep within these bounds.

### 2.3 Reflectors

- B reflectors (W = 24): stationary objects O with B + O -> C2 + A
  (O = 111111110100111001100111, right phase 13), -> C1 + A + A, and
  -> A_8_A (O consumed). A single B can be turned around.
- A + O -> O' + F (O = 0111001101111111, right phase 2): an A turned into a
  slow left-mover with a state change.
- Contrast: no stationary object <= 24 wide turns a single A into any
  B-train, or lets it pass as any A-train (all 14 right phases; scholar
  independently confirmed the pass-through part by hitting all 1260
  stationary objects <= 24 wide with an A: no A-type object ever leaves).

### 2.4 Only one linear conservation law

invariants.py: every verified reaction in collider's catalog among 22
named types (A, B, Bbar, Bhat, C1-3, D1, D2, E, Ebar, F, G, H, A^2..A^5,
B^2, B^3, E^2, E^3; 874 reactions, 597 distinct count vectors) as rows of
an integer matrix. Smith normal form: diag(1, ..., 1, 14), rank 22.

Interpretation: no weighted glider count is conserved, and every linear
law mod any m is a multiple of a single Z_14 law, which is slip. Scholar
re-derived it on 3293 reactions. Scope: laws linear in type counts; laws
involving positions or phases (e.g. the architect's no-winding
"potential") are not excluded.

## 3. Bounded non-existence results

All UNSAT, with the positive control used for that code. "Free" = the
solver chooses every cell.

| # | gadget asked for (by) | searched space | control |
|---|---|---|---|
| 1 | relay: P crosses C2, and P + C1 -> same C2 + same P + A (architect) | P (30,-8) <= 20, 14 slips x 4 classes, T2 330 | Ebar x C2: exactly 1 of 4 classes crosses |
| 2 | weak relay: P + C1 -> C2 + A, P consumed | same | same |
| 3 | perfect mirror: A-train + O -> O + B-train | trains <= 12, wall <= 16, 14 x 7 slips | walls.py known reactions |
| 4 | INC on F store: P + F -> F + new F 29 cells right, anywhere right, or anywhere left (architect) | P <= 20, 12 classes | Ebar/F controls |
| 5 | zero test on F memory floor: EE + O -> O + messenger (architect, spec Z) | floor (36,-4) <= 20, 14 slips x 6 classes, T2 450 | collider's Ebar pair: floors found in 8/12 |
| 6 | stationary Ebar annihilator X + Ebar -> nothing | X <= 20, 4 classes | - |
| 7 | pump: packet changes two C1 markers' distance by a lattice vector (counting by crossings) | P (30,-8) <= 20, 14 slips x 4 classes, marker gaps 51, 65 | single Ebar: 1-bit register reproduced |
| 8 | DEC E_n from the right with a B-train | <= 32, E_2 and E_3 separately | B-train INC E_n -> E_n+1 found |
| 9 | transport through E_1, E_2, E_3 (B-train / A-train / G-speed train) | B, A <= 24; G-speed <= 30, T2 1100; 14 slips (x 3 classes) | fixed A x Ebar: 4 of 6 classes; F x C1 classes with/without window |
| 10 | hard gate: A + H -> nothing / -> GB4 (collider) | H (42,-14) <= 30, slip 6, 9 starts; both also <= 44 (T2 170) | GB1 + A -> G in 1 of 9 |
| 11 | hard gate, any G-speed output | H <= 30, 14 slips | only GB1 -> G (excluding GB1: UNSAT) |
| 12 | zero test on architect's compound: K + F_19_F#3 -> itself + messenger (Z2) | K (30,-8) <= 24, 14 slips, T2 900, strict and with Ebar debris | F + E,Ebar packet -> F + C1_12_C2 in its class |
| 13 | compound -> (19,23) pair (architect's near miss) | K <= 24, 14 slips | only single Ebars (39 placements excluded -> UNSAT) |
| 14 | spec F with C1 or C2 messenger | P <= 20 (and <= 28 for 17/24 instances) | - |

Caveats that apply to every row (a skeptic's list):
- Time: the outcome must be complete by T2. A reaction that settles
  later (possible for slow partners such as F or G) is not covered.
- Windows: rows 5, 8, 9, 10, 11, 12, 13 used a moving window; any solution
  whose debris leaves the window transiently and returns is excluded.
- Classes: with free packets the class is covered only if the packet is
  narrower than its window by the class spacing (about 2-8 cells), so the
  bounds are complete for packets slightly narrower than stated.
- Widths count cells of the t = 0 window, not gliders; a packet of k
  gliders needs roughly 4-12 cells per glider.

Interpretation, stated with its limits: the clean gadgets that would
close the construction (a store that answers across other stores; a
clean absorber; a non-destructive zero read) do not exist among small
packets and objects. The bounds are modest (20-32 cells, 150-1100
steps), so this is evidence about where the difficulty lies, not a proof
that the gadgets cannot exist.

## 4. Sanity checks of the synthesizer

- Glider enumeration (gliders.py), P <= 30, width <= 30: primitive
  periodic defects exist exactly for (3,2) (4,-2) (7,0) (10,2) (12,-6)
  (15,-4) (30,-8) = A, B, C, D, Bbar/Bhat, E, Ebar (Cook's catalog below
  period 30). P = 31..100 was stopped for CPU.
- Known reactions recovered from free objects: A2 + C1-like -> Ebar,
  B + C3-like -> E, B + C1-like -> C2-like, B + C2 -> D1, A + C1 -> F.

## 5. Recommendations

1. For the E^n / G-speed stream design (collider), a clean hard gate
   (A + H -> nothing or -> GB4) is absent up to width 44, and up to width
   30 the only clean A-absorber of any kind is GB1 -> G. The promising
   route is a spec that accepts a known instruction as the product
   (collider found A + (GB3,GB5) -> GB3) and designs the program around
   it, rather than a new absorber.
2. For the F-pair counter (architect), a non-destructive zero read does
   not exist up to width 24 in any of the three forms tried; a
   destructive read (spec F, or collider's DEC at zero -> one A) plus
   re-creation of the zero state may be the realistic route.
3. The synthesizer is general: any new spec (scenes + region constraints)
   takes ~50 lines on top of scene.py. Always add a positive control.

## 6. Files

Library: r110sat.py (CNF, Spacetime, moving window), react.py (items,
single reactions), scene.py (multi-item scenes), classes.py, lib.py
(collider's gliders in my phase convention), identify.py / analyze.py
(object typing by period + bits + ether phases), en.py (E_n builder).
Searches: gliders.py, walls.py, experiments_heads.py, cross.py, chain.py,
mirror.py, relay.py, specf.py, specz.py, copyspec.py, eater.py, pump.py,
encross.py, hardgate.py, zc.py, zsplit.py, invariants.py. Written but not
run (superseded): inc.py, tmhead.py, ghost.py (control only).
Results: *_results.jsonl (every SAT answer with its decoded row and
frame), *.log (every instance, SAT or UNSAT, with timing).
