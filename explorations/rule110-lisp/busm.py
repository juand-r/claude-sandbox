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

    def __init__(self, n, V, ops):
        self.n, self.V, self.ops = n, V, ops
        self._schedule()
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
            ready[j] = max(ready[j], s + 2)    # emitter busy through s+1
            last_s = s
        self.unknown = unknown
        end = max([s + 3 for s, _, _ in self.bcasts] + [s + 1 for s, _ in
                  self.actions] + [1])
        self.passes = end

    # ---- nominal stream ---------------------------------------------------
    def _build(self):
        """Nominal (all bits 0) index of every register read, and the rules."""
        n, P = self.n, self.passes
        nominal = {}
        idx = 0
        blanks_after = {}          # pass -> set of j with a nominal blank
        for s, j, _ in self.bcasts:
            blanks_after.setdefault(s + 1, set()).add(j)   # b = 0: comp blank
        for s in range(P):
            prev = blanks_after.get(s - 1, set())   # blanks emitted at s-1
            for k in range(n):
                nominal[(s, k)] = idx
                idx += 1
                if k in prev:
                    idx += 1       # the blank appended after k at pass s-1
        # One table period is exactly the program. Running past the end
        # fails loudly (tags of pass P need not match pass 0's).
        p = idx
        for k in range(n):
            nominal[(P, k)] = p + k
        self.p, self.nominal = p, nominal

        V = self.V
        B = 2 * V + (-2 * V) % 6
        rules = {}
        for s in range(P):
            for k in range(n):
                N = nominal[(s, k)]
                us = (0, 1) if (s, k) in self.unknown else (0,)
                for u in us:
                    for v in range(V):
                        letter = 2 * v + (N % 2)
                        word = self._read(s, k, v, u)
                        key = ((N + u) % p, letter)
                        if key in rules and rules[key] != word:
                            raise AssertionError(f"rule clash at {key}")
                        rules[key] = word
        self.pm = PhaseMachine(B, p, rules)

    def _read(self, s, k, v, u):
        """Output word of register k read at pass s with value v and
        unknown bit u (the broadcast bit, if this read delivers one)."""
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
        t = self.nominal[(s + 1, k)] % 2
        return (2 * v + t,) + (BLANK,) * blank

    # ---- running ----------------------------------------------------------
    def initial_tape(self, values):
        return [2 * _check(v, self.V) + (self.nominal[(0, k)] % 2)
                for k, v in enumerate(values)]

    def run(self, values):
        """Run the compiled phase machine through all passes; return the
        final register values. Every broadcast has finished by then, so the
        actual stream length equals the nominal one, self.p."""
        q, reads = self.pm.run(self.initial_tape(values), self.p)
        if reads != self.p:
            raise AssertionError(f"queue emptied after {reads} reads")
        out = [c for c, _ in q if c != BLANK]
        if len(out) != self.n or len(q) != self.n:
            raise AssertionError(f"queue {list(q)} is not {self.n} registers")
        return [c // 2 for c in out]


def _bit(b):
    if b not in (0, 1):
        raise ValueError(f"emit returned {b!r}")
    return b
