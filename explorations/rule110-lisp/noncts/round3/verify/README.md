# round3/verify: independent verification, integration, instruments

Agent: verify (round 3). Re-runs every positive claim on the board through
my own code path (round-2 verify toolkit `vlib.py`/`libgen.py`/`xlate.py`,
imported read-only from `../../round2/verify/`, plus the exact engine
`../../../engine.py`), keeps `ledger.md`, assembles two-stream scenes (T1, T2,
T3) and builds/validates the instruments for long exact runs.

## Files
| file | what |
|---|---|
| `ledger.md` | every claim checked: claim, who, status, script |
| `NOTES.md` | running log, including mistakes |
| `v3.py` | shared helpers (imports round-2 vlib; exact runs; typing) |
| `streamwin.py` | exact two-stream moving window (free streams as checked periodic references; per-cell `run` and packed `run_packed`); `from_items`, `snapshot` |
| `test_streamwin*.py` | validation of streamwin against full engine runs, with controls |
| `t1lib.py`, `t1_nonzero.py`, `t1_validate.py`, `t1_build.py` | T1: left-stream packets I_L / A / Z_L in my library; greedy fixed-stream builder (CA in the loop) + validation with controls |
| `verify_inc.py`, `verify_zero.py` | checks of leftstream's INC and zero-test trains (their rows + my construction) |
| `t2_explore*.py`, `t2_class.py`, `t2_r2r1.py`, `t2_compose*.py`, `t2_kA.py`, `t2_zz.py`, `t2_multiA.py` | coupling-class studies (R1 -> R2 Bbar, R2 -> R1 A) |
| `edge_check.py` | which counter end moves under each op (exact trajectories) |
| `t2_demo.py`, `t2_demo_check.py`, `t2_demo.json` | T2 integrated demo: both coupling directions in one run |
| `verify_coupler1.py`, `verify_coupler2.py` | checks of coupler's J I semantics and T2 scenes (their scenes via xlate, rows equal) |
| `lm_check.py` | independent re-implementation of theory's transfer-machine compiler |
| `face_test.py` | generic tester for face reactions (shuttle candidates) |
| `refl_brute.py` | brute-force search for reflections by two-part A-family trains |
| `survey_A16.py` | A + E^n up to n = 15 (coupler's no-reflection claim) |
| `survey_left.py` | independent survey: right-movers / stationary objects hitting E^n, all classes |

## How to run
    python3 v3.py            # self test
    python3 survey_left.py   # starting-fact survey (writes survey_left.log)
    python3 test_streamwin.py; python3 test_streamwin_long.py; python3 test_streamwin_packed.py
    python3 verify_inc.py; python3 verify_zero.py           # leftstream's trains
    python3 t1_build.py ZIZZIDIIDIIZZDZZ 0 3 && python3 t1_build.py ZIZZIDIIDIIZZDZZ 0 11 check   # T1
    python3 t2_demo.py 2 7 && python3 t2_demo_check.py 9     # T2 demo (both directions)
    python3 verify_coupler2.py                               # coupler's T2 scenes
    python3 lm_check.py                                      # transfer machine compiler
