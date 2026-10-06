"""Variable-free Lisp compiled to a bus machine (busm.py), hence to a CTS.

Fragment: quote, car, cdr, cons, atom?, eq?, cond, and the constant t
(no lambda/define yet). Semantics are lisp.py's.

Representation. A value is a block of consecutive registers holding
tokens: PAD (ignored), OPEN, CLOSE, or an atom. Reading the non-PAD tokens
of a block in order gives the value: () is OPEN CLOSE, (a b) is
OPEN a b CLOSE. Every subexpression owns a contiguous range of registers,
nested inside its parent's range, so an operation can work in place: car
turns every token outside the first element into PAD; cons turns the
second argument's OPEN into PAD and puts a fresh OPEN in front. Anything
in a range that is not part of the value is PAD.

Operations scan blocks token by token with a scan register S: each token
says its kind in two broadcast bits, S runs a small automaton and answers
with one bit (keep, or "this is the head atom"). Atom codes travel to two
code registers CA and CB for eq?. Results of atom?/eq? and the () of a
cond without a true clause go into two fresh registers per operation.

Honesty. The bus program (hence the CTS table) is built from the
expression with every quoted datum replaced by its token count; the data
enter only as initial register values (the CTS tape). `program_key` and a
test check that two expressions differing only in data of equal size get
the same table.
"""

from busm import Bcast, Compiled, Local, run_reference
from lisp import parse, run as lisp_run

PAD, OPEN, CLOSE, ATOM = 0, 1, 2, 3
CODE_BITS = 3                       # atoms per program: at most 8, t is code 0
N_ATOMS = 1 << CODE_BITS


def tok_atom(code):
    return ATOM | (code << 2)


TOKENS = {PAD, OPEN, CLOSE} | {ATOM | (c << 2) for c in range(1 << 3)}


def kind(v):
    return v & 3


def code(v):
    return v >> 2


# ---- automata run by the scan register S ---------------------------------
# Each step reads one token kind and gives a 1-bit answer. Steps must be
# total (the table enumerates every state), so malformed input leads to a
# junk state instead of an exception; it only arises in cond branches that
# lisp.py would not evaluate, and those are discarded.

def first_auto(D):
    """car/cdr. answer = 1 iff the token is inside the list's first element."""
    states = ["BEFORE", "START", "AFTER"] + [("IN", d) for d in range(1, D + 1)]

    def step(s, k):
        if k == PAD:
            return s, 0
        if s == "BEFORE":
            return "START", 0                 # the list's own OPEN
        if s == "START":
            if k == OPEN:
                return ("IN", 1), 1
            return "AFTER", int(k == ATOM)
        if s == "AFTER":
            return "AFTER", 0
        d = s[1] + (1 if k == OPEN else -1 if k == CLOSE else 0)
        return (("IN", min(d, D)) if d else "AFTER"), 1
    return states, step, "BEFORE"


def head_auto():
    """Classify a value: ATOM, NIL (= ()), CONS. answer = 1 iff the token is
    the value's atom."""
    states = ["H0", "HOPEN", "ATOM", "NIL", "CONS"]

    def step(s, k):
        if k == PAD or s in ("ATOM", "NIL", "CONS"):
            return s, 0
        if s == "H0":
            return ("ATOM", 1) if k == ATOM else ("HOPEN", 0)
        return ("NIL" if k == CLOSE else "CONS"), 0
    return states, step, "H0"


def firsttok_auto():
    """answer = 1 iff the token is the first non-PAD token."""
    def step(s, k):
        if k == PAD:
            return s, 0
        return "SEEN", int(s == "NONE")
    return ["NONE", "SEEN"], step, "NONE"


def n_tokens(datum):
    if isinstance(datum, str):
        return 1
    return 2 + sum(n_tokens(x) for x in datum)


def size_bound(expr):
    """Upper bound on the token count of any value in the evaluation:
    quoted sizes plus two per operation (cons adds one, atom?/eq?/cond's
    fallback make two)."""
    if isinstance(expr, str):
        return 1
    if expr[0] == "quote":
        return n_tokens(expr[1])
    total = 2
    for a in expr[1:]:
        for e in (a if expr[0] == "cond" else [a]):
            total += size_bound(e)
    return total


class LispBus:
    """Compile one variable-free expression.

    self.ops / self.n / self.V: the bus program (shape-only, see module doc).
    self.values: initial register values (data included).
    self.block: registers holding the result."""

    def __init__(self, src):
        forms = parse(src)
        if len(forms) != 1:
            raise ValueError("one expression expected")
        self.expr = forms[0]
        self.atoms = {"t": 0}
        self.D = max(1, size_bound(self.expr) // 2)
        self.autos = {"first": first_auto(self.D), "head": head_auto(),
                      "firsttok": firsttok_auto()}
        self.S_states = [(name, st) for name, (sts, _, _) in
                         self.autos.items() for st in sts]
        self.S_index = {x: i for i, x in enumerate(self.S_states)}
        self.values, self.ops, self.data_regs = [], [], set()
        self.S, self.CA, self.CB, self.T = (self.reg(0) for _ in range(4))
        self.block = self.compile(self.expr)
        self.n = len(self.values)
        self.V = max(4 * len(self.S_states), 4 * N_ATOMS, C_EQ + 2 * C_VALUES)

    def reg(self, init):
        self.values.append(init)
        return len(self.values) - 1

    def data_reg(self, token):
        """A register whose initial value is quoted data (tape content)."""
        r = self.reg(token)
        self.data_regs.add(r)
        return r

    def atom_code(self, a):
        if a not in self.atoms:
            if len(self.atoms) == N_ATOMS:
                raise ValueError(f"more than {N_ATOMS} atoms")
            self.atoms[a] = len(self.atoms)
        return self.atoms[a]

    # ---- S: value = 4 * state index + aux; aux 0/1 = answer, 2/3 = got bit0
    def s_val(self, name, st, aux=0):
        return 4 * self.S_index[(name, st)] + aux

    def s_dec(self, v):
        i, aux = divmod(v, 4)
        if i >= len(self.S_states):
            return None, None, aux
        return self.S_states[i] + (aux,)

    def _s_bit0(self, v, b):
        name, st, aux = self.s_dec(v)
        return v if name is None else self.s_val(name, st, 2 + b)

    def _s_bit1(self, v, b):
        name, st, aux = self.s_dec(v)
        if name is None or aux < 2:
            return v
        st2, ans = self.autos[name][1](st, (aux - 2) | (b << 1))
        return self.s_val(name, st2, ans)

    def scan(self, blk, name, answer_to=None, after_token=None):
        """Run automaton `name` over blk's tokens. After each token r, if
        answer_to(r) is nonempty, S broadcasts its answer to those
        receivers; after_token(r) may append more ops."""
        start = self.s_val(name, self.autos[name][2])
        self.ops.append(Local({self.S: lambda v, start=start: start}))
        for r in blk:
            self.ops.append(Bcast(r, lambda v: kind(v) & 1, {self.S: self._s_bit0}))
            self.ops.append(Bcast(r, lambda v: kind(v) >> 1, {self.S: self._s_bit1}))
            recv = answer_to(r) if answer_to else {}
            if recv:
                self.ops.append(Bcast(self.S, lambda v: v & 1, recv))
            if after_token:
                after_token(r)

    def s_state_bit(self, pred):
        """emit fn: 1 iff S's state satisfies pred."""
        def emit(v):
            name, st, _ = self.s_dec(v)
            return int(name is not None and pred(st))
        return emit

    # ---- compilation ----
    def compile(self, e):
        if e == "t":
            return [self.reg(tok_atom(0))]
        if isinstance(e, str) or not e:
            raise ValueError(f"not in the fragment: {e!r}")
        op, args = e[0], e[1:]
        if op == "quote":
            return [self.data_reg(t) for t in self.tokens(args[0])]
        if op in ("car", "cdr"):
            (x,) = args
            blk = self.compile(x)
            if op == "car":
                keep = lambda v, a: v if a else PAD
            else:
                keep = lambda v, a: PAD if a else v
            self.scan(blk, "first", lambda r: {r: keep})
            return blk
        if op == "cons":
            x, y = args
            o = self.reg(OPEN)
            bx, by = self.compile(x), self.compile(y)
            self.scan(by, "firsttok",
                      lambda r: {r: lambda v, a: PAD if a else v})
            return [o] + bx + by
        if op == "atom?":
            (x,) = args
            bx = self.compile(x)
            r0, r1 = self.reg(PAD), self.reg(PAD)
            self.scan(bx, "head")
            self.write_bool(self.s_state_bit(lambda st: st in ("ATOM", "NIL")),
                            self.S, r0, r1)
            self.ops.append(Local({r: _const(PAD) for r in bx}))
            return bx + [r0, r1]
        if op == "eq?":
            x, y = args
            bx, by = self.compile(x), self.compile(y)
            r0, r1 = self.reg(PAD), self.reg(PAD)
            self.classify_into(bx, self.CA)
            self.classify_into(by, self.CB)
            self.compare(r0, r1)
            self.ops.append(Local({r: _const(PAD) for r in bx + by}))
            return bx + by + [r0, r1]
        if op == "cond":
            return self.cond(args)
        raise ValueError(f"not in the fragment: {op!r}")

    def tokens(self, datum):
        if isinstance(datum, str):
            return [tok_atom(self.atom_code(datum))]
        out = [OPEN]
        for x in datum:
            out += self.tokens(x)
        return out + [CLOSE]

    def write_bool(self, emit, src, r0, r1):
        """src broadcasts emit(v); r0 r1 become t (atom, PAD) or () ."""
        self.ops.append(Bcast(src, emit, {
            r0: lambda v, x: tok_atom(0) if x else OPEN,
            r1: lambda v, x: PAD if x else CLOSE}))

    def classify_into(self, blk, C):
        """C := atom code of blk's value, or C_NIL / C_CONS."""
        self.ops.append(Local({C: _const(C_UNSET)}))

        def after(r):
            for i in range(CODE_BITS):
                self.ops.append(Bcast(r, lambda v, i=i: (code(v) >> i) & 1,
                                      {C: lambda v, b, i=i: _c_bit(v, b, i)}))
            self.ops.append(Local({C: _c_close}))
        self.scan(blk, "head", lambda r: {C: _c_listen}, after)
        self.ops.append(Bcast(self.S, self.s_state_bit(lambda st: st == "NIL"),
                              {C: lambda v, b: C_NIL if b else v}))
        self.ops.append(Bcast(self.S, self.s_state_bit(lambda st: st == "CONS"),
                              {C: lambda v, b: C_CONS if b else v}))

    def compare(self, r0, r1):
        """r0 r1 := t if CA == CB and both are atoms (or nil), else ()."""
        CB = self.CB
        self.ops.append(Local({CB: lambda v: C_EQ + 2 * v + 1
                               if v < C_VALUES else v}))
        for i in range(C_VALUE_BITS):
            self.ops.append(Bcast(self.CA, lambda v, i=i: (v >> i) & 1,
                                  {CB: lambda v, b, i=i: _eq_bit(v, b, i)}))

        def answer(v):
            if v < C_EQ:
                return 0
            x, flag = divmod(v - C_EQ, 2)
            return int(flag and x != C_CONS)
        self.write_bool(answer, CB, r0, r1)

    def cond(self, clauses):
        T = self.T
        blocks = []
        self.ops.append(Local({T: _const(0)}))    # T = 2 * taken + truth
        for clause in clauses:
            if len(clause) != 2:
                raise ValueError("cond clause must be (test expr)")
            bp = self.compile(clause[0])
            be = self.compile(clause[1])
            blocks += bp + be
            self.scan(bp, "head")
            self.ops.append(Bcast(self.S,
                                  self.s_state_bit(lambda st: st != "NIL"),
                                  {T: lambda v, b: (v & 2) | b}))
            self.ops.append(Bcast(T, lambda v: int(v == 1),
                                  {r: lambda v, s: v if s else PAD for r in be}))
            self.ops.append(Local({T: lambda v: 2 if v else 0}))
            self.ops.append(Local({r: _const(PAD) for r in bp}))
        r0, r1 = self.reg(PAD), self.reg(PAD)
        self.ops.append(Bcast(T, lambda v: int(v == 0), {
            r0: lambda v, x: OPEN if x else PAD,
            r1: lambda v, x: CLOSE if x else PAD}))
        return blocks + [r0, r1]

    # ---- running ----
    def decode(self, values):
        toks = [values[r] for r in self.block if values[r] != PAD]
        names = {c: a for a, c in self.atoms.items()}
        pos = 0

        def read():
            nonlocal pos
            t = toks[pos]
            pos += 1
            if kind(t) == ATOM:
                return names[code(t)]
            if t != OPEN:
                raise ValueError(f"bad token stream {toks}")
            out = []
            while toks[pos] != CLOSE:
                out.append(read())
            pos += 1
            return out
        val = read()
        if pos != len(toks):
            raise ValueError(f"trailing tokens in {toks}")
        return val

    def run_reference(self):
        return self.decode(run_reference(self.ops, self.values, self.V))

    def domains(self):
        """Possible initial values per register: any token for quoted data
        (so the table cannot depend on the data), the constant otherwise."""
        return [TOKENS if r in self.data_regs else {v}
                for r, v in enumerate(self.values)]

    def compile_bus(self):
        return Compiled(self.n, self.V, self.ops, self.domains())


def _const(c):
    return lambda v: c


# ---- code registers CA, CB ------------------------------------------------
C_NIL, C_CONS = N_ATOMS, N_ATOMS + 1
C_VALUES = N_ATOMS + 2                     # atom codes, NIL, CONS
C_VALUE_BITS = (C_VALUES - 1).bit_length()
C_UNSET = C_VALUES
C_LISTEN = C_VALUES + 1                    # + partial code: listening
C_EQ = C_LISTEN + N_ATOMS                  # + 2 * value + equal-so-far


def _c_listen(v, a):
    return C_LISTEN if a else v


def _c_bit(v, b, i):
    if C_LISTEN <= v < C_LISTEN + N_ATOMS:
        return C_LISTEN + ((v - C_LISTEN) | (b << i))
    return v


def _c_close(v):
    if C_LISTEN <= v < C_LISTEN + N_ATOMS:
        return v - C_LISTEN
    return v


def _eq_bit(v, b, i):
    if v < C_EQ:
        return v
    x, flag = divmod(v - C_EQ, 2)
    return C_EQ + 2 * x + int(flag and ((x >> i) & 1) == b)
