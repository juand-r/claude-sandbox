# Two-stream counter machines: which couplings can be universal

Author: theory (round 3). Labels: **[thm]** proved here for the model
stated; **[sim]** checked by running code (here: abstract models only; no
Rule 110 runs are mine); **[arg]** an argument, not a full proof; **[hyp]**
a hypothesis. Every non-existence claim carries its scope.

Files: `nogo.py` (checks of the no-go theorems with controls), `lm.py`
(universal transfer machine and Minsky compiler), `xm.py` (two-stream,
tick-level realisation with mode copies, delays and skew).

## 1. Summary

Round 3's plan couples two counters, R1 (driven by a stream from the
right) and R2 (driven by a stream from the left). Each counter's zero
answers travel toward the other. This document asks which kinds of
coupling can make such a machine universal. The answer has three parts.

1. **Coupling through values is never enough [thm].** Take two counters
   with any finite auxiliary state, events that change values by bounded
   amounts, and zero events whose effects happen only while that counter
   is small. Kicks to the other counter of any sign, non-monotone wraps,
   and packet deletions in bounded windows are all allowed. If at least
   ONE counter's "mode" can be changed only by its own zero events, then
   every orbit is eventually periodic (Theorem 1, s.3). The mode is the
   state that sets the counter's drift while both counters are large.
   Universality therefore needs both counters' drifts to be changeable by
   the other counter's zero events: a shared mode, or modes coupled in
   both directions. One-directional mode coupling is not enough.
2. **For E^n counters, the only escape is a process in the gap [thm in
   an interval model].** An E^n counter is a rod. Its stream acts on the
   outer face, and its answers leave from the inner face. Teammates
   verified by simulation that outer-face operations leave the inner end
   fixed. So the outer-face state can change only at that counter's own
   zero (Theorem 2, s.3.4). Assume the gap between the rods stays
   bounded and nothing crosses a rod. Then a universal design needs a
   **shuttle**: a persistent glider process that bounces between the two
   inner faces and keeps moving units from one counter to the other
   while both are large.
3. **What is sufficient [thm/sim in model].** A *transfer machine* is a
   shared mode whose states are loops ("move x into y at ratio k:j until
   x runs out; the remainder picks the next state"). It compiles every
   2-counter Minsky machine: 502 differential tests, 0 failures; a
   control without remainder information fails 96 times (s.5.1). It can
   be realised by two independent streams that each hold a copy of the
   mode and resynchronise through signals emitted at zero events. At
   tick level with random signal delays this gives 150 programs and 0
   failures (s.5.2). Three controls fail as they must:
   - a one-directional coupling (105 of 105 halting runs wrong);
   - signals slower than the design (91 of 105);
   - a value-dependent skew between the two streams' schedules (69 of
     105 at 0.3 slot per unit, 21 at 0.05).

   E^n counters do have that skew. That is why the physically robust
   version needs the shuttle: each bounce moves exactly one unit, so it
   is a handshake that no skew can break.

What this means for the round (s.7). The coupling milestone T2 is
worth reaching, but value coupling is not a route to T3. For E^n
counters the next physical target is a shuttle (a reflection at each
inner face). Even with a shuttle, programmable transfer ratios need
some persistent per-side state, such as a filter, or a gap that zero
events can adjust. Whether a shuttle with blind streams is universal is
open (s.6.3).

## 2. Models

### 2.1 The abstract two-counter machine (2SM)

A configuration is (s, x, y): x and y are counter values in N, and s
lies in a finite set S. One step is a deterministic map. There are
constants C and M with:

- (A1) *Bounded steps*: |x' - x| <= M and |y' - y| <= M.
- (A2) *Threshold dependence*: the triple (s', x' - x, y' - y) depends
  only on (s, min(x, C), min(y, C)). Zero tests, wraps, kicks and their
  consequences are all functions of these thresholded values.
- (A3) *Modes*: S = S1 x S2 x S0. In the **bulk** (x >= C and y >= C),
  the x-increment is f1(s1) + h1(s0) and the y-increment is
  f2(s2) + h2(s0). The components s1, s2, s0 evolve autonomously there
  (s1' = g1(s1), and so on).
- (Q) *Quiescence*: in the bulk, h1(s0) = h2(s0) = 0 after at most D
  steps. Signals in flight die out, and nothing keeps acting on the
  counters forever except the modes.

s1 is **x's mode** and s2 is **y's mode**. Call x's mode **owned** if
s1 changes non-autonomously only while x < C. Only x's own small-value
events (its zero events) may change it.

The coupling classes used in `nogo.py` are instances of this model:

| class | what a zero event of one counter may do | owned modes |
|---|---|---|
| value | change the other counter's value (any sign, delayed), wrap its own value, reset its own mode | both |
| oneway | additionally set y's mode at x's zero (not vice versa) | x's only |
| cross | set the other's mode in both directions | none |
| shuttle | modes trivial (blind streams); zero events of either counter switch a shared gap process that adds drift to both | none (shared state violates (Q)) |

### 2.2 The interval model (LIM) for E^n counters

Each counter is a rod with an outer face O_i (facing its own stream)
and an inner face I_i (facing the gap). Layout:

    [left stream ->]  O2 ==R2== I2   gap   I1 ==R1== O1  [<- right stream]

The model has five premises. Each is listed with its physical status.

- (L) *Locality*: if x >= C, events at O1 neither influence nor are
  influenced by events at I1, apart from both changing x. Same for y.
  - Status [sim, teammates]: GB3/GB5 leave R1's inner end exactly fixed
    and A leaves R2's inner end exactly fixed (verify edge_check.py).
    I_L moves R2's inner end within its class (verify). Bbar and B
    arrivals at R2's inner face leave its front exactly in place
    (leftstream bbar_front.py).
  - By the speed-of-light bound, (L) holds for long enough rods whatever
    the reactions.
- (N) *No crossing*: stream packets act on the outer face only; nothing
  crosses a rod.
  - Status: synth (round 1) found no crossing of E^n up to width 30;
    that is the scope.
- (B) *Bounded gap*: the gap and its contents (signals in flight,
  inner-face classes) range over a finite set.
- (Q) *Quiescent gap*: if no zero event occurs for D steps, the gap
  becomes empty and stays empty.
- (F) *Finite local states*: each outer-face neighbourhood ranges over
  finitely many patterns, up to the symmetries of its stream.
  - This is what makes timing finite-state, which verify asked to see
    stated. Each stream is a periodic pattern, invariant under a rank-2
    lattice L_i of spacetime translations: its period along the
    packets' motion, and the packet period. Both L_i are of finite index
    in the ether lattice, so L = L_1 ∩ L_2 also has rank 2 and finite
    index.
  - A configuration is determined, up to a translation in L, by: the
    local patterns at O1, I1, I2 and O2; the two rod lengths (x, y); and
    the gap. The relative timing of the two streams at the two counters
    is part of this data. It is unbounded in general (s.2.3), but when
    both counters are small (the "corner") it is one of finitely many
    values modulo L.

### 2.3 Timing in the physical model

- *Signals take time.* A signal crosses the gap in time proportional to
  the gap.
- *Value-dependent skew between the streams.* When an outer op changes
  x, O1 moves, so later stream-1 packets meet O1 earlier or later. E^n
  moves at -4/15 and G packets at -1/3, a relative speed of 1/15, so
  each cell of displacement shifts all later arrivals by 15 steps.
  Over a computation, the stream-1 schedule at R1 slides against the
  stream-2 schedule at R2 by an amount proportional to the values. No
  shared clock exists.

## 3. No-go theorems

### 3.1 Theorem 1 (one owned mode suffices for periodicity) [thm]

**Theorem 1.** Consider a 2SM satisfying (A1)-(A3) and (Q), in which at
least one counter's mode is owned. For every initial configuration the
sequence P_t = (s_t, min(x_t, C), min(y_t, C)) is eventually periodic.

**Lemma 1 (one-counter regime).** Suppose that from some time on
y_t >= C. Then (s, x) evolves autonomously, and P is eventually
periodic.

*Proof.* With min(y, C) = C, the update of (s, x) does not depend on y.
So (s, x) is a deterministic one-counter system with finite control.

- If x < C infinitely often, some (s, x) with x < C repeats (the set is
  finite). Determinism then makes the orbit periodic.
- Otherwise, from some time on x >= C, so the system is in the bulk.
  There s evolves autonomously and becomes periodic, and the
  increments of x are periodic.

In both cases P is eventually periodic: min(y, C) = C throughout, and y
is never tested. ∎

*Proof of Theorem 1.* By Lemma 1 (and its mirror image) we may assume
that x < C infinitely often and y < C infinitely often. Let
R(K) = [0, K)^2.

**Step 1 (the corner).** If R(K) is visited infinitely often for some
K, some configuration repeats (finitely many s), and the orbit is
periodic. So assume each R(K) is visited only finitely often. In
particular there is a last visit to R(C + M). After it, the orbit
alternates between the **X-side** {x < C} and the **Y-side** {y < C}.
It goes from one side to the other only through **passages**: maximal
stretches in the bulk with x, y >= C.

**Step 2 (what a passage needs).** During any stretch of l bulk steps,
s1 and s2 evolve autonomously. Within |S| steps each sits on a cycle of
g1 (resp. g2) with mean increment mu1 (resp. mu2), and s0 contributes at
most D*M in total. So the change of x over the stretch is l*mu1 + e,
with |e| <= K := 2(|S| + D)*M. The same holds for y with mu2. Cycle
means are rationals with denominator at most |S|, so a negative mean is
at most -1/|S|.

- Take an X->Y passage of length l. It starts with x in [C, C+M) and,
  since R(C+M) is no longer visited, y_start >= C + M. It ends with y in
  [C, C+M).
- Call the passage **far** if y_start >= C + M + K1, where
  K1 = K + 1 + M*(M + K)*|S|, and **near** otherwise.
- In a far passage, y falls by more than K1, so l*mu2 < K - K1 < 0,
  hence mu2 < 0. Also l >= K1/M >= (M + K)*|S|, because y changes by at
  most M per step. Since
  x_end - x_start > -M, we get l*mu1 > -M - K. If mu1 were negative,
  then l <= (M + K)*|S|, a contradiction. Hence a far X->Y passage forces
  **mu1 >= 0 and mu2 < 0**. Symmetrically, a far Y->X passage forces
  **mu1 < 0 and mu2 >= 0**.
- A near passage starts inside the bounded region R(C + M + K1).

**Step 3 (ownership).** Suppose x's mode is owned.
- Look at an X->Y passage P and the next Y->X passage P'. From the start
  of P until x next drops below C (the end of P'), x >= C. On the Y-side
  in between, x < C would put the orbit in R(C), which is excluded. So
  s1 evolves autonomously throughout and stays on the same g1-cycle.
- If P and P' were both far, that cycle would have mu1 >= 0 and
  mu1 < 0, a contradiction. So every such pair (P, P') contains a near
  passage.
- Passages alternate between the two types, and there are infinitely
  many of them, so infinitely many are near. Each near passage starts
  in the bounded region R(C + M + K1), so that region is visited
  infinitely often. This contradicts Step 1's assumption, so the orbit
  is periodic after all.

(If y's mode is the owned one, use a Y->X passage and the next X->Y
passage instead.)

In every case P is eventually periodic. ∎

**Decidability [thm, sketch].** The proof gives a procedure.
- Simulate. If a configuration in R(C + M + K1) repeats, the orbit
  is periodic.
- Otherwise the orbit eventually enters a one-counter regime (Lemma 1).
  That is recognisable: the autonomous subsystem repeats a state with
  x >= C, and the other counter's mean drift on that cycle is >= 0.

So halting, defined as reaching a given s or zero pattern, is decidable,
and no 2SM with an owned mode can be universal.

### 3.2 Consequences [thm]

1. **Value coupling is not enough**, in any direction and with any
   signs. Kicks, wraps and deletions in bounded windows change values
   or act transiently; none changes a mode. Both modes stay owned.
   Examples include coupler's J I ("if R1 = 0 then R2 += 2 else
   R1 += 2"), leftstream's proposed chain "R2 = 0 -> (R1 > 0 ? R1 - 1 :
   R1 + 6)", and gate's Z6 wrap used across counters.
2. **Non-monotone answers do not help on their own.** Round 2 showed
   that monotone answers give decidable machines. Theorem 1 adds that,
   with two counters, non-monotone answers are still not enough. The
   essential non-monotone ingredient is a *mode switch*: a zero event
   that changes the future drift.
3. **One-directional mode coupling is not enough.** If x's zero can set
   y's mode but y's zero cannot set x's, then x's mode is owned.
   Universality needs both directions (or a shared mode).
4. **Clean zero tests.** Theorem 1 needs no cleanliness. Conversely, a
   universal design needs zero events whose outcome depends on the
   remainder (which slot of the transfer ran out; s.5). The control in
   `lm.py` removes exactly that information and fails 96 times.

### 3.3 Checks of Theorem 1 [sim] (`nogo.py`, log `nogo.log`)

- Random machines: 3000 in class `value` and 3000 in class `oneway`
  (program length 2-6, up to 3 modes per side, delayed kicks of sign
  -2..+6, wraps 0 or 6). All 6000 are eventually periodic within 3000
  periods.
- Controls:
  - A hand-built cross-mode doubling machine and a hand-built shuttle
    machine with blind streams (x3 per round) are both detected as not
    eventually periodic. Their zero events come at periods 1, 3, 6, 12,
    19, 33, ... and 0, 2, 4, 10, 16, 34, ...
  - Among random machines of class `shuttle`, 38 of 3000 are flagged
    non-periodic. Random `cross` machines gave 0 of 3000: random cross
    machines rarely ping-pong, and the hand-built one carries that
    control.
- Mistake caught by the controls: my first periodicity checker accepted
  any sequence ending in a long quiet stretch, so both doubling machines
  were wrongly called periodic. The fix requires the periodic part to
  start within the first quarter of the run.
- As in round 2, random machines rarely compute anything. These checks
  test the code and the statement; the proof carries the claim.

### 3.4 Theorem 2 (interval model) [thm in model]

**Theorem 2.** Under (L), (N), (B), (Q) and (F), a two-stream machine
of rods is a 2SM with both modes owned. Hence its orbits are eventually
periodic (up to translation) and its halting is decidable.

*Proof.* Translate each premise into the 2SM conditions:

- Take s1 = the outer-face neighbourhood of O1 modulo L_1, together
  with the stream-1 program phase it sees. Define s2 the same way for
  O2. Take s0 = the gap with both inner faces.
- (F) and (B) make S finite. By (N), stream packets touch only outer
  faces.
- By (L), while x >= C the evolution of s1 depends only on s1 (the
  packets it meets are fixed by its position relative to the stream).
  So x's mode is owned. The same holds for y.
- Zero events require a short rod, which gives (A2). (Q) is assumed.
- The skew of s.2.3 is inside s1 and s2. Each face's arrival times are
  part of its own local evolution. ∎

**What the premises exclude, i.e. the escapes:**

- ¬(Q): a persistent gap process. It acts on both inner faces while
  both rods are long. This is a shared mode (s.6).
- ¬(N): a crossing. A signal could then reach the other counter's
  outer-side state.
- ¬(B): an unbounded gap holding many signals in flight. That is a
  delay-line memory, close to Cook's queue; not analysed here.

### 3.5 Gap bookkeeping [arg]

- Let alpha be the length of one counter unit, and let span be the
  distance from O2 to O1. Then span = alpha*(x + y) + gap.
- An outer op changes the span and x (or y) together and leaves the gap
  unchanged. An inner-face event changes x or y and the gap in opposite
  directions. So **gap change = -alpha * (net units added at inner
  faces)**, plus bounded corrections at zero events, where the rod's two
  faces meet.
- Consequences:
  - Coupler's J I with its echo (+2 at I2, then -1 at I1) shrinks the
    gap by alpha per use.
  - A machine whose couplings add net units at the inner faces has a
    finite lifetime of about gap0/alpha uses.
  - A shuttle that is used for ever must conserve x + y (e.g. -2 at I1,
    +2 at I2 per round trip).
  - Growth of x + y must therefore come from the outer faces (the
    streams).

## 4. What the theorems say a universal two-stream machine needs

Positively, Theorem 1 says what to look for. While both counters are
large, some state must set the drift of BOTH counters, and the zero
events of BOTH counters must be able to change it. There are two ways
to arrange this.

- *Shared mode.* One object both counters' zeros can reach, which acts
  on both counters. For rods, that object must live in the gap and act
  on the inner faces: a shuttle.
- *Cross-coupled copies.* Each side keeps a copy of the mode, which
  only its own stream reads. Signals from the other counter's zero
  events must reach it. For rods this needs a crossing.

## 5. Sufficient models: compilers and tests

### 5.1 The transfer machine (`lm.py`) [thm/sim]

- **States.** A state is a loop:
  - XY(k, j, nxt): while x >= k, do x -= k and y += j. The remainder
    r = x (0..k-1) stays in x, and the machine goes to nxt[r].
  - YX(k, j, nxt) is the same with x and y swapped.
  - HALT.
- **Compiler.** Use Gödel numbering, with Minsky registers
  (a, b) -> x = 2^a 3^b and y = 0.
  - INC r -> j: XY(1,1), then YX(1, p_r). Here p_0 = 2, p_1 = 3.
  - DEC r -> (jp, jz): XY(p_r, 1).
    - Remainder 0: YX(1,1) gives x = n/p, then go to jp.
    - Remainder r != 0: YX(1, p_r) gives x = r + p*(n div p) = n, then
      go to jz.
- **Shape of the compiled code.** Two transfers per Minsky step. Only
  the forms XY(k,1) (divide x into y) and YX(1,j) (multiply y into x)
  occur.
- **Test.** 502 programs: 2 hand-written and 500 random with 2-8
  instructions, inputs 0..4, budget 1500 steps. All match scholar's
  interpreter. In the 235 halting runs the result is exact (register
  values, y = 0, transfer count = 2 x Minsky steps). The other runs are
  still running after the same budget.
- **Control.** Zero events that carry no remainder information fail 96
  times.

### 5.2 Two streams with cross-coupled mode copies (`xm.py`) [sim, model]

- **Realisation.** Each stream delivers one slot per tick, grouped in
  beats of B slots.
  - In state XY(k, j), stream 1 DECs x at beat offsets 0..k-1, and
    stream 2 INCs y j times at offsets >= k + dmax + 1.
  - A DEC on zero at offset r is a zero event. It leaves the counter at
    r (a slot-dependent wrap), makes its own side idle until the next
    beat, and emits a cross signal carrying the next state. The signal
    arrives after a random delay of 1..delay_max ticks, aborts the rest
    of the receiver's beat, and the receiver latches the new state at
    its next beat start.
  - No shared clock exists; the two sides agree only through these
    signals.
- **Results** (150 random Minsky programs, values <= 1500, 105 halting):

| configuration | wrong runs |
|---|---|
| lockstep streams, random delays 1..3, design dmax = 3 | 0 |
| same, design dmax = 5 (slack) | 0 |
| CONTROL: y's zero events not sent to stream 1 (one-directional) | 105/105 |
| CONTROL: signals slower than the design (1..8 vs 3) | 91/105 |
| CONTROL: value-dependent skew, 0.3 slot per unit | 69/105 |
| CONTROL: value-dependent skew, 0.05 slot per unit | 21/105 |

- **Interpretation.** Cross-coupled modes in both directions suffice,
  with bounded signal delays and a slack rule (the receiver's actions
  come after the latest possible signal). Rate-matched ("time-mediated")
  transfers between two streams fail under skew, even small skew,
  because the receiver no longer counts the sender's beats.
- **Generalisation.** In any two-stream world with value-dependent skew,
  transfers should be metered by a handshake per unit, not by timing.

## 6. The shuttle route for E^n counters

### 6.1 Requirements [arg, from Theorems 1-2 and s.3.5]

A shuttle is a right-mover X and a left-mover Y with:
- X + (R1 inner face, value n) -> R1 changed by -a, plus Y;
- Y + (R2 inner face, value m) -> R2 changed by +a, plus X;

for all n, m above a small threshold. a = 1 or 2 keeps the gap fixed.

- **Class consistency.** Verify found that successive A-DECs at R1's
  inner face rotate its class. So the round-trip translation of the
  whole configuration (both faces and the shuttle) must lie in the
  class-preserving lattice M = <P_E, P_A>. Otherwise the reflections
  must work in every class the shuttle visits; the classes then cycle
  with period at most 3.
- **Stop or reversal.** When the source counter is empty, the shuttle's
  arrival must give a clean and distinct outcome: reverse direction, or
  stop and leave a marker. The rod must stay alive.
- **Start.** A zero event of either counter must be able to emit X or Y.

### 6.2 What a shuttle buys [sim]

- The shuttle is a shared mode, so Theorem 1 no longer applies.
  `nogo.py`'s blind-stream shuttle machine grows x3 per round for ever.
- It is also a handshake, so skew cannot break it. Stream timing then
  matters only through each stream's own rate.

### 6.3 Is a shuttle with blind streams universal? Open, with a reduction [arg]

"Blind" means the stream drifts s1 and s2 never depend on data. As far
as anyone has measured, that is the E^n situation today: class
progressions are data-independent.

- **One round.** With a single shuttle type of rate sigma per
  direction, a long x -> y passage multiplies the large value by
  (sigma + s2)/(sigma - s1), and the return passage by
  (sigma' + s1)/(sigma' - s2). One round is therefore n -> lambda*n + c,
  with lambda fixed by physics and the streams. The offset c and the
  next zero-window choice depend on the program phase and on n mod m.
- **lambda = 1** (for example when the streams have no net drift): the
  machine is a one-counter system with mod tests, hence decidable.
- **lambda != 1**: the round map is a generalised Collatz map with a
  single multiplier. Conway's undecidability construction uses several
  multipliers. I do not know whether one multiplier plus finite control
  is enough.
- **Several multipliers** would come from:
  - (i) several shuttle types with different speeds;
  - (ii) a per-side persistent state that changes the stream's drift
    (a packet filter with several states);
  - (iii) the gap itself: zero-window couplings shift the gap by fixed
    amounts, and the shuttle's rate depends on the gap. That makes the
    gap a shared bounded register.

  With (ii) on both sides, plus a two-type shuttle to pass the branch
  bit, the transfer machine of s.5.1 can be laid out [arg]. I have not
  compiled it at tick level; the exact timing and residue bookkeeping is
  heavy.

## 7. Reaction spec for leftstream and coupler (E^n world)

Ranked by how directly the theorems demand each item.

**Tier A: necessary for any universal two-stream E^n machine** (by
Theorem 2, unless something crosses a rod)
- A1. **Shuttle reflections** at both inner faces, gap-conserving and
  class-consistent over round trips (s.6.1). Coupler (06:02) ruled out
  X = A, Y = Bbar from the catalog, and slip lists the pairs to try.
  For a 1-unit shuttle: (B^2, 6 A), (B^4, A^4), (B^5, A^3), (B^6, A^2),
  (B^7, A). B has a single class against E^n, which makes the R2 side
  class-free.
- A2. **Shuttle at an empty source**: a clean reversal, or a stop that
  leaves a marker. The rod must survive; A + E -> C3 does not qualify.
- A3. **Shuttle start from a zero event**: R1's J at zero should emit Y,
  and R2's Z_L at zero should emit X.

**Tier B: needed for programmable transfer ratios** [arg]
- B1. A persistent, settable per-side drift state. Candidates: a
  packet-eating filter (gate's C1 messenger eats certain packets and
  stays until removed), a packet whose bulk effect depends on the rod's
  class, or a gap-dependent shuttle rate with zero events that shift
  the gap by known amounts.
- B2. A way to pass one branch bit across: two shuttle types, or two
  start signals.

**Tier C: timing and class rules**
- C1. Every coupling event happens in a designated class. Class
  bookkeeping on each side should stay data-independent, as verified
  for the left ops and for Bbar at R2's back.
- C2. Over every cycle of the program, the net units added at inner
  faces must be 0, or the counters eventually collide (s.3.5).
- C3. Never rely on rate matching between the two streams (skew, s.5.2).

**Not needed**: a wrap at zero (the non-monotone ingredient is the mode
switch); more value-coupling variants beyond one demonstration of T2.

**Answer to leftstream's question** ("what should R2's zero do at R1?"):
once a shuttle pair exists, R2's zero should emit the shuttle's
right-mover X. Until then, the bare A (R1 DEC in one class) is enough to
demonstrate T2. The chain "R1 > 0 ? R1 - 1 : R1 + 6" is still value
coupling (s.3.2), so it is not worth a dedicated SAT search.

## 8. Open problems

1. Is a shuttle with blind streams universal? This is equivalent to
   asking whether single-multiplier Collatz maps with finite control and
   residue tests are universal (s.6.3).
2. Does any glider train cross an E^n rod beyond width 30? That would
   reopen route ¬(N).
3. An unbounded gap as delay-line memory (¬(B)): what does it compute
   without becoming a cyclic tag system?
4. A tick-level compile of the transfer machine onto a shuttle plus
   two-state filters (s.6.3, item ii).
