# Verification ledger (round 3)

Status: VERIFIED / REFUTED / CANNOT REPRODUCE / PENDING / [arg] ACCEPTED.
Each entry: claim, who, when posted, my check (script), control, result.

| # | claim | by | status | check | notes |
|---|---|---|---|---|---|
| 1 | INC from the left: (3,2) train I_L = 111110111110111110001110 (slip 6): I_L + E^n -> E^(n+1), nothing else, n = 1..12, one class (n = 1: two classes) | leftstream 05:40 | VERIFIED | verify_inc.py | A: their 36 exported rows run by the engine, typed by MY typer: 12/12 INC rows give E^(n+1); controls agree with theirs (their n=1 shift-2 exception reproduced). B: MY construction (my E^n from my own E+B harvests, train pasted at 3 time phases x 4 offsets): for each n = 1..12 exactly one class gives E^(n+1) (n = 1: two), consistent over 4 offsets; other classes debris. Cell-for-cell equality of my rows with theirs not done (my B rows use my E^n, not E + B's): independence is by construction instead |
| 2 | DEC from the left: A + E^n -> E^(n-1) in 1 class (n = 2..8); A + E -> C3 | leftstream 05:40 | VERIFIED (n = 2..6, survey) | survey_left.py | also A + E^2 -> E in all 3 classes; displacement (5,2) not separately checked |
| 3 | [integration, mine] fixed LEFT stream of INC (I_L) and DEC (A) packets operating E^n: 38-op word built on v = 1..4, = model on v = 1..11; program cells identical for all inputs; control (one slot to another class) fails 11/11 | verify | VERIFIED by me (needs a teammate's cross-check) | t1lib.py, t1_nonzero.py, t1_validate.py | no zero test yet: only words whose values stay >= 0 (v = 1 passes through 0) |
