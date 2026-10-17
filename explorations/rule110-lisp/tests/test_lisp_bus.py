"""Variable-free Lisp on the bus machine: right answers, at every level."""
import pytest

from lisp import run
from lisp_bus import LispBus

EXPRS = [
    "(quote a)", "(car (quote (a b)))", "(cdr (quote (a b)))",
    "(cons (quote a) (quote (b)))", "(cons (quote (a)) (quote ()))",
    "(atom? (quote a))", "(atom? (quote (a)))", "(atom? (quote ()))",
    "(eq? (quote a) (quote a))", "(eq? (quote a) (quote b))",
    "(eq? (quote ()) (quote ()))", "(eq? (quote (a)) (quote (a)))",
    "(eq? (quote a) (quote ()))",
    "(cond ((eq? (quote a) (quote b)) (quote x)) (t (quote y)))",
    "(cond ((quote ()) (quote x)))",
    "(cond ((atom? (quote a)) (car (quote (p q)))) (t (quote r)))",
    "(car (cdr (quote (a (b c) d))))",
    "(cdr (car (cdr (quote (a (b c) d)))))",
    "(cons (car (quote (a b))) (cdr (quote (c d))))",
]


@pytest.mark.parametrize("src", EXPRS)
def test_reference_and_compiled(src):
    lb = LispBus(src)
    want = run(src)
    assert lb.run_reference() == want
    assert lb.decode(lb.compile_bus().run(lb.values)) == want


def test_table_does_not_depend_on_data():
    """Same shape, same data sizes, different data: identical CTS table,
    different tape, different (correct) answers."""
    pairs = [("(car (quote (a b)))", "(car (quote (b a)))"),
             ("(eq? (quote a) (quote a))", "(eq? (quote a) (quote b))"),
             ("(cond ((atom? (quote (x))) (quote y)) (t (quote z)))",
              "(cond ((atom? (quote (x))) (quote z)) (t (quote y)))")]
    for s1, s2 in pairs:
        c1, c2 = LispBus(s1), LispBus(s2)
        p1, p2 = c1.compile_bus(), c2.compile_bus()
        assert p1.pm.appendants() == p2.pm.appendants()
        assert c1.decode(p1.run(c1.values)) == run(s1)
        assert c2.decode(p2.run(c2.values)) == run(s2)
        assert run(s1) != run(s2)


LAST = "(define (last l) (cond ((atom? (cdr l)) (car l)) (t (last (cdr l)))))"
APPEND = ("(define (append a b) (cond ((atom? a) b) "
          "(t (cons (car a) (append (cdr a) b)))))")
MEMBER = ("(define (member x l) (cond ((atom? l) (quote ())) "
          "((eq? x (car l)) t) (t (member x (cdr l)))))")
RECURSIVE = [
    ("((lambda (x) (cons x (quote (b)))) (quote a))", 1),
    (LAST + " (last (quote (a b c)))", 3),
    (APPEND + " (append (quote (a b)) (quote (c)))", 3),
    (MEMBER + " (member (quote b) (quote (a b c)))", 3),
    (MEMBER + " (member (quote d) (quote (a b)))", 3),
]


@pytest.mark.parametrize("src,depth", RECURSIVE)
def test_recursion(src, depth):
    lb = LispBus(src, depth)
    want = run(src)
    assert lb.run_reference() == want
    assert lb.decode(lb.compile_bus().run(lb.values)) == want


def test_recursion_bound_fails_loudly():
    lb = LispBus(LAST + " (last (quote (a b c d)))", 3)
    with pytest.raises(RecursionError):
        lb.run_reference()
    with pytest.raises(RecursionError):
        lb.decode(lb.compile_bus().run(lb.values))


SCOPED = [
    "((lambda (x) ((lambda (y) (cons (car y) x)) (cdr x))) (quote (a b)))",
    "((lambda (l) (cond ((atom? (cdr l)) (car l)) (t (quote z)))) (quote (a)))",
    "((lambda (x) (cons (car x) (cdr (cdr x)))) (quote (a b c)))",
]


@pytest.mark.parametrize("src", SCOPED)
def test_lambda_scope_and_last_use(src):
    """Lexical scope into applied lambdas; a variable's last use takes its
    block instead of copying it."""
    lb = LispBus(src, 3)
    assert lb.run_reference() == run(src)
    assert lb.decode(lb.compile_bus().run(lb.values)) == run(src)


def _cts_reads(comp, values):
    """The bit-level CTS's reads (Y/N per read) over one table period, as
    the glider run observes them."""
    from collections import deque
    apps = comp.pm.appendants()
    q = deque(comp.pm.encode(comp.initial_tape(values)))
    out = []
    for r in range(comp.p * comp.pm.B):
        ch = q.popleft()
        out.append(ch)
        if ch == "Y":
            q.extend(apps[r % len(apps)])
    return "".join(out)


@pytest.mark.parametrize("src", EXPRS)
def test_value_from_reads(src):
    """The decoder used on gliders (the last pass's reads, nothing else)
    gives the right value: every result register is read in that pass,
    after its last change. (It once missed cons's fresh register, which
    was born after the last pass.)"""
    from experiments import decode_reads
    lb = LispBus(src)
    comp = lb.compile_bus()
    assert decode_reads(lb, comp, _cts_reads(comp, lb.values)) == run(src)
