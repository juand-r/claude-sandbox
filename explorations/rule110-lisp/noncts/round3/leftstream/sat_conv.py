"""SAT for theory's wall converter (THEORY.md s.6.5, W1/W2) [search]:
a free co-moving object B (period (15,-4), width WB, slip sB) parked right
of R2 = E^n's back (minimal ether gap), and a front op F (I_L by default,
which launches a front->back wall; verify 06:26). Jointly for n in --ns:
  (stable)   E^n | B           -> at T2: E^n | B, undisturbed (same cells)
  (convert)  F + E^n | B       -> at T2: E^n (any) | B (any) | X
with X a free (3,2) train of slip sX (default 6 = an INC train for R1;
--X I_L forces X = I_L exactly). Slip: slip(F) + 0 = sX + 0 (F's unit
enters at the front, one unit leaves the back as X).
Usage: python sat_conv.py WB sB WX T2 [--ns 2,3] [--F I_L|Z_L] [--X free|I_L]
Results: sat_conv_results.jsonl."""
import argparse, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sat_inc import CNF, TILE, TrainVar, Scene, make_window, placements_by_class, en_item, MARGIN  # noqa
from react import Fixed  # noqa

OUT = os.path.join(HERE, "sat_conv_results.jsonl")
TRAINS = {"I_L": ("111110111110111110001110", 6),
          "Z_L": ("111110111110111000111011", 8)}


def back_piece(E, tauE, xE, B, gap=0):
    """(tau, x) for B right of E (E as piece (tauE, xE)) with consistent
    ether and the smallest gap >= `gap` cells between the pieces."""
    rph = (4 * tauE + E.pR - xE) % TILE
    end = xE + E.W + tauE
    for x in range(end + gap, end + gap + 80):
        for tau in range(B.period[0]):
            if (4 * tau - x) % TILE == rph and x - tau >= end + gap:
                return tau, x
    raise ValueError("no placement")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for a in ("WB", "sB", "WX", "T2"):
        ap.add_argument(a, type=int)
    ap.add_argument("--ns", default="2,3")
    ap.add_argument("--F", default="I_L")
    ap.add_argument("--X", default="free")
    ap.add_argument("--k", type=int, default=0, help="class of F vs E (its working class is 0)")
    ap.add_argument("--bgap", type=int, default=0)
    ap.add_argument("--control2", type=int, default=None,
                    help="positive control: B parked at gap 30 (untouched), "
                         "target = copy of stable E^(n+1)|B at gap CONTROL2, no X")
    ap.add_argument("--control3", action="store_true",
                    help="positive control: B parked at gap 30; S0 = E^(n+1) placed "
                         "where I_L's output really is (found by simulation) | B")
    ap.add_argument("--shift", default="0,0",
                    help="control3 only: build S0 translated so that the copy needs (q, dx)")
    ap.add_argument("--control", action="store_true",
                    help="code-path control: no F, no X (convert = stable copy)")
    A = ap.parse_args()
    ns = [int(v) for v in A.ns.split(",")]
    fbits, fs = TRAINS[A.F]
    t = time.time()
    cnf = CNF()
    Fi = Fixed(cnf, fbits, fs, (3, 2), name=A.F)
    B = TrainVar(cnf, A.WB, 15, -4, A.sB, name="B")
    sX = fs % TILE
    if A.X == "free":
        X = TrainVar(cnf, A.WX, 3, 2, sX, name="X")
    else:
        X = Fixed(cnf, TRAINS[A.X][0], TRAINS[A.X][1], (3, 2), name=A.X)
    scenes = []
    for n in ns:
        E = en_item(cnf, n)
        T2 = A.T2
        tauE, xE = placements_by_class(Fi, (0, 0), E, Fi.W + 6)[A.k]
        tb, xb = back_piece(E, tauE, xE, B, 30 if A.control2 is not None else A.bgap)
        # (stable) E^n | B alone, same pieces: at T2 both undisturbed
        if A.control3:
            tb, xb = back_piece(E, tauE, xE, B, 30)
            E1 = en_item(cnf, n + 1)
            # simulate I_L + E^n alone (exact), locate E^(n+1) at T2
            import numpy as np
            from r110sat import simulate as rsim, ether_bit as eb
            def piece_cells(item, tau, x):
                """{global x: bit} of an item placed as piece (tau, x) at
                t = 0: canonical row 0 (ether 0 | bits | ether pR) evolved
                tau steps, light cone [x - tau, x + W + tau)."""
                P = 40
                r = np.concatenate([
                    np.array([eb(0, 0, u) for u in range(-P, 0)], np.uint8),
                    np.array(item.bits, np.uint8),
                    np.array([eb(item.pR, 0, u) for u in range(item.W, item.W + P)], np.uint8)])
                hh = rsim(r, tau)
                return {x + u: int(hh[tau, u + P]) for u in range(-tau, item.W + tau)}
            cells = {}
            cells.update(piece_cells(Fi, 0, 0))
            cells.update(piece_cells(E, tauE, xE))
            lo_, hi_ = min(cells), max(cells) + 1
            pL = (4 * 0 - 0) % TILE
            pR = (4 * tauE + E.pR - xE) % TILE
            pad = 2 * T2 + 60
            pM = fs % TILE        # ether between F (slip fs, at (0,0)) and E
            mid_ = np.array([cells.get(x, eb(pL if x < 0 else (pM if x < xE else pR), 0, x))
                             for x in range(lo_, hi_)], np.uint8)
            left = np.array([eb(pL, 0, x) for x in range(lo_ - pad, lo_)], np.uint8)
            right = np.array([eb(pR, 0, x) for x in range(hi_, hi_ + pad)], np.uint8)
            h = rsim(np.concatenate([left, mid_, right]), T2)
            class _S: pass
            Sx = _S(); Sx.lo, Sx.hi = lo_, hi_
            off = pad - Sx.lo
            found = None
            P1 = 60
            r1 = np.concatenate([
                np.array([eb(0, 0, u) for u in range(-P1, 0)], np.uint8),
                np.array(E1.bits, np.uint8),
                np.array([eb(E1.pR, 0, u) for u in range(E1.W, E1.W + P1)], np.uint8)])
            h1 = rsim(r1, 15)
            for tau in range(15):
                elo, ehi = E1.extent(tau)
                pat = h1[tau, elo + P1:ehi + P1]
                rowT = h[T2]
                for delta in range(Sx.lo - T2 - elo, Sx.hi + T2 - ehi):
                    a = delta + elo + off
                    if np.array_equal(rowT[a:a + len(pat)], pat):
                        found = (tau, delta)
                        break
                if found:
                    break
            assert found, "I_L output E^(n+1) not found"
            q0, dx0 = map(int, A.shift.split(","))
            tS = T2 - q0
            tau0 = (found[0] - tS) % 15
            qq = (tau0 + tS) // 15
            x0 = found[1] - dx0 + 4 * qq
            tauB, deltaB = Scene.undisturbed(B, tb, xb, T2)
            tb0 = (tauB - tS) % 15
            qb = (tb0 + tS) // 15
            xb0 = deltaB - dx0 + 4 * qb
            S0 = Scene(cnf, T2, [(E1, tau0, x0), (B, tb0, xb0)])
            # E1 is checked exactly at T2 (as in the stable constraint):
            oE = Scene.undisturbed(E1, tau0, x0, T2)
            Eref = E1
        elif A.control2 is not None:
            E1 = en_item(cnf, n + 1)
            tb1, xb1 = back_piece(E1, tauE, xE, B, A.control2)
            S0 = Scene(cnf, T2, [(E1, tauE, xE), (B, tb1, xb1)])
            oE = Scene.undisturbed(E1, tauE, xE, T2)
            Eref = E1
        else:
            S0 = Scene(cnf, T2, [(E, tauE, xE), (B, tb, xb)])
            oE = Scene.undisturbed(E, tauE, xE, T2)
            Eref = E
        oB = Scene.undisturbed(B, tb, xb, T2)
        # stable: the composite is (15,-4)-periodic at the end, and the
        # E part is exactly undisturbed at T2 (E's exact extent)
        for x in range(S0.lo - (T2 - 15) + 2, S0.hi + (T2 - 15) - 2):
            a, b = S0.lit(T2, x - 4), S0.lit(T2 - 15, x)
            if isinstance(a, bool) and isinstance(b, bool):
                if a != b:
                    cnf.add([])
            elif isinstance(a, bool):
                cnf.add([b if a else -b])
            elif isinstance(b, bool):
                cnf.add([a if b else -a])
            else:
                cnf.equal(a, b)
        elo, ehi = Eref.extent(oE[0])
        for x in range(oE[1] + elo, oE[1] + ehi):
            a, b = S0.lit(T2, x), Eref.st.lit(oE[0], x - oE[1])
            if isinstance(a, bool) and isinstance(b, bool):
                if a != b:
                    cnf.add([])
            elif isinstance(b, bool):
                cnf.add([a if b else -a])
            elif isinstance(a, bool):
                cnf.add([b if a else -b])
            else:
                cnf.equal(a, b)
        # (convert) F left of E^n | B, F in its class k w.r.t. E
        pcs = [(E, tauE, xE), (B, tb, xb)]
        if not A.control:
            pcs = [(Fi, 0, 0)] + pcs
        S = Scene(cnf, T2, pcs,
                  window=make_window(T2, 0, xb + B.W + tb,
                                     -4 / 15, 2 / 3, margin=MARGIN))
        scenes += [S0, S]
        # at T2: [ether][copy of S0's rows (time T2 - q, shifted)][X]
        front = xE - 4 * T2 / 15
        L = int(front - 30)
        splitX = int(xb + B.W - 4 * T2 / 15 + 30)
        S.ether(T2, S.lo - T2, L, S.p_left)
        opts = []
        for q in range(15):
            t0 = T2 - q
            for dx in range(-40, 41):
                # convert row T2 [x] == stable row t0 [x - dx]
                lo0, hi0 = L - dx, splitX - dx
                if lo0 < S0.lo - t0 or hi0 > S0.hi + t0:
                    continue
                m = cnf.new_var()
                for x in range(L, splitX):
                    a = S.lit(T2, x)
                    b = S0.lit(t0, x - dx)
                    if isinstance(a, bool) and isinstance(b, bool):
                        if a != b:
                            cnf.add([-m])
                        continue
                    if isinstance(b, bool):
                        cnf.add([-m, a if b else -a])
                    elif isinstance(a, bool):
                        cnf.add([-m, b if a else -b])
                    else:
                        cnf.add([-m, -a, b]); cnf.add([-m, a, -b])
                opts.append(m)
        cnf.add(opts)
        if A.control or A.control2 is not None or A.control3:
            S.ether(T2, splitX, S.hi + T2, S.p_right)
        else:
            S.is_item(T2, splitX, S.hi + T2, X, far_right=S.p_right)
    sol = cnf.solve()
    rec = {"control": A.control, "control2": A.control2, "control3": A.control3, "WB": A.WB, "sB": A.sB, "WX": A.WX, "T2": A.T2, "ns": ns, "F": A.F,
           "X": A.X, "k": A.k, "bgap": A.bgap, "sat": sol is not None,
           "secs": round(time.time() - t, 1)}
    if sol is not None:
        rec["B"] = "".join(map(str, B.decode(sol)))
        if A.X == "free":
            rec["Xbits"] = "".join(map(str, X.decode(sol)))
        rec["sim_ok"] = all(Sc.check_sat_vs_sim(sol) for Sc in scenes)
        rec["rows0"] = ["".join(map(str, Sc.row(sol, 0))) for Sc in scenes]
        rec["frames"] = [(Sc.lo, Sc.p_left, Sc.p_right) for Sc in scenes]
    print(json.dumps({q: v for q, v in rec.items() if q != "rows0"}), flush=True)
    with open(OUT, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
