"""Step 1, LENIENT version of sat_reader.py: the answer may be DELAYED by
j*(30,-8) (j in -J..J) relative to the standard answer. Justification:
the table, the moving data and the leaders are all (30,-8)-invariant, so
an answer whose world line is translated by (30,-8) relative to them has
the same future up to a 30-step delay; the tape is behind it.
Target at T2 = t_in + T, window [K-250, K+WR): cells [K-250, K+XS) (the
remnant of the leader) must equal the target outcome exactly; cells
[K+XS, K+WR) (answer + static table) must equal the target outcome at
time T2 - 30 j, shifted by -8 j cells, for some j (one indicator per j).
    python sat_reader2.py MODE FL FR [T] [J]"""
import sys, time, json
import numpy as np
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2] / "synth"))
from splice import *
from r110sat import CNF, Spacetime, make_window, ether_bit
from react import TrainVar
from sat_reader import phase_glob

T_IN = 32700
WL, WR, XS = -250, 410, 150

def cut(tape, T, J):
    m = Machine(tape, ["YNNNNN"], T_IN + T + 2000, left_periods=4, right_periods=3)
    K = [a for n, a, b in m.blocks if n == "K"][0]
    r = Run(m.row, m.origin); r.step(T_IN)
    full = r.window(0, r.width).copy(); sh0 = r.ebar_frame()
    outs = {}
    r.step(T - 30 * J)
    for j in range(J, -J - 1, -1):          # times T2 - 30j, j = J..-J
        sh = r.ebar_frame()
        outs[j] = (r.window(K + WL + sh, K + WR + sh).copy(), sh)
        if j > -J:
            r.step(30)
    return m, K, full, sh0, outs

def build(mode, FL, FR, T, J):
    cnf = CNF()
    S = {t: cut(t, T, J) for t in ("NYYN", "NNYY")}
    OUT = {"Y": S["NYYN"][4], "N": S["NNYY"][4]}
    target = {"control": ("Y", "N"), "forcedN": ("N", "N"),
              "inverted": ("N", "Y"), "forcedY": ("Y", "Y")}[mode]
    m, K, full, sh0, _ = S["NYYN"]
    a, b = K + FL + sh0, K + FR + sh0
    pgL = phase_glob(full[a - 14:a], a - 14); pgR = phase_glob(full[b:b + 14], b)
    X = a + ((-pgL - a) % 14); Wt = b - X - 2; pR = (pgR + X) % 14
    P = TrainVar(cnf, Wt, 30, -8, pR, name="P")
    scenes = []
    for (tape, (m, K, full, sh0, _)), want in zip(S.items(), target):
        lo, hi = K + WL + sh0, K + WR + sh0
        init = {}
        for x in range(lo, hi):
            if a <= x < b:
                init[x] = P.st.lit(0, x - X) if X <= x < X + Wt else \
                    bool(ether_bit(pgL if x < X else pgR, 0, x))
            else:
                init[x] = bool(full[x])
        pl = phase_glob(full[lo:lo + 14], lo); pr = phase_glob(full[hi - 14:hi], hi - 14)
        st = Spacetime(cnf, T, lo, hi, pl, pr, init=init,
                       window=make_window(T, lo, hi, -8 / 30, -8 / 30, margin=0))
        L, R = st.bounds[T]
        tg0, sh1 = OUT[want][0]
        t0 = K + WL + sh1                      # array coord of window start at T2
        xs = K + XS + sh1
        for x in range(L, R):
            if x < xs:
                v = int(tg0[x - t0]) if t0 <= x else ether_bit(pl, T, x)
                st.fix(T, x, v)
        inds = []
        for j in range(-J, J + 1):
            tgj, shj = OUT[want][j]
            # target_j at T2: answer part of the outcome at T2 - 30j, moved by -8j
            ind = cnf.new_var(); inds.append(ind)
            for x in range(xs, R):
                src = x + 8 * j                # cell at T2-30j in array coords
                k = src - (K + WL + shj)
                v = int(tgj[k]) if 0 <= k < len(tgj) else ether_bit(pr, T, x)
                l = st.lit(T, x)
                cnf.add([-ind, l if v else -l if not isinstance(l, bool) else (not l)])
        cnf.add(inds)
        scenes.append((tape, st, inds))
    return cnf, P, scenes, S, OUT, target, (a, b, X, Wt, pgL, pgR)

def verify(bits, S, OUT, target, T, J, geom, js):
    """Full-machine re-simulation; checks the lenient condition with the
    j chosen by the solver for each scene, and also the exact (j = 0) one."""
    a, b, X, Wt, pgL, pgR = geom
    res = []
    for ((tape, (m, K, full, sh0, _)), want), j in zip(zip(S.items(), target), js):
        row = full.copy()
        row[a:b] = [ether_bit(pgL if x < X else pgR, 0, x) for x in range(a, b)]
        row[X:X + Wt] = bits
        r = Run(row, 0); r.t = T_IN; r.step(T)
        sh1 = OUT[want][0][1]              # base Ebar-frame shift at T2 (array coords)
        lo1 = K + WL + sh1
        w = r.window(lo1, K + WR + sh1)
        n = XS - WL
        rem = int((w[:n] != OUT[want][0][0][:n]).sum())
        tgj, shj = OUT[want][j]
        ans = 0
        for i in range(n, len(w)):
            k = (lo1 + i + 8 * j) - (K + WL + shj)
            v = tgj[k] if 0 <= k < len(tgj) else None
            if v is not None and w[i] != v:
                ans += 1
        res.append({"tape": tape, "j": j, "remnant_diff": rem, "answer_diff": ans})
    return res

if __name__ == "__main__":
    mode = sys.argv[1]; FL, FR = int(sys.argv[2]), int(sys.argv[3])
    T = int(sys.argv[4]) if len(sys.argv) > 4 else 1100
    J = int(sys.argv[5]) if len(sys.argv) > 5 else 4
    t0 = time.time()
    cnf, P, scenes, S, OUT, target, geom = build(mode, FL, FR, T, J)
    print(f"{mode} FL={FL} FR={FR} T={T} J={J}: vars {cnf.nvars} clauses {len(cnf.clauses)}", flush=True)
    sol = cnf.solve()
    rec = {"mode": mode, "FL": FL, "FR": FR, "T": T, "J": J, "sat": sol is not None,
           "secs": round(time.time() - t0)}
    if sol is not None:
        bits = P.decode(sol)
        rec["P"] = "".join(map(str, bits))
        rec["j"] = [[j for j, ind in zip(range(-J, J + 1), sc[2]) if sol.val(ind)] for sc in scenes]
        js = [rj[0] for rj in rec["j"]]
        rec["verify"] = verify(bits, S, OUT, target, T, J, geom, js)
    print(json.dumps(rec), flush=True)
    with open("sat_reader2.jsonl", "a") as fh:
        fh.write(json.dumps(rec) + "\n")
