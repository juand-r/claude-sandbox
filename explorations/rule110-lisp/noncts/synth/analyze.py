"""Re-simulate saved solutions (row0, lo, pl, pr) and list the objects
present at t = 0 and at late times (identify.describe: period, library
name matched by bits + ether phases, slip). Usage:
  python analyze.py FILE.jsonl [T]"""
import json, sys
import numpy as np
from identify import describe
from r110sat import ether_bit, simulate


def objects(rec, T, window=400):
    row0 = np.array([int(c) for c in rec["row0"]], np.uint8)
    lo = rec["lo"]
    pl, pr = rec.get("pl", rec.get("pfl")), rec.get("pr", rec.get("pfr"))
    pad = 2 * T + window + 100
    left = np.array([ether_bit(pl, 0, x) for x in range(lo - pad, lo)], np.uint8)
    right = np.array([ether_bit(pr, 0, x) for x in range(lo + len(row0), lo + len(row0) + pad)], np.uint8)
    h = simulate(np.concatenate([left, row0, right]), T + 40)
    off = pad - lo
    out = {}
    for t in (0, T):
        out[t] = [(a - off, b - off, per, nm, sl)
                  for a, b, per, nm, bits, sl in describe(h, t, off - window, off + window, merge=2)]
    return out


if __name__ == "__main__":
    T = int(sys.argv[2]) if len(sys.argv) > 2 else 800
    for l in open(sys.argv[1]):
        r = json.loads(l)
        if not r.get("sat") or "row0" not in r:
            continue
        o = objects(r, T)
        key = {k: r[k] for k in r if k in ("spec", "k", "pRP", "pRO", "pR", "slip", "X", "P", "O")}
        print(json.dumps(key))
        print("   t=0 :", o[0])
        print(f"   t={T}:", o[T])
