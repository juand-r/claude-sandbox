# Round 3: two program streams, summary

Four agents (theory, leftstream, coupler, verify) worked on this on
2026-10-01, starting from round 2 (round2/SUMMARY.md). This is the
lead's summary for a reader who has not followed the board. The record
of every claim and its status is `verify/ledger.md` (30 entries). The
proofs are in `theory/THEORY.md`. Each directory has a README.md with
reproduce commands and a NOTES.md log.

## The answer in one paragraph

Round 2 proved, in abstract models, that one program stream caps a
glider machine at eventually periodic behaviour. Round 3 tried two
streams: counter R1 driven from the right, as in round 2, and a new
counter R2 to its left driven from the left. Two of the three tiers
were reached and verified in the exact automaton:
- the left stream can increment, decrement and zero-test its own
  counter (T1);
- the two counters signal each other in both directions within one run
  (T2).

A universal machine (T3) was not reached. Theory proved, again in an
abstract model, that coupling the counters through their zero answers
can never be universal. Each counter's *drift* must be changeable by the
other counter. For these glider counters that requires a persistent
process between them (a shuttle), a signal that crosses a counter from
right to left, or the gap used as a register. Searches for the physical
pieces found none within their scopes.

## 1. Tiers

| tier | meaning | status |
|---|---|---|
| T1 | a left stream that increments, decrements and zero-tests its own counter | reached; verified by two independent builders; lead spot-check 270/270 |
| T2 | coupling: a zero of one counter changes the other, both directions | reached in one integrated run; verified; lead re-run 0 mismatches |
| T3 | a universal two-stream machine | not reached; theory shows what is missing |

## 2. What works (exact Rule 110, controls fail)

*Increment from the left.* Round 1 found no right-moving glider that
increments an E^n counter. Leftstream explained why with slip
conservation. An increment needs slip +6, but 1 to 5 A gliders carry
8k mod 14, never 6. A SAT search in the allowed space (a six-A-sized
train) found an increment train I_L. It works in one class for every
counter value tested, 1 to 23, and leaves nothing else; the other classes
fail. Verify reproduced it with its own construction for values 1 to
12; 13 to 23 rest on leftstream's runs.

*Zero test from the left.* Also by SAT: a train Z_L that decrements, but
at zero keeps the counter at 0 and sends one A glider to the right. The
counter moves by the same vector in both branches, so later packets need
no correction. Leftstream ran 270 random programs over {increment,
decrement, zero test} with 0 mismatches. The lead re-ran 270 more with a
fresh seed: 0 mismatches.

*Coupling in both directions.* R1's zero, through gate's round-2 packet
J, emits a Bbar to the left that raises R2 by 2. R2's zero, through Z_L,
emits an A to the right that lowers R1 by 1. Verify ran both in one
program: left stream I_L I_L, right stream (input) J I, left stream
Z_L Z_L Z_L. It matches the model for inputs 0..9, and three controls
fail; the lead re-ran it with 0 mismatches. Coupler's separate scenes
were verified at 16/16 and 15/15.

*A cleaner channel, and repeated coupling.* Coupler's packet K3 =
GB1+GB3 (from a scan of all 2,337 G-speed library packets) means "if R1
= 0 then R2 += 3, else R1 += 3". It needs no class condition at R2,
works for every R2 value including 0 and 1, and sends nothing back.
Exact automaton: 28 of 28 inputs. Verify confirmed it with its own
pipeline (ledger #31), and the controls fail. Coupler also showed that
one fixed program can serve inputs that trigger different numbers of
couplings (four for one input, one for another) once corrector packets
are placed. Its slip argument says when such counts can differ at all.

## 3. Why this is not yet universal

These are theorems in abstract models. Their physical premises were
measured; their scope is stated in THEORY.md.

- **Theorem 1** (theory; reviewed by verify). Take two counters, finite
  extra state, and effects of a zero event that happen only while that
  counter is small. If even one counter's "mode" (what sets its drift
  while both counters are large) can be changed only by its own zeros,
  every run is eventually periodic and halting is decidable. So coupling
  through values alone, coupling in one direction, and one-directional
  crossings are all not enough.
- **Theorem 2** (in a rod model). Inside an E^n counter, influence runs
  only from front to back. Verify searched exhaustively over 16-cell
  perturbations (3.3 million trials). The only moving defect it found is
  a front-to-back "domain wall", launched by I_L and Z_L, that vanishes
  at the back. So R2's front, which sets its drift, cannot be reached
  from the right. Escapes: a persistent process in the gap (a shuttle, or
  a converter at R2's back that turns walls into signals), a
  right-to-left crossing, or the gap used as an unbounded register.
- **Sufficient** (in a model). A "transfer machine" with a shared mode,
  moving units between counters by a per-unit handshake, compiles any
  Minsky machine: 502 tests, 0 failures. Verify re-implemented it from
  the text alone: 5567 halting runs, 0 mismatches. A version that meters
  transfers by timing between the two streams breaks under the
  value-dependent skew that E^n counters have. So units must move by
  handshake.

## 4. What was searched and not found (scoped)

- **Shuttle legs:** none.
  - The catalog's A + E^n never emits a left-mover (n ≤ 15).
  - All 2,523 library left-movers against E^4 give no shuttle.
  - Joint SAT for both reflections is unsatisfiable at widths 18-30,
    for the slips and classes run.
  - No reflection from two-part A-family trains up to 150 cells apart.
- **Crossings:** none.
  - No right-moving train up to 24 cells wide crosses E^n, even allowing
    conversion (SAT, all slips and classes).
  - No library left-mover crosses E^4.
- **Wall converters:** none.
  - No parked E, Ebar or E^2..E^4 behind a rod turns a wall into an
    outgoing glider.
- **A wrap from the left** (R2's own non-monotone branch): unsatisfiable
  at widths 24 and 36.

*Why no shuttle turned up* (coupler's structural reading, [arg]). In
this E^n world, the clean products a counter's front emits toward the
gap are B-family gliders. A counter's back absorbs B-family gliders in
their single class, as an increment. So every signal from R1 toward R2
is absorbed, and nothing bounces back. A loop would need a left-mover
outside the B family emitted by a front; that was seen only with debris
at n = 1, 2. The same B-family property is what makes R1 → R2 signals
class-free (K3). Signals R2 → R1 can never be class-free, because every
right-mover has at least 3 classes against E^n.

## 5. New physics

- E^n counters behave as two-ended rods. Left-stream packets act on the
  front, right-side packets on the back, and each side's class
  bookkeeping is independent of the other side's events (measured for
  A, B, Bbar, GB3, GB5; I_L moves the back by a class-preserving vector).
- The domain wall ("phonon"). Arriving at the back together with a
  Bbar, it changes the Bbar's effect (for example +2 becomes −1). It does
  not affect GB3/GB4/GB5.
- The original R1 → R2 channel (J's Bbar) works in one class of the counters' offset. That
  class is the same for every R2 ≥ 2; R2 = 0 needs another class, and
  R2 = 1 never works. R2 → R1 does not repeat: each A-decrement at R1's
  inner face rotates its class.

## 6. What a next round could try

1. A wider joint shuttle search with moving windows, widths beyond 30,
   and G-family left-movers (widths ≥ 50 were beyond the budget).
2. The gap as an unbounded register (THEORY.md s.6.4), the one escape
   nobody has examined.
3. A different counter object for R2 whose drift is set at its back.

## 7. How the round ran

Same rules as round 2: own directories, a shared board, verify re-running
every positive claim with its own code, every SAT "none" posted only
after its positive control passed. Agents corrected themselves in the
open:
- theory's periodicity checker was fooled by quiet tails, caught by its
  own controls;
- theory's locality premise was too strong and was restated after
  verify found the walls;
- a claim that per-side filters suffice was withdrawn;
- several guessed timestamps were corrected.

Lead spot-checks are in `lead/`.
