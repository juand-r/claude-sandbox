"""Reverse drift switch, step 2 (exact CA): uniform left stream of train Q
(lwalk.py) walking a zero window E; a B^3 (K3's shot through R1's zero)
reaches the window's back at a varying time (start distance b3_dx). Expect:
the window closes (E + B^3 -> E^4) and stops: final lone E^4 whose
position grows with the arrival time and then stays. Control: no B^3.
Usage: python lstop.py TRAIN_INDEX T0 [K] [M]"""
import json, os, sys
import lwalk
from lwalk import *  # noqa
idx, t0 = int(sys.argv[1]), int(sys.argv[2])
lwalk.K = int(sys.argv[3]) if len(sys.argv) > 3 else 10
lwalk.M = int(sys.argv[4]) if len(sys.argv) > 4 else 6
c = [json.loads(l) for l in open(os.path.join(HERE, "lgate4.jsonl")) if json.loads(l)["i"] == idx][0]
q = (c["bits"], 0, c["pR"], 0)
T = int((14 * lwalk.M * lwalk.K + 400) / (14 / 15)) + 900
sts, seed = lwalk.scene(q, t0)
ref = Fraction(seed[1]) - VE * seed[0]
p0 = run_to(sts, T)
print("control (no B^3):", [(p[0], round(float(lat(p) - ref), 2)) for p in p0], flush=True)
for dx in range(int(sys.argv[5]) if len(sys.argv) > 5 else 40, int(sys.argv[6]) if len(sys.argv) > 6 else 330, int(sys.argv[7]) if len(sys.argv) > 7 else 10):
    sts, seed = lwalk.scene(q, t0, b3_dx=dx)
    pr = run_to(sts, T)
    print(dx, [(p[0], round(float(lat(p) - ref), 2)) for p in pr], flush=True)
