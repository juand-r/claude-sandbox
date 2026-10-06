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
