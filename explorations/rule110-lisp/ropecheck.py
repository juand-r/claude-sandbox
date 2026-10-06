"""Check the debris rope against the plain event engine on a long program.

    python ropecheck.py run MODE OUTDIR [--every N] [--depth D] [--v V] SRC
    python ropecheck.py compare DIR_A DIR_B

`run` evaluates SRC on gliders (GasReads, as lisp_gliders does) with MODE
plain (every event in the event list; checkpointed every 5,000 reads so a
day-long run survives a restart), rope (the debris rope with stretch
jumps) or slowrope (the rope crossing every unit one by one). Every N reads (at the start of
that read's loop iteration, so at the same t in both modes) it saves the
gas items to OUTDIR/snap_<read>.npz; at the end OUTDIR/final.npz also
holds the read outcomes and census counts.

`compare` checks two such directories: equal t at every common snapshot,
and the items right of the rope's leftmost item equal item for item (the
rope keeps the debris left of that outside the event list); at the end
equal outcomes and census counts.
"""

import argparse
import os
import sys
import time

import numpy as np

import gasc
from experiments import block_gaps
from gasrun import GasReads
from lisp_bus import LispBus

CKPT_EVERY = 5000
GAP_MARGIN = 7.5          # lisp_gliders' default margin for the gap rule
ROPE_KEYS = ("units", "crossings", "memo", "misses", "prefix", "jumps", "jumped")


def _items(g):
    kind, ids, ph, left, _, _, _ = g.list_items(-gasc.FAR, gasc.FAR)
    keep = (kind == gasc.PART) | (kind == gasc.COMP)
    return np.stack([kind[keep], ids[keep], ph[keep], left[keep]]).astype(np.int64)


def run(mode, outdir, src, every, depth, v, ckpt_every=CKPT_EVERY):
    os.makedirs(outdir, exist_ok=True)
    lb = LispBus(src, depth)
    comp = lb.compile_bus()
    pm = comp.pm
    tape = pm.encode(comp.initial_tape(lb.values))
    apps = pm.appendants()
    n_reads = comp.p * pm.B
    if v is None:
        gap = max(g for *_, g in block_gaps(tape, apps, n_reads))
        v = int(gap / GAP_MARGIN) + 1
    print(f"{mode}: {n_reads} reads, v = {v}", flush=True)
    er = None

    def log(msg):
        print(msg, flush=True)
        if not msg.startswith("[gas] read "):
            return
        r = int(msg.split()[2].rstrip(":"))
        path = os.path.join(outdir, f"snap_{r}.npz")
        if r % every == 0 and not os.path.exists(path):
            g = er.run
            info = g.rope_info() if mode != "plain" else {}
            np.savez(path, t=g.t, events=g.n_events, items=_items(g),
                     rope=np.array([info.get(k, -1) for k in ROPE_KEYS]))

    ckpt = os.path.join(outdir, "plain.ckpt") if mode == "plain" else None
    t0 = time.time()
    er = GasReads(tape, apps, v, n_reads, log=log, checkpoint=ckpt,
                  ckpt_every=ckpt_every, rope=(mode != "plain"),
                  rope_jumps=(mode == "rope"))
    out = er.run_reads()
    g = er.run
    np.savez(os.path.join(outdir, "final.npz"), t=g.t, events=g.n_events,
             items=_items(g), outcome=np.array(list(out)),
             n_ebar=np.array([-1 if x is None else x for x in er.watch.n_ebar]))
    if mode != "plain":
        print("rope:", g.rope_info(), flush=True)
    print(f"{mode} done: {time.time() - t0:.0f}s, t = {g.t}, {g.n_events} events, "
          f"outcome {out.count('Y')} Y {out.count('N')} N {out.count('!')} ! "
          f"{out.count('.')} unread", flush=True)


def _suffix_equal(a, b):
    """a, b: item arrays (4 x n, sorted by left). The one that starts
    further right is the rope's; compare the other's items from there."""
    if a.shape[1] == 0 or b.shape[1] == 0:
        return a.shape == b.shape, 0
    if a[3, 0] < b[3, 0]:
        a, b = b, a
    sub = b[:, b[3] >= a[3, 0]]
    return sub.shape == a.shape and bool((sub == a).all()), a.shape[1]


def compare(da, db, partial=False):
    """partial: compare the snapshots both runs have so far (runs still
    going); otherwise both must have finished."""
    names = sorted(set(os.listdir(da)) & set(os.listdir(db)))
    snaps0 = [n for n in names if n.startswith("snap_")]
    if partial and not snaps0:
        print("MISMATCH: no common snapshot")
        return False
    if not partial and "final.npz" not in names:
        print(f"MISMATCH: final.npz missing in {da if 'final.npz' not in os.listdir(da) else db}")
        return False
    snaps = sorted((n for n in names if n.startswith("snap_")),
                   key=lambda n: int(n[5:-4]))
    ok = True
    for n in snaps + (["final.npz"] if "final.npz" in names and not partial else []):
        a, b = np.load(os.path.join(da, n)), np.load(os.path.join(db, n))
        same_t = int(a["t"]) == int(b["t"])
        eq, m = _suffix_equal(a["items"], b["items"])
        line = f"{n}: t {'equal' if same_t else 'DIFFERENT'}, {m} items right of the rope {'equal' if eq else 'DIFFERENT'}"
        good = same_t and eq
        if n == "final.npz":
            o = (a["outcome"] == b["outcome"]).all() and a["outcome"].shape == b["outcome"].shape
            e = (a["n_ebar"] == b["n_ebar"]).all() and a["n_ebar"].shape == b["n_ebar"].shape
            line += f", outcomes {'equal' if o else 'DIFFERENT'}, census counts {'equal' if e else 'DIFFERENT'}"
            good = good and o and e
        ok = ok and good
        print(line)
    print(("ALL EQUAL" + (" (so far)" if partial else "")) if ok else "MISMATCH")
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("mode", choices=("plain", "rope", "slowrope"))
    r.add_argument("outdir")
    r.add_argument("src")
    r.add_argument("--every", type=int, default=10000)
    r.add_argument("--depth", type=int, default=4)
    r.add_argument("--v", type=int, default=None)
    r.add_argument("--ckpt-every", type=int, default=CKPT_EVERY)
    c = sub.add_parser("compare")
    c.add_argument("a")
    c.add_argument("b")
    c.add_argument("--partial", action="store_true")
    a = ap.parse_args()
    if a.cmd == "run":
        run(a.mode, a.outdir, a.src, a.every, a.depth, a.v, a.ckpt_every)
    else:
        sys.exit(0 if compare(a.a, a.b, a.partial) else 1)


if __name__ == "__main__":
    main()
