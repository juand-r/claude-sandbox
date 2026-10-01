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
| 8 | Z = GB3@(0,0)+GB4@(-25,46): I^v Z^3 -> E^((v-3) mod 7 +1), v=0..6 | gate (NOTES 00:00) | VERIFIED as per-input compilations (gate withdrew it as a FIXED program, 00:53) | verify_gate_wrap.py | |
| 9 | Z as a general "DEC, wrap 0->6" instruction in gate's stream | gate (implied) | REFUTED: INZZ, INZNZ, INZZNZI, INZNZNIIN fail (gate's own pipeline agrees). Cause: Z on value 1 lets its GB4 hit the zero E -> class-dependent displacement | verify_gate_wrap2.py, localize.py | fix proposed: designate classes for value-1 slots too |
| 10 | two independently addressable F-lane registers (absorption kicks), 6 programs exact | address 00:09 | VERIFIED 16/16 (cell-level F region vs prediction; others Ebar-family); controls 9/9 fail | verify_address.py | scope: history-aware schedule; no zero test. Nuance: my check compares with the predicted F seeds evolved alone; at gaps <= ~26 those F's form a compound (address zero_probe), so the usable register range starts above that |
| 11 | gate's compound packets: behaviour on values 0..3 by class | verify | [sim] table (T=4000) | prim_table.py/.log | Z on value 1: 3 trajectories, clean. (My first T=1500 table showed false debris; corrected 00:17) |
| 12 | assembler v2 fixes INZZ etc.; random INZ words = model | gate 00:14 | VERIFIED 90/90 random words (seeds 11, 12) + the 4 former failures | verify_gate_wrap2.py SEED N v2 | |
| 13 | J^5 Z^6 = "DEC wrap to 1" (parity counter) as a reusable block | gate (NOTES) | single block OK for v=0..3 with my assembler; (J^5Z^6)^4 IMPOSSIBLE with per-slot phases alone (J at zero displaces E; zero E for v=0 vs v=2 differ after 2 blocks) | adaptive_ca.py, adaptive_parity4.log | needs a phase corrector or J^3 variant |
| 14 | (J^5 Z6^6)^2 with gate's classes: v=0..3 -> v mod 2, only Bbars leave | gate 00:27 | VERIFIED as per-input compilations only (gate withdrew the fixed-program reading 00:53); my own FIXED parity streams: #18, #21 | verify_gate_parity.py | |
| 15 | M2: (J^3 Z^4)^4 fixed stream, v=0..12 (0..6 used to build) = model | verify | VERIFIED by me (needs a teammate's cross-check) | adaptive_ca.py, m2_validate.py | 7 out-of-sample inputs pass; translation invariance; control 1/7 |
| 16 | zero/one events map class c -> c + p + k; no single-packet synchronizer | verify | [sim] (scope: 9 event types, 42 phases, 3 classes) | phase_charge.py, sync_search.py | |
| 17 | Cook internals: acceptor stationary C-family, rejector D1<->A^3 transducer, leader K composition, slips (Y,N symbols slip 2), mod-7 slip law, E9 forced-N reader | queue 00:20/00:33 | PENDING (descriptive; would need my own reading of Cook's acc/rej in casim runs; lower priority than tier claims). Slip law is the same mod-7 argument as gate's lemma: ACCEPTED [arg] | | |
| 18 | M2: (J^5 Z^6)^2 (parity) built by MY assembler, v=0..12 = model | verify | VERIFIED by me (independent of gate's builder; gate's own version VERIFIED as #14) | adaptive_ca.py, m2_validate.py | |
| 19 | Z^9, XZ^9 streams from my assembler (VMAX 6) | verify | REFUTED out of sample (v=7,8 / v=7): zero events at slots not covered in training | m2_batch.log | scope lesson posted 00:38 |
| 20 | class-level calculus (calib.json) is sound for streams at spacing >= 160 | verify | [sim] 129/129 valid predictions agree with CA (differential, random words/phases) | calculus.py | at spacing 110: 2 disagreements (3-body overlap) |
| 21 | M2 by compiler: 4 planned programs (parity x4, Z^12, (J3Z4)^8, (J6Z7)^3) = model in exact CA, inputs 0..15/14 (planned 0..12) | verify | VERIFIED by me; awaiting independent cross-check | plan_check.py, plan_batch.log | |
| 22 | fixed program (Z6 N)^10, v=0..9 -> (v-10) mod 7 | gate 00:53 | VERIFIED (items identical across inputs; own translation/typer; stable; control breaks v=1 only) | verify_gate_ra.py | |
| 23 | my M2 streams are fixed programs (program items identical for all inputs) | verify | checked (build_right placements) | inline check, plan_ZZZZZZZZZZZZ.json | |
| 24 | guarded-block machine (zero DEC aborts rest of block) with 5 registers (3 bounded) compiles any Minsky machine | verify | [sim, model] 402/402 differential tests vs scholar's interpreter; control 46 fail | gbm.py | |
| 25 | FIXED-stream two-register F lane (fixed_stream.py; 3/3 in run_fixed2.log) | address (NOTES 01:40) | VERIFIED 4/4 (own gap measurement), fixedness checked; MY dynamic controls 4/4 fail (address's own control fails at build time only) | verify_address_fixed.py | working range: registers >= -2 units (address) |
| 26 | fixed parity-8 stream (J^4 L Z6^6)^8, v=0..11 | gate (files, 01:1x) | VERIFIED (items identical; own translation/typer; stable) | verify_gate_ra2.py, verify_parity8.log | |
| 27 | F-lane abort step 1: C1 eats neutral pairs a=(-4,23)#3, b=(-22,39)#3 in any number, gate (-9,29)#3 removes it -> one Ebar | gate 01:22 | VERIFIED (+ abort-start independence; no-C1 pass; 2 controls fail) | verify_abort.py | |
