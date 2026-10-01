# What a stream-programmed counter machine in Rule 110 needs: two limits and one gadget

Author: verify (round 2). Status labels: **[thm]** proved here for the
abstract model stated; **[sim]** checked by exact Rule 110 simulation with my
own code (`vlib.py`); **[arg]** an argument, not a proof; **[hyp]** a
hypothesis; **[evid]** empirical evidence from searches of the abstract model.

## 1. Summary

The round-1 target was a two-counter "cyclic skip machine": counters stored in
E^n gliders, a rigid stream of G-speed packets (GB3 = DEC, GB4 = NOP, GB5 = INC),
and a zero answer (an A glider) that deletes part of the later stream. Gate's
slip lemma (BOARD 23:37) showed that a zero answer that is absorbed cleanly
can only land its missing -1 on a later packet. This document asks what
machines that physics can build, and answers with two limits and one
positive finding.

1. **Clean answers give monotone machines, and monotone machines are not
   universal [thm].** If every zero answer either lands exactly one unit of
   decrement on a later packet, passes or deletes zero-effect packets, or
   leaves the system, the machine is a *chain machine* (section 2). Every
   chain machine's per-cycle map is monotone in the register values. From
   that and Dickson's lemma, its zero pattern is eventually periodic and its
   halting problem is decidable. This holds for any number of registers and
   any addressing, including feedback from downstream to upstream registers.
2. **Feed-forward layouts are not universal whatever the answers do [thm].**
   If registers sit along one stream and no answer can cross an upstream
   register, information flows only downstream. Each register is then a
   one-counter automaton driven by an eventually periodic input, and the
   whole machine is eventually periodic (section 3). This is the formal
   version of scholar's "answers must cross stores" condition (round-1
   THEORY.md s.4.1).
3. **A non-monotone gadget exists [sim], but its garbage undoes it [sim].**
   The two-packet program [GB3 test, G] on an E^n counter maps value 0 to 2
   and value v >= 2 to v - 2, which is not monotone. The zero branch is
   garbage-free (the answer and the G become two B's that the counter absorbs).
   The nonzero branch leaves an A^3 moving right. In every placement I tried
   where a third packet absorbs that A^3 without leaving garbage (557 of
   them, rigid stream), the net map is exactly v -> v + c: the branch
   disappears. Gate's wrap packet Z = GB3@(0,0)+GB4@(-25,46) (value 0 -> 6,
   otherwise DEC) is a garbage-free non-monotone primitive, so this
   cancellation is specific to my gadget, not general. I verified Z for
   I^v Z^3 and found that it misfires after a NOP (section 4).

So universality needs **both** a non-monotone answer effect **and** either
feedback (an answer crossing an upstream store), unbounded answer travel
(the in-flight stream used as a queue), or a store that is consumed and
regrown as in Cook's tape. With one E^n counter, the best reachable goal is
M2 (a nontrivial one-counter program), not M3.

## 2. Chain machines are monotone, hence decidable

### 2.1 The model

A chain machine has k registers with values in N and a cyclic program of
operations, executed in order, forever:

- `INC(r)`: r += 1.
- `CH(r1, ..., rm)` (distinct registers): decrement the first register in
  the list that is nonzero. If all are zero, nothing happens (the answer
  "escapes").

One pass through the program is a *cycle*; F: N^k -> N^k is the cycle map.
The *zero pattern* of a cycle lists, for each CH, which link fired (or that
it escaped).

### 2.2 Why this is the physics of clean answers [arg]

On the E^n counter a packet with counter effect e < 0 decrements the counter
by one if it can and emits the rest of its charge as right-moving A's
(verified by me, `t5.py`: E^n + GBk -> E^(n-1) + A^(3-k) for k < 3, all 42
G phases; at zero GB3 -> E + A in its designated class). A packet with e >= 0
just adds. So a DEC is `CH(r, ...)` whose later links are wherever the answer
goes. Gate observed that clean conversions A + X -> Y of G-speed packets
satisfy e(Y) = e(X) - 1, and that an answer can pass or delete only packets
with e = 0 (mod 7). A conversion with e(Y) = e(X) - 1 on a packet addressed to
register s is exactly the next link of the chain: s is decremented if it is
nonzero, and if s is zero the converted packet answers again. An answer that
crosses all later packets is an escape. Under these three premises every
machine built from such parts is a chain machine:

- (P1) packets act on their register as "add e" or "one unit down, rest as
  answers";
- (P2) an answer's only effect is one unit down on a later packet's
  register, passing or deleting e = 0 packets, or escaping;
- (P3) which later packet an answer reaches is fixed by the program layout.

If (P3) fails because answers skip packets that earlier answers have
already converted, the answer lands on the "first free slot". I argue that
this is still monotone (more units means fewer answers means fewer
decrements everywhere), but I have not formalised it.

### 2.3 The theorem [thm]

**Lemma 1 (monotone).** If v <= w componentwise, then op(v) <= op(w) for
each operation, so F(v) <= F(w).

*Proof.* INC is trivial. For CH, let v's first nonzero link be i and w's be
j. Since w >= v, j <= i. If j = i, both lose one unit in the same place. If
j < i, then v_{rj} = 0 < w_{rj}, so after the step w_{rj} - 1 >= 0 = v_{rj},
and v_{ri} - 1 <= w_{ri}. If v escapes, w loses at most one unit from a
register where v is 0. In all cases the order is kept. ∎

**Lemma 2 (thresholds).** Let L be the number of operations per cycle and
p >= 1. The zero pattern of p consecutive cycles starting from x, and the
change of every register, depend only on u(x) = min(x, pL) (componentwise).

*Proof.* A register that starts at pL or more is still at least 1 at each of
the at most pL - 1 earlier operations of the block, so every test sees it as
nonzero. Registers below pL evolve deterministically from their values. ∎

**Theorem.** For every chain machine and every start vector, the zero
pattern is eventually periodic. Whether a given link of a given CH ever
fires is decidable.

*Proof.* By Dickson's lemma the orbit v(0), v(1), ... contains t1 < t2 with
v(t1) <= v(t2). Put p = t2 - t1. Applying the monotone F^p repeatedly gives
v(t1 + (j+1)p) >= v(t1 + jp) for all j. Let u_j = min(v(t1 + jp), pL). The
u_j are non-decreasing in the finite box {0..pL}^k, so there is some
j0 <= k·pL with u_j0 = u_(j0+1) =: u. By Lemma 2 the blocks j0 and j0+1 have
the same pattern and the same change D(u). Registers below the cap have
D_r(u) = 0 (they are equal at the two block starts). Registers at the cap
stay at the cap because the progression is non-decreasing. Hence
u_(j0+2) = u, and by induction every block from j0 on has the same pattern.
To decide, search for t1 < t2 (the search ends by Dickson's lemma) and then
simulate (k·pL + 2)·p more cycles. ∎

**Consequences.** No compiler from Minsky machines to chain machines can
preserve halting, because Minsky halting is undecidable. The limit does not
depend on the number of registers, on the addressing scheme, or on whether
chains run upstream (feedback). Saturating decrement, the case where a
chain ends in an escape, is covered too, so an answer that simply leaves
does not help on its own either.

**What breaks monotonicity.** An operation "if x = 0 then y += 1", a
deletion of a later *decrement* when x = 0, or any answer effect other than
"one unit down somewhere". Round 1's skip semantics ("zero deletes one
block", `scholar/csm.py`) is non-monotone because a deleted block may contain
DECs. By gate's slip lemma, such an effect must be paid for with garbage
that leaves, or with a reaction that changes the counter charge by a
multiple of 7.

### 2.4 Checks (`models.py`, `chain_search.py`)

- Forward chain machines, 300 random programs (k <= 3, L <= 8): all
  eventually periodic within 3000 cycles.
- All 2-register programs of length 5 and 6 (46,656 x 3 and 139,968
  runs, `scratch_chain.py`): all eventually periodic [evid].
- Random chain machines with backward chains: 200,000 (k = 3), 100,000
  (k = 4) and 50,000 (k = 5): no non-periodic one [evid].
- **Weak control, stated honestly:** adding a non-monotone op TZ(x, y)
  ("if x > 0 then x -= 1 else y += 1") and searching 50,000 random programs
  also found no non-periodic one (`tz_search.py`). Random programs almost
  never compute anything, so these searches are no evidence for the theorem.
  The proof is what carries it.

## 3. Feed-forward layouts [thm]

**Model.** Registers R_1 (upstream, meets the stream first) ... R_k. Each
register is a counter with finitely many extra local states (for example
the E^n zero-state phase). The program is periodic. A register's answers
may change packets that have not yet reached it, but only within a bounded
window of the stream, and never packets addressed to an upstream register.

**Theorem.** The sequence of answers of every register is eventually
periodic.

*Proof.* By induction from R_1. Suppose the input reaching R_j (the stream
as modified by upstream answers) is eventually periodic with period M
packets. Over one period, R_j's (state, value) map is (s, v) -> (s', v + d(s))
for v at least a threshold B, since a large counter never reaches zero
within one period. Above B the finite state runs through a cycle with
average drift d. If d > 0 the value grows forever and the answers become
periodic. If d < 0 it falls below B. If d = 0 it stays constant. Below B
the pair (state, value) lives in a finite set, so it becomes periodic. In
all three cases R_j's answers, and so the input of R_(j+1), are eventually
periodic. ∎

Unlike section 2, this needs no monotonicity: any finite-state answer logic
is allowed. It is the formal content of round-1 scholar's condition 2
("answers must cross stores"). For E^n counters that condition fails.
Synth (round 1) found no A-train of width <= 24 that crosses E_1..E_3 from
the left. Architect's F-lane is the only round-1 layout where it holds: in
the F frame the stationary C1 messengers move right and cross F in class 1.

*Scope of the premise.* "Bounded window" matters. If an answer can travel
through an unbounded stretch of stream (passing packets) and convert a
packet far away, then the in-flight stream is extra memory, like a queue,
and the theorem does not apply. That is the queue agent's territory.

## 4. The non-monotone gadget and its garbage [sim]

All runs below use the exact Rule 110 engine and my own row builder and
typer. The scripts are `m1_scan.py` and `m1_search.py`.

**Observation 1.** Counter E^(v+1) at event (0,0), a GB3 at t0 = 1 (the
class in which E + GB3 -> E + A), and a G behind it. Across 42 G phases and
11 offsets, 159 placements give v = 0 -> E^3 alone. In those placements the
answer A meets the G and makes B^2, which joins the counter (A + G -> B^2 is
a catalog reaction in 3 of 9 classes). With the G at (dt, dx) = (35, 54)
relative to the GB3, the results are:

| v (start) | result |
|---|---|
| 0 | E^3 (value 2), nothing else |
| 1 | E + A^4 |
| 2 | E + A^3 (value 0) |
| 3 | E^2 + A^3 |
| 4 | E^3 + A^3 |

*Interpretation.* The G acts as "+2" when the counter was zero and as
"-1, emit A^3" otherwise. F(0) = 2 > F(2) = 0, so the map is not monotone.
This gadget lies outside the chain-machine theorem.

**Observation 2.** I added a third packet X in {G, GB1, ..., GB5}, over 42
phases and 11 offsets, and asked for every v in {0, 2, 3, 4} to end with a
single counter and nothing else (`m1_search2.py`: rigid right-anchored
stream, counter written by the program, exact CA). There are 557 such
placements. Every one of them gives m(v) = v + c: c = 1 for X = GB3, 2 for
GB4 and 3 for GB5; G, GB1 and GB2 gave none. (A first version,
`m1_search.py`, used left-anchored placement that shifted the stream with
v. It gave the same picture, 202/202, but should not be cited.)

**Observation 3 (gate's wrap packet, verified by me).** Z = GB3@(0,0) +
GB4@(-25,46) is a DEC for values >= 1, and at value 0 the answer shatters
the trailing GB4 into B's, giving value 6. That makes Z garbage-free and
non-monotone. I reproduced I^v Z^3 -> (v - 3) mod 7 for v = 0..6. A control
that shifts the last Z's GB4 by (7,0) changes only the case where that Z
meets zero.

A differential test against the model "Z = DEC, wrap 0 -> 6" fails on words
with a NOP before a wrap (INZZ -> A^3 + Ebar). The cause is a Z acting on
value 1. Its GB3 brings the counter to zero, and its GB4 then hits the zero
E, which moves E in 2 of 3 classes. The zero state's trajectory class
therefore depends on history: E@13 instead of E@0 after INZ. Any stream
builder has to designate classes for value-1 slots as well as value-0
slots.

*Interpretation.* When a later packet absorbs the A^3, it does so by a
reaction that also shifts the charge by 7. That restores linearity exactly,
not just mod 7 as gate's lemma requires. Within this scope, a garbage-free
branch did not exist.

*Recommendation.* Keep the gadget's garbage out of the program: let the A^3
leave through the rest of the stream (it must cross every later packet), or
park it in something that is never read. Otherwise the branch cancels. For
M1 in the strict sense (a finite stream), the two-packet gadget already
works; its garbage simply leaves.

## 5. What each primitive buys (for teammates)

| primitives | best machine | status |
|---|---|---|
| INC, DEC, zero answer that lands one unit later (clean) | chain machine: decidable, never universal | [thm] |
| + garbage that leaves (saturation) | still a chain machine | [thm] |
| one counter + any answer logic in a bounded window | eventually periodic (M2 at most: parity, countdown) | [thm] |
| several counters, feed-forward layout, any answer logic | eventually periodic | [thm] |
| non-monotone answer (e.g. [GB3, G]) + feedback between two registers | could be universal (CSM with skips is) | [hyp] |
| non-monotone answer + unbounded answer travel on one counter | queue-like; could be universal | [hyp] |

## 6. Open questions

1. Is there a composable non-monotone gadget, one whose garbage crosses the
   rest of the stream? The catalog has A + G#2 -> G + A. Does A^3 cross
   anything?
2. A formal version of the "first free slot" extension of (P3).
3. Feedback in the F-lane, with non-monotone answers there.
