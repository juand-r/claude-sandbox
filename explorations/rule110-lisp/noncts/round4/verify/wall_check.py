"""Independent check of objects 23:11: E-bg carries walls at exactly -3/5 (lab)
between two phases of the E-bg (Z/50 phase h = 2t - 5s).

From my cone_brute witness (window of w zeros in the E-bg, bg time phase 0,
alignment 7), evolve with my own stepper; at several times, segment the row
into maximal runs that equal SOME E-bg phase (t-offset 0..4, shift 0..9) and
report the runs (position, phase h) and the speed of the leftmost boundary.
Control: in the unperturbed bg, the whole row is one run of one phase."""
import numpy as np
from cone_brute import TILE, step

N, T = 1400, 600


def bg_rows(n):
    r = TILE[np.arange(n) % 10][None, :]
    rows = [r]
    for _ in range(4):
        rows.append(step(rows[-1]))
    return [x[0] for x in rows]


BG = bg_rows(N + 40)


def phase_map(row, t):
    """For each cell i, the set of E-bg phases h (as (dt, s)) whose bg row
    matches row on [i, i+10). Phase (dt, s): bg at time t+dt shifted by s."""
    out = []
    for i in range(0, len(row) - 10):
        hs = []
        for dt in range(5):
            for s in range(10):
                ref = BG[(t + dt) % 5]   # bg(t') for t' = t + dt, ignoring the global roll
                # account for the bg's own drift: bg(t+5k) = roll(bg(t), 2k)
                k = (t + dt) // 5
                if np.array_equal(row[i:i + 10], ref[(np.arange(i, i + 10) - 2 * k - s) % 10 + 20]):
                    hs.append((dt, s))
        out.append(hs)
    return out


def runs(row, t):
    pm = phase_map(row, t)
    res, i = [], 0
    while i < len(pm):
        if len(pm[i]) == 0:
            i += 1
            continue
        h = pm[i][0]
        j = i
        while j < len(pm) and h in pm[j]:
            j += 1
        if j - i >= 30:
            res.append((i, j, h, 2 * h[0] - 5 * h[1]))
        i = j
    return res


if __name__ == "__main__":
    w, a0 = 10, N // 2
    row = TILE[(np.arange(N) + 7) % 10].copy()
    ref = row.copy()
    row[a0:a0 + w] = 0
    cur, rr = row[None, :], ref[None, :]
    edges = {}
    for t in range(1, T + 1):
        cur, rr = step(cur), step(rr)
        if t in (100, 200, 300, 400, 500, 600):
            d = np.nonzero(cur[0] != rr[0])[0]
            edges[t] = d[0]
            rs = runs(cur[0][T + 5:N - T - 5] if False else cur[0][50:N - 50], t)
            print(t, "left edge", d[0], "runs (lo, hi, (dt,s), h mod 50):",
                  [(a + 50, b + 50, h, hh % 50) for a, b, h, hh in rs])
    ts = sorted(edges)
    print("edge speeds:", [(edges[b] - edges[a]) / (b - a) for a, b in zip(ts, ts[1:])])
    rs0 = runs(rr[0][50:N - 50], 600)
    print("control (no perturbation):", len(rs0), "run(s)", [(a, b, h) for a, b, h, _ in rs0])
