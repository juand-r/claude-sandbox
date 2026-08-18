"""Differential tests across Layer 3 arrows:
   lisp.py (reference)  vs  lisp_to_ski + SKI engines.
The string engine (ski.py) is the TM specification; the graph engine
(ski_graph.py) is the fast executor. They are fuzz-tested against each
other, and compiled programs are checked on both (string engine only on
the small ones -- it is O(n^2) per step by design)."""

import random
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lisp_to_ski
import ski
import ski_graph
from lisp import parse, run as lisp_run
from lisp_to_ski import Compiler, decode_value


def compile_term(src):
    c = Compiler()
    return c.compile_program(parse(src)), c.symtab


def run_graph(src, budget=5_000_000):
    old = lisp_to_ski.ski
    lisp_to_ski.ski = ski_graph
    try:
        term, symtab = compile_term(src)
        return decode_value(term, symtab, budget)
    finally:
        lisp_to_ski.ski = old


def test_engines_agree_fuzz():
    random.seed(2)
    def rand_term(depth):
        if depth == 0 or random.random() < 0.35:
            return random.choice("SKIxy")
        return "`" + rand_term(depth - 1) + rand_term(depth - 1)
    tested = 0
    for _ in range(400):
        t = rand_term(6)
        try:
            a = ski.normalize(t, 300)
        except (RuntimeError, RecursionError):
            continue
        assert ski_graph.normalize(t, 20000) == a, t
        tested += 1
    assert tested > 150


PROGRAMS = [
    "(quote (a b c))",
    "(car (quote (a b)))",
    "(cons (quote a) (quote (b)))",
    "(atom? (quote a))",
    "(atom? (quote (a)))",
    "(eq? (quote a) (quote a))",
    "(eq? (quote a) (quote b))",
    "(cond ((eq? (quote a) (quote b)) (quote x)) (t (quote y)))",
    "((lambda (x) (cons x (quote ()))) (quote a))",
    """(define (append a b)
         (cond ((eq? a (quote ())) b)
               (t (cons (car a) (append (cdr a) b)))))
       (append (quote (a b)) (quote (c d)))""",
    """(define (add a b)
         (cond ((eq? a (quote ())) b)
               (t (cons (quote i) (add (cdr a) b)))))
       (define (mul a b)
         (cond ((eq? a (quote ())) (quote ()))
               (t (add b (mul (cdr a) b)))))
       (mul (quote (i i i)) (quote (i i)))""",
    """(define (make-adder a) (lambda (b) (cons (quote i) b)))
       ((make-adder (quote (i))) (quote (i i)))""",
]


def test_compiled_programs_graph_engine():
    for p in PROGRAMS:
        assert run_graph(p) == lisp_run(p), p


def test_compiled_small_programs_string_engine():
    # the string engine is the TM spec; run it on the cheap programs only
    for p in PROGRAMS[:9]:
        term, symtab = compile_term(p)
        assert decode_value(term, symtab, 2_000_000) == lisp_run(p), p
