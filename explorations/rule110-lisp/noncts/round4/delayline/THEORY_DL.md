# Gaps, delays and windows: what an unbounded distance can do in the E^n world

Author: delayline (round 4). Labels: [sim] exact Rule 110 simulation with a
control that can fail; [thm] proof in the stated model; [arg] argument, not a
full proof; [model] executable abstract model; [hyp] hypothesis. Every
negative result carries its scope. File names refer to this directory.

## 0. Summary for a reader in a hurry

Round 3's Theorem 1 says two counters coupled through zero events are
eventually periodic if one counter's drift-setting state (its *mode*) is
changed only by its own zeros. Its Theorem 2 adds that, for two E^n rods fed
by blind streams from both sides, the left rod's mode is always owned.
Theorem 2 assumes a bounded gap and a gap that falls quiet. This note asks
what an unbounded gap buys. The answer has four parts.

1. **A drift switch exists [sim].** A rod held at value 0 or 1 (a *window*)
   on the right side WALKS under right-stream no-op packets when it is at 0,
   and stays put at 1. The left rod's zero answer (an A glider) switches it
   from 1 to 0, at any arrival time. So a zero event of the left counter y
   turns on a drift of another unbounded quantity, the gap g. This is the
   kind of coupling Theorem 1 asks for, in one direction (s.3).
2. **Windows can gate distances, hardly values [thm + sim].** Slip
   conservation forces any right-stream block that leaves a closed window
   unchanged to shoot only multiples of 7 units through an open window that
   stays open (s.4). Among all 2,337 library G-speed packets exactly one,
   S43, is neutral on a closed window and shoots on an open one, and it
   closes the window behind it (one shot only). Walks carry no charge, so
   they are not restricted.
3. **"One signal in flight" is not a separate route for blind streams
   [arg].** The left rod at zero answers once per zero-test slot until it is
   refilled, and a refill caused by its own answer needs a round trip of
   length proportional to g. So either the left program refills itself
   (then everything the right side does to y is a delayed value kick, and
   Theorem 1's reasoning applies unless g = 0 has a repeatable contact
   reaction), or Theta(g) answers are in flight per zero episode: the
   delay-line regime (s.6).
4. **The delay-line regime converts distance into a count, but Rule 110's
   channel eats the refill [model + sim].** A zero episode emits
   floor(round trip / slot) + 1 answers (model, 15/15 cases). In Rule 110
   the answers (A) and every single-class refill (B-lattice trains, all 391
   of width <= 30) annihilate one unit per meeting, so a refill sent in
   reply cannot pass the rest of the burst; for large g the left rod is
   never refilled (s.7).

What remains open (s.8) is stated as three concrete search targets.

## 1. Setting

The layout is round 3's:

    [left stream ->]  O2 ==R2== I2   gap g   I1 ==R1== O1  [<- right stream]

- y = value of R2 (E^(y+1)), x = value of R1. Both streams are blind and
  periodic: their packets do not depend on data.
- A **window** is a rod kept at value 0 or 1, so that its stream can act on
  the gap through it (round-3 THEORY s.6.4). W below is R1 used as a window.
- Distances are measured as trajectory intercepts x - v t (cells) of the
  E-speed objects (v = -4/15), so a positive shift is to the right.

Slip (mod 14) is the only conservation law (round 1). A rod unit and a B
glider carry slip 6; an A carries 8 = -6. A rod value therefore changes by
the "charge" of what it absorbs, counted mod 7.

## 2. Physical inventory: what changes a distance

| effect | where | status |
|---|---|---|
| B-family unit absorbed at a rod's back: +1, single class | R2's back; g shrinks | known (rounds 1-3) |
| A from the left: -1 at a front; class-free only for E^2 -> E | R1's front | r3 ledger #8 |
| A + B -> nothing, A + B^k -> B^(k-1), single class | in the gap | catalog |
| K3 at R1 = 0 passes as B^3, R1 stays 0 | R1 window | r3 ledger #31 |
| **a zero window walks under NOPs**: E + GB4 -> E shifted +308/15, 0 or +364/15 cells (one per class); E^2 + GB4 -> E^2 unmoved, all classes | R1 window; g grows | catalog; walk.py, ds.py |
| 422 (packet, class) walks among 2,337 G-speed packets, all to the right (0 to 78.4 cells) | R1 window | scan_e2.jsonl, wclass.py |
| merge: D1 at R1's front dumps R1 into R2 (y := y + x + 2) | gap | shuttle 23:24, verify 23:33 |

Every walk found is to the RIGHT. The right stream can lengthen the gap by
walking its window; the gap shrinks only when units are added at R2's back.

## 3. The drift switch [sim]

**Scene** (ds.py, ds_ca.py, ds_sweep.py). Left stream I_L^v2 Z_L on R2 = E
(coupler's rigid left-stream builder); R1 = E^2 (round-2 input prefix,
value 1); right stream: 10 identical NOPs (GB4) in one slot class c.

**Observation.**
- v2 = 0: Z_L at R2's zero sends an A. It opens the window (E^2 -> E). Every
  later NOP walks the window right, 24.27 and 20.53 cells alternately.
- v2 >= 1: no A; the window stays E^2 at the same place; NOPs do nothing.
- Over Z_L times spread across 60,000 steps and gaps 600, 1200 and 2400
  (123 runs, exact CA), the final window position is always one of the
  points of the alternating walk sequence 27.6, 48.13, 72.4, ..., 206.8,
  and it falls as the A arrives later. So the result depends only on how
  many NOPs follow the arrival. Exception: one run (gap 1200, Z_L at 55,500)
  ended at 78.0, off the sequence (see s.3.1).
- Slot class c = 1 parks the opened window instead (no walk at all). The
  window's phase relative to the stream is itself a two-state mode.
- Controls: v2 = 1 at every gap (window unmoved), and the A arriving before
  the window holds value 1 (tz = 2,000: A + E -> C3, the window is
  destroyed), which documents the precondition.

**Interpretation.** A zero event of y turns on the drift of a different
unbounded quantity. In Theorem 1's terms the gap's mode (walking or not) is
set by y's zero. The reverse direction, a gap event changing y's drift, is
not provided by anything found (s.4, s.8).

### 3.1 The coincidence window (fine sweep)

(ds_fine.py; filled in below once the sweep is complete.)

## 4. The slip lemma for windows [thm]

**Lemma.** Let a block P of right-stream packets act on a window. Suppose P
takes a window of value w_c to value w_c' and emits nothing, and takes a
window of value w_o to value w_o' while emitting only a left-moving B-family
train worth k units. Then

    k = (w_c' - w_c) - (w_o' - w_o)   (mod 7).

*Proof.* The two runs start from the same packets, so the total slip of the
products agrees mod 14: 6(w_c' - w_c) = 6(w_o' - w_o) + 6k (mod 14). The
unit 6 is invertible mod 7 after dividing by 2. QED.

**Consequences.**
- A gate that is neutral when closed and stays open after shooting can
  shoot only 0 mod 7 units. A gate that closes itself to value d when it
  shoots sends 7 - d units (mod 7). The only library example is
  S43 = GB3@(0,0)+GB5@(-14,54): neutral on E^n, n >= 2, in every class, and
  E -> E^5 + B^3 in one class (d = 4, k = 3).
- Walks carry no charge. A window can therefore switch a DISTANCE drift
  freely, but a rod's VALUE drift only in 7-unit quanta, or by changing its
  own value (which then needs restoring, and restoring is blind).

**Search (scope: single library packets of velocity -1/3, all 2,337, every
class, windows E and E^2; scan_e2.jsonl + round-3 coupler's E scan;
wclass.py).** Neutral on E^2: 657 (packet, class) outcomes, 219 packets in
all classes. Neutral on E^2 AND shooting on E: S43 only. No 7-unit shooter,
no reusable reflector (E -> E^2 + B^6), no left walker, no packet that
passes a value-1 window.

## 5. Latency forces delay-insensitive control [arg]

A signal crossing an unbounded gap arrives after an unbounded time. A blind
periodic stream cannot wait for it. Its effect must therefore not depend on
when it arrives: the receiver must rest in a state its own stream leaves
unchanged, and the arriving signal must react with that state in one class.
E^2 under NOPs, with A + E^2 -> E, is such a pair (s.3). E^n (n >= 3)
receiving an A is not (one clean class out of three).

## 6. One signal in flight collapses [arg]

Premises (the E^n world as measured): (a) the left stream is blind with
period L slots; (b) R2's zero answer is made by a zero-test packet (Z_L)
finding R2 at 0, and every such slot sends one A; (c) what the right side
can send to R2's back in a timing-free way adds units (B family, single
class); (d) a right-side reply to an A needs at least the round trip,
proportional to g.

For y to have more than one zero episode the left program must have negative
net drift (by (c) nothing else lowers y). Then, while y is 0 and nothing has
arrived, each period has a zero-test slot at 0, so at least one A leaves per
period. Two cases per episode:
- **self-refill**: the left program's own INCs lift y within the period. A
  bounded number of A's leave. Everything the right side does to y arrives
  later as a value kick, while y's front program runs unchanged: y's mode is
  owned. With boundedly many signals in flight, Theorem 1's passage argument
  still bounds the in-flight contribution per passage, so an escape needs
  the gap's own zero (R2's back reaching the window) to switch the window,
  repeatably. In the E world, co-moving rods at contact merge into one rod
  (no reaction), so no such switch is known.
- **wait for the right side**: the episode lasts at least one round trip,
  and Theta(g) A's are in flight. This is the delay-line regime.

Caveat: Theorem 1's corner step needs a finite state space near the corner;
with unbounded g the corner revisits carry g along. The "Theorem 1 applies"
step above therefore needs Lemma 1 redone for a one-counter regime that also
carries g. That is why this section is labelled [arg].

## 7. The delay-line regime: value as a time delay

**The burst law [model].** In the waiting case, A's leave R2 at each slot
until the first refill arrives. If the refill passes the burst freely, the
burst has floor(rt/P) + 1 A's, where rt = g/v_A + latency + g/v_B is the
round trip (rod-frame speeds 14/15 and 7/30) and P the slot length. So a
zero episode CONVERTS THE DISTANCE g INTO A COUNT, rounded by a floor that
depends on phases. burstmodel.py checks this law in an event simulation:
15/15 cases (g = 100..3000, P = 150..300). If each reflection also moves the
reflector (a walk), g grows by a data-dependent factor per episode, and the
zero times are not eventually periodic (gaps 200, 354, 376, 376, 376, 706,
1124, ...; control without walking: constant). Affine maps with floors are
the raw material of Conway's generalised Collatz functions, so this regime
is not excluded by any theorem we have. It is a register machine with the
number in flight, not a queue of symbols, as long as one burst is in flight
at a time.

**Rule 110 eats the refill [model + sim].** In Rule 110 the answers are
A's. A refill must reach R2 through the oncoming burst, meeting A's at
uncontrolled phases, so it must cross A in every class that occurs. The only
left-movers with a single class against A are on the B lattice
(|det((3,2),(4,-2))|/14 = 1), and they are also single-class against rods.
bscan.py tested all 391 (4,-2) trains of width <= 30 (theory's SAT
enumeration), exact CA:
- every train acts as a pure charge carrier: E^m + Q -> E^(m+k) for
  m = 1, 2, 3, 5 (k = 1..8);
- an A never crosses it: A + Q -> Q with one unit less (or nothing, 4 cases);
- controls: B and B^3 reproduce the catalog (A + B -> nothing,
  A + B^3 -> B^2, E^m + B^k -> E^(m+k)).
With annihilation the model shows the consequence: the reply to the first A
meets the rest of the burst and is eaten. For g = 100, 600 and 1200 R2 is
never refilled.

**Interpretation.** In the round-3 layout the gap is an annihilating
channel for every timing-free signal pair found. The burst regime, which is
where an unbounded gap would act as memory, cannot close its loop with these
signals. Scope: (4,-2) trains of width <= 30, single-train refills.

## 8. What is missing, as search targets

Any one of these would reopen the gap route; none is excluded by a theorem.

1. **Burst-safe refill**: a left-mover that crosses A in every class it can
   meet and adds units at a rod's back in a timing-free way (s.7). B-lattice
   trains up to width 30: none. Next: wider trains; multi-class left-movers
   with a proof that only a crossing class occurs.
2. **Repeatable contact switch**: a reaction when R2's back reaches the
   window (g = 0) that changes the window's mode and leaves both objects
   usable (s.6). Co-moving E's merge instead (no reaction); shuttle's D1
   merge is a one-shot bulk transfer.
3. **Value gate**: a right-stream packet neutral on E^2 that, on E, shoots
   7 units and leaves E (or shoots 6 and leaves E^2: a reusable reflector).
   Library: none (S43 shoots 3 and closes to value 4). Next: SAT with the
   neutral case as one scene and the shot as the other.

Together with the drift switch of s.3, target 3 would give both directions
of Theorem 1's coupling (y's zero sets the gap's drift; the gap's walking
window then gates y's refills), still subject to s.6's contact problem.
