# rule110-lisp

A Lisp whose execution bottoms out in the Rule 110 cellular automaton,
built as a chain of translations, each tested against a reference
interpreter for the layer above:

    mini-Lisp -> SKI -> Turing machine -> clockwise binary TM
      -> 2-tag system (Neary-Woods) -> cyclic tag system
      -> Rule 110 initial condition (Cook's glider blocks)

Compiled Lisp runs on a 256-state Turing machine; the machine-to-CTS
tower is verified exactly; Cook's construction is reproduced exactly at
the initial-condition level and its glider dynamics are measured with a
glider census. What is and is not verified, and what it all costs, is in
REPORT.md.

Version 0.1.0 (tag `rule110-lisp-v0.1.0`).

## Documents

- `REPORT.md` - results, evidence, open problems, cost of the tower
- `DIRECTIONS.md` - proposal for faster / more direct constructions
- `REVIEW.md` - takeover review: every finding and its disposition
- `CHANGELOG.md` - release notes
- `PLAN.md` - work plan; `NOTES.md` - lab notes and debugging log

## Code

| module | layer |
|---|---|
| `lisp.py` | reference mini-Lisp interpreter |
| `lisp_to_ski.py` | Lisp -> SKI compiler, value decoder |
| `ski.py`, `ski_graph.py` | SKI engines: string (specification), graph (fast) |
| `ski_tm.py` | Turing machine that normalizes SKI terms |
| `tm.py` | two-way TMs; Cocke-Minsky TM -> tag system |
| `cw.py` | two-way -> clockwise -> binary clockwise TM |
| `nw.py` | Neary-Woods 2-tag system from a binary clockwise TM |
| `tag.py`, `cts.py` | tag systems, TS -> CTS; CTS interpreter |
| `encoder.py`, `data/blocks.json` | CTS -> Rule 110 initial row |
| `engine.py` | Rule 110 simulators (scalar, bit-packed) |
| `casim.py` | running an encoded CTS on the automaton |
| `census.py` | glider census: find and type gliders in a row |
| `decoder.py` | moving-data reader (diagnostic) |
| `experiments.py` | the long automaton runs cited in REPORT.md |
| `tools/extract_blocks.py` | regenerates the block data from arXiv:0906.3248 |

`trash/` holds retired files, kept for reference.

## Running

    pip install numpy pytest pillow
    pytest tests -q                      # ~8 s, all layers
    python experiments.py fronts         # REPORT.md 3.3, several minutes
