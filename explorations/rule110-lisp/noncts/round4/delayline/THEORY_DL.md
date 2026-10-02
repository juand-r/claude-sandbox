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
   from 1 to 0, at almost any arrival time. So a zero event of the left
   counter y turns on a drift of another unbounded quantity, the gap g.
   Left windows also walk (both directions, under uniform left streams),
   and a B^3 shot (what R1's zero sends) closes a walking left window and
   freezes it. So both kinds of zero signal can switch a gap's drift
   (s.3). Neither switches a ROD's drift, which is what Theorem 1 needs
   for two rod counters; for two GAP counters (theory's route 20) these
   are the needed switches, still missing a middle marker and contacts.
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

Every RIGHT-window walk found is to the right: the right stream can
lengthen the gap by walking its window, not shorten it. LEFT windows walk
both ways (s.3.2), so the left stream can move its side of a gap in either
direction.

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
- The A's own collision class at the window (3 classes; set by g mod a
  lattice) does not matter for switching: ds_cls.py (R2 seeded at times
  0, 1, 2) opens and walks the window in all three. But A + E^2 -> E leaves
  the E 1.87 cells further right in two of the classes (7.0 / 7.0 / 5.13 in
  isolation), so the walk starts from 3.33 or 5.2 with the alternation
  phase shifted. The earlier sweeps could not see this: their gaps and
  times differ by lattice vectors that keep the A class.
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

ds_fine.py swept every arrival slot (Z_L times are quantised to P_E = 15
steps) from 53,000 to 58,000 at gap 1200: 334 runs, exact CA, all with
clean products (R2 = E plus one lone E).
- 322 runs: the window ends on the walk sequence (delay-insensitive).
- 12 consecutive slots (55,370..55,535, i.e. 180 steps, where the A reaches
  the window while a NOP is colliding with it) end off the sequence:
  - 8 of them still walk, with the whole sequence shifted (e.g. 94.8,
    87.33, 78.0 instead of 92.93 / 72.4);
  - 4 of them (every third slot: 23.87, 18.27, 12.67, 7.07) walk once and
    then PARK: the switch fails.
So the drift switch is delay-insensitive except when the arrival coincides
with a NOP collision, about 180 of the ~7,100 steps between NOPs (2.5%);
the switch fails outright in about 1.2% of arrival phases. In a machine
with an unbounded gap the arrival phase sweeps through all values, so a
design must keep arrivals out of that window, e.g. by spacing NOPs so that
the arrival phase is fixed mod the NOP period [hyp].

### 3.2 Left windows walk both ways; a B^3 stops a walking left window [sim]

lscan.py tested all 6,398 A-lattice trains of width <= 30 (shuttle's SAT
enumeration) from the LEFT against a zero window E and against E^2, in
each of the 3 classes (exact CA; control: the library A reproduces the
catalog, A + E -> D1, D1, C3 and A + E^2 -> E). lclass.py:
- a zero left window walks in BOTH directions: single-packet shifts from
  -12.13 to +27.07 cells (rightward ones are far more common);
- 583 (train, class) outcomes leave E^2 as E^2; 49 trains leave E^2
  exactly unmoved in some class and walk E in some class.
lwalk.py: uniform streams of one train (copies 84 cells apart) keep a zero
window walking at a steady rate, e.g. train 499 at +11.2 cells per packet
(toward the gap's far side) and trains 875 / 1055 / 1199 at -2.8 per
packet (away from it), checked for 5, 10 and 20 packets.
lgate4.py: 47 walking trains are also neutral and unmoved on E^4 in some
class. E^4 is what a K3 shot (B^3, ledger r3 #31) makes of a zero window.
lstop.py (train 499, class 1; B^3 injected at the window's back at 75
arrival times spread over five packet periods, packets 280 cells apart):
63/75 give a lone E^4 frozen where the window was when the B^3 arrived
(11.6, 22.8, ..., 56.4: one step of 11.2 per packet before the stop);
12/75, three consecutive arrival slots per packet period (the B^3 arriving
during a packet collision), give debris (F, or B + Ebar). Control (no B^3):
the window walks on (56.0 after 5 packets). With packets 84 cells apart
the debris fraction is 3/7, so it scales with the collision's share of the
packet period. Train 875 (leftward walker) is NOT stopped: the closed E^4
is walked by the same amount.

So the opposite direction exists too: a B^3 (what R1's zero sends through a
zero R1) switches a left window's walk OFF.

**End to end (fullstop.py, fullstop_sweep.py; seeds fullstop_scenes.json).**
40 copies of train #499 (280 cells apart) walk W_L; ~1200 cells to the
right, R1 = E + v1 GB5's receives K3 in its zero class.
- v1 = 0: K3 passes R1's zero as B^3, W_L closes to E^4 and freezes
  (370.0, 358.8, 347.6, 336.4, 325.2 as the arrival moves earlier), R1 = E.
  25/30 arrival shifts clean; every 6th shift (B^3 during a packet
  collision) gives Ebar + Ebar + A.
- Controls: v1 = 1, 2: W_L walks all 40 packets (448.0), R1 = E^5 / E^6;
  K3 in R1-class 1: R1 -> Ebar + D1 + D1 (catalog), W_L walks 448.0.

### 3.3 Contact of a walking window with a marker (lead item 2) [sim, scoped negative]

contact.py: train #499 (class 1, 84-cell spacing, 16 packets) walks W_L
into a co-moving marker X in {E, E^2, E^3, E^4, Ebar}, at every seed time
and every ether-compatible offset 10..130 cells (770 scenes, exact CA).
contact_an.py: no clean outcome. 761 debris; 9 with X = E^4 end as
E^3 + D1 + A + A^4 (all right-moving), but W_L is consumed, so the
contact is not repeatable. No clean merge (W_L + E -> E^2) was reached:
the 11.2-cell walk steps do not land W_L in E^2 alignment.

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

### 4.1 Consequence for a per-unit handshake (lead item 3) [thm via s.4]

A per-unit handshake at the right window means: the window rests closed
(E^2, under a stream block that leaves it unchanged), an A opens it, it
takes ONE step, closes again, and sends a signal back. The block is
neutral on the closed state (w_c' = w_c) and takes the open state 0 to 1
while emitting a left-mover, so by the lemma the left-mover carries
k = 0 - 1 = 6 units (mod 7) of B-family charge (slip 8). So the handshake
needs exactly the "reusable reflector" E^2 -> E^2, E -> E^2 + (6 units
left), whatever stepping it also does. Library: none (s.4). SAT
(sat_refl.py, two scenes sharing the packet Y, G lattice, slip 0):
positive control "walk" (E^2 -> E^2 unmoved, E -> E) is SAT at W = 30 in
124 s and re-simulates; results of the reflector search are in s.8.

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
   merge is a one-shot bulk transfer. Library scan s.3.3: none.
   SAT spec (not run; one shared unknown, the left packet Q, A lattice,
   slip 0): scene 1, Q + E -> E (any placement: a walker or a no-op);
   scene 2, Q + [E, then marker X at a fixed contact spacing s] ->
   [E-family W_L' unmoved or closed] + [X unchanged, any placement] +
   [a right-moving A-lattice train beyond X]. X and s from the catalog
   compounds E@(0,0)+E@(-k,x) / E@(0,0)+Ebar@(...); the right-moving
   output must then cross X, which no single A does (A + E -> D1/C3), so
   X should be an object A crosses (Ebar, classes 0, 3, 4, 5).
3. **Value gate**: a right-stream packet neutral on E^2 that, on E, shoots
   7 units and leaves E (or shoots 6 and leaves E^2: a reusable reflector).
   Library: none (S43 shoots 3 and closes to value 4). Next: SAT with the
   neutral case as one scene and the shot as the other.

4. **For two gap counters (theory's route 20, W_L ~g1~ M ~g2~ W_R)**: a
   co-moving middle marker M that both windows' signals reach, with contact
   reactions at M (zero tests) that emit start/stop signals; s.3 supplies
   the window walks and the stop/start switches on the window side.

Together with the drift switch of s.3, target 3 would give both directions
of Theorem 1's coupling (y's zero sets the gap's drift; the gap's walking
window then gates y's refills), still subject to s.6's contact problem.
