"""Left-stream packet library (right-moving, all period (3,2)).

Each packet X is given by a reference scene: seeds P_X of the packet and
the seed e_X of a plain E it acts on in its working class (collider
convention), and its counter displacement delta_X (disp.py; the same for
every n >= 1 where it applies, measured by ops.py / claim scripts).
SAT trains are rebuilt by typing the stored SAT row (collider registers the
compound in memory)."""
import json
import os
from check_rec import train_of

HERE = os.path.dirname(os.path.abspath(__file__))


def _rec(f, i):
    return [json.loads(l) for l in open(os.path.join(HERE, f))][i]


def _sat(f, i):
    tr, e = train_of(_rec(f, i))
    return tr, e


PK = {}
# I: INC from the left (sat_inc_results.jsonl #6), delta (7,-8)
_t, _e = _sat("sat_inc_results.jsonl", 6)
PK["I"] = dict(seeds=_t, e=_e, delta=(7, -8))
# D: single A, DEC (n >= 2); A + E -> C3 at zero. delta (5,2)
PK["D"] = dict(seeds=[("A", 1, -64)], e=(0, 7), delta=(5, 2))
# Z: zero test (sat_zero_results.jsonl #1): DEC for n >= 2, at n = 1
# E stays and one A leaves to the right; delta (9,0) in BOTH cases
_t, _e = _sat("sat_zero_results.jsonl", 1)
PK["Z"] = dict(seeds=_t, e=_e, delta=(9, 0))
