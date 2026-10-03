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
   sampling settings and disappears at twice the spacing. The new HashLife
   engines (section 5) also re-ran the Collatz trajectory of claim 5
   independently, read for read, in about 40 s instead of 3.9 hours.
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
   than Cook's value itself (section 3.7). What the needed spacing
   depends on is open, and the savings on real programs may be small.
9. **Running the whole tower on gliders is out of reach by about 14
   orders of magnitude** (about 5e19 generations for the capstone with
   the direct binary construction, 3.6e20 with the old one; before any
   spacing reduction). The dominant cost grows with the cube of the tag
   alphabet.
10. **A programmable Rule 110 computer that is not a cyclic tag system
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
mechanism is not identified (the moving-data queue does not run dry:
it holds about 55 characters there). The small programs above have
rejection runs of at most two, which is why they did not show it.

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
  at 7e10 generations. An independent engine cannot reach this point in
  reasonable time (StreamRun's cost is quadratic in time).
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
about 200 reads long. An engine error is not excluded outright (see
above), but it would have to depend on the spacing and not on the epoch
and sampling choices. Why the character is missing (an ossification
that does not happen, or a character destroyed on its way to the read
point) is not identified.

*Scope.* One machine, one input, three spacings. The machine is as
small as a machine with a state change and a head move can be (two
states, one symbol); it shows the lower half of the tower working on
gliders end to end, not that larger machines do. The checks are as in
3.3 and 3.6: every read's outcome, and the TM's visits decoded from
them; the tape itself is not decoded.

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

Four engines are available, all exact and cross-checked cell for cell.

| engine | module | idea | measured on De Mol's 556 reads (3.6) |
|---|---|---|---|
| packed cyclic array | `engine.py`, `casim.Run` | 64 cells per word; with a numba kernel, 17 us per step at 870k cells | reference only (wrap-seam debris spreads from the array ends) |
| streaming window | `casim.StreamRun` | steps only where the state differs from the assembly's free evolution | 3.9 h |
| HashLife | `hashlife.py`, `hlc.c` | hash-consed binary tree in space, memoized results in time | 340 s (one tree for the whole run, Python core, 11 GB; this read loop was retired for the next row) |
| HashLife in epochs | `epochrun.py` | HashLife on a tree rebuilt every few reads from the active region and the next few ossifiers and appendants | 41 s (C core, 0.3 GB) |

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
7) would cost roughly a hundred times as much. A glider-level
simulator that steps each crossing as one event would remove most of
this cost; it is not built.

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

## 7. What comes next

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
  Cook's own spacing (3.7).

Open, roughly in order of value:

- Why the one-move machine fails at Cook's v at read 3,269 (3.7): the
  tape character for that read never arrives. A cell-level look at the
  ossification before it is the next step, and it bears directly on the
  spacing question below.
- A model of the ossifier spacing a program really needs. Small programs
  tolerate a quarter of Cook's value; De Mol needs more than half, the
  one-move machine more than all of it (3.5-3.7).
- A glider-level simulator that steps each junk crossing as one event
  (section 5). Without it the cost of a run grows with the square of its
  reads; a three-state machine that moves both ways (59,136 reads) is
  about a hundred times the one-move machine.
- Why Cook's short-leader block fails (3.4), and why one control program
  reads only every second ossifier period. Fixing the short leader would
  also remove the fill rewrite, which triples the reads of a compiled
  Turing machine.
- Non-CTS route: the open routes are in noncts/round4/theory/ROUTES.md
  (section 6).

## Reproduction

All results are deterministic.

- `pytest tests/` (about 15 s, 58 tests) covers every symbolic layer, the
  encoder's local exactness, the glider census, the sparse layout, the
  equivalence of the engines (including the epoch engine after several
  rebuilds), and the decoding of TM visits from CTS reads. hlc.c is
  compiled on first import (needs a C compiler).
- `python experiments.py reads 12` reproduces the 12/12 check in 3.3
  (about 3 minutes).
- `python experiments.py lblock 0..4` reproduces the first table in 3.4;
  `python experiments.py lblock 3 12 fill` (and `1 12 fill`) the second.
- `python experiments.py cost` reproduces the tables in section 4.
- `python experiments.py collatz` reproduces section 3.6 (about 4 hours;
  it checkpoints, so rerunning the same command resumes);
  `python experiments.py collatz-hash` the same reads on HashLife (~40 s).
- `python experiments.py tm-gliders one 2` reproduces the 2v run of 3.7
  (about 2 hours; checkpoints and resumes); `... one 1` the failure at
  Cook's v (it ends when the run's tree outgrows memory, after read
  3,272), `... one 4` the 4v run.
- `pytest tests/` includes the direct binary construction on the SKI
  machine (section 1).
- `python tools/extract_blocks.py DIR` regenerates the block data from
  the arXiv source of arXiv:0906.3248.
