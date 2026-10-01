# coupler (round 3): signals between two counters

Goal (tier T2): R1's zero changes R2 and R2's zero changes R1, verified in
the exact Rule 110 automaton; then (theory 05:49) a SHUTTLE between the
counters' inner faces. Running log with all claims, scopes and mistakes:
NOTES.md.

## Results
- verify_scenes.py (log verify_scenes.log) [sim: glidersim AND exact CA]:
  Scene A (R1 zero -> R2 += 2 via J's Bbar, echo absorbed by R1) and
  Scene B (R2 zero -> R1 -= 1 via leftstream's Z_L answer A), fixed program
  texts, several inputs, controls in the other classes fail.
- Physics facts used (NOTES.md): counter ends are independent (outer ops
  leave the inner end fixed); one Z3 phase per counter end for A/G/Bbar
  signals; two-counter slip lemma (v1 + v2 mod 7 fixed by consumption).
- Shuttle search: sat_shuttle.py (joint SAT for both reflections), batches
  run_shuttle*.sh -> run_shuttle*.log, sat_shuttle_results.jsonl.

## How to run (from this directory; imports round2/gate, collider, synth
read-only; nothing is written outside this directory)
- python verify_scenes.py all          # A and B scenes, glider + exact CA
- python verify_scenes.py A --noca     # glider level only (fast)
- python sat_shuttle.py --only r2 --wx 12 --wy 24 --sx 8 --K 2 --ns2 4 --T2 260 --c2 1
                                       # positive control (finds Bbar/A)
- python sat_shuttle.py --wx 30 --wy 30 --sx 8 --K 2 --ns1 4 --ns2 4
                                       # joint shuttle search
- python scan_bemit.py 6               # G-speed packets emitting at zero

## Files
cl.py (toolkit), two.py (two-counter scenes; leftstream's rigid left
stream reimplemented in collider's library), verify_scenes.py,
sat_shuttle.py, scan_bemit.py (+ .jsonl), run_shuttle*.sh.
