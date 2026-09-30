# synth: verified findings (living document; final summary at the end)

Every positive result below was found by SAT and then re-simulated with
../../engine.py (the SAT spacetime equals the simulation cell for cell,
and the claimed outputs persist for >= 400 further generations). Every
negative result is an UNSAT answer of CaDiCaL 1.5.3 for the exact bounds
stated; outside those bounds nothing is claimed.

Phase convention: ether with my-phase p is cell(t, x) = ETHER[(x + 4t + p)
mod 14]. Objects are given as the cells [0, W) at t = 0 with my-phase 0
ether to the left and my-phase pR to the right.

## 1. Sanity checks (the synthesizer reproduces known physics)

- Glider enumeration (gliders.py), periods P <= 30, widths <= 30: the
  only period vectors (P, D) with primitive periodic defects are
  (3,2) (4,-2) (7,0) (10,2) (12,-6) (15,-4) (30,-8), i.e. A, B, C, D,
  Bbar/Bhat, E, Ebar. Matches Cook's catalog below period 30. (P = 31..100
  was stopped for CPU; hard instances at P = 32 exceeded a 200k-conflict
  budget, so nothing is claimed there.)
- Known collisions recovered by free-object searches: C1-like object + A2
  -> Ebar; C3-like + B -> E; C1-like + B -> C2-like; B + C2 -> D1;
  A + C1 -> F. The class structure of Ebar x C2 (exactly 1 of 4 classes
  is a clean crossing) is reproduced by scene.py.

## 2. Bounded non-existence results (phase-free heads)

Setting: a single A (from the left) or B (from the right) hits a FREE
stationary object O (period (7,0), width W, all 14 right phases tried).
A and B have exactly one collision class against any period-7 object,
so these answers do not depend on timing. Outcome required within
T2 = 200 generations; O' = any stationary object (possibly empty).

| head | required outcome | W | result |
|---|---|---|---|
| A | nonempty B-train back to the left | <= 12 | none (all 14 pR) |
| A | nonempty A-train onward to the right | <= 24 | none (all 14 pR) |
| A | nonempty B-train back to the left | <= 24 | none (all 14 pR) |
| B | nonempty A-train back to the right | <= 24 | EXISTS for pR = 7, 10, 13 (sec. 3) |
| A-train (<= 12 wide, n A's) | O restored exactly + B-train (<= 12 wide) back | <= 16 | none (all 14 pR x 7 slips) |

## 3. Positive results

- A + O -> O' + F (an A reflected as a slow F; O changes state):
  O = 0111001101111111 (W = 16, pR = 2), T2 = 320; walls_results.jsonl.
- B reflectors (W = 24, T2 = 200; experiments_heads.py, heads_results.jsonl):
  O = 111111110100111001100111 (pR 13): B + O -> C2 + A
  O = 000111110000111110111111 (pR 7):  B + O -> C1 + A + A (A's 48 apart)
  O = 111011010111011010111110 (pR 10): B + O -> A_8_A (O consumed)
  The O's are tight stationary composites (not library gliders).

## 4. Spec F (architect): command packet + F -> stationary messenger only

SAT search: P = free (30,-8)-train of width <= 20 (all 14 slips, all 12
placements vs F), required: the row at T2 = 300 is ether | nonempty
period-7 object | ether (nothing moving). Hits (verified to T2 + 500):
only slip 4, only two packets, both E pairs (collider's names):
  E@(0,0)+E@(-13,15)  and  E@(0,0)+E@(-5,11)
Each gives F + P -> C3 alone (slip 13 + 4 = 3). For E@(0,0)+E@(-13,15)
(cells 00000111110000000010 on [0,20), my-phase 0 left / 4 right,
(15,-4)-periodic) this happens in exactly 1 of its 6 classes vs F.
No packet of width <= 20 leaves C1 or C2 (or any other messenger);
complete sweep, 168 instances. Neither E pair crosses F cleanly in any of
its 6 classes, so no packet <= 20 wide can decrement one F store while
crossing another (phase addressing).

## 5. Right-moving A-packets can cross stationary C cells (fuel cost)

cross.py, cross_analysis.txt. A free A-train (width <= 24) + fixed C cell
-> the same C glider (displaced) + a nonempty A-train onward:
| cell | packet in (slip) | cell displacement | out |
|---|---|---|---|
| C2 | 9 A's (2) | dx = -6, dt = 2 mod 7 | A^2 |
| C2 | 8 A's (8) | dx = -12, dt = 5 mod 7 | A |
| C1 | 9 A's (2) | dx = -6 | A^2 |
| C1 | 8 A's (8) | dx = -6 | A |
| C3 | 8 A's = A^3 + A^5 (8) | dx = -6 | A |
The cell absorbs 7 A's (one slip cycle, 7 x 8 = 0 mod 14) and the rest
pass. No A-train of width <= 24 re-emerges IDENTICAL after crossing C1,
C2 or C3 (all slips; UNSAT). D-speed trains (width <= 20, T2 = 260): no
crossing of C1, C2, C3 at all (UNSAT, all slips).

## 6. Relay (spec R) bounds

Strict relay (idle: P crosses C2; set: P + C1 -> the same C2 at the same
cells + the same P trajectory + an A): UNSAT for all free (30,-8)-trains
P of width <= 20, all 4 classes, all 14 slips, T2 = 330 (re-run after the
is_item extent fix of 03:55; same answer).
Weaker relay (P + C1 -> C2 + A, P consumed, C2 anywhere; no idle-crossing
requirement): UNSAT for the same bounds (56 instances).

## 7. Multi-cell A-packet crossing (scholar's question)

chain.py: Q0 + C2 -> C2 + Q1, Q1 + C2 -> C2 + (nonempty A-train), Q_i free
A-trains. UNSAT for widths Q0 <= 48, Q1 <= 28, slips 8 and 2 (15 or 9 A's
+ 7), T2 = 200. Control: the 1-cell version is SAT (0.6 s). So within
these bounds the fuel-paying crossing is one cell deep.

## 8. INC on an F store (copy)

copyspec.py: P + F -> F (untouched, same cells) + a second F exactly 29
cells to the right in the same phase (architect's clean train gap):
UNSAT for all free (30,-8)-trains P <= 20 wide (slip forced 13), all 12
classes, T2 = 300. Also UNSAT with the new F anywhere to the right.

## 9. E_n counters (scholar's one-glider unary counter)

en.py builds E_n = E + (n-1) B's by simulation (verified (15,-4)-periodic;
slips 9, 1, 7, 13, 5 for n = 1..5). B-trains are single-class against
E_n (|det((4,-2),(15,-4))| = 14).
- Control: a free B-train (<= 10 wide, slip 6) mapping E_1 -> E_2 and
  E_2 -> E_3 is found (= a single B), verified.
- DEC from the right: no free B-train <= 32 wide maps E_2 -> E_1 (alone),
  none maps E_3 -> E_2 (alone), none does both (slip forced 8; T2 = 400;
  moving window, margin 24). So with B-speed packets a counter can only be
  decremented from the left (scholar's A + E_n -> E_{n-1}).

## 10. Slip mod 14 is the ONLY linear conservation law of glider collisions

invariants.py: from collider's verified catalog (reactions.json, 874
reactions whose inputs and outputs are all named gliders A, B, Bbar, Bhat,
C1-3, D1, D2, E, Ebar, F, G, H or tight bundles A^2..A^5, B^2, B^3, E^2,
E^3; 597 distinct count vectors), the Smith normal form of the reaction
matrix over Z is diag(1, ..., 1, 14) with full rank 22. So:
- there is no exact integer conservation law (no conserved "number of"
  anything, even with weights);
- the only law mod m for any m is a multiple of one Z_14 law, and slip
  (ether offset) satisfies all 855 reaction rows, so slip mod 14 is it.
Scope: laws that are linear in the counts of glider types. Laws involving
positions/phases (e.g. architect's conjectured "phase potential" behind
no-winding) are not excluded; this says such a law cannot be a count.

## 11. More bounds (all UNSAT; exact scopes)

- Spec Z with the spec-F packet EE (E@(0,0)+E@(-13,15)): no F-speed floor
  O (free (36,-4)-train <= 20 wide, 14 slips x 6 classes, T2 = 450,
  moving window) with EE + O -> O + stationary messenger(s) only.
  Positive control: for collider's packet Ebar@(0,0)+Ebar@(-4,23) the same
  code finds floors (slip 13) in 8 of 12 placements.
- Transport through E_n: no free B-train <= 24 wide (14 slips) crosses
  E_1, E_2 and E_3 with both surviving (any displacement), T2 = 400.
- Pump: no free (30,-8)-packet <= 20 wide (14 slips x 4 classes) crosses
  two C1 markers 51 cells apart, both markers and the packet surviving,
  with the marker distance changed by a nonzero vector of
  M = <(7,0),(30,-8)> (the condition for an identical later packet to
  pump again). Control (single Ebar, no pump condition): SAT, distance
  change (2,6) or (0,0) = architect's 1-bit register. D0 = 65: running.
