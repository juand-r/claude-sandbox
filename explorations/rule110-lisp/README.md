# rule110-lisp

A Lisp that runs on the Rule 110 cellular automaton -- as far down the
tower as physics and arithmetic allow. The construction is a chain of
verified translations:

    mini-Lisp -> SKI -> Turing machine -> clockwise binary TM
      -> 2-tag system (Neary-Woods) -> cyclic tag system
      -> Rule 110 gliders (Cook's blocks)

Every arrow is differentially tested against the layer above. Compiled
Lisp runs on a 255-state Turing machine; a full machine-to-CTS tower is
verified exactly; Cook's glider construction is reproduced and runs real
cyclic tag programs on the actual automaton. Physical execution of the
whole tower is out of reach by ~17 measured orders of magnitude --
REPORT.md tells that story with the numbers.

## Files

- `REPORT.md` - the full writeup: results, defect analysis, blowup table
- `PLAN.md`, `NOTES.md` - live plan and lab notes (incl. debugging log)
- `engine.py` - Rule 110 simulators (scalar + bit-packed)
- `encoder.py`, `decoder.py`, `data/blocks.json` - CTS <-> Rule 110
- `cts.py`, `tag.py`, `tm.py`, `cw.py`, `nw.py` - the machine layers
- `lisp.py`, `lisp_to_ski.py`, `ski.py`, `ski_graph.py`, `ski_tm.py` - Lisp
- `run_*.py` - CA experiment scripts (see REPORT.md, Reproduction)
- `tools/extract_blocks.py` - regenerates block data from arXiv:0906.3248

## Running

    pip install numpy pytest pillow
    pytest explorations/rule110-lisp/tests -q     # 38 tests, ~8 s
