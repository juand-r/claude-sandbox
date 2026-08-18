import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lisp import run, parse


def test_basics():
    assert run("(quote (a b c))") == ["a", "b", "c"]
    assert run("(car (quote (a b)))") == "a"
    assert run("(cdr (quote (a b c)))") == ["b", "c"]
    assert run("(cons (quote a) (quote (b)))") == ["a", "b"]
    assert run("(atom? (quote a))") == "t"
    assert run("(atom? (quote (a)))") == []
    assert run("(eq? (quote a) (quote a))") == "t"
    assert run("(eq? (quote a) (quote b))") == []


def test_cond_lambda():
    assert run("(cond ((eq? (quote a) (quote b)) (quote x)) (t (quote y)))") == "y"
    assert run("((lambda (x) (cons x (quote ()))) (quote a))") == ["a"]


def test_define_recursion():
    # append two lists, unary-length equality
    src = """
    (define (append a b)
      (cond ((eq? a (quote ())) b)
            (t (cons (car a) (append (cdr a) b)))))
    (append (quote (a b)) (quote (c d)))
    """
    assert run(src) == ["a", "b", "c", "d"]


def test_unary_arithmetic():
    src = """
    (define (add a b)
      (cond ((eq? a (quote ())) b)
            (t (cons (quote i) (add (cdr a) b)))))
    (define (mul a b)
      (cond ((eq? a (quote ())) (quote ()))
            (t (add b (mul (cdr a) b)))))
    (mul (quote (i i i)) (quote (i i)))
    """
    assert run(src) == ["i"] * 6


def test_closures():
    src = """
    (define (make-adder a) (lambda (b) (cons (quote i) b)))
    ((make-adder (quote (i))) (quote (i i)))
    """
    assert run(src) == ["i", "i", "i"]
