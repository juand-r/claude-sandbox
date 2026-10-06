"""Bus machines: a bit-serial register machine compiled into a phase machine.

Model (INTERPRETER.md section 3). There are n registers, each holding a
value in range(V). A program is a list of ops, executed in order:

  Local(upd)                       every register k in upd: v := upd[k](v)
  Bcast(j, emit, recv)             b := emit(value of register j);
                                   every k in recv: v := recv[k](v, b)

That is all a register can do: change its own value, and hear one bit that
one other register says. The point of the model is that it compiles to a
CTS whose schedule does not depend on the data, so the CTS table can hold
the whole program, register by register and pass by pass.

Compilation. Each register is one phase-machine symbol, letter 2*v + t,
where t is a parity tag (below). One pass reads every register once, in
order 0..n-1. A broadcast by register j at pass s:
  - pass s:   j appends a blank after itself iff b = 1;
  - pass s+1: j appends a blank after itself iff b = 0.
So exactly one blank is emitted either way, and the queue length and every
later index are data independent. In between, the blank shifts by one the
absolute index (hence the phase) of every symbol appended after it:
register k > j is read one index late at pass s+1 iff b = 1, and register
k <= j likewise at pass s+2 (INTERPRETER.md derives this). The tag holds
the parity of the data-independent ("nominal") index, so at a delivery
read the register sees b = (actual index - tag) mod 2, and the table entry
knows from the phase which register and pass it is serving.

A read may carry at most one unknown bit; the scheduler places each
broadcast at the earliest pass where this holds and where the emitter has
received every earlier op.
"""

from dataclasses import dataclass, field
from typing import Callable

from phasem import BLANK, PhaseMachine


@dataclass
class Local:
    upd: dict                      # k -> fn(v) -> v


@dataclass
class Bcast:
    j: int
    emit: Callable                 # fn(v) -> 0/1
    recv: dict = field(default_factory=dict)   # k -> fn(v, b) -> v


def run_reference(ops, values, V):
    """Sequential semantics. Returns the final values."""
    vals = list(values)
    for op in ops:
        if isinstance(op, Local):
            for k, f in op.upd.items():
                vals[k] = _check(f(vals[k]), V)
        else:
            b = op.emit(vals[op.j])
            if b not in (0, 1):
                raise ValueError(f"emit returned {b!r}")
            for k, f in op.recv.items():
                if k == op.j:
                    raise ValueError("an emitter cannot receive its own bit")
                vals[k] = _check(f(vals[k], b), V)
    return vals


def _check(v, V):
    if not (isinstance(v, int) and 0 <= v < V):
        raise ValueError(f"value {v!r} outside range({V})")
    return v


class Compiled:
    """A bus program compiled to a phase machine.

    Attributes: pm (PhaseMachine), tape (initial letters), reads (symbol
    reads that complete the program), n, V, passes."""

    def __init__(self, n, V, ops, domains=None, keep=None, start=None):
        """domains: per register, the set of possible initial values
        (default: all of range(V)). Letters are numbered per read over the
        values reachable there, which keeps the symbol width B small.

        keep / start (both or neither): register lifetimes. Without them
        every register is in the queue for the whole program. With them a
        register is in the queue only from its first action (from pass 0
        if it is in `start`, i.e. its initial value comes with the tape) to
        its last (to the end if it is in `keep`, i.e. part of the result).
        Its live predecessor in register order writes it into the queue
        with its constant initial value, and it leaves by turning into a
        blank. Both are fixed by the program, so the schedule stays data
        independent; register 0 must stay live to anchor births."""
        self.n, self.V, self.ops = n, V, ops
        self.init_domains = [set(range(V)) if domains is None else
                             set(domains[k]) for k in range(n)]
        if (keep is None) != (start is None):
            raise ValueError("give both keep and start, or neither")
        self.keep, self.start = keep, start
        self._schedule()
        self._lifetimes()
        self._build()

    # ---- scheduling -------------------------------------------------------
    def _schedule(self):
        """Assign each op a pass. Per register, a list of (pass, action)
        where action is ('local', f) or ('recv', i, f) for broadcast i."""
        n = self.n
        ready = [0] * n            # first pass at which reg k is up to date
        self.bcasts = []           # (s, j, emit) per broadcast index
        self.actions = {}          # (s, k) -> list of actions
        unknown = {}               # (s, k) -> broadcast index delivered
        last_s = 0                 # ops are kept in order
        for op in self.ops:
            if isinstance(op, Local):
                for k, f in op.upd.items():
                    s = max(ready[k], last_s)
                    self.actions.setdefault((s, k), []).append(("local", f))
                    ready[k] = s
                continue
            j = op.j
            s = max(ready[j], last_s)
            while True:
                deliv = {k: (s + 1 if k > j else s + 2) for k in op.recv}
                # every read in the window that gets the unknown bit
                window = [(s + 1, k) for k in range(j + 1, n)] + \
                         [(s + 2, k) for k in range(0, j + 1)]
                ok = all(r not in unknown for r in window)
                ok = ok and all(deliv[k] >= ready[k] for k in op.recv)
                if ok:
                    break
                s += 1
            i = len(self.bcasts)
            self.bcasts.append((s, j, op.emit))
            for r in window:
                unknown[r] = i
            self.actions.setdefault((s, j), []).append(("emit", i))
            self.actions.setdefault((s + 1, j), []).append(("comp", i))
            for k, f in op.recv.items():
                self.actions.setdefault((deliv[k], k), []).append(
                    ("recv", i, f))
                ready[k] = deliv[k]
            # later ops on j go to s+1 or later: the compensation at s+1
            # reads j's letter, which must still give emit's bit. A new
            # broadcast by j at s+1 is fine: its window starts where this
            # one's ends (the scheduler's window check)
            ready[j] = max(ready[j], s + 1)
            last_s = s
        self.unknown = unknown
        end = max([s + 3 for s, _, _ in self.bcasts] + [s + 1 for s, _ in
                  self.actions] + [1])
        self.passes = end

    # ---- lifetimes ----------------------------------------------------------
    def _lifetimes(self):
        n, P = self.n, self.passes
        if self.keep is None:
            self.first, self.last = [0] * n, [P] * n
        else:
            acts = {}
            for (s, k) in self.actions:
                acts.setdefault(k, []).append(s)
            self.first, self.last = [None] * n, [None] * n
            for k in range(n):
                a = acts.get(k)
                if k == 0:
                    self.first[k], self.last[k] = 0, P
                    continue
                if a is None and k not in self.start and k not in self.keep:
                    continue                      # never needed
                self.first[k] = 0 if k in self.start else min(a or [P])
                self.last[k] = P if k in self.keep else max(a or [0])
                if self.first[k] > 0 and len(self.init_domains[k]) != 1:
                    raise ValueError(f"register {k} is born at pass "
                                     f"{self.first[k]} but has no constant "
                                     f"initial value")
        self.live = [[k for k in range(n) if self.first[k] is not None
                      and self.first[k] <= s <= self.last[k]]
                     for s in range(P + 1)]
        # newborns at pass s, grouped by their creator (live at s-1)
        self.births = {}
        for s in range(1, P + 1):
            prev = self.live[s - 1]
            for k in self.live[s]:
                if self.first[k] == s:
                    c = max((j for j in prev if j < k), default=None)
                    if c is None:
                        raise ValueError(f"register {k} has no live "
                                         f"predecessor at pass {s - 1}")
                    self.births.setdefault((s - 1, c), []).append(k)

    # ---- nominal stream ---------------------------------------------------
    def _build(self):
        """Nominal (all bits 0) index of every register read, and the rules."""
        n, P = self.n, self.passes
        comp_at = {(s + 1, j) for s, j, _ in self.bcasts}   # b = 0 blank
        nominal = {}
        idx = 0
        for k in self.live[0]:
            nominal[(0, k)] = idx
            idx += 1
        for s in range(1, P + 1):
            for j in self.live[s - 1]:     # Q_s = outputs of pass s-1, in order
                if j in self.live[s]:
                    nominal[(s, j)] = idx
                idx += 1                   # j's letter, or its death blank
                idx += (s - 1, j) in comp_at
                for k in self.births.get((s - 1, j), []):
                    nominal[(s, k)] = idx
                    idx += 1
        # One table period is exactly the program (up to the first read of
        # pass P). Running past it fails loudly.
        self.p, self.nominal = nominal[(P, self.live[P][0])], nominal

        # values reachable at each read, and their letter numbering
        dom = {}
        for s in range(P + 1):
            for k in self.live[s]:
                if s == self.first[k]:
                    dom[(s, k)] = set(self.init_domains[k])
                else:
                    us = (0, 1) if (s - 1, k) in self.unknown else (0,)
                    dom[(s, k)] = {self._step(s - 1, k, v, u)[0]
                                   for v in dom[(s - 1, k)] for u in us}
        self.enc = {r: {v: i for i, v in enumerate(sorted(d))}
                    for r, d in dom.items()}
        width = max(len(d) for d in dom.values())
        B = 2 * width + (-2 * width) % 6
        rules = {}
        for s in range(P):
            for k in self.live[s]:
                N = nominal[(s, k)]
                us = (0, 1) if (s, k) in self.unknown else (0,)
                born = tuple(self._letter(s + 1, kb, next(iter(self.init_domains[kb])))
                             for kb in self.births.get((s, k), []))
                for u in us:
                    for v in dom[(s, k)]:
                        letter = self._letter(s, k, v)
                        v2, blank = self._step(s, k, v, u)
                        own = (self._letter(s + 1, k, v2),) \
                            if k in self.live[s + 1] else (BLANK,)
                        word = own + (BLANK,) * blank + born
                        key = ((N + u) % self.p, letter)
                        if key in rules and rules[key] != word:
                            raise AssertionError(f"rule clash at {key}")
                        rules[key] = word
        self.pm = PhaseMachine(B, self.p, rules)

    def _letter(self, s, k, v):
        return 2 * self.enc[(s, k)][v] + self.nominal[(s, k)] % 2

    def _step(self, s, k, v, u):
        """Register k read at pass s with value v and unknown bit u (the
        broadcast bit, if this read delivers one) -> (new value, blanks)."""
        acts = self.actions.get((s, k), [])
        blank = 0
        v_letter = v
        for a in acts:                       # compensation uses the letter
            if a[0] == "comp":
                _, j, emit = self.bcasts[a[1]]
                blank += 1 - _bit(emit(v_letter))
        for a in acts:
            if a[0] == "local":
                v = _check(a[1](v), self.V)
            elif a[0] == "recv":
                if (s, k) not in self.unknown or self.unknown[(s, k)] != a[1]:
                    raise AssertionError("delivery without its bit")
                v = _check(a[2](v, u), self.V)
            elif a[0] == "emit":
                _, _, emit = self.bcasts[a[1]]
                blank += _bit(emit(v))
        return v, blank

    # ---- running ----------------------------------------------------------
    def initial_tape(self, values):
        for k, v in enumerate(values):
            if k in self.live[0] and v not in self.init_domains[k]:
                raise ValueError(f"register {k}: {v} outside its domain")
        return [self._letter(0, k, values[k]) for k in self.live[0]]

    def run(self, values):
        """Run the compiled phase machine through all passes; return the
        final register values (None for registers not live at the end).
        Every broadcast has finished by then, so the actual stream length
        equals the nominal one, self.p."""
        q, reads = self.pm.run(self.initial_tape(values), self.p)
        if reads != self.p:
            raise AssertionError(f"queue emptied after {reads} reads")
        out = [c for c, _ in q if c != BLANK]
        return self.decode_letters(out)    # checks the register count

    def decode_letters(self, letters):
        """Final letters (one per live register, blanks removed) -> list of
        values, None for registers not live at the end."""
        final = self.live[self.passes]
        if len(letters) != len(final):
            raise AssertionError(f"{len(letters)} letters for {len(final)} registers")
        vals = [None] * self.n
        for k, c in zip(final, letters):
            dec = {i: v for v, i in self.enc[(self.passes, k)].items()}
            vals[k] = dec[c // 2]
        return vals


def _bit(b):
    if b not in (0, 1):
        raise ValueError(f"emit returned {b!r}")
    return b
