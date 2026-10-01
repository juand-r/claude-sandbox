# Round 2: a non-CTS computer in Rule 110, summary

Four agents (gate, address, queue, verify) worked on this on 2026-09-30/
10-01, starting from round 1's results (noncts/SUMMARY.md). This is the
lead's summary, written for a reader who has not followed the board.
The authoritative record of every claim is `verify/ledger.md` (30
entries, each with its status and the script that checks it). The
agents' own write-ups are `verify/THEORY.md`, and `*/NOTES.md` and
`*/README.md` in each directory.

## The answer in one paragraph

Round 2 reached the first two of its three milestones and not the third.
There is now a **nontrivially programmable computer in Rule 110 that is
not a cyclic tag system**. A single counter, stored as the length of one
moving E^n glider, is driven by a fixed periodic stream of glider
packets. Stored data changes what the program does: zero versus nonzero
selects different later behaviour. A compiler turns one-counter loop
programs (parity, mod 4, mod 7, saturating subtraction) into such
streams, and their exact Rule 110 runs match the model on every tested
input, including inputs never used to build them. Two agents verified
this independently, and the lead re-ran two of the programs.

A **universal** non-CTS machine was not reached. Verify proved (in
abstract models) why the one-counter world cannot get there. It also
stated precisely which missing piece would suffice: a zero decrement
that aborts the rest of a program block, in a two-register layout.
Address built two independently addressable registers in a lane of F
gliders, and gate built the deleting half of an abort. The zero test
that would connect them was not found, and three precise synthesis
targets remain.

## 1. Milestones

| milestone | meaning | status |
|---|---|---|
| M1 | one data-dependent branch: zero vs nonzero changes later behaviour, cleanly | reached (gate; verify; lead) |
| M2 | a nontrivially programmable machine running end to end | reached, as a compiler (verify) and as fixed programs (gate) |
| M3 | a universal machine with a compiler from Minsky machines | not reached; target and missing pieces stated |

## 2. What works (verified by full Rule 110 simulation)

Every result below was re-run by verify with its own code: its own row
builder and glider typer, with rebuilt rows checked cell for cell against
the original builder's. Every result has a negative control that can and
does fail. The lead re-ran the two items marked (L).

*A clean branch (M1).* Gate's packet Z6 decrements the counter, but at
zero the counter's answer (one A glider) shatters the packet's trailing
no-op into six B gliders, which add 6 to the counter: 0 becomes 6, every
other value goes down by 1. Nothing is left over. This is the
non-monotone effect that verify's theory requires.

*Programs (M2).*
- Gate: one fixed 20-packet stream computes (v − 10) mod 7 for inputs
  0..14, including 5 not used to build it (L). A fixed 88-packet stream
  computes parity for inputs 0..8.
- Verify: a measured "calculus" of how each packet acts on the
  counter's value and collision class (129 of 129 predictions agree with
  the exact automaton), plus a planner that chooses packet phases and
  inserts corrector packets. Four planned programs (parity, a mod-7 loop,
  a mod-4 loop, saturating subtraction) match the model in the exact
  automaton on inputs 0..15, planned on 0..12 (L for parity).
- The program text is identical for every input; only the input
  encoding changes. An early version of gate's builder compiled the
  program per input; gate found this itself and withdrew those claims.

*Two independently addressable registers.* Address placed three F
gliders T > M > P in a lane. Register 1 is the gap T–M, register 2 the
gap M–P. A pair of Ebars, depending on its collision class, crosses some
of the F's and is absorbed by exactly one, which it displaces
("lock and key"). Four instructions (up and down for each register) run
from a fixed periodic stream. Address ran 7 of 7 random programs exact;
verify re-ran 4 of 4 fixed-stream programs and 16 of 16 history-placed
ones; shifted placements destroy the registers. The working range has a
floor (gaps below about 64 cells break).

*Half of an abort.* Gate: a stationary C1 glider eats any number of
instructions of two particular shapes and stays in place, and a "gate"
packet then removes it, leaving one Ebar. This works wherever in the
stream the abort starts.

## 3. Why one counter is not enough, and what M3 needs

These are theorems about abstract models of the glider machinery, not
about Rule 110 itself. Whether the models capture every possibility is
an assumption, stated next to each.

- **Clean answers give decidable machines** (verify). If a zero answer
  can only take one unit off a later packet, pass packets that do
  nothing, or escape, the machine is monotone and its halting is
  decidable, for any number of registers and any addressing. A universal
  machine needs a non-monotone answer, like gate's Z6.
- **Slip conservation forces garbage or 7-jumps** (gate; queue found the
  same law in Cook's machine). Slip mod 14 is conserved and a counter
  unit has slip 6, so a branch that leaves nothing behind changes the
  counter by the same amount mod 7 whatever the input. A branch must jump
  by a multiple of 7 (as Z6 does) or emit garbage that leaves.
- **One counter decides only eventually periodic properties** (verify).
  With one program stream and answers that cannot cross an upstream
  store, every register's behaviour is eventually periodic. So the E^n
  world stops at M2: v mod k, v < c, and the like.
- **The M3 target** (verify, tested 402 of 402 against a Minsky
  interpreter): two counters, three bounded flags, and one rule, *a
  decrement of a zero register aborts the rest of its block*. No jumps
  and no programmable skip lengths are needed.
- **The layout constraint** (verify, corrected in scope on the board):
  if every register is operated and tested at its own place in the lane,
  no arrangement is universal. A "near-end" layout escapes this: all
  operations and zero tests happen at the shared middle marker.

## 4. What is missing, stated as synthesis targets

1. **A zero test at the control point** (address): a packet that
   crosses an F cleanly and arrives as a specific Ebar pair in a specific
   class relative to the next F. That F would then emit a usable race
   token (verified: F + that pair → F + C3_14_C2).
2. **An abort that reaches the register instructions** (gate): no packet
   in the catalog or among 203 uncatalogued compounds both changes a
   register and can be eaten by the C1 messenger. A SAT search for one
   (a free Ebar-speed packet, both conditions in one formula) is
   unsatisfiable up to width 30, for all 12 F classes and one C1 class.
   The same code's positive controls find eaters and register kicks
   separately. Wider packets and other C1 classes are not covered.
3. **A state-dependent leader inside Cook's queue** (queue): a leader
   whose prepared form after an accept differs from that after a reject,
   at no charge cost. It would give a queue machine with genuine finite
   control. Queue first needed a clean alternative reader:
   - a screen of 11,285 placements of library objects found none;
   - SAT searches with one glider of the reader free (widths 30 and 17,
     strict and delay-tolerant targets) are unsatisfiable for forced-N,
     inverted and forced-Y readers; their positive controls recover
     Cook's reader exactly;
   - the leader-level search ("standard after accept, different after
     reject") is unsatisfiable in its region (width 36);
   - wider regions were beyond the solver's time budget (the positive
     control alone did not finish in 1,700 s).

## 5. Negative results, with scope

- No zero test among the 201 catalog movers at four register gaps
  (address, 804 full simulations).
- No packet that has crossed an F makes the next F emit a stationary
  object and survive (catalog, 1 and 2 upstream F's, all residues).
- A C1 messenger can neither eat nor neutralize the register-kick
  packets (catalog plus 203 compounds; spot-checked by verify).
- In Cook's machine, no single-glider change to the raw leader makes it
  respond differently to accept and reject (several hundred placements),
  and every rejector-transparent insertion emits B bursts that destroy
  the tape (queue).

## 6. Side findings for the main project

- Cook's "appendant length a multiple of 6" rule stands. Queue first saw
  lengths 8 and 10 work for 4 reads, but over 16 reads they fail from the
  first read of appended data while 12 reads 16/16; queue withdrew the
  claim.
- The round-1 formula E^n + GBk → E^(n+k−4) holds only for k ≥ 3;
  for k < 3 the result is E^(n−1) plus A^(3−k) (verify).

## 7. How the round was run

Each agent worked in its own directory and posted to `BOARD.md`. Verify
re-ran teammates' claims with its own code and kept the ledger. The lead
re-ran two M2 programs (`lead/`), sent agents back to work where the
board showed a concrete next step, and committed snapshots. Agents
corrected themselves in the open: gate withdrew its per-input
compilations, verify withdrew a "debris" finding that came from runs
that were too short and narrowed a theorem it had overstated, and queue
corrected a slip measurement and withdrew its odd/even appendant claim
after a longer run. Every SAT "none exists" was posted only after the
same code's positive control succeeded (two controls that failed at
first exposed placement bugs, which were fixed). No harness refusals
were worked around.

## 8. What a round 3 could try

In order of how directly the round-2 theory points at them:

1. **A second program stream from the other side.** Verify's theorems
   assume one stream; Cook's own machine has two (table from the right,
   ossifiers from the left). The E^n world already has a leftward
   channel (gate's J emits a Bbar to the left; E^n + Bbar → E^(n+2) + A),
   so a second counter driven from the left is a concrete layout.
2. **The near-end layout in the F lane.** All operations and zero tests
   at the middle marker: needs a kick that moves the middle and front
   markers together, a zero test with its answer at the middle marker,
   and an abort. Address's missing token-emitting packet is one SAT
   query away.
3. **Wider SAT searches** with moving windows (round-1 synth's
   technique): the scoped UNSATs above are all at widths 17-36; wider
   regions timed out in the formulations used.
