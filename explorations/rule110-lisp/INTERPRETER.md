# An efficient Lisp interpreter on Rule 110: design notes (phase 10)

Goal (user, 2026-10-06): a Lisp expression is typed, translated into a
Rule 110 initial row, Rule 110 evolves, and the result is read out. The
existing tower (Lisp -> SKI -> Turing machine -> Neary-Woods tag system ->
CTS -> gliders) is correct but costs about 1e19 generations or more even
for `(car (quote (a b)))`. "Find another way; focus on efficiency."

## 1. What a run costs, and the budget

*Observation (event engine, REPORT 3.9 and NOTES phase 9).* On gliders,
almost all the work is tape characters crossing the queued matter of the
CTS: every queued object is crossed about once per CTS read. The
three-state machine run took 2.7e10 events for 59,184 reads with a queue
of 8,000 to 10,000 CTS symbols, i.e. about 45 events per (read x queued
symbol). The engine did about 2.3e6 events per second.

*Cost model used below.* events ~ 45 x sum over reads of Q, where Q is
the CTS queue length in bits at that read. A budget of about 1e11 events
(half a day) allows sum(Q) ~ 2e9, e.g. 1e6 reads at Q = 2,000.

*Where the old tower spends it.* Not in SKI: `(car (quote (a b)))` is 61
normal-order SKI steps on terms of at most 1,475 characters (39k
characters touched in all). The cost is in the route from SKI to the CTS:
85.9M Turing machine steps, then a tag alphabet of ~7.9M symbols, each a
7.9M-bit one-hot word. Measured SKI sizes (normal order, probe applied):

| expression | SKI term | steps | max term | chars touched |
|---|---|---|---|---|
| `(quote a)` | 39 | 18 | 49 | 534 |
| `(car (quote (a b)))` | 311 | 61 | 1,475 | 3.9e4 |
| `(cdr (quote (a b)))` | 313 | 66 | 1,477 | 4.3e4 |
| `(cons (quote a) (quote b))` | 167 | 21 | 283 | 3.3e3 |
| `(atom? (quote a))` | 485 | 150 | 2,569 | 2.0e5 |
| `(eq? (quote a) (quote a))` | 1,675 | 699 | 7,457 | 2.0e6 |

So the target is a CTS that does the evaluation directly, with a queue of
hundreds to a few thousand bits, in at most ~1e6 reads.

## 2. What one pass of a CTS can compute

Cook's construction fixes two things (REPORT 3.4, NOTES): appendant
lengths that are ever appended must be multiples of 6, and no appendant
may be empty. The natural unit is therefore a *symbol*: a B-bit one-hot
word (B a multiple of 6), plus the all-N blank. If every appendant is a
whole number of symbols, the CTS acts symbol by symbol, and the symbol at
absolute index k is read at phase k mod m against appendant group k mod m
(m = number of phases, p = m*B appendants). `phasem.py` implements this
view; `tests/test_phasem.py` checks it against the CTS bit for bit.

*Consequence 1: a symbol knows only its letter and its phase.* Its phase
was fixed when it was appended: it is the queue's absolute length mod m at
that moment. Reading a symbol appends a fixed word chosen by (letter,
phase). Nothing else is visible.

*Consequence 2: information moves only through lengths.* A symbol that
appends one extra blank shifts the phase of everything appended after it.
Worked out exactly (see `phasem.py` docstring): if symbol j appends
len_j symbols in pass r, the child of symbol k is shifted, relative to
its parent, by n_r + sum_{j<k} (len_j - 1), with n_r the queue length.
With blanks this gives: extra blanks emitted in pass r are seen as a
*prefix* sum by later symbols' children, and in the next pass (when the
blanks vanish but still count in n) as a *suffix* sum by earlier ones.

*Consequence 3: no local communication in general.* Within one pass a
symbol learns a mod-m prefix (or suffix) sum of all earlier emissions,
never its neighbour's value alone. A symbol can isolate one sender's
value only if every other emission before it is known or cancels; a
cancelling pair needs the same information already placed on both sides
of the receiver. Information is monotone in queue order, so such pairs
cannot be regenerated without help. Tag systems live inside this model
(phase 0 reads, other phases delete), which is why their known
simulations of Turing machines are expensive.

*So a CTS pass is an associative SIMD step:* every symbol updates its own
small state from (letter, received sum), and the only interconnect is one
prefix/suffix sum mod m per pass. With few senders this is a broadcast
bus of log2(m) bits per pass over any distance; with many senders it is a
parallel count (depth of nesting, rank among marked symbols).

## 3. Plan

Design the interpreter for that machine instead of compiling a Turing
machine into it.
- Layer A, `phasem.py`: phase machine <-> CTS. Done, tested.
- Layer B: a small "bus machine" on top of phase machines: symbols with a
  letter, a broadcast per pass, prefix/suffix counts, insert/delete.
  Compiled to phase-machine rules automatically; checked by running the
  rules.
- Layer C: Lisp evaluation as a bus-machine program. Start with the
  variable-free fragment (quote car cdr cons atom? eq? cond), whose
  evaluation needs no copying; then lambda/define, where substitution
  copies values one symbol per broadcast.
- Measure passes, Q and sum(Q) per expression; then run the smallest on
  gliders with the event engine and read the result out.

Status log is in NOTES.md (phase 10).
