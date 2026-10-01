# coupler (round 3): signals between two counters

Goal (tier T2): R1's zero changes R2 and R2's zero changes R1, verified in
the exact Rule 110 automaton; then (theory 05:49) a SHUTTLE between the
counters' inner faces. Running log with every claim, scope and mistake:
NOTES.md. Labels: [sim] full Rule 110 simulation (collider glidersim and/or
gate's exact moving-window CA, fastca), [arg] argument, [hyp] hypothesis.

## Verified results
1. T2 scenes (verify_scenes.py, log verify_scenes.log) [sim, glider AND
   exact CA, product lists equal; re-verified by verify, ledger #16]:
   - A, R1 zero -> R2: R1 program J I N N. v1 = 0: R2 += 2 (Bbar #1 at
     R2's back), echo A taken by R1 = E^2 -> E. v2 = 2..5 work; v2 = 1 is
     impossible (E^2 + Bbar is garbage in every class) and v2 = 0 needs the
     other R2 class. Controls in the other classes fail 6/6.
   - B, R2 zero -> R1: leftstream's Z_L at R2 = 0 sends an A that DECs R1
     (v1 >= 1). 15/15 inputs; controls 6/6 fail.
2. Repeated couplings with a data-dependent count (repeat.py,
   run_repeat.log) [sim, glider AND exact CA]: J I J I J I N Z^7 N J I N N
   with two N (GB4) correctors serves v1 = 0 (4 couplings) and v1 = 1 (1
   coupling); 8 of 9 corrector class pairs fail (controls).
3. Physics facts [sim unless marked]: outer-face ops leave the inner end
   fixed (n >= 2); one Z3 phase per counter end for all A/G/Bbar signals
   ([arg] <P_E,P_A> = <P_E,P_Bbar> = <P_E,P_G>); two-counter slip lemma
   [arg]: v1 + v2 mod 7 and "2b + z mod 7" at pinned zero slots are fixed.

## Negative results (scoped; see NOTES.md)
- No library G-speed packet of slip 6 emits a B at R1's zero; only the 13
  GB1 pairs emit a Bbar (scan_bemit.py).
- No shuttle from library objects: 2523 left-movers vs R2 = E^4 (every
  class), 368 multi-glider echo trains vs R1 = E^3..E^8 (15 phases): only
  n-specific B-family "dumps" (scan_reflect.py, scan_reflect2.py).
- No library left-mover crosses E^4 (same scan).
- Joint shuttle SAT (sat_shuttle.py): UNSAT at X 18 / Y 24 (54 runs) and
  first runs at 30/30; positive controls pass.

## How to run (imports round2/gate, collider, synth read-only; writes only here)
- python verify_scenes.py all          # A and B scenes, glider + exact CA
- python repeat.py 3 JIJIJINZZZZZZZNJINN 0,1 6:2,14:1   # repeated coupling
- python sat_shuttle.py --only r2 --wx 12 --wy 24 --sx 8 --K 2 --ns2 4 --T2 260 --c2 1
                                       # SAT positive control (finds Bbar/A)
- python scan_reflect.py 4 -1/2 ; python scan_reflect2.py 4 5   # library scan
- python analyze_reflect.py 4 -1/3     # summary of a scan file

## Files
cl.py (toolkit), two.py (two-counter scenes; leftstream's rigid left stream
reimplemented in collider's library), verify_scenes.py, repeat.py,
sat_shuttle.py, scan_bemit.py, scan_reflect.py, scan_reflect2.py,
analyze_reflect.py, ident_sat.py, mirror.py, run_*.sh (batches), *.log,
*.jsonl (results).
