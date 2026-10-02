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
| `spot_phase.py` | for table rows: is a disagreeing wall_out our product in another time phase? |
| `bouncer_direct.py` (+ bd_L.jsonl, bd_L.log) | direct exact search for a perpetual bouncer: every clean L-reflection x every wall_R (84,700 runs) |
| `bd_chains.py` | (rough) inspection of long-lived bouncer runs |
| `verify_lstop.py`, `verify_fullstop.py` | delayline's reverse switch and end-to-end fullstop |
| `verify_cstack.py`, `verify_xconv.py`, `verify_scanfront.py` | objects' C-stacks, bubble-wall conversion, front-launched walls |
| `w4_scan.py`, `w4_repeat.py`, `w4_probe.py`, `w4_cands.py` (+ logs) | route 23 W4: class-dependent back blocks, their stream dynamics, class shift per unit |
| `queue_repro.log` | reproduction of queue's forced-N read (their code) |

## How to run
    python3 test_hrun.py; python3 test_hrun_long.py; python3 rawscene.py; python3 rodval.py
    python3 verify_ln1.py; python3 wall_check.py; python3 wall_plant.py walls
    python3 verify_merge.py            # ~3 min, writes nothing (redirect to verify_merge.log)
    python3 verify_window.py; python3 verify_ds.py; python3 verify_ds2.py; python3 verify_cross.py
    python3 spot_bounce.py ../shuttle/bounce_table_L.jsonl 150 2
    python3 review_gap2.py scan
    python3 spot_bounce.py SNAPSHOT 150 3 R; python3 spot_phase.py SNAPSHOT R absorbed 150 4
    python3 bouncer_direct.py control; python3 bouncer_direct.py SNAPSHOT bd_L.jsonl 40000   # resumable, ~50 min total
    python3 verify_lstop.py; python3 verify_fullstop.py ../delayline/fullstop_scenes.json
    python3 verify_cstack.py; python3 verify_xconv.py; python3 verify_scanfront.py
    python3 w4_scan.py 6; python3 w4_repeat.py 5 80 12 6 600 600; python3 w4_probe.py; python3 w4_cands.py 4
(SNAPSHOT = a frozen copy of shuttle/bounce_table.jsonl; the file is >100 MB and not committed.)

## Status (01:10 UTC)
See ledger.md (29 entries) and the final board post.
