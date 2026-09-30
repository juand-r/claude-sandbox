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
   the Lisp-running SKI machine itself goes as far as a 119,347-state
   binary clockwise machine that still normalizes SKI terms correctly.
   A new direct binary construction made that possible; the old
   two-stage binarization would need about 22 million states.
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
5. **Empty appendants are no longer a blocker.** Cook's block for them
   (the "raw short leader" L) breaks the machinery, for reasons still
   unknown. An exact rewrite of the CTS replaces each empty appendant by
   a run of N's one appendant-cycle long, so L is never needed. The
   minimal program that L broke now reads 12 of 12 correctly.
6. **Cook's ossifier spacing is far larger than needed.** For programs
   with 2 and 4 appendants, spacing reduced to 1/2 and 1/4 of Cook's
   value still reads correctly (10 of 10 and 12 of 12), at the cadence of
   a one-appendant program. The spacing a read needs appears to be set by
   one appendant, not by the whole table, which is what Cook's formula
   scales with. This is measured on small programs only.
7. **Running the whole tower on gliders is out of reach by about 14
   orders of magnitude** (about 5e19 generations for the capstone with
   the direct binary construction, 3.6e20 with the old one; before any
   spacing reduction). The dominant cost grows with the cube of the tag
   alphabet.

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
| two-way -> clockwise -> binary clockwise TM | `cw.py` | visit sequences; direct runs; halting; growth at both tape ends |
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
results. Binarizing that machine does not finish: the binarizer's state
carries both the symbolic machine's state (which includes a buffered
cell) and the code of the previously buffered cell being written out,
about 345,000 such pairs times 64 input prefixes, roughly 22 million
states.

`cw.two_way_to_binary_cw` (new in v0.1.1) builds the binary clockwise
machine directly from the two-way machine. A cell is w data bits
followed by a mark bit that flags the head. The one-cell delay that left
moves need is kept as raw bits: the state holds a queue of pending
output bits whose length, plus the bits read of the current cell, is one
cell's width in steady state. Placing the mark bit last is what makes
this work: when the head cell has been read completely, the previous
cell's mark bit has not been written yet, so a left move can still set
it. For the SKI machine the construction takes 1.5 seconds and gives
119,347 states, and the binary machine normalizes the test terms to the
same results (`tests/test_tower.py`). For the capstone machine it gives
66 states instead of 130, and the whole chain through Neary-Woods and
the CTS passes the same checks as the old path.

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

*Spacing.* The same check also measures how small the ossifier spacing
can be; section 3.5.

### 3.4 Empty appendants: the short-leader defect, and a way around it

Empty appendants compile to the paper's "raw short leader" block L.

*Observation.* The same machinery with and without empty appendants,
checked read by read with the decoder-free check of 3.3 (`python
experiments.py lblock N`, v = 3x default; `.` marks reads of empty
appendants, which leave no region to inspect):

| variant | program | empties | observed reads | reference |
|---|---|---|---|---|
| 1 | `{YYYYNN, e}`, tape `YYYYNN` | 1 | read 2 leaves 3 clusters (a real Y leaves 24); read 4 leaves 55 (region disturbed, not read) | `Y.Y.N.Y.` |
| 3 | `{YNNNNN, e}`, tape `YN` | 1 | read 2 fires ~10k generations after the short leader's read and leaves 4 clusters; read 4 leaves 55 | `Y.Y.N.N.` |
| 4 | `{YNNNNN, YNNNNN}`, tape `YN` (control) | 0 | `YNYNNN`, all six settled reads correct | `YNYNNNNN` |

Every program with an empty appendant breaks at the first read after
the short leader's read; the control without one does not. (Variant 4
reads only every second ossifier period, unlike `{YYYYNN}`; that is
unexplained but does not affect correctness.)

*Hypothesis tested: L is misplaced.* The paper says raw short leaders
sit "up +3 higher, as measured through the E-bar-n's, than the raw
regular leaders". Seam matching cannot see such an alignment, so the
placement was varied directly:

- shifting only L's first glider cluster by ether-lattice vectors
  (51 shifts covering both classes of the Ebar lattice quotient over the
  range): none reads correctly;
- shifting L and everything to its right, cumulatively per L: 11 of 52
  shifts run before the sweep was stopped, none correct.

So a rigid placement error within small lattice shifts is unlikely. The
L block passes every static check (extraction, periodicity, unique seam
fits, local rule validity, the 45-generation match); the cause remains
open.

*The workaround.* A CTS never needs an empty appendant. Replace each by
N^m with m a multiple of both the number of appendants p and 6
(`cts.fill_empty_appendants`, m = lcm(p, 6)). This is exact: the junk
N's are only ever read as N, which appends nothing, and they delay every
later symbol by m reads, a whole number of appendant cycles, so each
later symbol still meets the same appendant. `tests/test_tag.py` checks
it on Chapman's and De Mol's systems by comparing (appendant, symbol)
read traces with the junk reads removed; with a wrong m it fails.

*Observation, rewritten programs* (Cook's default spacing, which is
valid again because no appendant is empty):

| variant, filled | program | observed = reference |
|---|---|---|
| 3 | `{YNNNNN, NNNNNN}`, tape `YN` | 12 of 12 |
| 1 | `{YYYYNN, NNNNNN}`, tape `YYYYNN` | 12 of 12 |

*Cost.* Each Y read on a formerly empty appendant adds m N reads, and
the junk table data enlarges v. For the capstone: reads 1.05e9 -> 2.1e9
and v 1.1e10 -> 2.4e10, about 4x in total (section 4).

*Consequence.* Tag-compiled programs can now run on gliders. The first
candidate is De Mol's 3x+1 system; a run is in progress (NOTES.md).

### 3.5 Ossifier spacing: Cook's v is far larger than needed

Cook's spacing v grows with the total length of the appendant table
(section 4). The measurements below suggest the spacing a read needs is
set by one appendant.

*Observations* (uniform spacing, decoder-free check):

| program | Cook's v | v tried | result | generations per read |
|---|---|---|---|---|
| `{YYYYNN}` | 524 | 523-528 | 10 of 10 each | ~26,400 |
| `{YYYYNN}` | 524 | 262, 196, 160, 131, 30 | fail at read 3-4 | - |
| `{YYYYNN, NNNNNN}` | 1,064 | 532 | 10 of 10 | ~27,000 |
| `{YYYYNN, NNNNNN, NNNNNN, NNNNNN}` | 2,144 | 532 | 12 of 12 | ~27,000 |
| `{(YYYYNN)^3}` (18 symbols) | 1,452 | 532 | 1 of 8 | - |
| `{(YYYYNN)^3}` (18 symbols) | 1,452 | 1,000 | 8 of 8 | ~59,000 |
| `{(YYYYNN)^3}` (18 symbols) | 1,452 | 1,452 | 8 of 8 | ~72,000 |

*How the failures look.* Below v ≈ 500 even read 0 comes out wrong: the
region it leaves holds 13, 6, 3 and 2 Ebar clusters at v = 262, 196,
160, 131 instead of 24. The damage grows with the density of ossifiers.
A typed spacetime render at v = 262 also shows tape characters arriving
at the table faster than it is consumed, several of them stranded in the
empty gap a rejection leaves in the stream. The precise mechanism is not
yet identified.

*Interpretation.* With two or four appendants, spacing well below Cook's
value works, at the same cadence as with one. The minimum does not
depend on how many appendants the table holds, but it does grow with the
length of an appendant: it lies between 262 and 523 for six symbols and
between 532 and 1,000 for eighteen, so at most about 55 per symbol.
Cook's formula charges about 80 per symbol summed over the whole table.
The consistent reading for these programs is that v must cover the
longest single appendant, not the table; but see the next paragraph. That is the premise of "demand-timed
ossifiers" (DIRECTIONS.md), and a uniform spacing sized for the longest
appendant already captures it; a non-uniform schedule would only help
where appendant lengths differ a lot.

*A second constraint: long rejection runs.* De Mol's 3x+1 program (12
appendants, lengths 6 to 18, Cook's v = 12,216) at v = 1,600 read its
first 29 reads correctly, including an 18-symbol accept, then broke
during a run of 16 consecutive rejections. At v = 3,200 it reads 47 of 48
correctly through that run; the 48th had not happened within the
generation budget. So the spacing must also cover long runs of
rejections, as the encoder's own caveat on Cook's formula warns. The
mechanism is not identified (the moving-data queue does not run dry:
it holds about 55 characters there). The small programs above have
rejection runs of at most two, which is why they did not show it.

*Scope.* Five small programs with appendants of 6 and 18 symbols, 8 to
12 reads each, plus De Mol's program. Two lengths do not establish a scaling law; "at most
about 55 per symbol" is an upper bound from the 18-symbol case. The cost
figures in section 4 therefore still use Cook's v, with the reduced-v
estimate marked as such.

## 4. The cost of the tower

For the capstone machine (6 two-way TM steps, then halt), with the old
two-stage binarization and with the direct binary construction of
section 1 (`python experiments.py cost` recomputes every number):

| level | old path: size | old: steps | direct: size | direct: steps |
|---|---|---|---|---|
| two-way TM | 3 states | 6 | 3 states | 6 |
| clockwise TM (symbolic) | 12 states | ~50 rotations | - | - |
| binary clockwise TM | 130 states | 101 | 66 states | 101 |
| Neary-Woods 2-tag | 8,582 rules | 61,188 | 4,358 rules | 65,422 |
| CTS | 17,172 appendants, 1.4e8 symbols | 1.05e9 reads | 8,724 appendants, 3.7e7 symbols | 5.7e8 reads |
| Rule 110, Cook's v | v = 1.14e10 | ~3.6e20 generations | v = 2.9e9 | ~5e19 generations |
| Rule 110, L-free fill | v = 2.4e10 | ~1.5e21 generations | v = 6.2e9 | ~2.2e20 generations |

The Rule 110 rows are estimates from the measured read cadence (about
30v generations per read, section 3.3), not runs. The fill row is what
can actually run today, since the short-leader block does not work
(section 3.4). Both ignore the spacing reduction of section 3.5, whose
scaling to large appendants is not yet measured. At the packed engine's
1.1e10 cell-updates per second, any of these would take far longer than
the age of the universe.

*Where the cost comes from.* Write |Phi| for the tag alphabet. The unary
tag -> CTS encoding costs 2|Phi| reads per tag step, and v grows with the
total CTS appendant length, about 80·|Phi|·R where R ≈ 2|Phi| is the
total tag rule length. Together:

    generations per tag step ≈ 2|Phi| × 30 × 80·|Phi|·R
                             ≈ 9,600 |Phi|^3

The alphabet enters cubed, and it is inflated upstream: the binary
clockwise machine's states times 66 Neary-Woods symbols per state. The
direct binary construction halves the capstone's states (130 -> 66), and
the cube turns that into a factor of 7 in generations. A reachability
pruning of the tag alphabet was tried and removes nothing (REVIEW.md
D2). For the SKI machine the direct construction gives 119,347 binary
states, hence about 7.9 million tag symbols; the old path would have
needed about 22 million binary states.

If section 3.5's finding holds at scale, v need only cover the longest
appendant: at most about 55 per symbol of it, i.e. 55·|Phi|·r for
longest tag rule length r, instead of about 80·|Phi|·R for the whole
table. The cost per tag step would then be about 3,300·r·|Phi|^2,
quadratic instead of cubic. For the capstone with the direct
construction (|Phi| = 4,362 after padding, r = 7, longest CTS appendant
30,534 symbols): v ≤ 1.7e6 instead of 2.9e9, about 4.4e11 generations
per tag step instead of 7.7e14, and 2.9e16 in total instead of 5e19
(twice that with the L-free fill, whose junk appendants are shorter than
the longest real one). This is an extrapolation from five small
programs, not a measurement, and it ignores the rejection-run constraint
of section 3.5, which the capstone's long rejection runs (each skipped
code word is |Phi| - 1 consecutive N reads) would bring into play. The
realistic gain is smaller and unknown.

## 5. What comes next

DIRECTIONS.md ranks the options. Status after v0.1.1:

- Done: the dynamic-verification gap (3.3); empty appendants, by an
  exact rewrite (3.4); a direct binary clockwise construction that gets
  the Lisp-running machine to the binary level (section 1, section 4).
- Next measurement: how the spacing a read needs scales with appendant
  length (3.5). If it scales with one appendant, the bottom layer becomes
  quadratic in |Phi| instead of cubic.
- Engine: a streaming window or 1-D HashLife, so that runs such as De
  Mol's full Collatz trajectory fit in hours rather than months.
- Unexplained: why the short-leader block fails (3.4), and why the
  control program of 3.4 reads only every second ossifier period.

## Reproduction

All results are deterministic.

- `pytest tests/` (about 25 s) covers every symbolic layer, the
  encoder's local exactness, and the glider census.
- `python experiments.py reads 12` reproduces the 12/12 check in 3.3
  (about 3 minutes).
- `python experiments.py lblock 0..4` reproduces the first table in 3.4;
  `python experiments.py lblock 3 12 fill` (and `1 12 fill`) the second.
- `python experiments.py cost` reproduces the tables in section 4.
- `pytest tests/` includes the direct binary construction on the SKI
  machine (section 1).
- `python tools/extract_blocks.py DIR` regenerates the block data from
  the arXiv source of arXiv:0906.3248.
