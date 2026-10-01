# shuttle (round 4): a persistent process between two counters

Avenue (a): a shuttle between R2 (E^n, left; its BACK faces the gap) and R1
(E^n, right; its FRONT faces the gap): right-mover X reflects at R1's
front as a left-mover Y, Y reflects at R2's back as X, moving units.
Log with every claim, scope and mistake: NOTES.md. Plan: PLAN.md.
Labels: [sim] exact Rule 110, [arg], [hyp].

## Main results (details and scopes in NOTES.md)
1. [sim] E^n FRONTS NEVER EMIT: no right-moving input leaves the rod
   intact (any front shift K, any back shift J) and emits a left-mover.
   Scopes: all A-trains w <= 30 (6398), D-trains w <= 30 (1071),
   stationary patterns w <= 34 (4877), 368 library right-movers; n = 10, 11
   (library: 8..11), every class (frontsim.py, libscan.py). SAT, wall-free,
   all n >= ~10 at once (pert.py): A-trains w <= 24 every phase, w 40 one
   case. 36 other front terminations of the crystal (fronts.py): A-trains
   w <= 22 give only "eaters". So the literal shuttle is blocked at R1.
2. [sim, verified by verify] MERGE: E^m | D1 | E^n -> E^(m+n+1) (D1 in 3 of
   5 classes dumps R1 into n+1 B's that fuse into R2's back). dump2.py.
3. [sim] The dump is a GUN: a dissolution wave periodic under u = (5,2)
   (one unit eaten and one B emitted per 5 steps). gun.py finds it (6
   variants) and finds no slower front guns or back "pair-creation" guns
   in the scopes run (see NOTES).
4. Tools reusable by others: rod.py (E^n rows, crystal), pert.py (SAT
   around an exact background), trains.py (all (p,d)-trains of width <= W),
   frontsim.py / libscan.py / backscan.py (exhaustive exact face scans),
   fronts.py (crystal terminations), gun.py (periodic face structures),
   bounce.py (single-wall reflection tables for the bouncer).

## Reproduce
- python3 frontsim.py trains_3_2_30.jsonl 0 700 out.jsonl 10,11 ; python3 summarize.py out.jsonl
- python3 pert.py --K 1 --py 42,-14 --T 360 --wx 24 --wy 40 --depth 30 --phiL 0   (UNSAT)
- control: python3 pert.py --K 1 --T 120 --wx 6 --wy 10 --phiL 0 --allow_empty --out c.jsonl; python3 verify.py c.jsonl 0 2 14
- python3 dump2.py D1 0 3          (MERGE, n = 3..12)
- python3 gun.py --face front --j 0 --out g.jsonl   (dump wave; verify_gun in gun.py)
