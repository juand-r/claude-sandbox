Files retired from the project but kept for reference (see REVIEW.md for
why each was retired). Nothing here is imported or tested.

Experiment scripts retired 2026-09-30 (REVIEW.md E2). They duplicated
the same setup code; the two whose results are cited now live in
experiments.py on top of casim.py:
- run_L_min.py, run_empties_test.py -> experiments.py lblock
- run_demol.py -> experiments.py demol
The rest diagnosed the "one read per left period" timing model that
REVIEW.md B1 shows to be wrong (run_demol_arrv/diag/v2, run_L_event), or
validated programs the construction does not support (run_canonical:
unbounded rejection runs), or produced results that the decoder cannot
support (run_grower, run_mixed, run_drain: see REVIEW.md B3).
