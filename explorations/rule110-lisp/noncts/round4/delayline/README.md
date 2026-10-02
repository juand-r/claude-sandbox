# delayline (round 4): the gap between the counters as memory

Avenue (c): can unbounded DISTANCES (the gap between two co-moving rods,
windows that walk, signals in flight) give the mode coupling that round 3's
Theorem 1 demands? Write-up: THEORY_DL.md. Running log incl. mistakes:
NOTES.md.

## Results in one list
- [sim] DRIFT SWITCH: R2's zero answer (A) opens a value-1 window (R1 =
  E^2 -> E); from then on every right-stream NOP walks the window right
  (24.27 / 20.53 cells alternately), so the gap grows. Delay-insensitive
  except for arrivals during a NOP collision (~2.5% of phases; the switch
  fails in ~1.2%). Verified independently by verify (board 23:46).
- [sim] Window table: all 2,337 library G-speed packets on E^2 (and, from
  round-3 coupler, on E). All 422 walks of a zero RIGHT window are to the right.
  Only one packet (S43) is neutral when closed and shoots when open, and it
  closes the window at value 4.
- [sim] Left windows (A-lattice trains from the left, all 6,398 of width
  <= 30) walk BOTH ways; uniform streams walk a zero left window steadily
  (+11.2 or -2.8 cells per packet); a B^3 (R1's K3 shot) closes a rightward
  walking left window and freezes it (63/75 arrival times; the rest are
  arrivals during a packet collision).
- [sim] End to end: R1's own zero (K3 at R1 = 0 -> B^3) closes and
  freezes the walking left window (25/30 arrival shifts; controls walk on).
  Verified by verify (board 00:22, 41/41).
- [sim] Contact of a walking window with E/E^2/E^3/E^4/Ebar markers: no
  clean, repeatable contact (770 scenes).
- [SAT] Reusable reflector (needed for a per-unit handshake): none at
  width 30 (all 9 class pairs), encoding validated by fixed-packet controls.
- [thm] Slip lemma for windows: closed-neutral gates shoot 0 mod 7 units
  (or 7 - d if the shot closes the window to d).
- [sim] All 391 (4,-2) trains of width <= 30 are pure charge carriers: they
  INC rods from the back and annihilate one unit per A met; none crosses A.
- [model] Burst law floor(roundtrip/slot)+1; annihilating channel eats the
  refill; walking reflector gives non-periodic gaps.
- [arg] "One signal in flight" collapses into Theorem 1 territory or into
  the burst regime (THEORY_DL s.6).

## Files and how to reproduce (run from this directory; all write here)
| file | what | command |
|---|---|---|
| dl.py | toolkit (imports round-3 coupler two.py / cl.py read-only) | - |
| walk.py, walk2.py | zero window under uniform NOPs, per slot class (glider level) | python walk2.py |
| ds.py | drift-switch scene, glider level (+ exact CA without --noca) | python ds.py --noca |
| ds_ca.py, ds_ca.log | 18 drift-switch scenes, exact CA vs glider sim | python ds_ca.py |
| ds_dump.py, ds_scenes.json | seeds + exact-CA products of those 18 scenes | python ds_dump.py |
| ds_sweep.py, ds_sweep.log | gaps 600/1200/2400 x 41 arrival times + controls | python ds_sweep.py |
| ds_fine.py, ds_fine.log | every arrival slot 53k..58k at gap 1200 | python ds_fine.py 1200 53000 58000 |
| ds_cls.py | the A arriving in each of its 3 classes | python ds_cls.py |
| scan_e2.py, scan_e2.jsonl | 2,337 G-speed packets vs E^2, every class (~25 min) | nice -n 10 python scan_e2.py 2 |
| wtable.py, wclass.py, walkers.py | window table analysis (E and E^2 joined) | python wclass.py |
| bscan.py, bscan.jsonl, bscan.log | 391 (4,-2) trains vs A and E^m, controls B, B^3 | python bscan.py |
| burstmodel.py | event model of the burst regime (FAILURES 0) | python burstmodel.py |
| lscan.py, lscan.jsonl | left window table: 6,398 A-lattice trains vs E, E^2 from the left | python lscan.py |
| lclass.py | left window table analysis | python lclass.py |
| lgate4.py, lgate4.jsonl | walking left trains vs E^4 (window closed by B^3) | python lgate4.py |
| lwalk.py, lwalk.log | uniform left streams on a zero window | python lwalk.py 10 6 |
| lstop.py, lstop_*.log | B^3 stops a walking left window, arrival sweep | python lstop.py 499 1 5 20 100 400 4 |
| fullstop.py, fullstop_sweep.py, fullstop_scenes.json | END-TO-END: R1's zero (K3 -> B^3) stops the walking left window; 30 shifts + controls; seeds | python fullstop_sweep.py |
| contact.py, contact_an.py, contact_499_1.jsonl | walking left window into a marker (E..E^4, Ebar), 770 scenes | python contact.py 499 1 16 6; python contact_an.py contact_499_1.jsonl |
| sat_refl.py, sat_refl.jsonl, run_refl.sh, run_refl900.log, run_refl2.sh, run_refl2.log, run_ctl2.sh | SAT for the reusable reflector, controls (--fixY) | ./run_refl.sh |
| burst.py | A-burst vs R1 (first attempt, killed; superseded) | - |

PID files (*.pid) are stale once the job ends. Inputs read (never written):
round3/coupler (two.py, cl.py, scan_reflect_M1.jsonl), round2/gate,
collider, synth, round4/theory/trains_4_-2_30.jsonl,
round4/shuttle/trains_3_2_30.jsonl.
