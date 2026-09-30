# architect/

Machine architecture for a non-CTS computer in Rule 110. The design and
its status are in ARCHITECTURE.md; the running log is NOTES.md.

All scripts import collider's library read-only (`../collider`) and must
be run from this directory. Heavy runs take minutes to hours; run one at
a time.

| script | what it does |
|---|---|
| `rx.py` | placement helpers on collider's library (run, chain, class of a pair) |
| `cat_pairs.py X Y ...` | print every collision class of the given pairs |
| `yb.py`, `yb3.py` | clean-crossing displacements; three-body (order-independence) check |
| `m1_bidir.py`, `m1_robust.py` | F train + messenger + Ebars, pairwise-clean design (fails) |
| `m1_yb.py`, `m1_predict.py` | the order-independent lane (C1, F, Ebar): 20 timings, exact positions, census |
| `palg.py`, `winding.py`, `winding2.py` | no-winding test for single crossings |
| `multibody.py`, `winding3.py` | multi-body Ebar pairs; winding and INC/DEC cycles |
| `xcounter.py [long]` | crossing counter with history-relative placement |
| `xstream.py [seed n]` | crossing counter driven by a fixed periodic stream |
| `xcensus.py` | census view of a fixed-stream run |
| `xstream2.py` | variant with DEC' = DEC + split packets |
| `cpump.py` | stationary C pairs pumping an F pair from the left |
| `ztest*.py`, `zc_fast.py`, `probe_*.py` | zero-test searches (negative so far) |
| `zero_state.json` | exact zero state and slot seeds (for synth's SAT spec Z2) |
| `render.py` | ether-filtered spacetime PNG of placements |

`trash/` holds superseded scratch (my first glider zoo and harness).
