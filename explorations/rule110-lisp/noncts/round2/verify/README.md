# verify/ (round 2): independent verification, theory, integration

The verify agent re-checks teammates' positive claims through its own code
path, keeps the ledger, works out what glider-level primitives can and
cannot give, and assembles end-to-end demonstrations.

## Files

| file | what |
|---|---|
| `vlib.py` | Independent toolkit: Rule 110 step, ether-phase rule, row builder from Martinez strings, placement by spacetime seed, exact typer (canonical defect keys over all phases), compound harvesting. `python3 vlib.py` runs a self test. |
| `libgen.py` | Builds my compound library (E^2..E^15, GB1..GB8, A^2..A^4) from my own collisions; cached in `lib_v1.pkl`. |
| `xlate.py` | Translates collider-convention scenes (used by collider, gate, address) into my convention, and asserts that my rebuilt row equals collider's `build_row` cell for cell. |
| `ledger.md` | Every claim checked: who made it, status, script. |
| `THEORY.md` | Chain-machine theorem (clean answers give decidable machines), feed-forward theorem, the one-counter ceiling, tier status. |
| `models.py` | Chain machines with executable checks. `chain_search.py` and `tz_search.py` are random searches. |
| `m1_*.py` | My [GB3, G] non-monotone gadget (M1, weak form) and the garbage studies. |
| `verify_gate_wrap*.py`, `gate_scene.py` | Checks of gate's wrap packets and assemblers. |
| `verify_address.py` | Check of address's two F-lane registers. |
| `prim_table.py/.log` | Gate's packets on values 0..3 in every class, with trajectory offsets. |
| `adaptive_ca.py`, `m2_validate.py` | My own greedy assembler (exact CA in the loop) and the M2 validation. |
| `calib.py`, `calib.json`, `calculus.py`, `plan_check.py` | Measured class-level transition table, the abstract (value, class) machine with a planner that inserts correctors, and CA validation of planned streams. This is the M2 compiler. |
| `gbm.py` | Guarded-block machine (M3 target) and its Minsky compiler with a differential test. |
| `sync_search.py`, `phase_charge.py` | Class algebra measurements. |
| `verify_gate_ra*.py`, `verify_gate_parity.py`, `verify_abort.py`, `verify_address_fixed.py`, `verify_catalog.py` | Later verifications (see ledger). |
| `NOTES.md` | Running log, including mistakes. |

## How to reproduce the main checks

    python3 vlib.py                              # self test
    python3 models.py                            # chain-machine checks
    python3 m1_program.py                        # M1 gadget + control
    python3 verify_gate_wrap.py                  # gate's I^v Z^3
    python3 verify_gate_wrap2.py 11 30 v2        # gate's assembler v2, random words
    python3 verify_address.py 1 4                # address's two registers
    python3 adaptive_ca.py JJJZZZZJJJZZZZ 6      # build an M2 stream
    python3 m2_validate.py adaptive_<word>.json 12
    python3 calculus.py 2 30                     # calculus vs CA differential test
    python3 plan_check.py JJJJJZZZZZZJJJJJZZZZZZJJJJJZZZZZZJJJJJZZZZZZ 12 15   # parity stream
    python3 gbm.py                               # guarded-block machine compiler

All runs use the exact engine `../../../engine.py` (bit-packed, cyclic, with
margins wider than the light cone). My own stepper is cross-checked against
it in the self test.
