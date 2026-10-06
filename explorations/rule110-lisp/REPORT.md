# A Lisp on Rule 110: what runs, what is verified, and what it costs

Version 0.2 (2026-10-03, unreleased; sections 3.7 and 5 are new, see
CHANGELOG.md; v0.1.1 of 2026-09-30 corrected v0.1.0). This
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
5. **Rule 110 gliders compute a whole Collatz trajectory.** De Mol's
   3x+1 tag system from x = 3, compiled and assembled with Cook's
   blocks, runs 3 -> 5 -> 8 -> 4 -> 2 -> 1 on the glider field: all 556
   CTS reads observed and equal to the reference, 2.07e8 generations, at
   Cook's ossifier spacing (section 3.6). Below half of that spacing it
   fails.
6. **A compiled Turing machine runs on Rule 110 gliders.** The
   smallest machine that changes state and moves its head, compiled
   through Cocke-Minsky and the cyclic tag system and assembled with
   Cook's blocks, runs on the glider field for 2.5e11 generations at
   twice Cook's spacing (and 5e11 at four times): all 5,970 CTS reads
   equal the reference, and its visit sequence is recovered from the
   reads alone (section 3.7). At
   Cook's own spacing it fails at read 3,269, during a long run of
   rejections; that failure was reproduced with different epoch and
   sampling settings and disappears at twice the spacing, and an
   independent event engine (section 5) reproduces it read for read. A
   three-state machine that moves left and right then ran to its halt:
   all 59,184 reads correct over 1.2e13 generations, at twice Cook's
   spacing, and its four visits recovered from the reads (section 3.9).
   The new engines (section 5: HashLife in epochs, and an event engine
   that is exact against it cell for cell) also re-ran the Collatz
   trajectory of claim 5 independently, read for read, in 45 s and 9 s
   instead of 3.9 hours.
7. **Empty appendants are no longer a blocker.** Cook's block for them
   (the "raw short leader" L) breaks the machinery, for reasons still
   unknown. An exact rewrite of the CTS replaces each empty appendant by
   a run of N's one appendant-cycle long, so L is never needed. The
   minimal program that L broke now reads 12 of 12 correctly.
8. **Cook's ossifier spacing is larger than needed.** For programs
   with 2 and 4 appendants, spacing reduced to 1/2 and 1/4 of Cook's
   value still reads correctly (10 of 10 and 12 of 12), at the cadence of
   a one-appendant program, so the spacing is not set by the whole
   table, which is what Cook's formula scales with. But long runs of
   rejections need more: De Mol's program needs more than half of
   Cook's value at one point, and a compiled Turing machine needs more
   than Cook's value itself (section 3.7). For long programs the reason
   is now identified and quantified (section 3.8): an ossifier must meet
   the next queued symbol before it reaches the newest tape character,
   so the spacing must exceed the widest gap between consecutively
   queued appendant copies divided by about 11.2. One constant fits all
   twelve runs of two programs (it was bounded by them), with each
   failure at the first queue transition above it. A run made after the
   rule confirmed its prediction: at 1.25x Cook's v the machine runs to
   its halt, all 5,970 reads correct; so does the three-state machine of
   3.9 at 2x, where the rule asks for at least about 1.7x. Why small programs need more than
   about 55 per symbol is still open.
9. **Running the whole old tower on gliders is out of reach by about 14
   orders of magnitude** (about 5e19 generations for the capstone with
   the direct binary construction, 3.6e20 with the old one; before any
   spacing reduction). The dominant cost grows with the cube of the tag
   alphabet.
10. **Lisp runs on Rule 110 gliders through a direct compiler.** A
   compiler that writes the program into the CTS table ("bus machines",
   section 7) evaluates `(car (quote (a b)))` on the glider field in
   115 s (4,512 reads, all correct, value read off the gliders) and a
   cond/eq? expression in 37 min (34,818 reads). The old tower needs
   ~1e19 generations for the first. lambda and define work with a
   compile-time recursion bound; the recursive `last` of (a b c) ran on
   gliders in 2.0 h (157,824 reads, value `c`), after debris crossings
   were taken out of the event list and memoized (section 7.6).
11. **A programmable Rule 110 computer that is not a cyclic tag system
   exists; a universal one was not found.** A one-counter machine driven
   by a fixed glider stream branches on zero and runs compiled loop
   programs (parity, mod k) exactly, cross-verified. Theory shows one
   counter cannot be universal, and the missing zero-test-with-abort for
   two registers was not found (section 6).

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
is De Mol's 3x+1 system (section 3.6).

### 3.5 Ossifier spacing: small programs need much less than Cook's v

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
during a run of 16 consecutive rejections. At v = 3,200 it reads that
run correctly (and 83 reads in all, section 3.6). So the spacing must also cover long runs of
rejections, as the encoder's own caveat on Cook's formula warns. The
mechanism is now identified and quantified (section 3.8): what matters
is the spatial gap between consecutively queued appendant copies, which
a long run of rejections makes wide. The small programs above have
rejection runs of at most two, which is why they did not show it; their
own failures below v ~ 500 have tiny gaps and remain unexplained.

*Scope.* Five small programs with appendants of 6 and 18 symbols, 8 to
12 reads each, plus De Mol's program. Two lengths do not establish a scaling law; "at most
about 55 per symbol" is an upper bound from the 18-symbol case. The cost
figures in section 4 therefore still use Cook's v, with the reduced-v
estimate marked as such.

### 3.6 A Collatz trajectory computed by gliders

*Setup.* De Mol's 3x+1 tag system {A -> CY, C -> A, Y -> AAA} from tape
AAA (x = 3), compiled to a CTS by the unary encoding, empty appendants
filled as in 3.4 (12 appendants of 6 to 18 symbols), assembled with
Cook's blocks at uniform spacing v, run on the streaming engine
(`casim.StreamRun`), and checked read by read with the decoder-free
check of 3.3. In the reference CTS the tag tape is AAAAA (Collatz 5) at
read 72, eight A's at read 204, four at 372, two at 492, and one at 552.

*Result.* At Cook's own spacing, v = 12,216, all 556 reads that were run
are observed and equal the reference, 556 of 556. The glider field
passes Collatz 5 at generation ~2.7e7, 8 at ~7.7e7, 4 at ~1.4e8, 2 at
~1.8e8 and 1 at ~2.07e8. The run took 3.9 hours (`python experiments.py
collatz`). An earlier run of the same configuration, cut short by a
container restart after 205 reads, agrees with it read for read,
including every read time and cluster count.

*Interpretation.* The whole trajectory 3 -> 5 -> 8 -> 4 -> 2 -> 1 was
computed by Rule 110 gliders from an initial condition built with
Cook's blocks. (I have not searched the literature for earlier runs of
this kind, so I make no claim of priority.)

*Spacing below Cook's value.*

| v | reads correct | first failure |
|---|---|---|
| 1,600 | 0-28 (29) | reads 29-30, during 16 consecutive N reads |
| 3,200 | 0-82 (83) | read 83, the 5th of 17 consecutive N reads |
| 6,400 | 0-82 (83) | read 83 again, same signature (114 clusters) |
| 12,216 (Cook) | 0-555 (556 of 556) | none |

The failure at 1,600 is cured by 3,200; the one at read 83 survives at
3,200 and 6,400 with the same signature (which briefly misled me into
calling it spacing-independent) and is gone at Cook's value. So for this
program the spacing must exceed half of Cook's: his formula is not
grossly conservative here, whatever the small programs of 3.5 suggest.
Section 3.8 explains these failures and predicts their reads: the first
queue transition whose gap exceeds about 11.2v is at read 29 for
v = 1,600 and at read 83 for 3,200 and 6,400.

*Scope and caveats.* One program and one input. The check observes the
outcome of every read (the regions the acceptor and rejector leave
behind); it does not decode the tape itself, so a fault that preserved
every read outcome would not be seen. The empty appendants were
rewritten as in 3.4, so Cook's short-leader block is not exercised.

*Cost of simulating it.* Cook's machine leaves a permanent stream of
left-moving Ebars that later ossifiers must cross (the census finds 100
Ebar clusters in the leftmost 200k cells of the active region at
t = 2.8e7), so the region that must be simulated exactly grows linearly
with time (to about 1e6 cells here) and the run time quadratically. A
compiled stepping kernel (4x) and checkpointing made the run practical.

*Independent re-run.* The same 556 reads on the HashLife engines of
section 5, which share no stepping code with StreamRun, give the same
outcome and the same Ebar-cluster count for every read
(`data/collatz_v12216_hash.log`; `python experiments.py collatz-hash`,
about 40 s).

### 3.7 A compiled Turing machine on gliders

*Setup.* The smallest Turing machine that changes state and moves its
head: two states, one symbol; state 1 moves right into state 2, which
halts (`tests/machines.py one_move_tm`, started on a blank tape). Its
visit sequence is (1, 1), (2, 1). It goes down the tower's lower half:
- Cocke-Minsky TM -> tag system (`tm.py`): deletion number 3, alphabet
  of 30 symbols after padding;
- tag -> CTS by the unary code (`tag.py`): 90 appendants, 67 of them
  empty;
- empty appendants filled (3.4): 8,700 table symbols, tape of 720;
- Cook's blocks at spacing v (`casim.layout`).
In the reference CTS the tag system's first head (the TM's first visit)
is the code word that ends at read 750, and the halting visit (2, 1) the
one that ends at read 5,970. Cook's formula gives v = 701,044, so the run
is about 30v x 5,970 = 1.3e11 generations.

*How it was run.* On the epoch engine (section 5), with every read
checked as in 3.3, and the TM's visit sequence decoded from the observed
Y/N reads alone (`tag.heads_from_reads`: split the reads into code
words, drop the all-N words that the fill appends, take every third
symbol as a tag head). `python experiments.py tm-gliders one F` runs it
at F times Cook's v.

*Result at 2v.* All 5,970 reads equal the reference CTS: 103 accepts,
each leaving 4 Ebar clusters per symbol within one, and 5,867 rejections
(`data/tm_one_v2.log`). Reads come every 30.08v generations; the last
completes at generation 2.52e11. Decoded from those reads alone, the
tag heads give the TM's visit sequence (1, 1), (2, 1), equal to the
machine's own. The run took 2.4 hours, sharing four cores with two other
runs.

*Result at 4v.* The same: 5,970 of 5,970 reads, the same 103 accepts
(each within one cluster of 4 per symbol), the visits (1, 1), (2, 1)
decoded from the reads, the last read at generation 5.03e11
(`data/tm_one_v4.log`; 3.0 hours, sharing the cores).

*Result at Cook's v: a failure at read 3,269.* Reads 0 to 3,268 equal
the reference, including all 55 accepts (each leaves 4 Ebar clusters per
symbol, within one) and the TM's first visit. Then the machinery fails:
- Observation. Before each read a tape character (four C gliders)
  arrives at the read point. For read 3,269 none arrives. For 3.8e7
  generations, about two read intervals, nothing changes near the read
  point. Then the table collapses: within one sample the Ebar clusters
  in an 800,000-cell window around the read point drop from 4,257 to
  1,668, with untyped debris throughout. The tree then grows without
  bound (12.8 GB) and the run ends.
- Not the epochs or the sampling. A second run with a different epoch
  length (5 instead of 8) and sampling step (2^16 instead of 2^17) fails
  at the same read and the same generation, with the same cluster
  counts. Both runs share the HashLife core and the layout code; those
  are tested against the packed engine and the direct assembly, but not
  at 7e10 generations.
- Not the engine (added later). The event engine of section 5 shares no
  simulation code with HashLife (only the layout and the census). Run
  from t = 0, it reproduces reads 0 to 3,270 read for read, including
  the failure: 3,270 settles as '!' with 843 Ebar clusters, 3,269 then
  completes late, 3,272 settles as '!' with 844. At two HashLife
  checkpoints just before (reads 3,152 and 3,256) the two engines agree
  on every cell of the active region (1.4e8 cells each).
- Spacing-dependent. At 2v the same reads are correct.
- Where in the program. In the reference CTS the tape holds about 3,300
  symbols at that point, so the queue is not empty; read 3,269 is the
  197th of a run of 209 rejections. Earlier rejection runs of 215 and
  216 reads passed. Read times show no slow drift before the failure.

*Interpretation.* The explanation most consistent with this is the
construction itself failing at Cook's spacing. Like De Mol's program
below half of Cook's v (3.6), it breaks during a long run of rejections,
which fits the encoder's caveat that Cook's formula assumes a nonempty
append in every appendant cycle; the filled program's rejection runs are
about 200 reads long. Two independent engines agree on it, cell for cell
up to just before the failure and read for read through it, so an engine
error is no longer a live explanation. Section 3.8 identifies the
mechanism: the
character for read 3,269 is made correctly and then destroyed by the
next ossifier, which finds no queued symbol in its way.

*Scope.* One machine, one input, three spacings. The machine is as
small as a machine with a state change and a head move can be (two
states, one symbol); it shows the lower half of the tower working on
gliders end to end, not that larger machines do. The checks are as in
3.3 and 3.6: every read's outcome, and the TM's visits decoded from
them; the tape itself is not decoded.

### 3.8 Why long rejection runs need a larger spacing

*The failure, observed directly.* Epoch checkpoints of the Cook's-v run
of 3.7 were kept from read 3,152 on, and the tape characters (groups of
four C gliders) were located by census over the whole active region.
- Up to read 3,248 the tape is healthy: 19 complete characters wait
  ahead of the read point, 5.6e6 cells apart.
- The character for read 3,269 is made correctly, four C gliders, at
  generation ~6.8796e10.
- One ossifier period later the next ossifier arrives at that character
  and destroys three of its four C gliders. The character for read 3,270
  is never made; the characters after it are scattered C gliders.
So the ossifier did not meet a moving-data symbol to turn into the next
character; it ran into the newest character instead.

*Where in the queue.* In the reference CTS, reads 3,262-3,269 read the
last symbols of the appendant copy queued by the accept at read 783, and
read 3,270 reads the first symbol of the copy queued at read 999.
Between those two copies' regions in the table lie the 215 appendant
regions that were read and rejected in between: a spatial gap of
9,449,496 cells. Every earlier queue transition in the run crossed at
most 1.8e6 cells.

*Model.* In the Ebar frame the queued symbols (moving data) are static,
while tape characters, stationary in the lab, drift through that frame
at 8/30 cell per generation. An ossifier makes the next character only
if the next queued symbol has already drifted past the newest character
when it arrives. Within an appendant copy the next symbol is one symbol
away. At the boundary between two queued copies it is the whole gap
between them, and in one ossifier period (about 30v generations) the
tape drifts only about 8v cells. A gap much wider than that, and the
ossifier meets the newest character first.

*Test.* `experiments.block_gaps` lists a program's queue transitions and
their gaps. Runs of De Mol's program at nine spacings (epoch engine,
each stopped at its first wrong read) and the compiled machine of 3.7
give:

| program, v | first wrong read | gap there / v | largest earlier gap / v |
|---|---|---|---|
| De Mol, 1,600 | 30 | 17.9 (read 29) | - |
| De Mol, 2,205 | 29 | 13.0 | - |
| De Mol, 2,389 | 29 | 12.0 | - |
| De Mol, 2,606 | 53 | 13.2 | 11.05 |
| De Mol, 2,867 | 53 | 12.0 | 10.04 |
| De Mol, 3,018 | 53 | 11.39 | 9.54 |
| De Mol, 3,200 | 83 | 28.5 | 10.74 |
| De Mol, 6,400 | 83 | 14.25 | 5.37 |
| De Mol, 12,216 (Cook) | none (556 reads) | - | 8.39 |
| one-move TM, 701,044 (Cook) | 3,269 | 13.48 | 2.55 |
| one-move TM, 1.25v, 2v, 4v | none (5,970 reads) | - | 10.92, 6.83, 3.41 |

One threshold fits all of them: the machine breaks at the first queue
transition with gap G > c v, where 11.05 < c < 11.39. The model's 8v is
the right order; the rest of the constant is geometry the model ignores
(where symbols sit within their regions, the drift that junk crossings
add to the tape). The 1,600, 3,200 and 6,400 rows reproduce the
StreamRun results of 3.6 with a different engine.

*Prediction, tested.* At 1.25x Cook's v (876,305) the one-move machine's
two widest transitions are 10.78v (read 3,269) and 10.92v (read 5,519),
just below the threshold, so the rule predicts all 5,970 reads correct
where Cook's own v fails at read 3,269. The run (made after the rule)
gives 5,970 of 5,970, the visits (1, 1), (2, 1) decoded from the reads,
and the last read at generation 1.58e11 (`data/tm_one_v1.25.log`). This
is the smallest spacing tried that runs the machine to its halt. Its
own critical gaps (up to 10.92v) sit just below De Mol's bound, so the
range 11.05 < c < 11.39 stands.

*What it means for the spacing.* A filled CTS reads correctly at
spacing v only if v exceeds G_max / 11.2, where G_max is the largest gap
between consecutively queued appendant copies over the run. G_max is
roughly the total width of the appendant regions in the longest run of
rejections between two accepts. Cook's formula grows with the whole
table, which is enough when an appendant is accepted at least once per
cycle (his stated assumption) and can be too little otherwise. For
compiled Turing machines the long rejection runs come from the unary
code and from the fill rewrite.

*Scope.* Two programs, one CTS family (filled, unary-coded); c is an
empirical constant measured on De Mol's table and consistent with the
compiled machine's runs. This explains the failures of long programs; the
small programs of 3.5, whose gaps are a few hundred cells, fail below
v ~ 500 for another reason that is still open.

### 3.9 A Turing machine that moves both ways, on gliders

*Setup.* A three-state, two-symbol machine that steps left, steps back
right, then marches right over 1s and halts on the first 2
(`tests/machines.py three_state_tm`), started in state 1 on the tape
... 1 1 [1] 2 1 ... (head in brackets). Its visit sequence is (1, 1),
(2, 1), (3, 1), (3, 2): both head directions, a state change at every
step, and a halt. It is compiled as in 3.7:
- Cocke-Minsky TM -> tag system -> CTS: 192 appendants, 153 of them
  empty;
- the empty appendants filled (3.4): 40,752 table symbols, a tape of
  1,920;
- the halting visit's code word ends at read 59,184 of the reference CTS
  (ten times the one-move machine of 3.7);
- Cook's formula gives v = 3,270,732.

*The spacing was chosen by the rule of 3.8, before the run.* The widest
gap between consecutively queued appendant copies in the first 59,184
reads is 61,995,404 cells (the transition after read 21,695). The rule
needs v above that gap divided by c, with 11.05 < c < 11.39, so above
1.66x to 1.71x Cook's v. At Cook's v it predicts the first failure at
read 10,799. The run used 2x Cook's v (v = 6,541,464). There the widest
gap is 9.5v, 14% below the smallest threshold measured.

*How it was run.* The run used the event engine (section 5), with every
read checked as in 3.3 and the visits decoded from the reads as in 3.7
(`python experiments.py tm-gliders three 2 gas`). It covers about
1.2e13 generations.

*Result.*
- All 59,184 reads equal the reference CTS: 405 accepts and 58,779
  rejections. Every accept left 4 Ebar clusters per symbol within one
  (128 one fewer, 171 exact, 106 one more).
- The last read completed at generation 1.16e13.
- Decoded from those reads alone, the tag heads give the visit sequence
  (1, 1), (2, 1), (3, 1), (3, 2), equal to the machine's own.
- The data: `data/tm_three_v2_gas.log`.

*Cross-check on a second engine.* The epoch HashLife engine ran the same
configuration for its first 3,072 reads. They are identical read for
read, outcome and cluster count (`data/tm_three_v2_hash_first3072.log`).
HashLife took about 0.5 s per read at that stage, and its cost per read
grows with the junk; the event engine took about 0.15 s.

*Cost.*
- The run took 2.7e10 events and about 3.3 hours of wall time. It ran in
  three legs, resumed from checkpoints at reads 3,500 and 29,000, and
  shared four cores with other jobs.
- The whole run needed only 65 distinct collisions and 37 particle
  kinds.
- The cost per read stayed between 0.1 and 0.3 s. It follows the queue
  of the CTS, which holds 8,000 to 10,000 symbols for most of the run
  and 25,000 at the end.

*Interpretation.* This is the first compiled machine with a left move, a
right move and repeated states to run to its halt on Rule 110 gliders
here. It is also the second prediction of the spacing rule to hold, the
first being the one-move machine at 1.25x (3.8). This run supports the
rule's sufficiency side: 2x passes where the rule says 1.7x is needed.
Cook's v was not run for this machine, so the predicted failure at read
10,799 remains a prediction.

*Scope.* One machine, one input, one spacing. The checks are those of 3.7:
every read's outcome and cluster count, and the visits decoded from
them. The tape itself is not decoded.

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

## 5. Simulating long runs

Five engines are available, all exact and cross-checked cell for cell.

| engine | module | idea | measured on De Mol's 556 reads (3.6) |
|---|---|---|---|
| packed cyclic array | `engine.py`, `casim.Run` | 64 cells per word; with a numba kernel, 17 us per step at 870k cells | reference only (wrap-seam debris spreads from the array ends) |
| streaming window | `casim.StreamRun` | steps only where the state differs from the assembly's free evolution | 3.9 h |
| HashLife | `hashlife.py`, `hlc.c` | hash-consed binary tree in space, memoized results in time | 340 s (one tree for the whole run, Python core, 11 GB; this read loop was retired for the next row) |
| HashLife in epochs | `epochrun.py` | HashLife on a tree rebuilt every few reads from the active region and the next few ossifiers and appendants | 45 s (C core, 0.3 GB) |
| event engine | `gas.py`, `gasc.c`, `gasrun.py` | gliders as particles moved in closed form; only patches that come within two cells are simulated, and each such collision once (memoized) | 9 s (C event loop) |

*Why the streaming window works.* Far from the collisions, the left side
(the ossifier train) and the right side (the unread table) evolve freely,
and the jigsaw assembly defines their state at every time. StreamRun
steps a window around the rest. Every 256 steps it rebuilds the window.
Garbage from the window's wrap and real activity each spread at most one
cell per step, so a margin of twice that plus a check zone keeps the
interior exact. A check zone that disagrees with the free evolution
raises an error. Left of the window's centre only the left side's free
row is valid, right of it only the right side's. An earlier version let
the right row overwrite the left one. That made the window grow without
bound and, past the table's end, used a row that was not the truth;
both were caught by a 200k-generation comparison with the full run.

*Why HashLife needs long jumps.* HashLife stores the row as a binary tree
of hash-consed blocks and memoizes, for each block, its centre half after
2^j steps. Two observations decide how to use it here.
- Its cost follows events, not generations. About 50 Collatz reads cost
  6-7 s at v = 12,216, 24,432 and 48,864 alike, although the number of
  generations quadruples: the ether between ossifiers is free.
- Sampling must be sparse. Advanced in jumps of 2^20 to 2^24 generations,
  the whole Collatz configuration (2.1e8 generations) runs in about 135 s
  without any sampling. The first measurement ("about 2x StreamRun",
  v0.1.1) came from the read check stepping it 600 generations at a time.
  The read check now samples only near each read, at a time predicted
  from the previous two reads, and jumps over the ~30v generations in
  between.

*Why epochs.* A tree that holds the whole table and every ossifier pays
for all of them at every advance, because rigid motion moves each block
to a new alignment that HashLife has not seen. For a compiled Turing
machine at Cook's v (3.3e6) that cost about 6 s per read with three
table periods in the tree, 10 s with nine, and 1.6 s with the table cut
after the next 14 appendants (Python core). So `epochrun.EpochReads` rebuilds the tree
every 8 reads from three parts:
- the active region (every cell that differs from free evolution:
  tape, moving data, junk, a read in progress), carried over from the
  previous tree as aligned blocks;
- left of it, only the next few ossifiers;
- right of it, only the next few appendants.

Both free sides move rigidly (the ossifier train by (3, 2), the table by
(30, -8)), so their state at any time t = 0 mod 30 is the t = 0 layout
translated. A cut made in clean ether between gliders evolves exactly
like the same cells of the full row, so truncation changes nothing until
an excluded glider could reach an included one. Each rebuild checks that
the previous universe's cut edges still lie outside the active region and
raises an error otherwise. The memo tables are cleared at each rebuild,
so memory stays bounded (15,000 to 70,000 nodes just after a rebuild
in the runs of 3.7).

Three supporting pieces make this possible:
- `casim.layout` describes the t = 0 row without materializing it:
  ossifiers as short segments, the A-block runs between them as ether
  gaps placed in closed form, and a long table as shared copies of one
  super-period (the blocks' row phase repeats after m periods; m = 15
  for `{YYYYNN}`, 1 for De Mol). The left side of a compiled Turing
  machine at Cook's v is about 6e12 cells; described this way it is a
  few thousand segments.
- Samples step a local copy of the tree around the watched regions
  (exact by light cone), never the big tree.
- The HashLife core is C (`hlc.c`, through ctypes). The pure-Python core
  it replaced is about 4x slower on the same runs; most of the remaining
  time is spent in numpy (census and local history).

*Checks.* Tests compare the layout with the materialized row cell for
cell, HashLife with the packed engine, and the epoch engine's row with a
full run's row over the active region after three rebuilds. On De Mol's
program all 556 reads match the StreamRun run read for read, Ebar-cluster
count for cluster count (`data/collatz_v12216_hash.log`).

*What still limits it: junk.* Cook's machine leaves every rejected
appendant behind as Ebars that drift left forever, and every later
ossifier must cross all of them. So the active region grows linearly
with the number of reads (about 45,000 cells per read for the compiled
machine of 3.7), and so does the cost of each read: the total is
quadratic in the number of reads. For the machine of 3.7 at 2v the
active region reached 2.6e8 cells by the last read, and the cost per read
rose from about 0.5 s to about 2 s (three runs sharing four cores). A
three-state machine that moves both ways (59,136 reads; NOTES.md, phase
7) would cost roughly a hundred times as much. The event engine below
was built for this.

*Tuning, measured.* On a fixed late stretch of the one-move machine (32
reads from read 3,152) the engine went from 55 s and 1.64 GB to 38.6 s and
1.06 GB, with every read's outcome and cluster count unchanged:
- the main tree jumps on a power-of-two grid, so a jump is one or two
  HashLife advances instead of about thirteen, and local copies skip to
  the predicted read in whole sample steps;
- hash tables fill to 3/4 before growing, and a node takes 12 bytes
  instead of 24.
Three ideas were measured and dropped (NOTES.md, phase 8):
- HashLife in the Ebar frame, where table and junk are static: exact,
  but no faster, because the lab frame already reuses most of that work;
- interleaved hash-table entries: 12% slower;
- stepping larger blocks directly instead of memoizing: slower at every
  size tried.
After tuning, main-tree advances take about 87% of the time and their
cost is linear in simulated generations: what is left is the glider
interactions themselves.

*The event engine (v0.2, Phase 9).* HashLife spends its time on glider
interactions that differ only in where and when they happen: a tape
character (four C gliders) crossing a queued Ebar is the same collision
thousands of times per read, at a handful of relative phases. The event
engine treats the row as particles instead.
- *Why it is exact.* Rule 110 has radius 1. If two non-ether patches,
  each evolved alone in ether, stay at least two ether cells apart, no
  cell's neighbourhood ever touches both, so the row evolves as the union
  of the two isolated evolutions (induction on time). The engine
  therefore moves each particle in closed form and simulates exactly,
  cell by cell, only patches that come within two cells of each other
  (a composite), until the composite splits into pieces at least one
  ether tile apart.
- *Particles and keys.* A patch is its cells plus the ether phase on each
  side, normalized by translation (the canonical key). A patch is a
  particle if its key recurs under isolated evolution (a period of at
  most 120 steps, found automatically): Cook's gliders, bound groups,
  pure phase slips (an A glider has phases of width 0).
- *Memoization.* A composite's whole evolution is memoized by its key at
  the moment of merging. The whole one-move machine at 1.25x Cook's v
  (3.2e8 events) needs only 63 distinct collisions and 37 particle kinds,
  and De Mol's program the same 63.
- *Bound groups.* A tape character is four C gliders 20 to 49 cells apart.
  Merged one by one, a character crossing an Ebar costs four collisions.
  Instead, stationary neighbours closer than 64 cells are joined into one
  particle (their union, which is periodic because they never
  interact), and a collision's pieces that leave at the same velocity
  within 64 cells stay one group; a split waits while neighbouring
  pieces within 64 cells are still closing in. A character then crosses
  an Ebar as one collision: on De Mol's program the C-Ebar merges fall
  from 912,000 to 224,000 and all events from 4.8e6 to 2.5e6, with every
  read, read time and cluster count unchanged. (Grouping the table the
  same way was measured to be much slower: its groups are all
  different.)
- *Structure.* Items sit in a linked list; the next collision of each
  adjacent pair is in a heap. For two particles the collision time comes
  from a cached table of their relative edge offsets over one joint
  period (one division and a short scan). The ossifier train and the
  table are materialized lazily from `casim.layout`: a sentinel stands
  for each unmaterialized side and fires when anything not moving with
  that side gets close. The event loop is C (`gasc.c`); Python keeps all
  cell-level work (new collisions, period detection), and the Python
  engine `gas.Gas` remains the reference (identical event counts and
  reads).

*Is it exact? Checked against HashLife, cell for cell.* The one-move
machine at Cook's v was run from t = 0 on the event engine to the times
of two HashLife checkpoints, and the whole active region was compared
(`python experiments.py gas-vs-hash CHECKPOINT`).

| HashLife checkpoint | generations | cells compared | differing | event engine time |
|---|---|---|---|---|
| read 3,152 | 6.67e10 | 137,190,722 | 0 | 10 min (first C version) |
| read 3,256 | 6.89e10 | 141,909,284 | 0 | 101 s (5.4e8 events); with bound groups 115 s (1.1e8 events) |

Beyond Cook's gliders, random patches in ether (60 trials of up to
3,000 steps, with debris, unknown gliders and phase slips; 638 particle
kinds appeared) give the same cells on the event engine and on HashLife.

With the read check, the same machine at Cook's v gives reads 0 to 3,270
identical to HashLife's (outcome and cluster count). That includes the
failure of 3.7, read for read: 3,270 '!' with 843 Ebar clusters, 3,269
late 'N', 3,271 'N', 3,272 '!' with 844. This is the independent-engine
check of that failure that the to-do list asked for (PLAN.md, phase 9,
item 4). Shortly afterwards the
debris that follows the failure filled memory (13.5 GB), as it did for
HashLife. Debris is a spreading region, not a collision; the engine now
stops with an error when a composite grows beyond 2^16 cells.

*How fast.* Measured on the same container as the HashLife numbers.

| run | HashLife epochs | event engine |
|---|---|---|
| De Mol's Collatz program, 556 reads | 45 s | 9 s |
| one-move TM at 1.25x Cook's v, 5,970 reads, 1.6e11 generations | 9,151 s | 907 s; with bound groups 524 s |
| one-move TM at Cook's v, time to read 3,000 | 2,331 s (older build) | 295 s |

All reads were identical in each pair. Three measured costs set the
speed:
- the event loop, 0.2 to 0.3 us per event before bound groups (bound
  groups mean fewer but longer collisions, whose neighbours are found by
  a bounded scan);
- materializing the sides, which was a quarter of the time until each
  distinct table chunk was split once (the table repeats one
  super-period, so chunks are cut at the same offsets in every period);
- the read check (rendering windows, the census), about 0.07 s per read,
  now the largest part.

*The read check from the particles.* Rendering the watched span (about
200,000 cells on the three-state machine) and running census() on it was
most of the remaining time. `gascensus.py` takes the same census from
the particles. A clump of old particles moving together, with nothing
else within 96 cells, has over the census's 30 steps exactly the history
of the clump alone in ether. Its clusters are therefore a function of its
composition, computed once and memoized; the repeating table is almost
all such clumps. Everything else (a collision under way, young
particles, different velocities nearby) still gets census() on a local
window.
- Checked: computed both ways at every sample, the two never differed
  inside a watched region, over De Mol's 556 reads, all 5,970 reads of
  the one-move machine at 1.25x, and the first 3,000 reads of the
  three-state machine. The reads equal the earlier runs, including read
  times.
- Speed: the first 2,000 reads of the three-state machine took 116 s
  instead of 246 s.

Runs now also stop at the first read that settles as '!' and keep the
last checkpoint. After a construction failure the debris spreads with
no particles to exploit, at a cost quadratic in time for any exact
engine; there is nothing left to compute.

*What still limits it.* The number of events per read grows with the
junk, as HashLife's cost did: every ossifier still crosses every Ebar
left by every rejected appendant. The total remains quadratic in the
number of reads, with a much smaller constant.

*A bug found at small v.* At De Mol's smaller spacings, reads come closer
together than a local copy's reach, and a copy could be built from an
earlier time than the last sample. A read already under way was then
seen unread and settled as '!'. Samples are now forced into time order
(ReadWatch raises otherwise). Runs at Cook-scale v, with reads 2e7
generations apart, could not hit this.

*Operational note.* Long runs checkpoint (StreamRun: the live window;
EpochReads: the tree at each rebuild, a few MB). The cloud container
running this project is reclaimed within minutes of the session going
idle, and rerunning the same command resumes.

## 6. Beyond cyclic tag systems

Four rounds of agent teams (four, four, four and six agents) tried to
build a Rule 110 computer that does not emulate a cyclic tag system.
Full accounts: `noncts/SUMMARY.md` (round 1), `noncts/round2/SUMMARY.md`,
`noncts/round3/SUMMARY.md` (two program streams) and
`noncts/round4/SUMMARY.md` (every remaining avenue; the route map is
`noncts/round4/theory/ROUTES.md`); each round's `verify/ledger.md`
records every claim's status.

*Result.* A **nontrivially programmable non-CTS computer exists in Rule
110**; a **universal** one was not found.

- **What it is.** A single counter is stored as the length of one moving
  E^n glider, and a fixed periodic stream of glider packets operates on
  it. Stored data changes what the program does: one packet decrements,
  but at zero its answer turns a following no-op into six increments. A
  compiler turns one-counter loop programs (parity, mod 4, mod 7,
  saturating subtraction) into such streams.
- **How it was checked.** Exact Rule 110 runs match the model on every
  tested input, including inputs never used in planning. Two agents
  verified this with independent code, and the lead re-ran two programs
  (`noncts/round2/lead/`).
- **Why it stops there.** In abstract models of the glider machinery,
  one counter driven by one stream can only decide eventually periodic
  properties of its input (v mod k and the like). If the zero answer can
  only act "cleanly", every such machine has decidable halting. So
  universality needs two registers with non-monotone feedback.
- **What exists toward universality.** Two independently addressable
  registers, held as the gaps between three F gliders and driven from a
  fixed stream, are verified. So is the deleting half of an abort.
- **What is missing (round 2).** A zero test that can abort the rest of
  a program block, which is all a precise universal target (a
  guarded-block machine, compiled from Minsky machines) needs. Searches
  for it are unsatisfiable within stated widths of 17 to 36 cells.
- **Round 3: two program streams.** A second counter driven from the
  left now increments, decrements and zero-tests from its own stream
  (verified). The two counters signal each other in both directions in
  one exact run, and a class-free channel K3 makes repeated coupling
  robust. Theory proved, in abstract models, that coupling counters
  through zero answers is never universal: each counter's drift must be
  changeable by the other. For these glider counters, influence inside a
  counter runs only front to back, which leaves three escapes. One is a
  shuttle between the counters, another a right-to-left crossing, the
  third the gap used as a register. None was found within the searched
  scopes. So universality remains open on this route.
- **Round 4: every remaining avenue.** Six agents mapped 23 routes. The
  best-founded is "window + rod": both counters' zero signals switch a
  gap's drift on or off, verified end to end. It still lacks a contact
  that signals through a counter (W3) and a back reaction with three
  distinct class outcomes (W4). Every class-dependent back reaction
  found has outcomes (x, x, x+7), and no G-speed one up to 40 cells is
  class-dependent at all. Rod interiors turn out to carry right-to-left
  walls, but no glider launches one. Bouncers and particle Turing
  machines find no closed reaction cycle in tables of 435,000 reactions.
  No universal non-CTS machine was found; each blocked route's scope is
  stated.

## 7. Lisp on Rule 110 without the tower

Sections 2 to 4 put Lisp on Rule 110 through a universal Turing machine,
and section 4 shows the price: about 1e19 generations or more even for
`(car (quote (a b)))`. This section replaces everything between Lisp
and the cyclic tag system with a compiler written for the CTS itself.
The same expression then runs on the glider field in two minutes.
Design notes and the full derivations are in INTERPRETER.md.

### 7.1 Where the old tower spends

*Observation.* The SKI level is small. `(car (quote (a b)))` is 61
normal-order reduction steps on terms of at most 1,475 characters. The
cost appears below it: the SKI Turing machine takes 85.9M steps, and
the Neary-Woods construction turns that machine into a tag system with
about 7.9M symbols, each encoded in the CTS as a 7.9M-bit one-hot word.

*Interpretation.* The CTS is not slow because Lisp is hard. It is slow
because a universal Turing machine is a poor fit for a CTS, and the
encodings that bridge the two multiply.

### 7.2 What one pass of a CTS can compute

A useful way to read a CTS is by symbols. Cook's construction requires
appendant lengths that are multiples of 6 and no empty appendants
(sections 3.4, 3.5). Take as a symbol a B-bit one-hot word (B a
multiple of 6), plus the all-N blank. If every appendant is a whole
number of symbols, the CTS acts symbol by symbol. The symbol at absolute
index k is read against the appendants of group k mod m ("its phase").
`phasem.py` implements this view and is checked against the bit-level
CTS (`tests/test_phasem.py`).

*What a symbol knows.* Its letter and its phase, nothing else. The phase
was fixed when the symbol was appended. A symbol that appends an extra
blank shifts the phase of everything appended after it. That is the
only way information moves between symbols.

*Consequence.* One pass can give each symbol a prefix or suffix count
(mod m) of earlier emissions, but not its neighbour's value: isolating
one sender requires every other emission before the receiver to cancel,
and nothing can arrange that without the information already being on
both sides of the receiver (INTERPRETER.md section 2 gives the
argument). Tag systems live inside this model, which explains why their
known simulations of Turing machines are expensive. The constructive
lesson: give the CTS a schedule that does not depend on the data, and
let the table, not the data, carry the program.

### 7.3 Bus machines

*Mechanism* (`busm.py`). Registers are symbols, read once per pass in a
fixed order. The CTS table holds one entry per pass, register and
letter, so it "knows" at every read which register and which step of
the program it serves, and a letter needs to hold only the register's
current value. Communication is a broadcast of one bit per pass:

- Register j appends a blank after itself at pass s if the bit is 1,
  and at pass s+1 if it is 0. Exactly one blank is emitted either way.
  So the queue length, and every later index, is independent of the
  data.
- In between, the symbols appended after the blank are read one index
  late. Each letter carries the parity of its data-independent index
  (a tag), so a receiver reads the bit as (index - tag) mod 2, and the
  table entry still knows whom it serves.
- A scheduler places each broadcast at the earliest pass where no read
  carries two unknown bits.

Two refinements matter for cost:
- Letters are numbered per read over the values the register can hold
  there (a reachability pass). This took the symbol width for `car`
  from 108 bits to 24.
- Registers have lifetimes. A register enters the queue at its first
  use, written in by its live predecessor, and leaves after its last use
  as a blank. Both events are fixed by the program, so the schedule
  stays data independent.

*Checks.* Random bus programs agree with the reference semantics: 60
without lifetimes, 80 with, and one against the bit-level CTS. A variant
that decodes the wrong bit fails 92 of 240 runs (`tests/test_busm.py`).

### 7.4 Lisp as a bus program

*Translation* (`lisp_bus.py`).
- A value is a block of token registers (PAD, OPEN, CLOSE, atom), read
  in register order with PAD skipped.
- Operations work in place. car pads everything outside the first
  element; cdr pads the first element; cons pads the second argument's
  OPEN and puts a fresh OPEN in front; cond pads the branches not
  taken.
- Blocks are scanned token by token by a scan register that runs a
  small automaton (two broadcast bits per token, one answer bit back).
- eq? moves atom codes through two code registers.
- lambda and define are inlined at compile time, up to a depth bound
  fixed when compiling, like a stack size. A deeper call compiles to an
  overflow marker, and decoding it raises an error, so a too-small bound
  fails loudly instead of giving a wrong value.
- A variable's uses are copies of its block, except the last use,
  which takes the block itself.

*Honesty of the translation.* The table is built from the expression
with each quoted datum replaced by its size; registers holding quoted
data are given every token value as their domain. The data enter only
as the CTS tape. A test checks that different data of equal size give an
identical table and different, correct answers
(`tests/test_lisp_bus.py`). All test expressions agree with `lisp.py` at
the reference level and through the compiled CTS.

*Measured, CTS level* (current compiler):

| expression | registers | passes | B | CTS reads | queue (max) |
|---|---|---|---|---|---|
| `(car (quote (a b)))` | 8 | 18 | 24 | 2,448 | 120 bits |
| `(cond ((eq? (quote a) (quote b)) (quote x)) (t (quote y)))` | 13 | 55 | 42 | 14,238 | 294 bits |
| `last` of `(a b c)`, depth 3 | 50 | 362 | 24 | 157,824 | 600 bits |
| `append` of `(a b)` and `(c)`, depth 3 | 61 | 415 | 24 | 255,648 | 792 bits |

The old tower runs `(car (quote (a b)))` as 85.9M Turing-machine steps
on a 7.9M-symbol tag alphabet; the new CTS has 2,448 reads.

### 7.5 On gliders

*Setup.* The compiled CTS is laid out with Cook's blocks (section 1) and
run by the event engine (section 5). Every read is checked against the
reference CTS, and the Lisp value is decoded from the glider reads
alone: the program's last pass reads every live register once, and each
register's B reads hold one Y, whose offset is its letter. The ossifier
spacing v is set by the gap rule of 3.8, with the widest queued-copy gap
at 7.5 v (failures were measured above ~11.05 v). Command:
`python lisp110.py --gliders "<expr>"`.

*Results.*

| expression | compiler state | CTS reads | v | reads correct | value from the gliders | generations | events | wall |
|---|---|---|---|---|---|---|---|---|
| `(car (quote (a b)))` | before lifetimes | 4,512 | 99,303 | 4,512 / 4,512 | `a` | 1.35e10 | 1.6e8 | 115 s |
| `(cond ((eq? (quote a) (quote b)) (quote x)) (t (quote y)))` | before lifetimes | 34,818 | 117,027 | 34,818 / 34,818 | `y` | 1.23e11 | 9.6e9 | 37 min |
| `(define (last l) (cond ((atom? (cdr l)) (car l)) (t (last (cdr l))))) (last (quote (a b c)))`, depth 3 | lifetimes, debris rope (7.6) | 157,824 | 108,214 | 157,824 / 157,824 | `c` | 5.14e11 | 1.35e9 | 2.0 h |

*Interpretation.* A Lisp expression typed by the user is translated into
a Rule 110 initial condition, Rule 110 evolves, and the value is read
out of the glider field. The compiler, the schedule, the read check and
the decoding are exact and tested at every level.

The first two runs used the compiler before register lifetimes and the
scheduler fix; the current compiler needs 2,448 and 10,836 reads for
them. The third is a recursive program (inlined to depth 3) and ran
with the debris rope of 7.6. The logs are `data/lisp_car_gas.log`,
`data/lisp_cond_gas.log` and `data/lisp_last_gas.log`.

*Scope.* Three expressions were run on gliders, one of them recursive
(`last`, with the recursion inlined at compile time). The bus compiler
supports lambda and define only with a compile-time depth bound;
unbounded recursion would need a periodic interpreter loop, which is not
built.

### 7.6 The remaining cost: junk left of the queue

*Observation.* On the glider field, events per read grow linearly with
the read count. For `car` they grew from 2.4e4 to 6.8e4 per read, and
the three-state machine of 3.9 shows the same growth (items 675 ->
190,847, events per read 7.5e4 -> 8.4e5). 14.0M of 16.0M merges in the
first 2,000 reads of `car` are ossifiers crossing E-family objects.
Those objects are spread evenly over the zone left of the queue and
repeat with a period of five items.

*Interpretation.* Ossification appears to leave debris, and every later
ossifier crosses all of it, so the work grows as reads². This is work
Rule 110 itself does, not an engine artefact, and it dominates whenever
the queue is small, as it is here. A fit to the `car` run gives about
8 x reads² events. For `last` (157,824 reads) that is about 2e11
events, a day of simulation, against about 3e9 for the queue crossings.

*The remedy built: the debris rope.* The debris left of the rightmost
ossifier is taken out of the event list into a separate structure, the
rope. It is grouped into units: runs of debris items closer than 1,600
cells to each other. Ossifiers are swept through the rope one unit at a
time, and each ossifier x unit crossing is looked up in a memo keyed by
the exact relative configuration (orbit, phase and offset of every
glider and item) at the moment the lead glider comes within 32 cells of
the unit. A key not yet in the memo is simulated once by the reference
engine. When an ossifier has crossed the whole rope it re-enters the
event list at the left edge. A single glider x item crossing could not
be used as the unit, because the four gliders of an ossifier pass an
item through a multi-step reaction. Every assumption the rope makes is
checked at run time and stops the run with an error code when it fails
(gasc.c, codes 30-49).

*Exactness check.* The rope was compared with the plain engine on two
programs, at the spacing set by the gap rule:

| program | reads | plain: events, wall | rope: events, wall | rope crossings | memo entries |
|---|---|---|---|---|---|
| `car` (test, 600 reads) | 600 | - | - | > 10,000 | - |
| `cond` (current compiler) | 10,836 | 9.32e8, 330 s | 7.53e7, 229 s | 5.35e7 | 2 |

In both, every read outcome and every census count are equal, the final
time is equal, and the gas right of the rope is equal item for item.
The debris inside the rope is not compared item by item; it changes
only through memoized crossings, each of which was simulated exactly
once.

*Result on a long program.* With the rope, `last` of (a b c) ran all
157,824 reads correctly in 2.0 h with 1.35e9 events (7.5). Without the
rope the fit above predicts about 2e11 events; that run was not made.
Events per block of 10,000 reads stayed at 17 to 21 times the CTS queue
summed over the block's reads. That ratio is the cost of the program's
own work, and it no longer grows with the read count.

*Interpretation.* The quadratic growth has moved, not vanished. The
number of crossings is still quadratic (1.24e10 for `last`), but a
crossing is a memo lookup in C, far cheaper than an event. It shows as
a slowly rising time per event, from 3.2 µs early in the `last` run to
about 7 µs at the end. Only two distinct crossing configurations
occurred in either program, so the debris is far more regular, seen
from an ossifier, than its raw item list suggests.

*Remaining uncertainty.* The rope was checked against the plain engine
on `car` and `cond` only. On `last` it was checked against the CTS (every
read) but not against the plain engine, which would need about a day.

*A pitfall met on the way.* A first `cond` run with the rope stopped
with a rope error at read ~4,990. The cause was a spacing v reused from
the old compiler's run, at which the current CTS has a gap of 11.45 v,
past the failure threshold of 3.8. The plain engine fails at the same
place. The rope's check caught a failing construction, as it should.

## 8. What comes next

Done in v0.1.1:
- the dynamic-verification gap (3.3);
- empty appendants, by an exact rewrite (3.4);
- a direct binary clockwise construction (sections 1 and 4);
- the streaming engine (section 5);
- a whole Collatz trajectory on gliders (3.6).

Done since (v0.2, unreleased):
- HashLife engines: a sparse initial row, epochs, a C core (section 5);
- an independent re-run of the Collatz trajectory (3.6);
- a compiled Turing machine on gliders, and a construction failure at
  Cook's own spacing (3.7);
- why long rejection runs need a larger spacing (3.8);
- an event engine: gliders as particles, collisions simulated once and
  memoized, exact against HashLife cell for cell, 5 to 17 times faster
  (section 5); it also confirmed the failure of 3.7 independently.

Done in phase 10: a direct Lisp -> CTS compiler (section 7); Lisp on
gliders, value read out.

Open, roughly in order of value:

- Done: the debris sweep (7.6). Open: the number of rope crossings is
  still quadratic in reads (cheap, but it dominates very long runs); a
  unit-level memo of whole stretches would remove it.
- Unbounded recursion: a periodic interpreter loop in the bus machine
  (memory bounded by a register file), instead of compile-time inlining.

- Done: why long programs fail at small spacing (3.8). Open: the
  constant 11.2 from geometry rather than fits, and the second
  constraint that small programs show (3.5). With both, a non-uniform
  ossifier schedule could give each stretch of a run only the spacing
  it needs.
- Done: an event engine (section 5). Open: its cost per read follows
  the queue of the CTS. The census is now taken from the particles
  (about 2x on the three-state machine's early reads).
- Why Cook's short-leader block fails (3.4), and why one control program
  reads only every second ossifier period. Fixing the short leader would
  also remove the fill rewrite, which triples the reads of a compiled
  Turing machine.
- Non-CTS route: the open routes are in noncts/round4/theory/ROUTES.md
  (section 6).

## Reproduction

Phase 10 (section 7):

    python lisp110.py "(car (quote (a b)))"              # CTS level
    python lisp110.py --gliders "(car (quote (a b)))"    # ~1-2 min
    python -m pytest tests/test_phasem.py tests/test_busm.py tests/test_lisp_bus.py

All results are deterministic.

- `pytest tests/` (about 40 s, 67 tests) covers every symbolic layer, the
  encoder's local exactness, the glider census, the sparse layout, the
  equivalence of the engines (including the epoch engine after several
  rebuilds, and both event engines against HashLife on Cook's layouts and
  on random patches), event-engine checkpoints, and the decoding of TM
  visits from CTS reads. hlc.c and gasc.c are compiled on first import
  (needs a C compiler).
- `python experiments.py reads 12` reproduces the 12/12 check in 3.3
  (about 3 minutes).
- `python experiments.py lblock 0..4` reproduces the first table in 3.4;
  `python experiments.py lblock 3 12 fill` (and `1 12 fill`) the second.
- `python experiments.py cost` reproduces the tables in section 4.
- `python experiments.py collatz` reproduces section 3.6 (about 4 hours;
  it checkpoints, so rerunning the same command resumes);
  `python experiments.py collatz-hash` the same reads on HashLife (~40 s),
  `python experiments.py collatz-gas` on the event engine (~10 s).
- `python experiments.py tm-gliders one 2` reproduces the 2v run of 3.7
  (about 2 hours; checkpoints and resumes); `... one 1` the failure at
  Cook's v (it ends when the run's tree outgrows memory, after read
  3,272), `... one 4` the 4v run. Adding `gas` runs any of them on the
  event engine: `... one 1.25 gas` (about 9 minutes), `... three 2 gas`
  the run of 3.9 (about 3 hours; checkpoints and resumes).
- `python experiments.py gas-vs-hash CKPT` compares the event engine with
  a HashLife checkpoint of `tm-gliders one 1`, cell for cell (5).
- `pytest tests/` includes the direct binary construction on the SKI
  machine (section 1).
- `python tools/extract_blocks.py DIR` regenerates the block data from
  the arXiv source of arXiv:0906.3248.
