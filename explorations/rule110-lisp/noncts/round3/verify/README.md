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
| `survey_left.py` | independent survey: right-movers / stationary objects hitting E^n, all classes |

## How to run
    python3 v3.py            # self test
    python3 survey_left.py   # starting-fact survey (writes survey_left.log)
    python3 test_streamwin.py; python3 test_streamwin_long.py; python3 test_streamwin_packed.py
