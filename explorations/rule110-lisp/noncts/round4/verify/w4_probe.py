"""Does the back's class (against Bbar) shift by a fixed amount per unit
added at the back? Rod E^10; n B's first (n = 0..8, each +1, single
class), then a Bbar probe (+ 5 B eaters) at a FIXED seed behind them.
If the class shift per B is beta != 0 mod 3, the probe's outcome (total
change minus n) cycles with period 3 in n."""
import hrun
import rodval

vlib = hrun.vlib


def probe(n, t0, k=5, S=80):
    items = [("E^10", 0, 0)] + [("B", 0, 60 + 40 * i) for i in range(n)]
    b = 60 + 40 * 9 + 100
    items.append(("Bbar", t0, b))
    items += [("B", 0, b + 60 + S * (i + 1)) for i in range(k)]
    row, org, placed = vlib.build(items, pad=400)
    T = (b + 60 + S * k) * 30 // 7 + 1500
    v = rodval.value(row, org, T)
    return None if v is None else v - 10 - n


if __name__ == "__main__":
    for t0 in (0, 1, 2):
        print(f"Bbar seed t0={t0}: probe outcome for n = 0..8 B's first:",
              [probe(n, t0) for n in range(9)], flush=True)
