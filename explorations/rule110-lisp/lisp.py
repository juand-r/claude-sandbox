"""Layer 3: mini-Lisp -- specification and reference interpreter.

Scope (Malbolge-Lisp-like, pure):
  - atoms (symbols), lists
  - special forms: quote, cond, lambda, define
  - primitives: car, cdr, cons, atom?, eq?
  - truth: the atom t is true, the empty list () is false
  - recursion via define; lexical closures via lambda

Primitive semantics follow McCarthy's LISP 1.5:
  - atom? is true for symbols and for nil (), false for conses.
  - eq? is true only when both arguments are the same atom (nil counts as
    an atom); two conses are never eq?, even if structurally equal.
  - atom? and eq? applied to functions are undefined (the compiled
    encoding gives no meaningful answer), as is car/cdr of an atom.

No numbers, strings, or side effects: numbers can be built as lists.
This reference interpreter defines the semantics that the lower layers
must reproduce.
"""


def is_atom(x):
    """Symbols and nil are atoms; conses (non-empty lists) are not."""
    return isinstance(x, str) or x == []


class Closure:
    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env


def parse(src):
    """S-expression source -> nested Python lists/strings."""
    tokens = src.replace("(", " ( ").replace(")", " ) ").split()
    pos = 0

    def read():
        nonlocal pos
        if pos >= len(tokens):
            raise SyntaxError("unexpected end of input")
        tok = tokens[pos]
        pos += 1
        if tok == "(":
            out = []
            while tokens[pos] != ")":
                out.append(read())
            pos += 1
            return out
        if tok == ")":
            raise SyntaxError("unexpected )")
        return tok

    out = []
    while pos < len(tokens):
        out.append(read())
    return out


def evaluate(expr, env):
    while True:   # tail-call loop
        if isinstance(expr, str):
            for frame in env:
                if expr in frame:
                    return frame[expr]
            raise NameError(f"unbound symbol {expr!r}")
        if not isinstance(expr, list) or not expr:
            raise ValueError(f"cannot evaluate {expr!r}")
        head = expr[0]
        if head == "quote":
            (_, x) = expr
            return x
        if head == "cond":
            for clause in expr[1:]:
                test, body = clause
                if evaluate(test, env) != []:
                    expr = body
                    break
            else:
                return []
            continue
        if head == "lambda":
            (_, params, body) = expr
            return Closure(params, body, env)
        if head == "define":
            raise ValueError("define only allowed at top level")
        f = evaluate(head, env)
        args = [evaluate(a, env) for a in expr[1:]]
        if f == "car":
            return args[0][0]
        if f == "cdr":
            return args[0][1:]
        if f == "cons":
            return [args[0]] + args[1]
        if f == "atom?":
            return "t" if is_atom(args[0]) else []
        if f == "eq?":
            a, b = args
            return "t" if is_atom(a) and is_atom(b) and a == b else []
        if isinstance(f, Closure):
            frame = dict(zip(f.params, args))
            if len(f.params) != len(args):
                raise TypeError("arity mismatch")
            env = [frame] + f.env
            expr = f.body
            continue
        raise TypeError(f"not callable: {f!r}")


def top_eval(forms, env=None):
    """Evaluate a list of top-level forms; returns the last value.
    (define name expr) and (define (name . params) body) update the global
    frame."""
    genv = [{p: p for p in ("car", "cdr", "cons", "atom?", "eq?")},
            {"t": "t"}]
    if env:
        genv = env
    val = []
    for form in forms:
        if isinstance(form, list) and form and form[0] == "define":
            if isinstance(form[1], list):
                name, params = form[1][0], form[1][1:]
                genv[0][name] = Closure(params, form[2], genv)
            else:
                genv[0][form[1]] = evaluate(form[2], genv)
            val = []
        else:
            val = evaluate(form, genv)
    return val


def run(src):
    return top_eval(parse(src))
