# leftstream (round 3): a left program stream operating its own counter

Goal (tier T1): right-moving packets from the LEFT that INC, DEC and
zero-test a counter R2 (an E^n glider moving at -4/15), as a rigid stream,
verified in exact Rule 110. Running log: NOTES.md. Plan: PLAN.md.

## Results (all [sim] = exact Rule 110, typed with collider's library)
- I_L (INC from the left): (3,2) train, slip 6, cells
  111110111110111110001110 (left ether phase 0, E at seed (7,44)):
  I_L + E^n -> E^(n+1), n = 1..23, one class, displacement (7,-8).
  Found by SAT (sat_inc.py) after noting that slip conservation forbids
  any INC by fewer than 6 A's (round 1 only tried slips 8,2,10,4,12,3,9).
- D = A (DEC): E^n -> E^(n-1), n >= 2, one class, displacement (5,2);
  A + E -> C3 (counter destroyed; I_L + C3 -> E rebuilds it).
- Z_L (zero test): (3,2) train, slip 8, cells 111110111110111000111011
  (E at (6,46)): E^n -> E^(n-1) (n >= 2), E -> E + A (A leaves right);
  displacement (9,0) in both branches. Found by SAT (sat_zero.py).
- Rigid stream (lstream.py): placement by bookkeeping, one stream text for
  all inputs; 270/270 random runs (30 programs x v = 0..8) match the model;
  class-shift controls fail. Verified independently by verify (ledger).

## Searches for theory's escapes (scoped negatives)
All SAT runs have a passing positive control in the same code unless
stated; widths are the free train/object widths in cells.
- Wrap (Z + E -> E^7, DEC for n = 2,3): UNSAT, slip-8 (3,2) trains,
  W 24 and 36, all classes (sat_zero.py mode wrap; sat_wrap36.log).
- Reflection at R1's front with Y = Bbar: UNSAT W 24, k = 1,2,3
  (sat_reflect.py/.log). Moot: Bbar at R2's back emits only A.
- Crossing front -> back, any (3,2) output of the same slip: UNSAT W 24,
  all slips x classes, n = 2,3 jointly, T2 350 (sat_cross.py/.log).
- Crossing back -> front: B-trains W 24 (n 2,3 joint), Bbar-trains W 24
  (n 3, 3 classes): UNSAT, all slips (sat_crossL.py/.log). No positive
  control of the same target form exists.
- Wall converter (theory s.6.5), SAT with free co-moving B (W 24, all
  slips), I_L front op, free X (slip 6): UNSAT for n = 2,3 jointly
  (sat_conv.py/.log); controls --control and --control3 (real I_L physics,
  shifted copies) SAT. Fused caps not covered.
- Wall converter, exact scan of library co-moving objects behind E^4
  (conv_scan.py, conv_scan.jsonl): partial, see NOTES.md.

## How to run
- python3 claim_inc.py 12            INC n = 1..12 + controls, writes inc_scenes.json
- python3 check_rec.py sat_zero_results.jsonl 1 9    zero test Z_L, n = 1..9
- python3 lstream.py ZIZZIDIIDIIZZDZZ 0,1,2,3,4,5,6,7,8 [i:j]   program (+control)
- python3 rand_test.py 30 16 8 2     random programs vs model
- python3 export_stream.py PROG VS [i:j]   exact rows for re-checking
- SAT: python3 sat_inc.py 3 2 24 220 --ns 1,2,3,4 ;
       python3 sat_zero.py 3 2 24 250 A   (modes A, wrap)

## Files
lsl.py (library, placement, exact run, export), disp.py (displacement and
class key), ops.py (packet vs E^n in 3 classes), lpk.py (packet table),
lstream.py (stream builder + model), check_inc.py / check_rec.py
(independent checks of SAT rows), *_results.jsonl (SAT records).
