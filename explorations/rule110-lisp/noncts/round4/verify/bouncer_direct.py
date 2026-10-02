"""Direct exact search for a perpetual bouncer (route 14 milestone), as an
independent check of theory 00:08 ("0 bouncers") that does not chain table
rows: it simulates the whole 3-object scene, so it also follows chains that
leave the enumerated tables.

Scene (rawscene, exact, hrun):  wall_L --40-- head --G2-- wall_R
  (wall_L, head) = every clean L-reflection of shuttle's L-table (the head
         moves left, hits wall_L and turns around);
  wall_R = every physical wall (one list representative per canonical form).
A run is ALIVE at time T if no defect has left [x_L - M - T/20, x_R + M + T/20]
(nothing escaped; walls may drift up to 1/20 cell per step, every free glider is
faster) and the content inside still changes between T and T + 420 (not
all stationary). Survivors at T1 are re-run to T2 = 10 T1; survivors there
are printed as candidates (to be inspected by hand).
Resumable: results appended to OUT (one line per (row, wall_L)); done keys
are skipped on restart.

python3 bouncer_direct.py TABLE_SNAPSHOT OUT [CHUNK]   (or: control)"""
import json
import os
import sys

import numpy as np

import hrun
import rawscene

vlib = hrun.vlib
T1, T2 = 6000, 60000
M = 60


def alive(row, org, starts_span, T):
    h = hrun.HRun(row, org)
    h.goto(T)
    xl, xr = starts_span
    big_lo, big_hi = org - T - 100, org + len(row) + T + 100
    r = h.cells(big_lo, big_hi)
    ds = vlib.defects(r)
    if not ds:
        return False, "empty"
    lo = min(d["lo"] for d in ds) + big_lo
    hi = max(d["hi"] for d in ds) + big_lo
    D = T // 20             # allowed wall drift (a counter-bouncer moves its walls);
    if lo < xl - M - D or hi > xr + M + D:   # every free glider is faster than 1/20
        return False, "escaped"
    a = h.cells(xl - M - D, xr + M + D)
    h.goto(T + 420)
    b = h.cells(xl - M - D, xr + M + D)
    if np.array_equal(a, b):
        return False, "frozen"
    return True, "alive"


def main(table, out, G2=150, chunk=None):
    """Start from every clean L-reflection (B-lattice head hits wall_L from the
    right and turns into a right-mover); add every physical wall as wall_R,
    G2 cells right of the head. Every perpetual bouncer contains an
    L-reflection, so within the L-table's scope (391 B-trains x 193 walls)
    this covers every bouncer, whatever the right-moving heads are."""
    rows = []
    walls = {}
    for l in open(table):
        r = json.loads(l)
        if r["side"] == "L":
            walls.setdefault(tuple(r["wall_canon"]), (r["wall"]["bits"], r["wall"]["pR"]))
            if r["kind"] == "reflect":
                rows.append(r)
    wl = sorted(walls.values())
    print(len(rows), "L-reflections,", len(wl), "physical walls", flush=True)
    done = set()
    if os.path.exists(out):
        for l in open(out):
            j = json.loads(l)
            done.add((j["head_i"], j["wall_j"], j["wr"]))
    fh = open(out, "a")
    n_alive = n_new = 0
    for r in rows:
        hd, wL = r["head"], r["wall"]
        for k, (wb, wp) in enumerate(wl):
            key = (r["head_i"], r["wall_j"], k)
            if key in done:
                continue
            if chunk is not None and n_new >= chunk:
                print("chunk done", n_new, flush=True)
                return
            row, org, st = rawscene.assemble([(wL["bits"], wL["pR"], 100), (hd["bits"], hd["pR"], 40),
                                              (wb, wp, G2)])
            span = (st[0], st[2] + len(wb))
            ok, why = alive(row, org, span, T1)
            if ok:
                ok, why = alive(row, org, span, T2)
                why = "ALIVE_T2" if ok else why + "_T2"
                n_alive += ok
            fh.write(json.dumps({"head_i": r["head_i"], "wall_j": r["wall_j"], "wr": k,
                                 "res": why}) + "\n")
            n_new += 1
        fh.flush()
    print("done; alive at T2:", n_alive, flush=True)


def control():
    """Classifier controls: (1) a B 4000 cells right of a C1 wall is ALIVE at
    T1 (in flight) and dead at T2 (B + C1 -> C2, theory's lnscan row:
    frozen); (2) two walls alone are 'frozen' at T1."""
    def bits_of(g):
        ds = vlib.defects(g.base)
        lo = min(d["lo"] for d in ds)
        hi = max(d["hi"] for d in ds)
        lo -= lo % 14
        return "".join(map(str, g.base[lo:hi])), (lo + g.w) % 14
    wb, wp = bits_of(vlib.LIB["C1"])
    bb, bp = bits_of(vlib.LIB["B"])
    row, org, st = rawscene.assemble([(wb, wp, 100), (bb, bp, 4000)])
    span = (st[0], st[1] + len(bb))
    r1 = alive(row, org, span, T1)
    r2 = alive(row, org, span, T2)
    assert r1 == (True, "alive") and not r2[0], (r1, r2)
    row, org, st = rawscene.assemble([(wb, wp, 100), (wb, wp, 300)])
    r3 = alive(row, org, (st[0], st[1] + len(wb)), T1)
    assert r3 == (False, "frozen"), r3
    print("bouncer_direct controls ok:", r1, r2, r3)


if __name__ == "__main__":
    if sys.argv[1] == "control":
        control()
    else:
        control()
        main(sys.argv[1], sys.argv[2], 150, int(sys.argv[3]) if len(sys.argv) > 3 else None)
