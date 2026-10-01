"""Step 2 of option (c) by SAT: a raw-leader core K' (free (30,-8) train
replacing K's [E5][E2] in the Ebar-frame region [K+FL, K+FR) at t = 0)
such that
  scene A (tape YYNN, t_a = 14010, the ACCEPTOR 163 cells left of K):
      the Ebar-frame window [K-250, K+240) at t_a + 1000 equals the plain
      machine cell for cell (K' is prepared exactly like K), and
  scene R (tape NYYN, t_r = 11010, the REJECTOR ~150 cells left of K):
      mode control: equals the plain machine at t_r + 690;
      mode diff   : equals the plain machine OUTSIDE the core region
                    C = [K+20, K+110) at t_r + 690, while inside C it is a
                    (30,-8)-invariant pattern (rows T, T+30) that DIFFERS
                    from the plain prepared core;
      mode exact  : equals a given target core (file) inside C.
Both t_a and t_r are = 0 (mod 30), so K' sits at the same time phase.
Every SAT answer is re-simulated in the full machine.
    python sat_leader.py MODE [FL FR]"""
import sys, time, json
import numpy as np
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2] / "synth"))
from splice import *
from r110sat import CNF, Spacetime, make_window, ether_bit, neg
from react import TrainVar
from sat_reader import phase_glob

WL, WR = -250, 240
CL, CR = 20, 110
SCENES = {"A": ("YYNN", 14010, 1000), "R": ("NYYN", 11010, 690)}

def cut(tape, t_in, T, extra=0):
    m = Machine(tape, ["YNNNNN"], t_in + T + extra + 2000, left_periods=2, right_periods=3)
    K = [a for n, a, b in m.blocks if n == "K"][0]
    r = Run(m.row, m.origin); r.step(t_in)
    full = r.window(0, r.width).copy(); sh0 = r.ebar_frame()
    r.step(T); sh1 = r.ebar_frame()
    out = r.window(K + WL + sh1, K + WR + sh1).copy()
    return m, K, full, sh0, sh1, out

def build(mode, FL, FR):
    cnf = CNF()
    data = {s: cut(tp, t, T) for s, (tp, t, T) in SCENES.items()}
    m, K, full, sh0, _, _ = data["A"]
    a, b = K + FL + sh0, K + FR + sh0
    pgL = phase_glob(full[a - 14:a], a - 14); pgR = phase_glob(full[b:b + 14], b)
    X = a - ((a + pgL) % 14); Wt = b - X; pR = (pgR + X) % 14   # X = -pgL (mod 14), X <= a
    P = TrainVar(cnf, Wt, 30, -8, pR, name="Kp")
    sts = {}
    for s, (m, K, full, sh0, sh1, out) in data.items():
        tp, t_in, T = SCENES[s]
        Tm = T + (30 if (s == "R" and mode == "diff") else 0)
        lo, hi = K + WL + sh0, K + WR + sh0
        a_s, b_s = K + FL + sh0, K + FR + sh0
        X_s = X - a + a_s
        init = {}
        for x in range(lo, hi):
            if X_s <= x < b_s:
                if X_s <= x < X_s + Wt:
                    init[x] = P.st.lit(0, x - X_s)
                else:
                    init[x] = bool(ether_bit(pgL if x < X_s else pgR, 0, x))
            else:
                init[x] = bool(full[x])
        pl = phase_glob(full[lo:lo + 14], lo); pr = phase_glob(full[hi - 14:hi], hi - 14)
        st = Spacetime(cnf, Tm, lo, hi, pl, pr, init=init,
                       window=make_window(Tm, lo, hi, -8 / 30, -8 / 30, margin=0))
        L, R = st.bounds[T]
        t0 = K + WL + sh1
        c0, c1 = K + CL + sh1, K + CR + sh1
        free_core = (s == "R" and mode == "diff")
        for x in range(L, R):
            v = int(out[x - t0]) if t0 <= x < t0 + len(out) else ether_bit(pl if x < t0 else pr, T, x)
            if free_core and c0 <= x < c1:
                continue
            st.fix(T, x, v)
        if free_core:
            # inside C: differs from plain; (30,-8)-invariant on its interior;
            # ether bands of 14 at both ends are already enforced? no: force
            # the first/last 14 cells of C to the plain values (plain has ether there)
            for x in list(range(c0, c0 + 14)) + list(range(c1 - 14, c1)):
                st.fix(T, x, int(out[x - t0]))
            st.differs(T, c0, c1, [int(out[x - t0]) for x in range(c0, c1)])
            for x in range(c0 + 14, c1 - 14):
                cnf.equal(st.lit(T + 30, x - 8), st.lit(T, x))
        sts[s] = (st, lo, hi, a_s, b_s, X_s)
    return cnf, P, sts, data, (pgL, pgR, Wt)

def verify(P, sol, data, sts, pg, mode):
    pgL, pgR, Wt = pg
    bits = P.decode(sol)
    res = {}
    for s, (m, K, full, sh0, sh1, out) in data.items():
        tp, t_in, T = SCENES[s]
        st, lo, hi, a_s, b_s, X_s = sts[s]
        row = full.copy()
        row[X_s:b_s] = [ether_bit(pgL if x < X_s else pgR, 0, x) for x in range(X_s, b_s)]
        row[X_s:X_s + Wt] = bits
        r = Run(row, 0); r.t = t_in; r.step(T)
        w = r.window(K + WL + sh1, K + WR + sh1)
        d = (w != out)
        res[s] = {"diff_total": int(d.sum()),
                  "diff_outside_core": int(d[:CL - WL].sum() + d[CR - WL:].sum())}
    return bits, res

if __name__ == "__main__":
    mode = sys.argv[1]
    FL, FR = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (13, 112)
    t0 = time.time()
    cnf, P, sts, data, pg = build(mode, FL, FR)
    print(f"{mode} FL={FL} FR={FR}: vars {cnf.nvars} clauses {len(cnf.clauses)}", flush=True)
    sol = cnf.solve()
    rec = {"mode": mode, "FL": FL, "FR": FR, "sat": sol is not None, "secs": round(time.time() - t0)}
    if sol is not None:
        bits, res = verify(P, sol, data, sts, pg, mode)
        st, lo, hi, a_s, b_s, X_s = sts["A"]
        m, K, full, sh0, sh1, out = data["A"]
        rec.update({"Kp": "".join(map(str, bits)), "X_rel_ebar": int(X_s - K - sh0), "check": res})
    print(json.dumps(rec), flush=True)
    with open("sat_leader.jsonl", "a") as fh:
        fh.write(json.dumps(rec) + "\n")
