"""Step 2 of option (c) by simulation: raw-leader core variants K'.

The core of the first raw leader (Ebar-frame region [K-2, K+110) at t = 0,
holding [E5][E2], slip 6) is replaced by one library Ebar-speed object of
slip 6 at every placement (rest of the machine unchanged). Two scenes,
exact runs from t = 0: tape YYNN (an ACCEPTOR reaches K at ~14000) and
NYYN (a REJECTOR reaches K at ~8700). At T = 20000 (both reactions done,
before the leader reads) the Ebar-frame window [K-700, K+400) is compared
cell for cell with the plain machine:
  acc label 'P' = identical to plain (K' prepared exactly like K);
  rej label 'P' = identical to plain; otherwise the window is kept as a
  candidate alternative prepared leader (hash + census) for step 1/3.
Wanted: acc 'P' and rej != 'P' with no non-Ebar objects (clean).
Log: leader_screen.jsonl (resumable)."""
import json, os, hashlib
from splice import *

T_OUT = 20000
LOG = "leader_screen.jsonl"

def base(tape):
    m = Machine(tape, ["YNNNNN"], T_OUT + 2000, left_periods=2, right_periods=3)
    K = [a for n, a, b in m.blocks if n == "K"][0]
    r = Run(m.row, m.origin); r.step(T_OUT)
    sh = r.ebar_frame()
    return m, K, r.window(K - 700 + sh, K + 400 + sh).copy()

def run_variant(m, K, placements):
    c = ether_cut(m.row, m.origin + K - 2, search=3, tight=True)
    new = replace_exact(m.row, c, m.origin + K + 110, placements, 0, 0)
    if new is None:
        return None, None
    r = Run(new, m.origin); r.step(T_OUT - MAX_DT)
    sh = r.ebar_frame(T_OUT)
    h = r.history(K - 700 + sh, K + 400 + sh, MAX_DT)
    return h[-1], census(h)

def main():
    lib = [x for x in json.load(open(ROOT / "noncts" / "collider" / "gliders.json"))["gliders"]
           if x["velocity"] == "-4/15" and x["slip"] == 6]
    B = {t: base(t) for t in ("YYNN", "NYYN")}
    done = set()
    if os.path.exists(LOG):
        for line in open(LOG):
            d = json.loads(line); done.add((d["name"], d["k"], d["o"]))
    out = open(LOG, "a")
    for g in lib:
        tiles = glider_tiles(g["name"])
        for k in range(len(tiles)):
            for o in range(0, 112):
                if (g["name"], k, o) in done:
                    continue
                res = {}
                for tape, (m, K, ref) in B.items():
                    w, cs = run_variant(m, K, [(tiles, k, o)])
                    if w is None:
                        res = None; break
                    same = bool(np.array_equal(w, ref))
                    res[tape] = {"same": same, "diff": int((w != ref).sum()),
                                 "objs": [f"{kk}{x}" for x, y, kk in cs if kk != "E"],
                                 "h": hashlib.md5(w.tobytes()).hexdigest()[:10]}
                if res is None:
                    continue
                out.write(json.dumps({"name": g["name"], "k": k, "o": o, "r": res}) + "\n")
                out.flush()

if __name__ == "__main__":
    main()
