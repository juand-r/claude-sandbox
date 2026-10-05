# rule110-lisp

A Lisp whose execution bottoms out in the Rule 110 cellular automaton,
built as a chain of translations, each tested against a reference
interpreter for the layer above:

    mini-Lisp -> SKI -> Turing machine -> clockwise binary TM
      -> 2-tag system (Neary-Woods) -> cyclic tag system
      -> Rule 110 initial condition (Cook's glider blocks)

Compiled Lisp runs on a 256-state Turing machine; the machine-to-CTS
tower is verified exactly; Cook's construction is reproduced exactly at
the initial-condition level; and the glider machinery, checked read by
read, computes De Mol's 3x+1 tag system through the whole Collatz
trajectory 3 -> 5 -> 8 -> 4 -> 2 -> 1 (2.07e8 generations). A compiled
Turing machine (the smallest that changes state and moves) also runs on
the glider field, 5,970 CTS reads over 2.5e11 generations, with its
visits decoded from the reads; that takes the HashLife engines of
REPORT.md section 5. What is and is not verified, and what it all costs,
is in REPORT.md. `noncts/` holds
a team exploration of Rule 110 computers that are not cyclic tag
systems: a programmable (not universal) one-counter machine was built
and cross-verified (noncts/round2/SUMMARY.md).

Version 0.2, unreleased (v0.1.0 was tagged `rule110-lisp-v0.1.0`; v0.1.1 was not tagged; see CHANGELOG.md).

## Documents

- `REPORT.md` - results, evidence, open problems, cost of the tower
- `DIRECTIONS.md` - options for faster / more direct constructions, with status
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
| `cw.py` | two-way -> clockwise -> binary clockwise TM; direct binary construction |
| `nw.py` | Neary-Woods 2-tag system from a binary clockwise TM |
| `tag.py`, `cts.py` | tag systems, TS -> CTS; CTS interpreter; empty-appendant rewrite |
| `encoder.py`, `data/blocks.json` | CTS -> Rule 110 initial row |
| `engine.py` | Rule 110 simulators (scalar, bit-packed) |
| `casim.py` | running an encoded CTS on the automaton: `Run` (cyclic array), `StreamRun` (exact streaming window, checkpointable), `layout` (the initial row as segments, never materialized) |
| `hashlife.py`, `hlc.c` | 1-D HashLife (exact): C core via ctypes (compiled on first import), Python API, `HashRun` |
| `epochrun.py` | long runs: HashLife on a tree rebuilt every few reads from the active region and the next ossifiers and appendants |
| `gas.py`, `gasc.c`, `gasc.py`, `gasrun.py`, `gascensus.py` | event engine (exact): gliders as particles, collisions simulated once and memoized; C event loop; Cook's layout with lazy sides and the read driver |
| `census.py` | glider census: find and type gliders in a row |
| `decoder.py` | moving-data reader (diagnostic) |
| `experiments.py` | the long automaton runs cited in REPORT.md |
| `tools/extract_blocks.py` | regenerates the block data from arXiv:0906.3248 |
| `data/collatz_v12216.log` | the read-by-read log of the Collatz run (REPORT.md 3.6); `_hash.log`: the same on HashLife |
| `noncts/` | non-CTS team: SUMMARY.md, BOARD.md, one directory per agent |

`trash/` holds retired files, kept for reference.

## Running

    pip install numpy numba pytest pillow    # and a C compiler (cc) for hlc.c
    pytest tests -q                      # ~15 s, all layers and engines
    python experiments.py reads 12       # REPORT.md 3.3, ~1 minute
    python experiments.py lblock 3       # REPORT.md 3.4 (0..4; add 'fill')
    python experiments.py cost           # REPORT.md section 4 tables
    python experiments.py collatz        # REPORT.md 3.6, ~4 hours, resumable
    python experiments.py collatz-hash   # the same on HashLife, ~1 minute
    python experiments.py collatz-gas    # the same on the event engine, ~10 s
    python experiments.py tm-gliders one 2   # REPORT.md 3.7: a compiled TM at 2x Cook's v, resumable
    python experiments.py tm-gliders one 1.25 gas   # the same on the event engine (~9 min)
    python experiments.py gas-vs-hash CKPT  # event engine vs a HashLife checkpoint, cell for cell
