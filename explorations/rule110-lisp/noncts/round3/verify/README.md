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
| `ebg_search.py`, `ebg_vel.py`, `longrod.py`, `rod_defect.py`, `rod_inject.py` | defects inside the E-infinity background of a rod (phonon = +2/5 domain wall; co-moving cuts); long rods by splicing |
| `phonon_bbar.py`, `phonon_g.py`, `phonon_emit.py` | does a phonon change back-face reactions (Bbar: yes; G packets: see log); which front ops launch one (I_L, Z_L yes; A no) |
| `shuttle_run.py`, `mktrain.py` | long exact runs of candidate shuttles (streamwin, no streams); cutting rigid trains as raw cells |
| `census_check.py` | second typer (project census.py) on the T2 demo's final rows |
| `verify_coupler4.py` | coupler's class-free back-face pair reactions (42/42 phases) |
| `ebg_exh.py`, `ebg_exh.log` | exhaustive 16-cell perturbations of the rod interior |
| `wall_conv.py`, `wall_conv2.py` | theory s.6.5 wall-converter test (parked objects behind the back) |
| `test_streamwin_t1.py` | streamwin on the real 40-op T1 program vs full engine |
| `verify_coupler3.py` | coupler's SAT reflection rows (X + E^4 -> B + E^2) |
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

## Status (06:35 UTC)
- Ledger: 26 entries. Teammates' positive claims VERIFIED through my own
  code path (my builder/typer, rows equal where rebuilt from their seeds):
  leftstream I_L, Z_L, rigid streams, C-ladder DI, Bbar-front invariance;
  coupler J I semantics and T2 scenes A/B, SAT row X + E^4 -> B + E^2;
  theory's transfer-machine compiler (independent re-implementation).
  Reviewed theory's Theorems 1-2 (fixes adopted by theory).
- Integration: T1 (fixed left streams over I_L/A/Z_L, my builder) and T2
  (both coupling directions in one exact run, fixed programs) done; T3 not
  reachable: theory proves value coupling insufficient; no shuttle /
  crossing / wall converter found (my side searches, scoped).
- Instrument: streamwin.py (exact two-stream moving window), validated.
- Physics found on the way: R1's inner face rotates class per A-DEC (no
  repeated R2 -> R1 signals); inside a rod a +2/5 domain wall ("phonon")
  launched by I_L / Z_L, which switches a coincident Bbar's class at the back.
