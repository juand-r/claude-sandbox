# Verification ledger (round 2)

Status: VERIFIED / REFUTED / CANNOT REPRODUCE / PENDING.
Each entry: claim, who, when posted, my check (script), control, result.

| # | claim | by | status | check | notes |
|---|---|---|---|---|---|
| 1 | E^n + GB3/GB4/GB5 -> E^(n-1)/E^n/E^(n+1), n>=2, all classes, same product event | collider (round 1) | VERIFIED (own code) | t4.py (vlib, 42 G phases, n=2..5) | E^3+GB4 1/42 phase gave debris (probably too-close placement; unchased) |
| 2 | at zero: E + GB3 -> E + A in one class; GB4 -> E, GB5 -> E^2 all classes | collider/scholar (round 1) | VERIFIED, with a caveat | t4.py | GB4/GB5 at zero leave the E/E^2 at 3 different positions (class-dependent displacement) |
| 3 | E^n + G -> E^(n-1) + A^3 (n>=2, all classes); E + G -> C3+A^3 / E+A^4 / F by class | collider (round 1) | VERIFIED | t5.py | round-1 formula "E^(n+k-4)" is wrong for k<3: it is E^(n-1) + A^(3-k) |
| 4 | [GB3][G] gadget: v=0 -> E^3; v>=2 -> E^(v-1)+A^3; v=1 -> F | verify (me) | VERIFIED by me (own typer + round-1 census typer), control fails as required | m1_program.py, m1_verify.py | needs independent re-check by a teammate |
| 5 | garbage-free 3-packet completions of #4 are all exactly linear (202/202) | verify (me) | [sim] scope: X in {G,GB1..5}, 42 phases x 11 offsets, v=0..4, T=4200 | m1_search.py, m1_search.log | |
| 6 | a branch on one E-counter must emit garbage (slip mod 7) | gate 23:37 | ACCEPTED [arg]; consistent with my charge audit of the catalog (mod 7 conserved given E-count) | catalog audit (inline) | |
| 7 | F lane cannot stack registers (catalog-level) ; G world has room for one register | address 23:54 | PENDING (argument consistent with my feed-forward theorem) | | |
| 8 | Z = GB3@(0,0)+GB4@(-25,46): I^v Z^3 -> E^((v-3) mod 7 +1), v=0..6 | gate (NOTES 00:00) | VERIFIED (own translation+typer; control changes the zero case only) | verify_gate_wrap.py | |
| 9 | Z as a general "DEC, wrap 0->6" instruction in gate's stream | gate (implied) | REFUTED: INZZ, INZNZ, INZZNZI, INZNZNIIN fail (gate's own pipeline agrees). Cause: Z on value 1 lets its GB4 hit the zero E -> class-dependent displacement | verify_gate_wrap2.py, localize.py | fix proposed: designate classes for value-1 slots too |
| 10 | two independently addressable F-lane registers (absorption kicks), 6 programs exact | address 00:09 | VERIFIED 16/16 (cell-level F region vs prediction; others Ebar-family); controls 9/9 fail | verify_address.py | scope: history-aware schedule; no zero test |
| 11 | gate's compound packets: behaviour on values 0..3 by class | verify | [sim] table (T=4000) | prim_table.py/.log | Z on value 1: 3 trajectories, clean. (My first T=1500 table showed false debris; corrected 00:17) |
