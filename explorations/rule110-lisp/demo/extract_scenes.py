"""Cut demo scenes (cell rows) out of the one-move TM run at 1.25x."""
import sys, json; sys.path[:0]=['.','tests']
import numpy as np
import machines
from experiments import TM_RUNS
from cts import fill_empty_appendants
from encoder import _left_v
from tag import ts_to_cts
from tm import tm_to_ts
from gasrun import GasReads
from census import ether_phase
make, cfg = TM_RUNS["one"]
rules, ts_tape, s = tm_to_ts(getattr(machines, make)(), *cfg)
tape, apps, order = ts_to_cts(rules, ts_tape, s)
apps = fill_empty_appendants(apps)
gr = GasReads(tape, apps, int(1.25 * _left_v(apps)), 5970, log=lambda *a: None)
g = gr.run
def fam(o):
    if o.d == 0: return "C"
    if 3 * o.d == 2 * o.p: return "A"
    if 15 * o.d == -4 * o.p: return "E"
    return "X"
scenes = {}
def items(lo, hi):
    kind, ids, ph, left, width, cls, tc = g.list_items(lo, hi)
    out=[]
    for k,i,l,w in zip(kind, ids, left, width):
        if k == 1: out.append((int(l), int(l+w), fam(g.reg.orbits[i])))
        elif k == 2: out.append((int(l), int(l+w), "X"))
    return out
def cut(lo, hi, name, T):
    cells = g.window(lo, hi)
    # ether constants at both ends: row coordinate phase -> global constant at time t
    pl = ether_phase(cells[:14])[0]; pr = ether_phase(cells[-14:])[0]
    assert pl >= 0 and pr >= 0, "window ends must be ether"
    scenes[name] = {"cells": "".join(map(str, cells.tolist())), "t": int(g.t), "x0": int(lo),
                    "T": T, "items": len(items(lo, hi))}

def snap(t):
    g.advance_to(t)
    return items(-(1<<40), 1<<40)
# scene 1: a tape character and the next Ebar pair arriving from the right
t = 3_000_000_000
its = snap(t)
c = next(it for it in its if it[2] == "C")
e = next(it for it in its if it[2] == "E" and it[0] > c[1])
t1 = t + (e[0] - c[1] - 300) * 15 // 4
t1 -= t1 % 30
its = snap(t1)
c = next(it for it in its if it[2] == "C")
cut(c[0] - 330, c[1] + 2300, "char", 5400)
print("char scene at", t1, "items", [(it[0]-c[0], it[2]) for it in its if c[0]-400 < it[0] < c[1]+2300])
# scene 2: an ossifier (A gliders) closing in on Ebars
t = t1
while True:
    t += 50_000_000
    its = snap(t)
    pair = None
    for k, it in enumerate(its[:-1]):
        if it[2] == "A" and its[k+1][2] == "E" and its[k+1][0] - it[1] < 200_000:
            pair = (it, its[k+1]); break
    if pair: break
a, e = pair
t2 = t + int((e[0] - a[1] - 420) / (2/3 + 4/15))
its = snap(t2)
a = max((it for it in its if it[2] == "A" and it[1] < e[0] + 10**6), key=lambda it: it[1])
grp = [it for it in its if a[0] - 400 < it[0] <= a[1] and it[2] == "A"]
lo = min(it[0] for it in grp) - 260
cut(lo, a[1] + 1000, "oss", 2400)
print("oss scene at", t2, [(it[0]-lo, it[2]) for it in its if lo - 100 < it[0] < a[1]+1000])
json.dump(scenes, open("/tmp/claude-0/-home-user-claude-sandbox/28d7251d-9c80-5c64-bf0f-12d94ea66db5/scratchpad/gas/demo/scenes.json", "w"))
print({k: (v["t"], len(v["cells"]), v["items"]) for k, v in scenes.items()})
