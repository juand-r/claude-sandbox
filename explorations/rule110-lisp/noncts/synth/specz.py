"""Spec Z (architect): an F-speed "floor" object O (free (36,-4)-train of
width WO) that survives a command packet P and leaves a stationary
messenger:   P + O -> O (same object, any position/phase) + messenger.
P arrives from the right. P = a fixed packet: a library glider name, or
"EE" = the E pair found for spec F (E@(0,0)+E@(-13,15), slip 4), or
"free:W:slip" = a free (30,-8)-train.
Required at T2: ether | O | ether band | nonempty period-7 object | ether.
Usage: python specz.py WO T2 P [--pR list] [--k list]
"""
import argparse, json, time
from lib import load_gliders
from r110sat import CNF, TILE
from react import TrainVar, Fixed, fixed_from_glider
from scene import Scene, BAND
from classes import placements_by_class, n_classes

G = load_gliders()
# the spec-F packet, as found by SAT (specf_results.jsonl, k=0): cells
# [0, 20) at t=0, my-phase 0 left, 4 right; (15,-4)-periodic
EE = ("00000111110000000010", 4, (15, -4))


def packet_item(cnf, seeds, width, name):
    """Fixed item from library glider seeds [(name, t0, x0)] at t=0, shifted
    so that my-phase 0 holds left of cell 0."""
    from lib import compose
    sts = [G[n].state(t0, x0, 0) for n, t0, x0 in seeds]
    lo0 = min(s[3] for s in sts) - 2
    cells, pl, pr = compose(sts, 0, lo0 - 14, lo0 - 14 + width + 28)
    # shift: need -(start) = pl (mod 14)
    start = lo0 - 14
    while (-start) % TILE != pl:
        start += 1
    cells, pl2, pr2 = compose(sts, 0, start, start + width)
    assert pl2 == pl
    per = G[seeds[0][0]].p, G[seeds[0][0]].d
    return Fixed(cnf, "".join(map(str, cells)), (pr2 + start) % TILE, per, name=name)


def make_P(cnf, spec):
    if spec == "EbEb":   # collider's spec-Z candidate packet
        return packet_item(cnf, [("Ebar", 0, 0), ("Ebar", -4, 23)], 48, "EbEb")
    if spec == "EE":
        return Fixed(cnf, EE[0], EE[1], EE[2], name="EE")
    if spec.startswith("free"):
        _, w, s = spec.split(":")
        return TrainVar(cnf, int(w), 30, -8, int(s), name="P")
    return fixed_from_glider(cnf, G[spec], 24)


def build(WO, T2, Pspec, pRO, k, a=None, b=None, win=40):
    cnf = CNF()
    O = TrainVar(cnf, WO, 36, -4, pRO, name="O")
    P = make_P(cnf, Pspec)
    pl = placements_by_class(O, (0, 0), P, WO + 6)
    tau, x = pl[k]
    # estimated collision point: floor right edge WO - t/9 meets P's left
    # edge x - 4t/15; messenger window around it
    tc = (x - WO) / (4 / 15 - 1 / 9)
    xc = int(round(WO - tc / 9))
    a = xc - 16 if a is None else a
    b = xc + 24 if b is None else b
    S = Scene(cnf, T2 + 7, [(O, 0, 0), (P, tau, x)])
    S.ether(T2, b + BAND, S.hi + T2, S.p_right)
    bl = S.ether(T2, a - BAND, a)
    S.ether(T2, b, b + BAND)
    S.invariant(T2, a - 7, b + 7, 7, 0)
    for ph in range(TILE):
        S.nonempty(T2, a, b, ph, guard=bl[ph])
    # floor: undisturbed at about -T2/9; search it within +-win of that
    xo = (-4 * T2) // 36
    x1 = min(a - BAND, xo - win)
    S.ether(T2, S.lo - T2, x1, S.p_left)
    S.is_item(T2, x1, a - BAND, O, far_left=S.p_left)
    return cnf, O, P, S, len(pl)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("WO", type=int); ap.add_argument("T2", type=int)
    ap.add_argument("P")
    ap.add_argument("--pR", default=",".join(map(str, range(TILE))))
    ap.add_argument("--k", default=None)
    A = ap.parse_args()
    for pRO in map(int, A.pR.split(",")):
        cnf0 = CNF()
        n = n_classes((36, -4), make_P(cnf0, A.P).period)
        ks = range(n) if A.k is None else map(int, A.k.split(","))
        for k in ks:
            t = time.time()
            cnf, O, P, S, _ = build(A.WO, A.T2, A.P, pRO, k)
            sol = cnf.solve()
            rec = {"spec": "Z", "WO": A.WO, "T2": A.T2, "P": A.P, "pRO": pRO,
                   "k": k, "sat": sol is not None, "secs": round(time.time() - t, 1)}
            if sol is not None:
                rec["O"] = "".join(map(str, O.decode(sol)))
                rec["sim_ok"] = S.check_sat_vs_sim(sol)
                rec["row0"] = "".join(map(str, S.row(sol, 0)))
                rec["lo"], rec["pl"], rec["pr"] = S.lo, S.p_left, S.p_right
                if not rec["sim_ok"]:
                    raise AssertionError("SAT/sim mismatch")
            print(json.dumps({q: v for q, v in rec.items() if q != "row0"}), flush=True)
            with open("specz_results.jsonl", "a") as fh:
                fh.write(json.dumps(rec) + "\n")
