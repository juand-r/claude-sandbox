# A Lisp on Rule 110: what runs, what is verified, and what it costs

Version 0.1.0 (2026-09-30). This report supersedes the phase-1 report of
2026-08-18; REVIEW.md lists every claim that changed and why.

## Summary

The project builds a Lisp interpreter whose execution bottoms out in the
Rule 110 cellular automaton, through a tower of translations:

    mini-Lisp -> SKI combinators -> Turing machine
      -> clockwise binary Turing machine -> 2-tag system (Neary-Woods)
      -> cyclic tag system (CTS) -> Rule 110 initial condition (Cook)

The main claims, in decreasing order of the strength of their evidence:

1. **Every arrow above the automaton is implemented and differentially
   tested** against a reference interpreter for the layer above it. The
   layers are generic, and their composition is tested twice: a small
   3-state Turing machine goes through all of them down to the CTS, and
   the Lisp-running SKI machine itself goes as far as a 10,897-state
   clockwise machine that still normalizes SKI terms correctly. Below
   that, the SKI machine is too large for the current binarization.
2. **Compiled Lisp runs on a Turing machine.** A 256-state, 21-symbol
   machine that normalizes SKI terms evaluates `(car (quote (a b)))` to
   `a` in 85,892,768 steps, including the probes that decode the result.
3. **Cook's construction is reproduced exactly at the level of initial
   conditions.** The paper's glider blocks were extracted from its
   figures; assembled rows reproduce 1,152,891 spacetime cells of the
   paper's patches exactly over 45 generations.
4. **The glider machinery runs, and its mechanism is now measured.** A
   new glider census types every defect in a row by lattice invariance.
   It shows that ossifiers convert moving data into C gliders of tape
   data (four per ossifier at the start of a run), and that reads happen
   only when such tape data exists. For the first three ossifier arrivals
   of a test program, the moving data each ossifier meets is exactly what
   the reference CTS predicts (9 of 9 symbols); from the fourth arrival
   on, 4 of 6 arrivals disagree with that simple accounting. Long-run
   dynamic correctness is therefore unverified.
5. **Running the whole tower on gliders is out of reach by 14 to 15
   orders of magnitude** (roughly 1e20 to 4e20 generations for the
   capstone program). The dominant cost grows with the cube of the tag
   alphabet.
6. **One construction defect is unresolved:** initial conditions with
   empty appendants (Cook's "short leader" block L) stop producing moving
   data. Every program compiled from a tag system has empty appendants,
   so none can yet run on gliders.

## 1. The tower and how it is verified

The design principle is that each layer is a small translator with its
own reference interpreter, and each translator is tested by running the
same computation at both of its ends. Correctness of the whole then
rests on correctness of the parts plus the composition test.

| layer | module | verified by |
|---|---|---|
| mini-Lisp reference | `lisp.py` | closures, recursion, unary arithmetic, McCarthy `atom?`/`eq?` |
| Lisp -> SKI compiler | `lisp_to_ski.py` | the reference, on both SKI engines |
| SKI string engine (the specification) | `ski.py` | hand-checked reductions |
| SKI graph engine (fast, with sharing) | `ski_graph.py` | random terms against the specification |
| SKI Turing machine | `ski_tm.py` | 1,497 random terms against the specification; Lisp programs end to end |
| two-way TM, Cocke-Minsky TM -> tag | `tm.py` | visit sequences of TM and tag system |
| two-way -> clockwise -> binary clockwise TM | `cw.py` | visit sequences; direct runs; halting |
| Neary-Woods 2-tag from binary clockwise TM | `nw.py` | decoded configurations, including counter doubling |
| tag -> CTS | `tag.py` | Chapman's and De Mol's 3x+1 tag systems, exactly |
| CTS -> Rule 110 initial row | `encoder.py`, `data/blocks.json` | seam validity; 1.15M-cell evolution match |
| Rule 110 engines | `engine.py` | scalar against bit-packed; ether periodicity |
| glider census | `census.py` | pure ether, assembled rows, first ossification |

The capstone test (`tests/test_tower.py`) runs a 3-state, 2-symbol
two-way Turing machine (one step left, one back, a march right, halt)
through the two-way -> clockwise -> binary -> Neary-Woods -> CTS layers
and checks each level against the one above: identical visit sequences,
identical configurations, and an exact CTS emulation of the tag system
for 40 tag steps.

The machine that actually runs Lisp is tested through the first of these
conversions. `ski_tm.as_two_way_tm` restates it in the numbered two-way
format (stay-moves become a right move and a left move; the halt state
becomes explicit), and `cw.two_way_to_cw` turns that into a clockwise
machine with 10,897 states, which normalizes SKI terms to the same
results. The next conversion, binarization, does not finish within five
minutes for a machine this size; this is the size wall discussed in
section 4.

The review before this release found two semantic disagreements that the
tests had not covered: the compiled `atom?` returned false for nil, and
the reference `eq?` used structural equality on lists while the compiler
used McCarthy's `eq` (conses never `eq?`). Both now follow McCarthy's
LISP 1.5, and the edge cases are in the differential suite.

## 2. Lisp on a Turing machine

The Turing machine does not interpret Lisp directly. Lisp is compiled to
SKI combinators: bracket abstraction with K/I/eta optimizations,
Church-encoded tagged values, recursion through the Y combinator, and
`cond` compiled to Church-boolean selection, which normal-order
reduction makes lazy. The machine is then a fixed normalizer of SKI
terms, independent of the program.

Three observations keep that machine small:

- In prefix notation the spine of a redex is string-adjacent to its
  combinator, so the leftmost occurrence of `` `I ``, `` ``K `` or
  `` ```S `` is exactly the normal-order redex. A finite scan finds it.
- `I` and `K` redexes rewrite in place if deleted characters become a
  transparent skip symbol.
- Only `S` duplicates a subterm. The machine copies the term into a
  fresh tape region, rearranging on the fly, with subterm extents found
  by a unary pebble counter.

**Measured**, for `(car (quote (a b)))` evaluated and decoded entirely
on the machine: 85,892,768 steps (25 s in a pure-Python interpreter).

**A fix in this release** accounts for most of that figure. Previously
the pebble counter sat at the far left of the tape, and every counter
operation and every rescan walked back across all regions abandoned by
earlier S-copies; 79% of steps read a blank cell. The counter now lives
beside the live term. On the same inputs the step counts fell by factors
of 4.1 to 7.3, the factor growing with the number of S-reductions
(587,376,602 steps for the `car` program before the fix).

The cost is still steep. Each S-reduction copies the whole term with an
O(n) round trip per character, so a reduction costs O(n^2) steps, and the
Church encodings make terms of several hundred characters even for
trivial programs.

## 3. The glider level

### 3.1 The initial condition is exact

The CTS -> Rule 110 arrow follows Cook, "A Concrete View of Rule 110
Computation" (arXiv:0906.3248). The paper specifies twelve bit-blocks
(A-L) as raster figures, one pixel per cell. `tools/extract_blocks.py`
decodes them from the arXiv source; re-running it on a fresh download
reproduces `data/blocks.json` bit for bit. The encoder glues blocks along
their zig-zag seams; each placement is solved by edge-profile matching
and must be unique.

Evidence that the assembled rows are what the paper describes:

- Every seam type in a real assembly is locally a valid Rule 110
  evolution over 50 generations.
- Evolving an assembled row for 45 generations reproduces all 1,152,891
  cells that the block patches define.
- The paper's worked example of the appendant encoding is reproduced.

This establishes the initial condition, not the long-run dynamics.

### 3.2 How the machinery runs, measured

Until this release, every statement about the dynamics came from
substring-matching rows against the moving-data blocks E and F. That
decoder sees only moving data, not the tape data the machinery reads.
The glider census (`census.py`) replaces it for this purpose.

*Method.* A 14-cell window that equals a rotation of the ether fixes the
ether's phase. Defects lie wherever matching is interrupted or the phase
changes; the phase test matters because an A glider can be a pure phase
slip with no non-ether cell. Each defect is then typed by the spacetime
shift that leaves it unchanged. The ether is invariant under (7, 0) and
(3, 2) and all their combinations; C gliders are invariant only under
(7, 0), A gliders only under (3, 2), Ebars only under (30, -8).

*Observations* (program `{YYYYNN}` from tape `YYYYNN`, ossifier spacing
v = 3 x the paper's default):

- The first ossifier's four A^4 packets produce four C gliders, one per
  packet, about 45 cells apart, within 2,000 generations.
- Across that ossifier, the moving data in flight advances by four
  characters: the next ossifier meets `N N Y`, which are tape characters
  4-6 (`Y Y Y Y | N N Y ...`).
- Each C glider disappears within about 6,000 to 16,000 generations of
  its creation. Reads show up as A material heading right from inside
  the Ebar stream (acceptors and rejectors) and, in a typed spacetime
  render of De Mol's program, as wedges of deleted components after
  rejected reads.
- Between ossifiers there is no tape data at all.
- The C gliders drift right slowly as Ebars cross them, as the paper's
  crossing diagrams predict.

*Interpretation.* At least at the start of a run, each A^4 converts one
moving-data character into one C glider of tape data. That character
travels into the Ebar stream (static in its own frame) until it meets
the next unread leader, which reads it and emits an acceptor or
rejector. Reads are therefore gated by ossification: a burst of reads
per ossifier, then none until the next ossifier, about 30v generations
later. Whether every ossifier converts four characters is not settled
(section 3.3), so the cost of a read lies between 7.5v generations (four
per ossifier) and 30v (one per ossifier), whatever the size of the
appendant table.

This corrects two earlier models. The phase-1 report said one read per
left period; the first draft of the review said reads follow the table
at a fixed rate. Both were wrong (REVIEW.md B1, NOTES.md).

### 3.3 Dynamic correctness: partial evidence, one open gap

If each A^4 converts one character, ossifier k meets tape characters
4k, 4k+1, 4k+2, ... of the CTS's read sequence. For `{YYYYNN}` that
sequence is `YYYYNN` repeated. `python experiments.py fronts` checks
this at each ossifier arrival by decoding the first three moving-data
symbols the ossifier will meet:

| arrival | generation | meets | predicted | |
|---|---|---|---|---|
| 0 | 250 | `YYY` | `YYY` | match |
| 1 | 45,250 | `NNY` | `NNY` | match |
| 2 | 93,750 | `YYN` | `YYN` | match |
| 3 | 142,000 | `YNN` | `YYY` | differs |
| 4 | 190,500 | `NNY` | `NNY` | match |
| 5 | 238,750 | `NYY` | `YYN` | differs |
| 6 | 287,250 | `YYY` | `YYY` | match |
| 7 | 335,500 | `YYY` | `NNY` | differs |
| 8 | 384,000 | `YYY` | `YYN` | differs |

The first three arrivals match (9 of 9 symbols), and they already
exercise appended data (characters 6 and 8-10 were appended during the
run). From arrival 3 on, the simple accounting fails: arrival 3 meets
what look like characters 15-17 instead of 12-14. Arrivals 4 and 6
match again, but the later mismatches show that "four characters per
ossifier" is not the whole story.

Two explanations remain open, and nothing yet distinguishes them:

- *The machinery goes wrong* between arrivals 2 and 3, for example by
  losing or skipping three characters.
- *The accounting is too simple.* The moving-data decoder was built from
  the E and F blocks as drawn for the initial tape; appended characters
  are produced by acceptors and may not be recognized until they settle.
  If some of characters 12-14 were not visible to the decoder, the front
  would appear shifted.

Until this is resolved, the defensible claim is: the machinery performs
reads and appends, and the 9 characters checked (0-2, 4-6 and 8-10, of
which 6 and 8-10 were appended during the run) follow the reference.
Characters 3, 7 and 11 were not observed, and long-run correctness is
unverified.

### 3.4 The short-leader defect

Empty appendants compile to the paper's "raw short leader" block L.

*Observation.* The same machinery with and without empty appendants,
run for 250,000 generations at 3 x the default v (`python experiments.py
lblock N`; outcome = whether the moving-data decoder still finds
moving data):

| variant | program | empty appendants | moving data at 250k |
|---|---|---|---|
| 0 | `{YYYYNN}` | 0 | present |
| 1 | `{YYYYNN, e}` | 1 | gone by ~160k |
| 2 | `{YYYYNN, e, e}` | 2 | gone by ~200k |
| 3 | `{YNNNNN, e}`, tape `YN` | 1 | gone by ~137k |
| 4 | `{YNNNNN, YNNNNN}`, tape `YN` | 0 | present |

*Interpretation.* Empty appendants correlate perfectly with the loss of
moving data in these five runs. The L block passes every static check
(extraction, periodicity, unique seam fits, local rule validity, the
45-generation match). The paper notes that raw short leaders sit "up +3
higher, as measured through the E-bar-n's, than the raw regular
leaders", a long-range alignment that seam matching cannot check; that
is the leading hypothesis, not a finding. The phase-1 report also
localized the failure to one collision; that localization relied on the
old decoder and the old cadence model, and is withdrawn until
re-examined with the census.

*Consequence.* The tag -> CTS conversion pads every cycle with empty
appendants, so no tag-compiled program runs on gliders yet. This
includes De Mol's 3x+1 system, which is exact at the CTS level (Collatz
3 -> 5 -> 8 -> 4 -> 2 -> 1) and was meant to be the first Collatz
computation performed by gliders.

## 4. The cost of the tower

For the capstone machine (6 two-way TM steps, then halt):

| level | program size | steps for the run |
|---|---|---|
| two-way TM | 3 states | 6 |
| clockwise TM | 12 states | ~50 rotations |
| binary clockwise TM | 130 states (45 entered) | 101 |
| Neary-Woods 2-tag | 8,582 rules | 61,188 |
| CTS | 17,172 appendants, 1.4e8 appendant symbols | 1.05e9 reads |
| Rule 110 | v = 1.14e10 | 7.5v-30v per read: 1e20-4e20 generations (estimate) |

The bottom row is an estimate from the measured read cadence, not a run;
the range reflects the open question in section 3.3.
At the packed engine's 1.1e10 cell-updates per second it would take far
longer than the age of the universe.

*Where the cost comes from.* Write |Phi| for the tag alphabet (8,586
here). The unary tag -> CTS encoding costs 2|Phi| reads per tag step,
and v grows with the total CTS appendant length, about 80·|Phi|·R where
R ≈ 2|Phi| is the total tag rule length. Together:

    generations per tag step ≈ 2|Phi| × (7.5 to 30) × 80·|Phi|·R
                             ≈ 2,400 to 9,600 |Phi|^3

For the capstone this gives 1.5e15 to 6e15 per tag step and 9e19 to
3.7e20 in total.

The alphabet enters cubed, and it is inflated upstream: binarization
turns 12 clockwise states into 130 (of which the run enters 45), and
Neary-Woods multiplies each state by 66 tag symbols. A reachability
pruning of the tag alphabet was tried and removes nothing (REVIEW.md
D2). For the SKI machine the same pipeline starts from a 10,897-state
clockwise machine, and binarization alone does not finish; its alphabet
would be several orders of magnitude larger again.

## 5. What comes next

DIRECTIONS.md ranks the options for making this faster and more direct.
In short: first close the dynamic-verification gap (section 3.3) and the
short-leader defect (3.4). Then the largest expected gain comes from
timing ossifiers to demand instead of Cook's worst-case spacing, which
changes the bottom layer from cubic to quadratic in |Phi|, an estimated
7,000-27,000x for the capstone. Shrinking |Phi| and a one-dimensional
HashLife engine come after that.

## Reproduction

All results are deterministic.

- `pytest tests/` (about 8 s) covers every symbolic layer, the
  encoder's local exactness, and the glider census.
- `python experiments.py fronts` reproduces the table in 3.3 (several
  minutes).
- `python experiments.py lblock 0..4` reproduces the table in 3.4.
- `python experiments.py demol` runs De Mol's program on gliders (it
  loses its moving data, per 3.4).
- `python tools/extract_blocks.py DIR` regenerates the block data from
  the arXiv source of arXiv:0906.3248.
