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

## 3. The bus machine: put the program in the table

*Idea.* If the queue's layout never depends on the data, the CTS table
can know at every read which register it is serving and at which step of
the program. Then the table itself is the program, unrolled pass by pass
and register by register, and a symbol's letter only needs to hold that
register's current value. Communication is a broadcast bus.

*Mechanism (`busm.py`).* Registers are symbols, read once per pass in a
fixed order. To broadcast bit b, register j appends a blank after itself
at pass s iff b = 1 and at pass s+1 iff b = 0. Either way exactly one
blank is emitted, so the queue length and all later indices are data
independent. In between, every symbol appended after the blank is one
index late: registers after j at pass s+1 and registers up to j at pass
s+2. Each letter carries the parity of its data-independent index (a
tag), so a register reads b as (actual index - tag) mod 2, and the table
entry knows from the index which register and pass it is serving. A
read may carry at most one unknown bit; the scheduler enforces it, and
consecutive broadcasts overlap when emitters do not move left.

*Cost of the model.* One bit per pass on the bus, plus any local update
of every register. Letters are numbered per read over the values the
register can hold there (a reachability pass), so the symbol width B is
2 x the largest such set, rounded up to a multiple of 6.

*Checks.* 60 random bus programs agree with the reference semantics,
and one with the bit-level CTS; a variant that decodes the wrong bit
fails 92 of 240 runs (`tests/test_busm.py`).

## 4. Variable-free Lisp on the bus machine (`lisp_bus.py`)

Fragment: quote, car, cdr, cons, atom?, eq?, cond, t. A value is a block
of token registers (PAD, OPEN, CLOSE, atom); every subexpression owns a
contiguous range nested in its parent's, so operations work in place:
car pads everything outside the first element, cons pads the second
argument's OPEN and fronts a fresh OPEN, cond pads the unselected
branches. Blocks are scanned token by token by a scan register S (two
broadcast bits per token, a small automaton, one answer bit back).

*Honesty of the translation.* The table is built from the expression with
each quoted datum replaced by its size; data registers are given the full
token domain. The data enter only as the CTS tape. A test checks that
different data of equal size give the identical table and different,
correct answers.

*Measured, CTS level* (all equal to `lisp.py`; `tests/test_lisp_bus.py`):

| expression | registers | B | passes | CTS reads | sum of queue over reads |
|---|---|---|---|---|---|
| `(car (quote (a b)))` | 8 | 24 | 22 | 4,512 | 8.7e5 |
| `(cons (quote a) (quote (b)))` | 9 | 24 | 17 | 3,888 | 8.4e5 |
| `(atom? (quote (a)))` | 9 | 24 | 13 | 2,976 | 6.4e5 |
| `(eq? (quote a) (quote b))` | 8 | 42 | 38 | 13,650 | 4.6e6 |
| `(cond ((eq? (quote a) (quote b)) (quote x)) (t (quote y)))` | 13 | 42 | 61 | 34,818 | 1.9e7 |
| `(cdr (car (cdr (quote (a (b c) d)))))` | 12 | 36 | 122 | 55,296 | 2.4e7 |

For comparison, the old tower runs `(car (quote (a b)))` as 85.9M Turing
machine steps on a 7.9M-symbol tag alphabet, ~1e19 generations or more.

## 5. Plan

- [x] `phasem.py`: phase machines = the CTS read by symbols.
- [x] `busm.py`: bus machines compiled into the CTS table.
- [x] `lisp_bus.py`: variable-free Lisp, exact at the CTS level.
- [ ] Run `(car (quote (a b)))` on gliders and read the value out
      (`python experiments.py lisp-gliders "(car (quote (a b)))"`).
- [ ] lambda/define (recursion): needs a heap or substitution with
      copying; the open design question (section 6, to come).

Status log: NOTES.md (phase 10).
