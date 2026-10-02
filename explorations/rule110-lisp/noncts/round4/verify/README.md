# round4/verify: independent verification, ledger, integration, instruments

Agent: verify (round 4). Re-runs every positive claim posted on
../BOARD.md through an independent code path (round-2/3 verify toolkit
`vlib.py`, `libgen.py`, `xlate.py`, imported read-only, plus the exact
engine `../../../engine.py` and the project's `../../../hashlife.py`),
keeps `ledger.md`, assembles scenes, and provides fast exact runners.

## Files
| file | what |
|---|---|
| `PLAN.md`, `NOTES.md`, `ledger.md` | plan, running log (incl. mistakes), every claim checked |
| `hrun.py` | HashLife runner for long scenes (`HRun(row, origin).goto(T).cells/objects`) |
| `test_hrun.py`, `test_hrun_long.py` | validation of hrun vs the packed engine (cell for cell, T <= 30,000, controls) |
| `clib.py` | collider-library objects (and collider auto-names of I_L / Z_L) into my vlib library; `rebuild(scene, T)` asserts my rows = collider's |
| `rodval.py` | value k of a rod E^k of ANY length (charge mod 7 + length), whole light cone checked |
| `rawscene.py` | scenes from raw (bits, pR) objects (shuttle's table format), with selftest |
| `pairscan.py` | all collision classes of two library objects (class = lattice fraction; asserted one outcome per class) |
| `cone_brute.py`, `wall_check.py`, `wall_plant.py` | E-bg influence cone (3/5), -3/5 walls and their phase jump, wall launches in E^45 |
| `verify_ln1.py` | theory's particle-TM example head steps (route 12) |
| `verify_merge.py` (+ .log) | shuttle's MERGE E^m, D1, E^n -> E^(m+n+1) |
| `verify_window.py`, `verify_ds.py`, `verify_ds2.py` | delayline's window walk and drift switch |
| `verify_cross.py` | queue: C x Ebar crossing displacement |
| `spot_bounce.py` | spot checks of shuttle's bounce tables |
| `review_gap2.py` | review of theory's route-20 kinematics (skipping) |

## How to run
    python3 test_hrun.py; python3 test_hrun_long.py; python3 rawscene.py; python3 rodval.py
    python3 verify_ln1.py; python3 wall_check.py; python3 wall_plant.py walls
    python3 verify_merge.py            # ~3 min, writes nothing (redirect to verify_merge.log)
    python3 verify_window.py; python3 verify_ds.py; python3 verify_ds2.py; python3 verify_cross.py
    python3 spot_bounce.py ../shuttle/bounce_table_L.jsonl 150 2
    python3 review_gap2.py scan
