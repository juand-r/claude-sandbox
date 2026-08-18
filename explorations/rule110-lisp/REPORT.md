# Running a Lisp on Rule 110: what was built, what runs where, and what the costs are

## Summary

This project set out to build a Lisp interpreter that executes on the Rule
110 cellular automaton. The result is a complete, tested tower of
translations:

    mini-Lisp -> SKI combinators -> Turing machine -> clockwise binary
    Turing machine -> 2-deletion tag system (Neary-Woods) -> cyclic tag
    system (CTS) -> Rule 110 initial condition (Cook's glider blocks)

Every arrow is implemented and differentially tested against a reference
interpreter for the layer above it. The main claims, each backed by a
test in `tests/` or a run documented below:

1. Compiled Lisp programs execute correctly on a 255-state Turing
   machine: `(car (quote (a b)))` evaluates to `a` in 587,376,602 TM
   steps.
2. A two-way Turing machine, compiled through the full polynomial route
   to a cyclic tag system with 17,172 appendants, computes identically
   at every level (verified exactly, junction by junction).
3. Cook's 2009 glider-block construction was extracted from the paper's
   own figures and reproduced: the assembled Rule 110 initial conditions
   are locally exact (1.15 million spacetime cells verified against the
   real automaton), and cyclic tag programs without empty appendants run
   correctly on the actual CA for hundreds of thousands of generations.
4. Physical execution of the full tower is out of reach not marginally
   but by ~17 orders of magnitude, and the project measured exactly
   where those orders of magnitude come from (table below).
5. One genuine unresolved defect: initial conditions containing Cook's
   "short leader" block (empty appendants) self-destroy at the first
   short-leader preparation collision. Localized but not fixed; all
   TS-compiled programs need empty appendants, so physical runs are
   currently limited to hand-written CTS programs without them.

## 1. The tower and its verification

The architecture principle: each layer is a small, independently testable
translator, and correctness of the composition follows from correctness
of the parts. The layers, top down:

| layer | file | verified by |
|---|---|---|
| mini-Lisp reference | `lisp.py` | `test_lisp.py` (closures, recursion, unary arithmetic) |
| Lisp -> SKI compiler | `lisp_to_ski.py` | vs `lisp.py` on both SKI engines (`test_lisp_to_ski.py`) |
| SKI string engine (spec) | `ski.py` | hand cases + engine cross-fuzz |
| SKI graph engine (fast) | `ski_graph.py` | 800/800 random terms vs spec |
| SKI Turing machine | `ski_tm.py` | 776/776 random terms vs spec; Lisp programs end-to-end |
| two-way TM model + Cocke-Minsky TM->tag | `tm.py` | visit-sequence equality (`test_tm.py`) |
| two-way -> clockwise TM | `cw.py` | visit-sequence equality incl. boundary growth |
| clockwise -> binary clockwise | `cw.py` | direct run + state-projection + halt |
| Neary-Woods 2-tag from clockwise TM | `nw.py` | config decode vs reference machine, incl. counter doubling (`test_nw.py`) |
| tag -> CTS | `tag.py` | Chapman's and De Mol's 3x+1 systems emulated exactly |
| CTS -> Rule 110 row | `encoder.py` + `data/blocks.json` | seam rule-validity + 1.15M-cell evolution match (`test_encoder.py`) |
| Rule 110 engines | `engine.py` | scalar vs bit-packed cross-check; ether periodicity |

The capstone test (`test_tower.py`) composes five layers on one 3-state
two-way TM and verifies the same computation at every level, ending with
exact CTS-level verification.

### The Lisp-on-Turing-machine result

The SKI machine is the deliberate pivot of the design. Rather than
compiling a Lisp evaluator into thousands of TM states, the Lisp is
compiled to SKI combinators (bracket abstraction with K/I/eta
optimizations; Church-encoded tagged values; Y-combinator recursion;
`cond` inherits laziness from normal-order reduction), and the TM is a
fixed 255-state, 21-symbol machine that normalizes any SKI term. Three
observations made this machine small:

- In backtick (prefix) notation, the spine backticks of a redex are
  string-adjacent to the combinator, so the leftmost occurrence of
  `` `I ``, `` ``K `` or `` ```S `` -- findable by a finite scan -- is
  exactly the normal-order redex.
- `I` and `K` redexes rewrite in place if deleted material is replaced
  by a transparent skip symbol.
- Only `S` needs real copying (its argument is duplicated); this is done
  by copying the term to a fresh tape region, with subterm extents
  computed by a unary pebble counter.

Measured: `(car (quote (a b)))` -> `a` in 5.9e8 TM steps (196 s in the
Python TM interpreter). Church-numeral equality (`eq?`) exceeds 2e9
steps; it was verified on the string and graph engines instead. This
gap is the first blowup lesson: the O(n^2)-per-redex tape machine pays
heavily for the arithmetic-flavored parts of the encoding.

## 2. The glider level: Cook's construction reproduced

The CTS -> Rule 110 arrow follows Cook, "A Concrete View of Rule 110
Computation" (arXiv:0906.3248) exactly. The paper's twelve bit-blocks
(A-L) were extracted from the arXiv source's Mathematica raster figures
(one pixel per cell; a marker row gives the t=0 line; the EPS y-flip was
detected because patch rows must evolve downward under the rule).
Assembly is jigsaw gluing along zig-zag seams; the solver finds each
block's placement by exact edge-profile matching and asserts uniqueness.

Evidence that the encoder is right, strongest first:

- Every seam type in a real assembly is locally a valid Rule 110
  evolution (zero rule violations over 50 generations x all seams).
- Evolving the assembled row for 45 generations reproduces every one of
  1,152,891 defined patch cells exactly.
- The paper's worked appendant example (`{YN, NYYN, e, e}` ->
  `HIIJKHJIIIIIJLLK`) is reproduced by the sequence builder.
- Programs without empty appendants run *dynamically* for as long as
  tested: `{YYYYNN}` from `YYYYNN` tracked its reference interpreter
  through 200k generations of consumption, appending, and maturation.

Two dynamical facts had to be learned from the CA itself, and both
corrected the mental model:

- The whole assembly `B A^13 B A^11 B A^12 B` is ONE ossifier (the
  paper does say this); its four A^4 packets arrive ~390 generations
  apart and perform one CTS read per left period, i.e. one read per
  ~30v generations, where v is the paper's spacing parameter.
- Freshly appended symbols are not born as finished moving-data blocks;
  their glider spacings pass through configurations that alias the other
  symbol. Tape decoding is therefore only trustworthy for matured
  symbols; validation uses quiescent windows and consumed-symbol
  sequences, not raw mid-flight reads.

### The short-leader defect

Empty appendants compile to Cook's "raw short leader" block L, and every
initial condition containing an L dies at a specific, reproducible
moment: when the acceptor/rejector from the previous read reaches the L
to prepare it (the paper's figSketchesPQR(r) collision). A controlled
five-program experiment pinned this (all at 3x the default ossifier
spacing, T = 250k):

| program | empties | outcome |
|---|---|---|
| `{YYYYNN}` | 0 | healthy at 250k |
| `{YYYYNN, e}` | 1 | dead by ~160k |
| `{YYYYNN, e, e}` | 2 | dead by ~200k |
| `{YNNNNN, e}` tape `YN` | 1 | dead by ~180k |
| `{YNNNNN, YNNNNN}` tape `YN` | 0 | healthy at 250k |

All static checks on the L data pass (clean figure extraction, correct
(30,-8) periodicity, unique seam fits, local rule validity, inclusion in
the 1.15M-cell evolution match). The paper notes that raw short leaders
sit "up +3 higher, as measured through the E-bar-n's, than the raw
regular leaders" -- a long-range alignment condition that jigsaw gluing
cannot check. The defect is either in the paper's L figure, in my
reading of it, or in a phase relation my assembly fails to satisfy.
Because the tag->CTS conversion necessarily produces empty appendants
(the (s-1)|Phi| padding), the defect blocks physical runs of all
TS-compiled programs. It does not affect any symbolic layer.

De Mol's 3x+1 tag system -- verified exactly at the CTS level, tracing
Collatz 3 -> 5 -> 8 -> 4 -> 2 -> 1 -- was the intended physical
flagship; it needs nine consecutive L blocks per cycle and is therefore
parked behind this defect.

## 3. The cost of the tower, measured

For the capstone 3-state two-way TM (6 TM steps to halt):

| level | size of program | steps for the 6-TM-step run |
|---|---|---|
| two-way TM | 3 states | 6 |
| clockwise TM | 13 states | ~50 rotations |
| binary clockwise TM | 130 states | 101 |
| NW 2-tag system | 8,582 rules | 61,188 |
| CTS | 17,172 appendants, 1.4e8 appendant symbols | 1.05e9 reads |
| Rule 110 | v = 1.14e10, left period ~3.2e11 cells | ~3.6e20 generations |

The bit-packed engine does 1.1e10 cell-updates/second; the bottom row
would need ~10^21 seconds of compute at the widths involved. For
comparison, the measured physical runs (hand-written CTSs) sit at
~10^5-10^6 generations and ~10^5-10^6 cells: the gap between "CTS as
data for the encoder" and "CTS small enough to run" is a factor of
~10^10 in v alone. Lisp makes it strictly worse: the `car` program's
5.9e8 TM steps sit two multiplicative layers above the 6-step TM in the
table. This is the honesty clause of the original plan landing with
numbers attached: universality composes; physical execution does not.

What DOES run on the actual automaton, today, in this repository:

- Any empty-appendant-free CTS at ~30v generations per read (e.g. the
  `{YYYYNN}` family), with consumption and appending verified against
  the reference interpreter.
- The full encoder pipeline for arbitrary CTSs, verified locally exact.

## 4. What would come next

1. Fix the short leader: implement Cook 2004's ovd/upd bookkeeping and
   check the L block's alignment mod 6 statically, or diff against a
   known-good published initial condition (Martinez's simulations).
   A fixed L unlocks De Mol's 3x+1 on real gliders (~5M generations for
   one Collatz step at x=3 -- minutes at packed-engine speed).
2. A faster TM interpreter (compiled transition arrays) to push
   Lisp-on-TM past `eq?`.
3. Formal statement of the composition theorem for the tower as built,
   with the per-layer step-count bounds now known empirically.

## Reproduction

Everything is deterministic. `pytest tests/` (38 tests, ~8 s) covers
all symbolic layers and the encoder's local exactness. The long CA runs
are scripts: `run_mixed.py` (healthy dynamics), `run_empties_test.py`
(the L defect table), `run_demol.py` (the parked Collatz run). Block
data derives from the arXiv source via `tools/extract_blocks.py`.
