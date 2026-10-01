# Non-CTS computers in Rule 110, round 3: two program streams (started 2026-10-01)

Round 2 (round2/SUMMARY.md) built a programmable one-counter machine that
is not a cyclic tag system, and proved, in abstract models, that one
program stream cannot do more: one counter decides only eventually
periodic predicates, and with one stream a downstream register cannot
feed back to an upstream one. Those theorems assume ONE stream. Cook's
own machine has two (table data from the right, ossifiers from the
left). Round 3 tests the two-stream route.

Idea: two counters, each the frontmost store of its OWN stream (a right
stream of G-speed packets for R1, a left stream of right-moving packets
for R2), coupled by the answers they emit toward each other.

Goal, in tiers:
- T1: two-stream physics: a left stream that can INC, DEC and zero-test
  its own counter, verified in the exact automaton.
- T2: coupling: a zero event of one counter changes the other counter
  (both directions), verified in the exact automaton.
- T3: a universal two-stream machine: an abstract model with a compiler
  from Minsky machines (theory) realised end to end in Rule 110 on a
  small program.

Agents, one directory each:
- theory/     - abstract two-stream machines: what coupling suffices for
                universality; compiler + differential tests; reaction specs
- leftstream/ - the left stream acting on its own counter (T1)
- coupler/    - signals between the two counters, geometry, classes (T2)
- verify/     - independent verification, ledger, end-to-end integration
