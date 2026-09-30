"""Layer 3: SKI combinator calculus -- reference reduction engine.

Terms are strings in backtick (prefix application) notation:
    `fx  means (f x);   ``Sxy means ((S x) y)
Combinators: S, K, I. Reduction is normal order (leftmost-outermost):
    ```Sxyz -> ``xz`yz      ``Kxy -> x      `Ix -> x

The TM implementation (ski_tm.py) must reproduce reduce_once exactly.
"""


def parse_spine(term, pos=0):
    """End index (exclusive) of the complete term starting at pos. A term
    is a single symbol or ` followed by two terms."""
    if term[pos] == "`":
        mid = parse_spine(term, pos + 1)
        return parse_spine(term, mid)
    return pos + 1


def subterm(term, pos):
    """The substring that is the complete term starting at pos."""
    return term[pos:parse_spine(term, pos)]


def reduce_once(term):
    """One leftmost-outermost reduction; None if in normal form.

    In prefix notation the leftmost spine is the leading run of backticks
    and the head is the symbol after it; the number of backticks is the
    number of arguments available to the head. If the head has enough
    arguments it is the redex. Otherwise the head is stuck and the first
    argument (left to right) that is not in normal form is reduced.
    """
    # walk the spine from the root, remembering application nodes
    apps = []          # positions of ` nodes on the leftmost spine
    p = 0
    while term[p] == "`":
        apps.append(p)
        p += 1
    head = term[p]
    args = len(apps)   # number of arguments available to head
    if head == "I" and args >= 1:
        # innermost spine node applying I is apps[-1]: `Ix
        a = apps[-1]
        x = subterm(term, a + 2)
        return term[:a] + x + term[a + 2 + len(x):]
    if head == "K" and args >= 2:
        a = apps[-2]
        x = subterm(term, a + 3)
        y = subterm(term, a + 3 + len(x))
        return term[:a] + x + term[a + 3 + len(x) + len(y):]
    if head == "S" and args >= 3:
        a = apps[-3]
        x = subterm(term, a + 4)
        y = subterm(term, a + 4 + len(x))
        z = subterm(term, a + 4 + len(x) + len(y))
        rest = term[a + 4 + len(x) + len(y) + len(z):]
        return term[:a] + "``" + x + z + "`" + y + z + rest
    # head is a free symbol or under-applied: normal form at the spine head;
    # reduce the leftmost reducible argument instead
    # arguments are the second children of the spine nodes, outermost first
    pos_of_arg = []
    for a in reversed(apps):        # innermost application first
        arg_pos = a + 1 + len(subterm(term, a + 1))
        # a+1's subterm is the function part; its arg follows
        pos_of_arg.append(arg_pos)
    for ap in pos_of_arg:
        sub = subterm(term, ap)
        r = reduce_once(sub)
        if r is not None:
            return term[:ap] + r + term[ap + len(sub):]
    return None


def normalize(term, max_steps=100000):
    """Reduce to normal form; raises if it takes more than max_steps."""
    for _ in range(max_steps):
        r = reduce_once(term)
        if r is None:
            return term
        term = r
    raise RuntimeError("no normal form within step budget")
