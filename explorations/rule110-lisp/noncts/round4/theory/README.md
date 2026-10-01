# theory (round 4): the map of what is still possible

Avenue (f): keep the map of routes to a universal, non-CTS Rule 110
computer; prove or sharpen no-go theorems and find their loopholes; write
executable models for the most promising routes; post reaction specs.

- `ROUTES.md`: the route table (needs, theorem, status, owner) and ranking.
- `THEORY.md`: results with labels ([thm], [model], [sim], [arg], [hyp]).
- `NOTES.md`: running log, including mistakes.  `PLAN.md`: checklist.

Code (all imports of collider/, scholar/, round3/theory, shuttle/ are read-only):

| file | what | how to run |
|---|---|---|
| `ptm.py` | particle-TM layer: exact single-class head/cell reactions (collider pipeline), the natural TM `run()` | library module |
| `test_ptm.py` | differential test of `ptm.react` vs the census (control: wrong cell) | `python3 test_ptm.py 120 1` -> 120/120, control 9/120 |
| `lnscan2.py` | census: library heads x library stationary objects (resumable) | `nice -n 10 python3 lnscan2.py 2` |
| `lnscan.py` | the same question on collider's existing catalog only | `python3 lnscan.py` |
| `passsearch.py` | packets of base A/B/D gliders vs cells: passes and fixpoints | `nice -n 10 python3 passsearch.py A 5 70` |
| `btrains.py` | SAT enumeration of all B-lattice trains (uses shuttle's enumerator) | `nice -n 10 python3 btrains.py 30` |
| `passraw.py` | all trains w <= 30 (A, D, B lattices) vs C1-C3: passes, fixpoints; controls | `python3 passraw.py 3 2 C1 controls`; `nice -n 10 python3 passraw.py 3 2 C1,C2,C3` |
| `explore.py`, `explore2.py` | run the natural TM from library heads / from all trains on uniform tapes (bouncer and ratchet search) | `nice -n 10 python3 explore2.py 200` |
| `bouncer.py` | route 14 model: Minsky -> transfer machine -> bouncer reflection table; differential test + 2 controls | `python3 bouncer.py` (exit 0 = pass) |

Every Rule 110 claim here comes from collider's exact stepper and typer;
see THEORY.md s.3 for the scope of each search.
