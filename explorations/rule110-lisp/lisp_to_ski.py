"""Layer 3: mini-Lisp -> SKI compiler.

Pipeline: Lisp AST -> lambda calculus IR -> bracket abstraction -> SKI
string (backtick notation, ski.py).

Value encoding (all Church-style, normal order):
    value       = PAIR tag payload      (PAIR x y f = f x y)
    tag         = Church numeral: 0 atom, 1 cons, 2 nil
    atom payload= Church numeral symbol id (from a compile-time table)
    cons payload= PAIR car cdr
Booleans inside the machinery are Church booleans; Lisp-level truth is
LIFTed to the atom t / nil. cond compiles to nested Church-boolean
application, which under normal order is lazy, matching Lisp's cond.
eq? is Church-numeral equality on atom ids (atoms and nil only; conses
compare unequal). Recursion (define) uses the Y combinator; a define may
reference itself and earlier defines only. NOTE: argument evaluation is
lazy here vs strict in lisp.py -- results agree for terminating programs.

Decoding a result value back to Lisp data is decode_value(), which probes
the normalized term with K / K I selectors.
"""

import ski

# ---------------------------------------------------------------- lambda IR

class V:
    def __init__(self, name): self.name = name
class L:
    def __init__(self, var, body): self.var, self.body = var, body
class A:
    def __init__(self, f, x): self.f, self.x = f, x
class Raw:                       # literal SKI string (S, K, I or bigger)
    def __init__(self, s): self.s = s


def parse_lambda(src, env):
    """Tiny lambda parser: ^x.body, application by juxtaposition,
    parentheses, names (alnum, longest match) resolved via env (dict
    name -> IR) or as bound variables."""
    toks = []
    i = 0
    while i < len(src):
        c = src[i]
        if c.isspace(): i += 1; continue
        if c in "^.()":
            toks.append(c); i += 1; continue
        j = i
        while j < len(src) and (src[j].isalnum() or src[j] == "_"):
            j += 1
        if i == j:
            raise SyntaxError(f"bad char {c!r}")
        toks.append(src[i:j]); i = j
    pos = 0
    def atom(bound):
        nonlocal pos
        t = toks[pos]
        if t == "(":
            pos += 1
            e = expr(bound)
            assert toks[pos] == ")"
            pos += 1
            return e
        if t == "^":
            pos += 1
            var = toks[pos]; pos += 1
            assert toks[pos] == "."; pos += 1
            return L(var, expr(bound | {var}))
        pos += 1
        if t in bound:
            return V(t)
        if t in env:
            return env[t]
        raise NameError(f"unknown name {t}")
    def expr(bound):
        nonlocal pos
        e = atom(bound)
        while pos < len(toks) and toks[pos] not in (")",):
            e = A(e, atom(bound))
        return e
    e = expr(set())
    assert pos == len(toks)
    return e


def free_in(x, e):
    if isinstance(e, V): return e.name == x
    if isinstance(e, L): return e.var != x and free_in(x, e.body)
    if isinstance(e, A): return free_in(x, e.f) or free_in(x, e.x)
    return False


def _abstract(x, e):
    """[x] e for lambda-free e, with K/I/eta optimizations. Returns IR."""
    if isinstance(e, V) and e.name == x:
        return Raw("I")
    if not free_in(x, e):
        return A(Raw("K"), e)
    # e is an application containing x
    if isinstance(e.x, V) and e.x.name == x and not free_in(x, e.f):
        return e.f                # eta
    return A(A(Raw("S"), _abstract(x, e.f)), _abstract(x, e.x))


def _eliminate(e):
    """Remove all lambdas bottom-up. Returns lambda-free IR."""
    if isinstance(e, (V, Raw)):
        return e
    if isinstance(e, A):
        return A(_eliminate(e.f), _eliminate(e.x))
    return _abstract(e.var, _eliminate(e.body))


def to_ski(e):
    """Closed IR -> SKI string (backtick notation)."""
    def render(e):
        if isinstance(e, Raw):
            return e.s
        if isinstance(e, V):
            raise NameError(f"unbound {e.name}")
        return "`" + render(e.f) + render(e.x)
    return render(_eliminate(e))


# ------------------------------------------------- combinator library

def church(n):
    """Church numeral as an IR term."""
    body = V("x")
    for _ in range(n):
        body = A(V("f"), body)
    return L("f", L("x", body))


def build_env():
    env = {"S": Raw("S"), "K": Raw("K"), "I": Raw("I")}
    def defn(name, src):
        env[name] = Raw(to_ski(parse_lambda(src, env)))
    defn("TRUE", "^x.^y.x")
    defn("FALSE", "^x.^y.y")
    defn("PAIR", "^x.^y.^f.f x y")
    defn("NOT", "^b.^x.^y.b y x")
    defn("AND", "^p.^q.p q FALSE")
    defn("OR", "^p.^q.p TRUE q")
    env["N0"] = Raw(to_ski(church(0)))
    env["N1"] = Raw(to_ski(church(1)))
    env["N2"] = Raw(to_ski(church(2)))
    defn("SUCC", "^n.^f.^x.f (n f x)")
    defn("ISZERO", "^n.n (^z.FALSE) TRUE")
    defn("PRED", "^n.^f.^x.n (^g.^h.h (g f)) (^u.x) (^u.u)")
    defn("SUB", "^m.^n.n PRED m")
    defn("LEQ", "^m.^n.ISZERO (SUB m n)")
    defn("EQN", "^m.^n.AND (LEQ m n) (LEQ n m)")
    defn("Y", "^f.(^x.f (x x)) (^x.f (x x))")
    defn("TAG", "^v.v TRUE")
    defn("PAYLOAD", "^v.v FALSE")
    defn("VNIL", "PAIR N2 N0")
    defn("VCONS", "^h.^t.PAIR N1 (PAIR h t)")
    defn("VATOM", "^i.PAIR N0 i")
    defn("CAR", "^v.PAYLOAD v TRUE")
    defn("CDR", "^v.PAYLOAD v FALSE")
    defn("TRUTHY", "^v.NOT (EQN (TAG v) N2)")
    return env


# ------------------------------------------------------------- compiler

PRIMS = ("car", "cdr", "cons", "atom?", "eq?")


class Compiler:
    def __init__(self):
        self.env = build_env()
        self.symtab = {"t": 0}

    def sym_id(self, s):
        if s not in self.symtab:
            self.symtab[s] = len(self.symtab)
        return self.symtab[s]

    def lam(self, src):
        return parse_lambda(src, self.env)

    def quote(self, x):
        if isinstance(x, str):
            return A(self.env["VATOM"], church(self.sym_id(x)))
        out = self.env["VNIL"]
        for item in reversed(x):
            out = A(A(self.env["VCONS"], self.quote(item)), out)
        return out

    def compile_expr(self, e, bound, defs):
        env = self.env
        if isinstance(e, str):
            if e in bound:
                return V(e)
            if e in defs:
                return defs[e]
            if e == "t":
                return self.quote("t")
            raise NameError(f"unbound {e}")
        head = e[0] if e else None
        if head == "quote":
            return self.quote(e[1])
        if head == "lambda":
            _, params, body = e
            out = self.compile_expr(body, bound | set(params), defs)
            for p in reversed(params):
                out = L(p, out)
            return out
        if head == "cond":
            out = env["VNIL"]
            for test, body in reversed(e[1:]):
                tv = self.compile_expr(test, bound, defs)
                bv = self.compile_expr(body, bound, defs)
                out = A(A(A(env["TRUTHY"], tv), bv), out)
            return out
        # application, possibly of a primitive
        if head == "car":
            return A(env["CAR"], self.compile_expr(e[1], bound, defs))
        if head == "cdr":
            return A(env["CDR"], self.compile_expr(e[1], bound, defs))
        if head == "cons":
            return A(A(env["VCONS"], self.compile_expr(e[1], bound, defs)),
                     self.compile_expr(e[2], bound, defs))
        if head == "atom?":
            v = self.compile_expr(e[1], bound, defs)
            b = A(A(env["EQN"], A(env["TAG"], v)), env["N0"])
            return self.lift(b)
        if head == "eq?":
            a = self.compile_expr(e[1], bound, defs)
            b = self.compile_expr(e[2], bound, defs)
            return self.eqp(a, b)
        f = self.compile_expr(head, bound, defs)
        for arg in e[1:]:
            f = A(f, self.compile_expr(arg, bound, defs))
        return f

    def lift(self, church_bool):
        env = self.env
        return A(A(church_bool, self.quote("t")), env["VNIL"])

    def eqp(self, a, b):
        env = self.env
        ir = parse_lambda(
            "^a.^b.(AND (EQN (TAG a) (TAG b))"
            " (OR (EQN (TAG a) N2)"
            " (AND (EQN (TAG a) N0) (EQN (PAYLOAD a) (PAYLOAD b)))))",
            env)
        return self.lift(A(A(ir, a), b))

    def compile_program(self, forms):
        """-> SKI string of the last top-level expression."""
        defs = {}
        last = None
        for form in forms:
            if isinstance(form, list) and form and form[0] == "define":
                if isinstance(form[1], list):
                    name, params = form[1][0], form[1][1:]
                    body = form[2]
                    inner = self.compile_expr(body, set(params), 
                                              {**defs, name: V(name)})
                    for p in reversed(params):
                        inner = L(p, inner)
                    defs[name] = A(self.env["Y"], L(name, inner))
                else:
                    defs[form[1]] = self.compile_expr(form[2], set(), defs)
            else:
                last = self.compile_expr(form, set(), defs)
        return to_ski(last)


# ------------------------------------------------------------- decoding

def _count_apps(term, f="f", x="x"):
    """Church numeral in normal form applied to f,x -> int."""
    n = 0
    while term.startswith("`" + f):
        term = term[2:]
        n += 1
    if term != x:
        raise ValueError(f"not a numeral: {term!r}")
    return n


def decode_value(term, symtab, max_steps=2_000_000):
    """Normalize probes of a value term -> Lisp data (strings/lists)."""
    inv = {v: k for k, v in symtab.items()}
    def probe(t):
        return ski.normalize(t, max_steps)
    tag = _count_apps(probe("``" + "`" + term + "K" + "fx"))
    if tag == 2:
        return []
    payload = "`" + term + "`KI"       # v FALSE
    if tag == 0:
        return inv[_count_apps(probe("``" + payload + "fx"))]
    if tag == 1:
        car = "``" + payload + "K" + ""
        cdr = "``" + payload + "`KI"
        # payload is PAIR car cdr: payload K = car? PAIR x y f = f x y:
        # payload TRUE = car, payload FALSE = cdr
        h = decode_value("`" + payload + "K", symtab, max_steps)
        t = decode_value("`" + payload + "`KI", symtab, max_steps)
        return [h] + t
    raise ValueError(f"bad tag {tag}")


def compile_and_run(src, max_steps=2_000_000):
    from lisp import parse
    c = Compiler()
    term = c.compile_program(parse(src))
    return decode_value(term, c.symtab, max_steps)
