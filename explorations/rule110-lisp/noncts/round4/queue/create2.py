"""Creation + read screen. X (Ebars, tiles may overlap in margins) is put
into a gap of D cells opened just before the raw leader K0 (machine
symmetry (0, D), D = 0 mod 56). Pipeline per X:
 Stage A (t_c = 6000 -> 17400, exact local scene, gap version):
   answer arrives (rej: tape NYYN; acc: tape YYNN), K0 is prepared.
   Require the right part [K0+D-20, K0+D+WR) to equal the control (gap, no X).
 Stage B (read scene t_in = 31500, gap version, as zscreen): the region
   [K0+RA, K0+D-20) is replaced by stage A's final cells (same Ebar time
   phase: 17400 = 31500 = 0 mod 30); then s_1 is read (rej path tapes
   NYYN/NNYY; acc path YYNN/YNYN). Classify the right part vs the gap
   control's Y/N reads (delays 30j) and the left part's V-equivalence.
Goal (AND gate): rej path forced-N, acc path normal, all debris V-standard.
Goal (AND-NOT): rej normal, acc forced-N.
    python create2.py D XLO XHI out.jsonl"""
import sys, json
import numpy as np
from lscene import *
from engine import ETHER
from create import open_gap, placements
ETH = np.array([int(c) for c in ETHER], dtype=np.uint8)
import os
import encoder as enc
VMULT = int(os.environ.get("VMULT", "2"))
VV = enc._left_v(["YNNNNN"]) * VMULT
TC, TA = 6000, 11400
TIN, TB = (31500 if VMULT == 1 else 47460), 3000
JS = range(-8, 9)
RA = -345
WR = 800

def build_tight(g, sc, K0, items, lo, hi, mingap=3):
    a, b = sc.ebar_to_seg(K0 + lo), sc.ebar_to_seg(K0 + hi)
    p, pb = phase_at(g, a), phase_at(g, b - TILE)
    new = g.copy(); new[a:b] = ETH[(p + np.arange(a, b)) % TILE]
    core_end = a - mingap
    for tiles, k, xr in items:
        arr, cl, cr = tiles[k]
        x = sc.ebar_to_seg(K0 + xr)
        if x + 16 < core_end + mingap or x < a or x + len(arr) > b or (cl - x) % TILE != p:
            return None
        s0 = max(0, core_end - x)
        new[x + s0:x + len(arr)] = arr[s0:]
        core_end = x + len(arr) - 16; p = (cr - x) % TILE
        new[x + len(arr):b] = ETH[(p + np.arange(x + len(arr), b)) % TILE]
    return new if p == pb else None

class Path:
    """One answer path: stage-A scene (tape_a) and two read scenes."""
    def __init__(self, D, tape_a, tapes_b, ra):
        self.D, self.RA = D, ra
        m = Machine(tape_a, ["YNNNNN"], TC + TA + 500, v=VV, left_periods=3, right_periods=2)
        self.K0 = K0 = [a for n, a, b in m.blocks if n == "K"][0]
        self.scA = Scene(m, m.row, TC, K0 - 1500, K0 + D + WR, TA + 50)
        self.gA = open_gap(self.scA, K0, D)
        self.refA = self.scA.run(self.gA, TA)
        self.B = {}
        for t in tapes_b:
            mb = Machine(t, ["YNNNNN"], TIN + TB + 500, v=VV, left_periods=3, right_periods=2)
            K0b = [a for n, a, b in mb.blocks if n == "K"][0]
            assert K0b == K0
            sc = Scene(mb, mb.row, TIN, K0 - 400, K0 + D + WR, TB + 30 * 8 + 50)
            g = open_gap(sc, K0, D)
            self.B[t] = (sc, g, {j: sc.run(g, TB - 30 * j) for j in JS})
        self.tapes_b = tapes_b

    def stageA(self, items):
        sc, K0, D = self.scA, self.K0, self.D
        seg = build_tight(self.gA, sc, K0, items, -10, D - 10)
        if seg is None:
            return None, None
        w = sc.run(seg, TA)
        split = (K0 + D - 20) - (K0 - 1500)
        dR = int((w[split:] != self.refA[split:]).sum())
        # final cells of the whole seg at TC+TA (for transplant)
        full = unpack(step_packed_n(pack(seg), TA), len(seg))
        return dR, full

    def stageB(self, fullA):
        """Transplant Ebar-frame [K0+RA, K0+D-20) from stage A into each read
        scene; return per tape [dY, jY, dN, jN, dL_vs_Y, dL_vs_N]."""
        K0, D = self.K0, self.D
        out = {}
        for t in self.tapes_b:
            sc, g, R = self.B[t]
            a_src = self.scA.ebar_to_seg(K0 + self.RA, TC + TA)
            b_src = self.scA.ebar_to_seg(K0 + D - 20, TC + TA)
            a_dst = sc.ebar_to_seg(K0 + self.RA)
            src = fullA[a_src:b_src]
            new = g.copy()
            # ether phase check at both ends
            if phase_at(new, a_dst - TILE) != phase_at(fullA, a_src - TILE) or \
               phase_at(new, a_dst + len(src)) != phase_at(fullA, b_src):
                out[t] = "phase"; continue
            new[a_dst:a_dst + len(src)] = src
            w = sc.run(new, TB)
            s = (K0 + D + 100) - (K0 - 400)
            rec = []
            for rt in self.tapes_b:
                Rr = self.B[rt][2]
                d = {j: int((w[s:] != Rr[j][s:]).sum()) for j in JS}
                j = min(d, key=lambda q: (d[q], abs(q)))
                rec += [d[j], j]
            rec += [int((w[:s] != self.B[rt][2][0][:s]).sum()) for rt in self.tapes_b]
            out[t] = rec
        return out

if __name__ == "__main__":
    D, xlo, xhi, outp = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rej = Path(D, "NYYN", ("NYYN", "NNYY"), -345)
    acc = Path(D, "YYNN", ("YYNN", "YNYN"), -200)
    # controls: no X -> stage A identical, stage B standard
    for P_ in (rej, acc):
        dR, full = P_.stageA([])
        print("control", P_.tapes_b, "stageA dR", dR, "stageB", P_.stageB(full), flush=True)
    E = ebar_tiles()
    p0 = phase_at(rej.gA, rej.scA.ebar_to_seg(rej.K0 - 10))
    fh = open(outp, "a"); n = 0
    for k2, x2, p1 in placements(rej.scA, rej.K0, E, max(-10, xlo), xhi, p0):
        for k1, x1, _ in placements(rej.scA, rej.K0, E, x2 + 5, xhi, p1):
            items = [(E, k2, x2), (E, k1, x1)]
            rec = {"D": D, "X": [[k2, x2], [k1, x1]]}
            dR, full = rej.stageA(items)
            if dR is None:
                continue
            rec["rejA"] = dR
            if dR == 0:
                rec["rejB"] = rej.stageB(full)
                dRa, fulla = acc.stageA(items)
                rec["accA"] = dRa
                if dRa == 0:
                    rec["accB"] = acc.stageB(fulla)
            fh.write(json.dumps(rec) + "\n"); n += 1
        fh.flush()
    print("done", n, flush=True)
