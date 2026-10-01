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
2. K3 channel (best R1 -> R2 coupling found): K3 = GB1@(0,0)+GB3@(-18,30)
   is a class-free INC 3 for n >= 2 and, at R1's zero (its class 0),
   passes R1 as a B^3 that INCs R2 by 3 at R2's back in its ONLY class:
   "if R1 = 0 then R2 += 3 else R1 += 3", no echo, valid for every R2
   value. Scene C (verify_scenes.py C, verify_scenes_C.log) [sim, glider
   AND exact CA]: 28/28 inputs, R2 at all three seed times 6/6, controls
   4/4. Repeated: K3 Z^7 K3 N N serves v1 = 0 (2 couplings) and v1 = 4
   (1 coupling) with no correctors (repeat.py; exact CA; controls 4/4).
   Family of clean zero-crossing packets: cross0_clean.txt.
3. Repeated Bbar couplings with a data-dependent count (repeat.py,
   run_repeat.log) [sim, glider AND exact CA]: J I J I J I N Z^7 N J I N N
   with two N (GB4) correctors serves v1 = 0 (4 couplings) and v1 = 1 (1
   coupling); 8 of 9 corrector class pairs fail (controls).
4. Physics facts [sim unless marked]: outer-face ops leave the inner end
   fixed (n >= 2); one Z3 phase per counter end for all A/G/Bbar signals
   ([arg] <P_E,P_A> = <P_E,P_Bbar> = <P_E,P_G>); two-counter slip lemma
   [arg]: v1 + v2 mod 7 and "2b + z mod 7" at pinned zero slots are fixed.

## Negative results (scoped; see NOTES.md)
- No library G-speed packet of slip 6 emits a B at R1's zero; only the 13
  GB1 pairs emit a Bbar (scan_bemit.py).
- No shuttle from library objects: 2523 left-movers vs R2 = E^4 (every
  class), 368 multi-glider echo trains vs R1 = E^3..E^8 (15 phases): only
  n-specific B-family "dumps" (scan_reflect.py, scan_reflect2.py).
- No library left-mover crosses E^4 (same scan). At R1's ZERO, 42
  library G-speed packets do cross as pure B-trains (scan_reflect_M1),
  7 of them clean at n >= 2 (cross0_clean.txt).
- [arg] Every right-moving signal meets E^n in >= 3 classes; the only
  one-class left-mover faster than E is the B family.
- Joint shuttle SAT (sat_shuttle.py): UNSAT at X 18 / Y 24 (54 runs) and
  first runs at 30/30; positive controls pass.

## How to run (imports round2/gate, collider, synth read-only; writes only here)
- python verify_scenes.py all          # A and B scenes, glider + exact CA
- python repeat.py 3 JIJIJINZZZZZZZNJINN 0,1 6:2,14:1   # repeated Bbar coupling
- python repeat.py 1 TZZZZZZZTNN 0,4  # repeated K3 coupling (T = K3)
- python verify_scenes.py C            # K3 scenes, glider + exact CA
- python cross0.py 6 'GB1@(0,0)+GB3@(-18,30)'   # K3 vs E^1..E^6, all classes
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

## Notes on files
- *.pid files are stale (no process of mine is running); scan_reflect.pid
  recorded a wrapper PID by mistake (see NOTES.md).
- run_repeat2.sh (Bbar single coupling + correctors) was prepared but not
  run; with K3 the question is moot (K3 needs no correctors).
