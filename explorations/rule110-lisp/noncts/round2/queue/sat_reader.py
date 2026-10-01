"""Step 1 of option (c) by SAT (synth's r110sat/react machinery):
find a READER core P' (free Ebar-speed train, period (30,-8), width W,
replacing the rejector-prepared leader core in the Ebar-frame region
[K+FL, K+FR)) such that, in two scenes cut from exact runs at
t_in = 32700 (the leader about to read a Y: tape NYYN; an N: tape NNYY),
the whole Ebar-frame window [K-250, K+240) at t_in + T equals given
targets cell for cell (nothing may leave the window either):
  control  : Y-scene -> plain Y outcome, N-scene -> plain N outcome
  forcedN  : both -> plain N outcome
  inverted : Y-scene -> plain N outcome, N-scene -> plain Y outcome
  forcedY  : both -> plain Y outcome
The plain outcomes are the plain machine's cells (NYYN / NNYY runs).
Every SAT answer is re-simulated in the FULL machine (splice.Run) and the
window compared again.
    python sat_reader.py MODE [FL FR] [T]"""
import sys, time, json
import numpy as np
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2] / "synth"))
from splice import *
from r110sat import CNF, Spacetime, make_window, ether_bit
from react import TrainVar

T_IN = 32700
WL, WR = -250, 240

def cut(tape, T):
    m = Machine(tape, ["YNNNNN"], T_IN + T + 2000, left_periods=4, right_periods=3)
    K = [a for n, a, b in m.blocks if n == "K"][0]
    r = Run(m.row, m.origin); r.step(T_IN)
    full_in = r.window(0, r.width).copy()
    sh0 = r.ebar_frame()
    r.step(T)
    sh1 = r.ebar_frame()
    out = r.window(K + WL + sh1, K + WR + sh1).copy()
    return m, K, full_in, sh0, sh1, out

def phase_glob(cells, x0):
    for p in range(14):
        if all(cells[i] == ether_bit(p, 0, x0 + i) for i in range(14)):
            return p
    raise ValueError("not ether")

def build(mode, FL, FR, T):
    cnf = CNF()
    S = {t: cut(t, T) for t in ("NYYN", "NNYY")}
    OUT = {"Y": S["NYYN"][5], "N": S["NNYY"][5]}
    target = {"control": ("Y", "N"), "forcedN": ("N", "N"),
              "inverted": ("N", "Y"), "forcedY": ("Y", "Y")}[mode]
    # free region in array coords (same in both scenes: same layout & time)
    m, K, full, sh0, sh1, _ = S["NYYN"]
    a, b = K + FL + sh0, K + FR + sh0
    pgL = phase_glob(full[a - 14:a], a - 14)
    pgR = phase_glob(full[b:b + 14], b)
    W = b - a
    X = a + ((-pgL - a) % 14)          # X = -pgL (mod 14), X >= a
    Wt = b - X - 2
    pR = (pgR + X) % 14
    P = TrainVar(cnf, Wt, 30, -8, pR, name="P")
    scenes = []
    for (tape, (m, K, full, sh0, sh1, _)), want in zip(S.items(), target):
        lo, hi = K + WL + sh0, K + WR + sh0
        cells = full[lo:hi]
        init = {}
        for x in range(lo, hi):
            if a <= x < b:
                if X <= x < X + Wt:
                    init[x] = P.st.lit(0, x - X)
                elif x < X:
                    init[x] = bool(ether_bit(pgL, 0, x))
                else:
                    init[x] = bool(ether_bit(pgR, 0, x))
            else:
                init[x] = bool(cells[x - lo])
        pl = phase_glob(cells[:14], lo)
        pr = phase_glob(cells[-14:], hi - 14)
        win = make_window(T, lo, hi, -8 / 30, -8 / 30, margin=0)
        st = Spacetime(cnf, T, lo, hi, pl, pr, init=init, window=win)
        L, R = st.bounds[T]
        tgt = OUT[want]
        # target window in array coords at time T: [K+WL+sh1, K+WR+sh1)
        t0 = K + WL + sh1
        for x in range(L, R):
            st.fix(T, x, int(tgt[x - t0]) if t0 <= x < t0 + len(tgt) else
                   ether_bit(pl if x < t0 else pr, T, x))
        scenes.append((tape, st, lo, hi, (a, b, X, Wt, pgL, pgR)))
    return cnf, P, scenes, S, OUT, target

def verify(P, sol, S, OUT, target, T, a, b, X, Wt, pgL, pgR):
    bits = P.decode(sol)
    res = []
    for (tape, (m, K, full, sh0, sh1, _)), want in zip(S.items(), target):
        row = full.copy()
        row[a:b] = [ether_bit(pgL, 0, x) if x < X else ether_bit(pgR, 0, x) for x in range(a, b)]
        row[X:X + Wt] = bits
        r = Run(row, 0); r.t = T_IN; r.step(T)
        w = r.window(K + WL + sh1, K + WR + sh1)
        res.append(int((w != OUT[want]).sum()))
    return bits, res

if __name__ == "__main__":
    mode = sys.argv[1]
    FL, FR = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (20, 110)
    T = int(sys.argv[4]) if len(sys.argv) > 4 else 800
    t0 = time.time()
    cnf, P, scenes, S, OUT, target = build(mode, FL, FR, T)
    print(f"{mode} FL={FL} FR={FR} T={T}: vars {cnf.nvars} clauses {len(cnf.clauses)} "
          f"built {time.time()-t0:.0f}s", flush=True)
    sol = cnf.solve()
    rec = {"mode": mode, "FL": FL, "FR": FR, "T": T, "sat": sol is not None,
           "secs": round(time.time() - t0)}
    if sol is not None:
        a, b, X, Wt, pgL, pgR = scenes[0][4]
        bits, diffs = verify(P, sol, S, OUT, target, T, a, b, X, Wt, pgL, pgR)
        rec.update({"P": "".join(map(str, bits)), "X_rel": int(X - (scenes[0][2] - WL)),
                    "full_machine_window_diffs": diffs})
    print(json.dumps(rec), flush=True)
    with open("sat_reader.jsonl", "a") as fh:
        fh.write(json.dumps(rec) + "\n")
