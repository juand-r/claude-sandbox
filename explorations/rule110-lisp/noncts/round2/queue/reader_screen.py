"""Step 1 of option (c): search for a clean ALTERNATIVE READER.

The core of a REJECTOR-prepared leader (Ebar-frame region [K-30, K+110)
at t_in = 32000, slip 2: [Ebar][E]) is replaced by one library Ebar-speed
object of slip 2 (collider gliders.json, velocity -4/15) at every
placement. Two scenes from exact runs of the plain machine at t_in: the
leader about to read a Y (tape NYYN, read 1) and an N (NNYY).
Each candidate is run to T2 = 34000 and the Ebar-frame window
[K-700, K+700) is compared CELL FOR CELL with the plain outcomes OY (Y
read) and ON (N read). Labels per scene: Y / N / '-' (neither).
A forced-N reader is (N, N); inverted (N, Y); forced-Y (Y, Y).
Log: reader_screen.jsonl (resumable)."""
import json, os, sys
from splice import *

T_IN, T2 = 32000, 34000
LOG = "reader_screen.jsonl"

def base_state(tape):
    m = Machine(tape, ["YNNNNN"], T2 + 2000, left_periods=4, right_periods=3)
    K = [a for n, a, b in m.blocks if n == "K"][0]
    r = Run(m.row, m.origin)
    r.step(T_IN)
    row_in = r.window(0, r.width).copy()
    sh_in = r.ebar_frame()
    r.step(T2 - T_IN)
    sh2 = r.ebar_frame()
    out = r.window(K - 700 + sh2, K + 700 + sh2).copy()
    return m, K, row_in, sh_in, sh2, out

def run_candidate(m, K, row_in, sh_in, sh2, placements, lo_rel, hi_rel):
    c, c2 = K + lo_rel + sh_in, K + hi_rel + sh_in       # array coords
    new = replace_exact(row_in, c, c2, placements, 0, 0)
    if new is None:
        return None
    r = Run(new, 0)
    r.t = T_IN
    r.step(T2 - T_IN)
    return r.window(K - 700 + sh2, K + 700 + sh2)

def main():
    import json as _j
    lib = [x for x in _j.load(open(ROOT / "noncts" / "collider" / "gliders.json"))["gliders"]
           if x["velocity"] == "-4/15"]
    S = {t: base_state(t) for t in ("NYYN", "NNYY")}
    OY, ON = S["NYYN"][5], S["NNYY"][5]
    done = set()
    if os.path.exists(LOG):
        for line in open(LOG):
            d = json.loads(line); done.add((d["mode"], d["name"], d["k"], d["o"]))
    out = open(LOG, "a")
    modes = [("core", 2, -30, 110, None)]
    for mode, slip, lo_rel, hi_rel, _ in modes:
        for g in lib:
            if g["slip"] != slip:
                continue
            tiles = glider_tiles(g["name"])
            for k in range(len(tiles)):
                for o in range(0, hi_rel - lo_rel):
                    if (mode, g["name"], k, o) in done:
                        continue
                    labels, dists = [], []
                    ok = True
                    for tape in ("NYYN", "NNYY"):
                        m, K, row_in, sh_in, sh2, _o = S[tape]
                        w = run_candidate(m, K, row_in, sh_in, sh2, [(tiles, k, o)], lo_rel, hi_rel)
                        if w is None:
                            ok = False; break
                        dY, dN = int((w != OY).sum()), int((w != ON).sum())
                        labels.append("Y" if dY == 0 else "N" if dN == 0 else "-")
                        dists.append([dY, dN])
                    if not ok:
                        continue
                    out.write(json.dumps({"mode": mode, "name": g["name"], "k": k, "o": o,
                                          "lab": "".join(labels), "d": dists}) + "\n")
                    out.flush()

if __name__ == "__main__":
    main()
