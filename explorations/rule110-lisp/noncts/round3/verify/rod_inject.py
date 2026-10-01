"""Inject localized E-infinity defects (found on the ring by ebg_vel.py /
ebg_search.py) into a long rod E^30 in ether and report what leaves the
rod and whether the rod is changed (compared with the unperturbed run;
exact engine; outside objects typed by my typer)."""
import sys, re
import numpy as np
import v3, vlib, engine
import ebg_search as S
import longrod as LR

H = 12


def ring_defect(k, x, bits, T0=S.T0):
    ring = S.VAR[0].copy()
    ring[x:x + k] = [int(c) for c in bits]
    r = engine.unpack(engine.step_packed_n(engine.pack(ring), T0), S.W)
    mis = (S.VAR != r[None, :])
    vi = mis.sum(axis=1).argmin()
    start, span = S.localized(mis[vi])
    idx = (np.arange(start - H, start + span + H)) % S.W
    return r[idx], S.VAR[vi][idx]


def inject(win_def, win_bg, n=30, T=3000, site=0):
    r, org = LR.rod(n)
    L = len(win_bg)
    hits = [i for i in range(0, len(r) - L) if np.array_equal(r[i:i + L], win_bg)]
    if not hits:
        return None
    i = hits[min(site, len(hits) - 1)]
    r2 = r.copy()
    r2[i:i + L] = win_def
    rs = vlib.runs(r)
    cl, cr = rs[0][2], rs[-1][2]
    pad = 2 * T + 200
    E = vlib.ETHER
    mk = lambda rr: np.concatenate([E[(np.arange(-pad, 0) + cl) % 14], rr,
                                    E[(np.arange(len(rr), len(rr) + pad) + cr) % 14]])
    a = engine.unpack(engine.step_packed_n(engine.pack(mk(r)), T), len(r) + 2 * pad)
    b = engine.unpack(engine.step_packed_n(engine.pack(mk(r2)), T), len(r) + 2 * pad)
    same = np.array_equal(a, b)
    ida = [(v3.base(nm), xx) for nm, xx, w, k in vlib.identify(a, -pad, T=T)]
    idb = [(v3.base(nm), xx) for nm, xx, w, k in vlib.identify(b, -pad, T=T)]
    return same, ida, idb, len(hits), i


if __name__ == "__main__":
    for line in open("ebg_vel.log"):
        m = re.search(r"v=([+-][\d.]+) count=(\d+) example=\((\d+), (\d+), (\d+), '(\d+)'", line)
        if not m:
            continue
        v, cnt, tr, k, x, bits = m.groups()
        wd, wb = ring_defect(int(k), int(x), bits)
        for site in (0, 3):
            res = inject(wd, wb, site=site)
            if res is None:
                print(f"v={v}: background window not found in the rod")
                break
            same, ida, idb, nh, i = res
            print(f"v={v} (example {bits}) site {site}/{nh}: identical to unperturbed: {same}; "
                  f"unperturbed {[n for n, _ in ida]} perturbed {[n for n, _ in idb]}")
