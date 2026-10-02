"""G1 by SAT: a front marker Z (free (30,-8)-periodic train in the
Ebar-frame region [K+FL, K+FR) in front of the rejector-prepared reader
P_1 = Ebar@K+39, E@K+68) such that BOTH tape symbols are read as N with
the exact standard outcome (debris included: stricter than 'mod V').
Scenes: exact cuts of the full machine (program {YNNNNN}, Cook's v) at
t_in = 32250, tapes NYYN (s_1 = Y) and NNYY (s_1 = N); Z cells shared.
Window: Ebar-frame [K+WL, K+WR), moving with the Ebar frame, margin 0.
Targets at T: the whole window equals the plain machine's window of tape
TGT at time T - 30 j for some j in [-JM, JM] (answer delay; indicator per
scene).  Modes:
  control : NYYN -> plain NYYN (Y read), NNYY -> plain NNYY (N read)
  forcedN : both -> plain NNYY
  inverted: NYYN -> plain NNYY, NNYY -> plain NYYN
Every SAT answer is re-simulated in the full machine.
    python sat_g1.py MODE FL FR [T] [JM]"""
import sys, time, json
import numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "synth"))
from q import *
from r110sat import CNF, Spacetime, make_window, ether_bit
from react import TrainVar
from sat_k import phase_glob

import os
T_IN = int(os.environ.get("G1_TIN", "32250"))
WL, WR = int(os.environ.get("G1_WL", "-320")), 240

def cut(tape, T, JM):
    m = Machine(tape, ["YNNNNN"], T_IN + T + 30 * JM + 2000, left_periods=4, right_periods=3)
    K = [a for n, a, b in m.blocks if n == "K"][0]
    r = Run(m.row, m.origin); r.step(T_IN)
    full = r.window(0, r.width).copy(); sh0 = r.ebar_frame()
    outs = {}
    r.step(T - 30 * JM)
    for j in range(JM, -JM - 1, -1):           # times T - 30j ascending
        sh = r.ebar_frame()
        outs[j] = r.window(K + WL + sh, K + WR + sh).copy()
        r.step(30)
    return dict(K=K, full=full, sh0=sh0, outs=outs)

def build(mode, FL, FR, T, JM):
    import os
    cnf = CNF(os.environ.get("SOLVER", "cadical153"))
    D = {t: cut(t, T, JM) for t in ("NYYN", "NNYY")}
    tgt = {"control": {"NYYN": "NYYN", "NNYY": "NNYY"}, "forcedN": {"NYYN": "NNYY", "NNYY": "NNYY"},
           "inverted": {"NYYN": "NNYY", "NNYY": "NYYN"}}[mode]
    d = D["NYYN"]; K, full, sh0 = d["K"], d["full"], d["sh0"]
    a, b = K + FL + sh0, K + FR + sh0
    pgL = phase_glob(full[a - 14:a], a - 14); pgR = phase_glob(full[b:b + 14], b)
    X = a - ((a + pgL) % 14); Wt = b - X; pR = (pgR + X) % 14
    Z = TrainVar(cnf, Wt, 30, -8, pR, name="Z")
    sts = {}
    for tape in ("NYYN", "NNYY"):
        d = D[tape]; K, full, sh0 = d["K"], d["full"], d["sh0"]
        lo, hi = K + WL + sh0, K + WR + sh0
        init = {x: (Z.st.lit(0, x - X) if X <= x < b else bool(full[x])) for x in range(lo, hi)}
        pl = phase_glob(full[lo:lo + 14], lo); pr = phase_glob(full[hi - 14:hi], hi - 14)
        st = Spacetime(cnf, T, lo, hi, pl, pr, init=init,
                       window=make_window(T, lo, hi, -8 / 30, -8 / 30, margin=0))
        L, R = st.bounds[T]
        shT = sh0 + int(round(-8 / 30 * T))       # Ebar-frame shift over T steps (T = 0 mod 30)
        t0 = K + WL + shT
        cands = []
        for j, out in D[tgt[tape]]["outs"].items():
            cands.append([int(out[x - t0]) if t0 <= x < t0 + len(out) else ether_bit(pl if x < t0 else pr, T, x)
                          for x in range(L, R)])
        st.one_of(T, L, R, cands)
        sts[tape] = (st, lo, hi)
    return cnf, Z, sts, D, (a, b, X, Wt, pgL, pgR), tgt

def verify(Z, sol, D, geo, tgt, T, JM):
    a, b, X, Wt, pgL, pgR = geo
    bits = Z.decode(sol)
    res = {}
    for tape in ("NYYN", "NNYY"):
        d = D[tape]
        row = d["full"].copy()
        row[a:b] = [ether_bit(pgL if x < X else pgR, 0, x) for x in range(a, b)]
        row[X:X + Wt] = bits
        r = Run(row, 0); r.t = T_IN; r.step(T)
        sh = d["sh0"] + int(round(-8 / 30 * T))
        w = r.window(d["K"] + WL + sh, d["K"] + WR + sh)
        res[tape] = {j: int((w != o).sum()) for j, o in D[tgt[tape]]["outs"].items()}
    return bits, res

if __name__ == "__main__":
    mode, FL, FR = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    T = int(sys.argv[4]) if len(sys.argv) > 4 else 1350
    JM = int(sys.argv[5]) if len(sys.argv) > 5 else 6
    t0 = time.time()
    cnf, Z, sts, D, geo, tgt = build(mode, FL, FR, T, JM)
    print(f"{mode} FL={FL} FR={FR} T={T} JM={JM} Wt={geo[3]}: vars {cnf.nvars} clauses {len(cnf.clauses)} built {time.time()-t0:.0f}s", flush=True)
    sol = cnf.solve()
    rec = {"mode": mode, "FL": FL, "FR": FR, "T": T, "JM": JM, "Wt": geo[3], "sat": sol is not None, "secs": round(time.time() - t0)}
    if sol is not None:
        bits, res = verify(Z, sol, D, geo, tgt, T, JM)
        rec.update({"Z": "".join(map(str, bits)), "X_rel": int(geo[2] - (D["NYYN"]["K"] + D["NYYN"]["sh0"])),
                    "full_machine_min_diff": {t: min(v.values()) for t, v in res.items()}})
    print(json.dumps(rec), flush=True)
    with open("/home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/queue/sat_g1.jsonl", "a") as fh:
        fh.write(json.dumps(rec) + "\n")
