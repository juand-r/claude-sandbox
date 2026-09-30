# A Lisp on Rule 110: what runs, what is verified, and what it costs

Version 0.1.1 (2026-09-30; corrects v0.1.0, see CHANGELOG.md). This
report supersedes the phase-1 report of
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
4. **The glider machinery computes correctly for programs without empty
   appendants.** A glider census types every defect by lattice
   invariance, and a decoder-free check reads each CTS read's outcome
   off the glider field. For the program `{YYYYNN}` the observed reads
   equal the reference CTS for 12 of 12 reads at 3x Cook's ossifier
   spacing and 10 of 10 at his default spacing; the later reads consume
   characters appended during the run. Each ossifier converts one
   moving-data character into one tape character (four C gliders), so a
   read costs about 30v generations.
5. **Running the whole tower on gliders is out of reach by about 15
   orders of magnitude** (about 3.6e20 generations for the capstone
   program). The dominant cost grows with the cube of the tag alphabet.
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
trivial programs. `(eq? (quote a) (quote b))`, whose compiled form
compares Church numerals, exceeds 3e9 steps in a single decoding probe
and was not completed on the machine; it is verified on the two SKI
engines instead.

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

Until v0.1.0 every statement about the dynamics came from
substring-matching rows against the moving-data blocks E and F. That
decoder turned out to be unreliable (section 3.3). Two instruments
replace it.

*The glider census* (`census.py`). A 14-cell window that equals a
rotation of the ether fixes the ether's phase. Defects lie wherever
matching is interrupted or the phase changes; the phase test matters
because an A glider can be a pure phase slip with no non-ether cell.
Each defect is then typed by the spacetime shift that leaves it
unchanged. The ether is invariant under (7, 0) and (3, 2) and all their
combinations; C gliders are invariant only under (7, 0), A gliders only
under (3, 2), Ebars only under (30, -8).

*C-glider births.* Counting where and when C gliders appear gives a
direct view of ossification.

*Observations* (program `{YYYYNN}` from tape `YYYYNN`, ossifier spacing
v = 3 x the paper's default, 490,000 generations):

- Every ossifier produces exactly one burst of four C gliders, one per
  A^4, about 45 cells apart. No other C gliders appear.
- Each burst's C gliders disappear within about 6,000 to 16,000
  generations. Their disappearance coincides with A material leaving the
  Ebar stream to the right (acceptors and rejectors).
- Between bursts there is no tape data at all.

*Interpretation.* One ossifier converts one moving-data character into
one tape character, and that character is four C gliders, one per A^4.
The character then moves into the Ebar stream until it meets the next
unread leader, which reads it and emits an acceptor or rejector. Reads
are therefore gated by ossification: one read per ossifier, about 30v
generations apart, plus a travel term described in 3.3. This is what the
phase-1 report said ("one read per left period"). The v0.1.0 report
claimed four characters per ossifier; that claim came from the
unreliable decoder and is withdrawn (NOTES.md tells the full story).

### 3.3 Dynamic correctness: verified for programs without empty appendants

*Method* (`python experiments.py reads`). The check avoids decoding
moving data altogether. Each CTS read is carried out by a leader, whose
acceptor or rejector then sweeps that appendant's table data: an accept
turns the components into moving data (Ebar material remains in the
region), a reject deletes them (the region becomes ether). So the
outcome of read j can be read off the region that held appendant j's
components, tracked in the Ebar frame where the table is static:

- The region is sampled every 600 generations, a multiple of the Ebar
  period of 30, so that samples of a static region compare equal.
- The first change in a region marks the read.
- The region is classified once it is settled: no C, A or untyped
  material inside, and unchanged since the previous sample. Empty is N.
  Four Ebar clusters per appendant symbol, within 2, is Y (every run
  that matched the reference left 23-25 clusters for a six-symbol
  appendant). Any other count is reported as malformed (`!`): the
  region was disturbed, not read. An earlier version called every
  nonempty region Y, which let a broken run with 2 and 53 clusters pass
  as a match.

The settling rule matters. A reject sweep takes about 5,000 generations,
and the sweeping rejector is not always typed A. A first version without
the "unchanged" condition fired mid-sweep and misclassified two rejects
as accepts.

*Observations.*

| program | v | reads checked | observed = reference | generations per read |
|---|---|---|---|---|
| `{YYYYNN}`, tape `YYYYNN` | 1,572 (3x default) | 12 | 12 of 12 | ~58,000 |
| `{YYYYNN}`, tape `YYYYNN` | 524 (default) | 10 | 10 of 10 | ~26,400 |

Reads 6 onward consume characters that were appended during the run, so
reading, accepting, rejecting, appending and ossifying are all exercised.
A Y read leaves about 24 Ebar clusters (four per symbol of the six-symbol
appendant); an N read leaves none.

*The read cadence.* At v = 1,572 reads happen at t ≈ 9.0k, 67.2k,
124.8k, 183.0k, 240.6k, 299.4k and 356.4k. The interval, about 58k, is
one ossifier period (48.8k) plus about 9.2k. The interpretation most
consistent with this: each tape character is delivered at about the
same place in the Ebar frame, and the next unread leader is one
appendant further along each time, so each read adds one appendant
traversal. For cost estimates the ossifier period, about 30v, dominates.

*What went wrong in v0.1.0.* The moving-data decoder is
phase-dependent. After the first cycle's reads the moving data is static
in the Ebar frame, yet its decoded string changes with the sampling time
modulo 30 (t = 0 gives `YYYNN YYYYNN`, t = 10 gives `NNYNN YYYYN`,
t = 20 decodes nothing). The E and F cores are distinct; the aliasing
comes from context, since cores overlap neighbouring characters and
acceptor-made moving data sits in different surroundings than the
initial tape. The v0.1.0 "fronts" table and its mismatches from arrival
3 on were artifacts of this. The decoder (`decoder.py`) is kept only as
a diagnostic.

*Scope.* The evidence covers one program without empty appendants, for
10 to 12 reads, at two ossifier spacings. It does not cover programs
with empty appendants (section 3.4), long runs, or other spacings.

*Spacing below the default.* A sweep of uniform v with the same check
(`{YYYYNN}`, 10 reads): v = 523 and 524 match; v = 262, 196, 160, 131
and 30 do not, failing at read 3 or 4. So Cook's estimate is not
grossly conservative for this program under a uniform schedule; where
the threshold lies between 262 and 523 is being measured (section 5).

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
| Rule 110 | v = 1.14e10 | ~30v per read: ~3.6e20 generations (estimate) |

The bottom row is an estimate from the measured read cadence (one read
per ossifier, section 3.3), not a run.
At the packed engine's 1.1e10 cell-updates per second it would take far
longer than the age of the universe.

*Where the cost comes from.* Write |Phi| for the tag alphabet (8,586
here). The unary tag -> CTS encoding costs 2|Phi| reads per tag step,
and v grows with the total CTS appendant length, about 80·|Phi|·R where
R ≈ 2|Phi| is the total tag rule length. Together:

    generations per tag step ≈ 2|Phi| × 30 × 80·|Phi|·R
                             ≈ 9,600 |Phi|^3

For the capstone this gives about 6e15 per tag step and 3.7e20 in
total.

The alphabet enters cubed, and it is inflated upstream: binarization
turns 12 clockwise states into 130 (of which the run enters 45), and
Neary-Woods multiplies each state by 66 tag symbols. A reachability
pruning of the tag alphabet was tried and removes nothing (REVIEW.md
D2). For the SKI machine the same pipeline starts from a 10,897-state
clockwise machine, and binarization alone does not finish; its alphabet
would be several orders of magnitude larger again.

## 5. What comes next

DIRECTIONS.md ranks the options for making this faster and more direct.
In short: the dynamic-verification gap is closed (section 3.3); the
short-leader defect (3.4) is next. Then the largest expected gain comes
from timing ossifiers to demand instead of Cook's worst-case spacing,
which would change the bottom layer from cubic to quadratic in |Phi|,
an estimated 27,000x for the capstone. The uniform-spacing sweep in 3.3
shows this cannot be had by simply shrinking v; it needs a non-uniform
schedule, and whether one exists is open. Shrinking |Phi| and a one-dimensional
HashLife engine come after that.

## Reproduction

All results are deterministic.

- `pytest tests/` (about 8 s) covers every symbolic layer, the
  encoder's local exactness, and the glider census.
- `python experiments.py reads 12` reproduces the 12/12 check in 3.3
  (about 3 minutes).
- `python experiments.py lblock 0..4` reproduces the table in 3.4.
- `python experiments.py demol` runs De Mol's program on gliders (it
  loses its moving data, per 3.4).
- `python tools/extract_blocks.py DIR` regenerates the block data from
  the arXiv source of arXiv:0906.3248.
