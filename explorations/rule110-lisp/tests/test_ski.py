import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ski import normalize, reduce_once, subterm


def test_subterm():
    assert subterm("`Ix", 0) == "`Ix"
    assert subterm("`Ix", 1) == "I"
    assert subterm("``Kxy", 2) == "K"
    assert subterm("```Sxyz", 0) == "```Sxyz"


def test_basic_reductions():
    assert reduce_once("`Ix") == "x"
    assert reduce_once("``Kxy") == "x"
    assert reduce_once("```Sxyz") == "``xz`yz"
    assert reduce_once("x") is None
    assert reduce_once("`xy") is None


def test_normalize():
    assert normalize("```SKKx") == "x"
    assert normalize("```SKxy") == "y"      # S K x y -> K y (x y) -> y
    B = "``S`KSK"
    assert normalize("```" + B + "xyz") == "`x`yz"
    C = "``S``S`K``S`KSKS`KK"
    assert normalize("```" + C + "xyz") == "``xzy"


def test_arg_reduction_under_free_head():
    assert reduce_once("`f`Ix") == "`fx"
    assert normalize("``f`Ix`Ky") == "``fx`Ky"
