"""Layer 3: fast SKI reduction by graph rewriting with sharing.

Semantics: normal-order reduction to normal form, same results as
ski.normalize (differentially tested on small terms). Used to execute
compiled Lisp programs at practical speed; the string engine remains the
specification that the TM implements.

Graph: a node is ['app', f, x] (mutable for in-place update) or a string
(combinator/free symbol). S duplicates its z argument BY REFERENCE, so
shared subterms reduce once.
"""

import sys


def parse(term):
    pos = 0
    def rd():
        nonlocal pos
        c = term[pos]; pos += 1
        if c == "`":
            f = rd(); x = rd()
            return ["app", f, x]
        return c
    g = rd()
    assert pos == len(term)
    return g


def render(g):
    out = []
    stack = [g]
    while stack:
        n = stack.pop()
        if isinstance(n, str):
            out.append(n)
        else:
            out.append("`")
            stack.append(n[2])
            stack.append(n[1])
    return "".join(out)


def _whnf(g, budget):
    """Reduce g to weak head normal form in place; returns (head, spine)."""
    spine = []
    node = g
    while True:
        node = _chase(node)
        while not isinstance(node, str):
            spine.append(node)
            node = _chase(node[1])
        n = len(spine)
        if node == "I" and n >= 1:
            budget[0] -= 1
            top = spine[-1]
            arg = _chase(top[2])
            _overwrite(top, arg)
            spine.pop()
            node = top
        elif node == "K" and n >= 2:
            budget[0] -= 1
            x = _chase(spine[-1][2])
            top = spine[-2]
            _overwrite(top, x)
            spine.pop(); spine.pop()
            node = top
        elif node == "S" and n >= 3:
            budget[0] -= 1
            x = spine[-1][2]; y = spine[-2][2]; top = spine[-3]
            z = top[2]
            top[1] = ["app", x, z]
            top[2] = ["app", y, z]
            spine.pop(); spine.pop(); spine.pop()
            node = top
        else:
            return node, spine
        if budget[0] <= 0:
            raise RuntimeError("reduction budget exhausted")


def _overwrite(node, val):
    if isinstance(val, str):
        node[:] = ["ind", val, None]   # indirection to a leaf
    else:
        node[:] = val


def _chase(g):
    while not isinstance(g, str) and g[0] == "ind":
        g = g[1]
    return g


def normalize(term, max_steps=10_000_000):
    budget = [max_steps]
    g = parse(term)
    root = ["app", "I", g]     # guard node so top-level overwrites work
    def nf(node):
        node = _chase(node)
        if isinstance(node, str):
            return node
        head, spine = _whnf(node, budget)
        # spine bottom is `node` itself; normalize remaining args
        out = head
        for app in reversed(spine):
            out = ["app", out, nf(app[2])]
        return out
    result = nf(root[2])
    return render(_strip_inds(result))


def _strip_inds(g):
    g = _chase(g)
    if isinstance(g, str):
        return g
    return ["app", _strip_inds(g[1]), _strip_inds(g[2])]
