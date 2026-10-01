# Gaps, delays and windows: what an unbounded distance can do in the E^n world

Author: delayline (round 4). Status: working draft, updated as results come in.
Labels: [sim] exact Rule 110 simulation (with a control that can fail),
[thm] proof in the stated model, [arg] argument, [model] executable abstract
model, [hyp] hypothesis.

## 1. The question

Round 3 proved (Theorem 1) that two counters coupled only through their zero
events are eventually periodic whenever one counter's *mode* (the state that
sets its drift while both counters are large) can be changed only by its own
zeros. For E^n rods driven by two blind streams, Theorem 2 adds that the left
rod's mode is owned, because nothing reaches its front from the right.
Theorem 2 assumes (B) a bounded gap and (Q) a gap that falls quiet. This
note asks what an *unbounded* gap buys:

1. Can the distance between two co-moving objects be changed by controlled
   amounts and read?
2. Can signals in flight between two walls act as memory?
3. Can a counter's value act as a time delay, and can that give the mode
   coupling Theorem 1 demands?

The layout throughout is round 3's:

    [left stream ->]  O2 ==R2== I2   gap g   I1 ==R1== O1  [<- right stream]

with y = value of R2 and x = value of R1. A rod held at value 0 or 1 is
called a **window** (round-3 THEORY s.6.4): its two faces touch, so its
stream can act through it.

## 2. Physical inventory (what moves a distance)

| effect | where | status |
|---|---|---|
| B-family unit absorbed at a rod's back: +1, single class | R2's back; g shrinks by one unit | known (round 1-3) |
| A from the left: -1 at a front; class-free only at E^2 -> E | R1's front; g grows | known (r3 ledger #8) |
| A + B annihilate; A + B^k -> B^(k-1) (single class) | in the gap | catalog |
| K3 at R1 = 0 passes as B^3 (R1 stays 0) | R1 window | r3 ledger #31 |
| **a zero window WALKS under NOPs**: E + GB4 -> E shifted +308/15, 0, +364/15 cells (3 classes); E^2 + GB4 -> E^2 unmoved (all classes) | R1 window; g grows | catalog; walk.py, ds.py [sim] |
| 23+ further NOP packets (slip 0) neutral on E^2 in every class, walking E by 24-50 cells in some classes | R1 window | walkers.py (scan in progress) |

Every walk found so far is to the RIGHT (away from R2): the right stream can
only lengthen the gap by walking; the gap shrinks only when units are added
at R2's back.

## 3. A drift switch: R2's zero turns the gap's drift on [sim]

Scene (ds.py): left stream I_L^v2 Z_L on R2; R1 = E^2 (a closed window);
right stream = a uniform train of NOPs (GB4) in slot class c.

- If v2 = 0, Z_L's answer A crosses the gap and opens the window
  (E^2 -> E, class-free). From then on every NOP walks the window right
  (24.27 and 20.53 cells alternately), so the gap grows at a fixed average
  rate of 22.4 cells per NOP.
- If v2 >= 1, no A is sent; the window stays E^2 and NOPs do nothing.
- The walk depends only on HOW MANY NOPs follow the arrival, not on when
  the A arrives (A leaves the window's back E in a fixed place; arrival
  times varied over 40,000 steps). The design is delay-insensitive.
- One slot class (c = 1 in this layout) parks the window instead (no walk):
  the window's phase relative to the stream is itself a 2-state mode.

So a zero event of y changes the DRIFT of another unbounded quantity, the
gap. This is the kind of coupling Theorem 1 asks for, in one direction.

## 4. Why one direction is all a window gives cheaply: the slip lemma for windows [thm]

Slip (mod 14) is conserved; a rod unit and a B carry slip 6, an A carries 8
(= -6). Let a block P of right-stream packets act on a window whose states
have rod values w_c (closed) and w_o (open). Suppose P leaves the closed
window at value w_c' and emits nothing, and leaves the open window at w_o'
and emits only a left-moving B-family train of k units. Then

    k = (w_c' - w_c) - (w_o' - w_o)   (mod 7).

*Proof.* Both runs start with the same packets, so their total slips agree
mod 14: slip(P) = 6(w_c' - w_c) = 6(w_o' - w_o) + 6k (mod 14). Divide by
the unit 6, which is invertible mod 7. QED.

Consequences:
- A gate that is NEUTRAL when closed (w_c' = w_c) and stays open after
  shooting (w_o' = w_o) can shoot only multiples of 7 units.
- If shooting also closes the window to value d (w_o = 0, w_o' = d), the
  shot is 7 - d units (mod 7). The one such packet seen so far is
  S43 = GB3@(0,0)+GB5@(-14,54) (round-3 cross0_clean.txt): NOP on E^n for
  n >= 2 (class-free), and on E in one class: E^5 + B^3 (d = 4, k = 3).
- Walks carry no charge, so a neutral window can switch POSITIONAL drifts
  (the gap) freely, but it can switch a rod's VALUE drift only in 7-unit
  quanta or by changing its own value.

## 5. Latency forces delay-insensitive control [arg]

A signal that crosses an unbounded gap arrives after an unbounded time. A
blind periodic stream cannot wait for it, so its effect on the receiver must
not depend on when it arrives: the receiver must sit in a state that its own
stream leaves unchanged, and the arriving signal's reaction with that state
must be single-class. E^2 under NOPs, with A + E^2 -> E, is such a pair;
E^n (n >= 3) receiving an A is not (one class only).

## 6. One signal in flight collapses into Theorem 1 (the gap-register route) [arg]

On the left, R2's zero answer is made by a Z_L at R2 = 0. Every Z_L slot
that finds R2 at zero sends an A. The right side can only add units at R2's
back (B-family), and its reply needs at least one round trip, of length
proportional to g. Hence, per zero episode of y:

- either the left program refills R2 itself within a bounded time (a wrap),
  so a bounded number of A's leave per episode. Then everything the right
  side does to y is a delayed value kick, y's front program is untouched,
  and y's mode is owned. With boundedly many signals in flight Theorem 1's
  passage argument goes through (the in-flight kicks are bounded per
  passage). Escape is possible only if g's own zero (R2's back meeting the
  window) switches the window's state, repeatably;
- or R2 waits for the right side's refill, and sends Theta(g) A's per
  episode. Many signals are then in flight: the delay-line regime (s.7).

So "one signal in flight" (row 8 of theory's route map) is not a separate
route for blind streams: it is Theorem 1 territory unless a repeatable
contact reaction at g = 0 exists, and otherwise it becomes row 9.

Caveat: Theorem 1's corner step assumes a finite state space near the
corner; with an unbounded g the corner revisits carry g along. The step
"bounded in-flight content => Theorem 1" therefore needs Lemma 1 redone
for a one-counter regime that also carries g. Status [arg].

## 7. The delay-line regime: value as a time delay [arg/model, to be filled]

(burst counting: the number of answers in flight is the round-trip time
divided by the left period, so a zero episode converts g into a count;
in-flight A's and B's annihilate pairwise.)

## 8. What is missing for an escape, as search targets

(to be filled after the window table is complete)
