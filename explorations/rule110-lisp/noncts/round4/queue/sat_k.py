"""Option (c) by SAT: a raw leader K' (free (30,-8)-periodic train replacing
the Ebar-frame region [K+FL, K+FR) at t = 0, i.e. part of the table) that
two answers prepare DIFFERENTLY.

Scenes (exact cuts of the full Cook machine, program {YNNNNN}, Cook's v):
  A: tape YYNN, t_a = 14250 (the ACCEPTOR ~85 cells left of K), horizon TA
  R: tape NYYN, t_r = 11130 (the REJECTOR ~110 cells left of K), horizon TR
  (t_a = t_r = 0 mod 30: the free train has the same cells in both.)
Window: Ebar-frame [K+WL, K+WR), moving with the Ebar frame, margin 0
(synth's moving window: nothing may leave it - a scope restriction).
Measured: the window is static (answer absorbed, leader prepared) from
t_a + 420 resp. t_r + 360 on (t_horizon.py).

Modes (targets at the scene horizon T and T + 30):
  control : both windows equal the plain machine (positive control: the
            original K must be found).
  rejdiff : A equal to plain; R equal to plain outside the core region
            C = [K+CL, K+CR), inside C static ((30,-8)-invariant between
            T and T+30) and DIFFERENT from plain.
  accdiff : the same with A and R exchanged.
Every SAT answer is re-simulated in the full machine (both scenes; window
diffs reported) and saved.
    python sat_k.py MODE FL FR [CL CR]"""
import sys, time, json
import numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "synth"))
from q import *
from r110sat import CNF, Spacetime, make_window, ether_bit
from react import TrainVar

WL, WR = -180, 240
SCENES = {"A": ("YYNN", 14250, 450), "R": ("NYYN", 11130, 390)}

def phase_glob(cells, x0):
    for p in range(14):
        if all(cells[i] == ether_bit(p, 0, x0 + i) for i in range(14)):
            return p
    raise ValueError("not ether")

def cut(tape, t_in, T):
    m = Machine(tape, ["YNNNNN"], t_in + T + 2000, left_periods=4, right_periods=3)
    K = [a for n, a, b in m.blocks if n == "K"][0]
    r = Run(m.row, m.origin); r.step(t_in)
    full = r.window(0, r.width).copy(); sh0 = r.ebar_frame()
    r.step(T); sh1 = r.ebar_frame(); outT = r.window(K + WL + sh1, K + WR + sh1).copy()
    r.step(30); sh2 = r.ebar_frame(); outT30 = r.window(K + WL + sh2, K + WR + sh2).copy()
    return dict(m=m, K=K, full=full, sh0=sh0, sh1=sh1, sh2=sh2, out=outT, out30=outT30)

def build(mode, FL, FR, CL, CR):
    import os
    cnf = CNF(os.environ.get("SOLVER", "cadical153"))
    D = {s: cut(tp, t, T) for s, (tp, t, T) in SCENES.items()}
    d = D["A"]; K, full, sh0 = d["K"], d["full"], d["sh0"]
    a, b = K + FL + sh0, K + FR + sh0
    pgL = phase_glob(full[a - 14:a], a - 14); pgR = phase_glob(full[b:b + 14], b)
    X = a - ((a + pgL) % 14); Wt = b - X; pR = (pgR + X) % 14
    P = TrainVar(cnf, Wt, 30, -8, pR, name="Kp")
    sts = {}
    for s, (tp, t_in, T) in SCENES.items():
        d = D[s]; K, full, sh0, sh1, sh2 = d["K"], d["full"], d["sh0"], d["sh1"], d["sh2"]
        lo, hi = K + WL + sh0, K + WR + sh0
        a_s, b_s = K + FL + sh0, K + FR + sh0
        X_s = X - a + a_s
        init = {}
        for x in range(lo, hi):
            if X_s <= x < b_s:
                init[x] = P.st.lit(0, x - X_s) if x < X_s + Wt else bool(ether_bit(pgR, 0, x))
            elif a_s <= x < X_s:
                init[x] = bool(ether_bit(pgL, 0, x))
            else:
                init[x] = bool(full[x])
        pl = phase_glob(full[lo:lo + 14], lo); pr = phase_glob(full[hi - 14:hi], hi - 14)
        free_core = (mode == "rejdiff" and s == "R") or (mode == "accdiff" and s == "A")
        Tm = T + 30
        st = Spacetime(cnf, Tm, lo, hi, pl, pr, init=init,
                       window=make_window(Tm, lo, hi, -8 / 30, -8 / 30, margin=0))
        for tt, out, sh in ((T, d["out"], sh1), (T + 30, d["out30"], sh2)):
            L, R = st.bounds[tt]
            t0 = K + WL + sh
            c0, c1 = K + CL + sh, K + CR + sh
            for x in range(L, R):
                if free_core and c0 + 14 <= x < c1 - 14:
                    continue
                v = int(out[x - t0]) if t0 <= x < t0 + len(out) else ether_bit(pl if x < t0 else pr, tt, x)
                st.fix(tt, x, v)
        if free_core:
            c0, c1 = K + CL + sh1, K + CR + sh1
            st.differs(T, c0 + 14, c1 - 14, [int(d["out"][x - (K + WL + sh1)]) for x in range(c0 + 14, c1 - 14)])
            for x in range(c0 + 14, c1 - 14):
                cnf.equal(st.lit(T + 30, x - 8), st.lit(T, x))
        sts[s] = (st, a_s, b_s, X_s)
    return cnf, P, sts, D, (pgL, pgR, Wt)

def verify(P, sol, D, sts, pg):
    pgL, pgR, Wt = pg
    bits = P.decode(sol)
    res = {}
    for s, (tp, t_in, T) in SCENES.items():
        d = D[s]; st, a_s, b_s, X_s = sts[s]
        row = d["full"].copy()
        row[a_s:b_s] = [ether_bit(pgL if x < X_s else pgR, 0, x) for x in range(a_s, b_s)]
        row[X_s:X_s + Wt] = bits
        r = Run(row, 0); r.t = t_in; r.step(T)
        w = r.window(d["K"] + WL + d["sh1"], d["K"] + WR + d["sh1"])
        dd = (w != d["out"])
        res[s] = {"diff_total": int(dd.sum()), "diff_idx": [int(i) + WL for i in np.nonzero(dd)[0][:5]]}
        res[s]["window"] = "".join(map(str, w))
    return bits, res

if __name__ == "__main__":
    mode, FL, FR = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    CL, CR = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (-120, 120)
    t0 = time.time()
    cnf, P, sts, D, pg = build(mode, FL, FR, CL, CR)
    print(f"{mode} FL={FL} FR={FR} C=[{CL},{CR}) Wt={pg[2]}: vars {cnf.nvars} clauses {len(cnf.clauses)} built {time.time()-t0:.0f}s", flush=True)
    sol = cnf.solve()
    rec = {"mode": mode, "FL": FL, "FR": FR, "CL": CL, "CR": CR, "Wt": pg[2], "sat": sol is not None, "secs": round(time.time() - t0)}
    if sol is not None:
        bits, res = verify(P, sol, D, sts, pg)
        rec.update({"Kp": "".join(map(str, bits)), "check": res})
    print(json.dumps({k: v for k, v in rec.items() if k != "check"}), json.dumps({s: {k: v for k, v in c.items() if k != "window"} for s, c in rec.get("check", {}).items()}), flush=True)
    with open("/home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/queue/sat_k.jsonl", "a") as fh:
        fh.write(json.dumps(rec) + "\n")
