# Non-CTS computers in Rule 110, round 4: every remaining avenue (started 2026-10-01)

State after three rounds (noncts/SUMMARY.md, round2/SUMMARY.md,
round3/SUMMARY.md):
- Built and verified: a programmable one-counter non-CTS machine (fixed
  glider stream, branches on zero, compiled loop programs); two
  addressable F-lane registers; a two-stream setup in which each counter
  has INC/DEC/zero test from its own stream and the counters signal each
  other in both directions (class-free channel K3).
- Proved in abstract models: one stream is eventually periodic; clean
  answers give decidable machines; coupling two counters through zero
  answers is never universal (Theorem 1: each counter's DRIFT must be
  changeable by the other); inside an E^n rod influence runs only front
  -> back (Theorem 2).
- Remaining escapes named by theory, none found yet: (a) a SHUTTLE (a
  persistent signal bouncing between the counters, one unit per round
  trip); (b) a RIGHT-TO-LEFT CROSSING of a counter; (c) the GAP between
  the counters used as an unbounded register / delay line; plus routes
  never tried: (d) other counter objects; (e) a queue machine with
  genuine finite control (not a CTS); (f) anything else.

Goal: a UNIVERSAL Rule 110 computer that is not a cyclic tag system,
verified end to end in the exact automaton on a small compiled program.
Intermediate goals: any construction that escapes Theorems 1/2 (a
verified shuttle, crossing, gap register, or drift switch), or a proof
that an avenue is closed (with its exact scope).

Agents, one directory each:
- delayline/ - avenue (c): the gap / unbounded distances as memory
- shuttle/   - avenue (a): wide and multi-glider shuttles, moving-window SAT
- objects/   - avenue (b)+(d): other storage objects and crossings
- queue/     - avenue (e): queue/tag machines with finite control
- theory/    - avenue (f): the map of what is still possible; models,
               literature, new escapes, closing proofs
- verify/    - independent verification, ledger, integration
