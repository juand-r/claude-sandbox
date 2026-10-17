"""Recorded glider runs for the Lisp-on-Rule-110 dashboard (an HTML replay).

    python dashboard.py record OUTDIR [NAME ...]   # run presets, write NAME.json
    python dashboard.py build OUTDIR PAGE.html     # inline them into the page

A browser cannot run these computations (car alone is 6.5e9 generations
of about 2e7 cells), so the page replays recordings of the real engine:
gasrun.GasReads with the plain event engine (every glider kept, no rope)
and the light read check, exactly as lisp110.py --gliders runs it. Per
run it keeps:

- overview: a space-time image (x: Ebar-frame position, the frame in
  which the table stands still; y: time) of particle counts by family
  (A: ossifier gliders, E: table, moving data and debris, C/other:
  collisions), with the unread table drawn from the layout;
- micro: exact Rule 110 cells (window + local stepping, exact by the
  light cone) around the read under way, at a few reads;
- the read outcomes, read times, CTS queue length, and the decoding of
  the value from the last pass's reads (experiments.decode_reads).
"""

import base64
import io
import json
import os
import sys
import time
from collections import deque

import numpy as np

PRESETS = {
    "quote": ("(quote a)", 4),
    "car": ("(car (quote (a b)))", 4),
    "cdr": ("(cdr (quote (a b)))", 4),
    "cons": ("(cons (quote a) (quote (b)))", 4),
    "atom": ("(atom? (quote (a)))", 4),
    "eq": ("(eq? (quote a) (quote b))", 4),
    "cond": ("(cond ((eq? (quote a) (quote b)) (quote x)) (t (quote y)))", 4),
}
N_ROWS = 360          # overview rows (frames)
N_COLS = 720          # overview columns
OVERSAMPLE = 2        # frames recorded per overview row (rows pick the nearest)
N_MICRO = 24          # cell windows per run
MICRO_W, MICRO_H = 320, 200
MICRO_NEAR = 80       # an ossifier glider this close to debris is about to cross it
FAMS = ("A", "C", "E", "X")

# colors of the overview (it is a dark "scope" image in both page themes)
BG = np.array([14, 17, 26])
TABLE = np.array([58, 66, 86])
E_LO, E_HI = np.array([24, 52, 92]), np.array([92, 160, 235])
A_COL = np.array([255, 178, 64])
X_COL = np.array([255, 92, 140])


def _png(rgb):
    from PIL import Image
    buf = io.BytesIO()
    Image.fromarray(rgb.astype(np.uint8)).save(buf, format="PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def _families(g, kind, ids):
    ob, ooff, ow, op, od = g._orbit_flat()
    oid = np.where(kind == 1, ids, 0).astype(np.int64)
    p_, d_ = op[oid], od[oid]
    fam = np.full(len(kind), 3, np.int8)                       # X: other, composites
    part = kind == 1
    fam[part & (3 * d_ == 2 * p_)] = 0                         # A
    fam[part & (d_ == 0)] = 1                                  # C
    fam[part & (15 * d_ == -4 * p_)] = 2                       # E
    return fam


def _cells(g, lo, w, h):
    """Exact rows t..t+h-1 of cells [lo, lo + w): a window wider by h on each
    side, stepped locally (influence travels one cell per step)."""
    from engine import pack, step_packed, unpack
    g.ensure(lo - h, lo + w + h)
    words = pack(g.window(lo - h, lo + w + h))
    rows = []
    for _ in range(h):
        rows.append(unpack(words, w + 2 * h)[h:h + w])
        words = step_packed(words)
    return np.array(rows, np.uint8)


def _collision(g, x_read):
    """Left edge of a collision under way (a composite item), or of an
    ossifier glider about to cross debris, nearest to x_read; None if
    neither exists."""
    import gasc
    kind_, ids, ph, left, width, _, _ = g.list_items(-gasc.FAR, gasc.FAR)
    keep = kind_ < 3
    kind_, ids, left, width = kind_[keep], ids[keep], left[keep], width[keep]
    comp = left[kind_ == 2]
    if len(comp):
        return int(comp[np.argmin(np.abs(comp - x_read))])
    fam = _families(g, kind_, ids)
    nxt = np.r_[left[1:], np.iinfo(np.int64).max]
    gap = nxt - (left + width)
    near = np.nonzero((fam == 0) & (np.r_[fam[1:], -1] == 2) & (gap < MICRO_NEAR))[0]
    if len(near):
        return int(left[near[np.argmin(np.abs(left[near] - x_read))]])
    return None


def _micro_rgb(cells):
    """Ether faint, cells that break the ether's spatial period (gliders) bright."""
    a = cells.astype(np.int16)
    d = a[:, 14:] != a[:, :-14]
    m = np.zeros(a.shape, bool)
    m[:, 14:] |= d
    m[:, :-14] |= d
    rgb = np.zeros(a.shape + (3,), np.uint8)
    rgb[...] = (16, 19, 28)
    rgb[a == 1] = (44, 50, 66)
    rgb[m & (a == 0)] = (64, 38, 22)
    rgb[m & (a == 1)] = (255, 178, 64)
    return rgb


def record(name, src, depth):
    from encoder import _left_v
    from experiments import block_gaps, decode_reads
    from gasrun import GasReads
    from lisp import run as lisp_run
    from lisp_bus import ATOM, CLOSE, OPEN, PAD, LispBus, code, kind
    import gasc

    lb = LispBus(src, depth)
    comp = lb.compile_bus()
    pm = comp.pm
    tape = pm.encode(comp.initial_tape(lb.values))
    apps = pm.appendants()
    n = comp.p * pm.B
    gaps = [g for *_, g in block_gaps(tape, apps, n)]
    v = int(max(gaps) / 7.5) + 1 if gaps else _left_v(apps)
    # reference CTS: reads and queue length
    q, ref, qlen = deque(tape), [], []
    for r in range(n):
        qlen.append(len(q))
        ch = q.popleft()
        ref.append(ch)
        if ch == "Y":
            q.extend(apps[r % len(apps)])
    ref = "".join(ref)

    er = GasReads(tape, apps, v, n, log=lambda *a: None, rope=False, census="light")
    g = er.run
    regs = er.regs[:n]
    xs = [a for a, _ in regs if a is not None] + [b for _, b in regs if b is not None]
    span = max(xs) - min(0, min(xs))
    x_lo, x_hi = min(0, min(xs)) - span // 40, max(xs) + span // 40
    # frames at a fixed time step from an estimate of the run's length; the
    # rows of the image are picked from them once the length is known
    est = 30 * v * n
    dt_frame = max(1, est // (N_ROWS * OVERSAMPLE))
    frames = []                                     # (t, reads settled, events, counts[4, N_COLS])

    def snap():
        kind_, ids, ph, left, width, _, _ = g.list_items(-gasc.FAR, gasc.FAR)
        keep = kind_ < 3
        fam = _families(g, kind_[keep], ids[keep])
        x = left[keep] - g.ebar_frame(g.t)
        b = ((x - x_lo) * N_COLS // (x_hi - x_lo)).astype(np.int64)
        m = (b >= 0) & (b < N_COLS)
        cnt = np.zeros((4, N_COLS), np.int32)
        for f in range(4):
            cnt[f] = np.bincount(b[m & (fam == f)], minlength=N_COLS)[:N_COLS]
        settled = sum(1 for s in er.watch.state if s in "YN!")
        frames.append((g.t, settled, g.n_events, cnt))

    micro = []                                      # (read j, t, rgb)
    next_micro = [0]
    adv = g.advance_to
    smp = er._sample

    def adv2(t):
        r = adv(t)
        while g.t >= len(frames) * dt_frame:
            snap()
        return r

    def smp2(pending, d):
        smp(pending, d)
        if not pending or len(micro) >= N_MICRO:
            return
        j = pending[0]
        if er.watch.state[j] != "r" or j < next_micro[0]:
            return
        c = _collision(g, regs[j][0] + g.ebar_frame(g.t))
        if c is None:
            return                                  # nothing colliding now: try the next sample
        micro.append((j, g.t, _micro_rgb(_cells(g, c - MICRO_W // 3, MICRO_W, MICRO_H))))
        next_micro[0] = j + max(1, n // N_MICRO)

    g.advance_to, er._sample = adv2, smp2
    t0 = time.time()
    out = er.run_reads()
    wall = time.time() - t0
    snap()
    if out != ref:
        raise AssertionError(f"{name}: glider reads differ from the CTS")
    value = decode_reads(lb, comp, out)
    want = lisp_run(src)
    if value != want:
        raise AssertionError(f"{name}: decoded {value}, lisp.py {want}")

    # overview image: one row per uniform time step
    t_end = g.t
    ts = np.array([f[0] for f in frames])
    rows = [int(np.argmin(np.abs(ts - t_end * k / (N_ROWS - 1)))) for k in range(N_ROWS)]
    read_at = er.watch.read_at
    img = np.zeros((N_ROWS, N_COLS, 3), np.float32)
    col_of = lambda x: int((x - x_lo) * N_COLS // (x_hi - x_lo))
    for r, fi in enumerate(rows):
        t, _, _, cnt = frames[fi]
        e = np.log1p(cnt[2]) / np.log1p(max(1, cnt[2].max()))
        rgb = BG + (E_LO - BG) * (cnt[2] > 0)[:, None] + (E_HI - E_LO) * e[:, None] * (cnt[2] > 0)[:, None]
        unread = np.zeros(N_COLS, bool)
        for j in range(n):
            a, b = regs[j]
            if a is not None and (read_at[j] is None or read_at[j] > t):
                unread[col_of(a):col_of(b) + 1] = True
        rgb[unread] = TABLE
        rgb[cnt[0] > 0] = A_COL
        rgb[(cnt[1] + cnt[3]) > 0] = X_COL
        img[r] = rgb

    # the answer, read off the last pass
    B, last = pm.B, comp.passes - 1
    names = {c: a for a, c in lb.atoms.items()}

    def tok(val):
        k = kind(val)
        return "·" if val == PAD else "(" if val == OPEN else ")" if val == CLOSE else names[code(val)]
    regs_out = []
    for k in comp.live[last]:
        i = comp.nominal[(last, k)] * B
        word = out[i:i + B]
        letter = word.index("Y")
        val = {ii: x for x, ii in comp.enc[(last, k)].items()}[letter // 2]
        regs_out.append({"reg": k, "start": i, "word": word, "letter": letter,
                         "token": tok(val) if k in lb.block else None, "result": k in lb.block})
    order = {k: i for i, k in enumerate(lb.block)}
    tokens = [r["token"] for r in sorted((r for r in regs_out if r["result"]), key=lambda r: order[r["reg"]])]

    step = max(1, n // 600)
    sheet = np.concatenate([m[2] for m in micro]) if micro else np.zeros((1, 1, 3), np.uint8)
    return {
        "name": name, "src": src, "value": _fmt(value), "lisp": _fmt(want),
        "meta": {"registers": lb.n, "passes": comp.passes, "B": B, "reads": n,
                 "appendants": len(apps), "tape_bits": len(tape), "v": v, "t_end": int(t_end),
                 "events": int(g.n_events), "wall_s": round(wall, 1), "x_lo": int(x_lo),
                 "x_hi": int(x_hi), "Y": out.count("Y")},
        "rows": {"t": [int(frames[i][0]) for i in rows], "reads": [frames[i][1] for i in rows],
                 "events": [int(frames[i][2]) for i in rows]},
        "overview": _png(img),
        "micro": {"w": MICRO_W, "h": MICRO_H, "reads": [m[0] for m in micro],
                  "t": [int(m[1]) for m in micro], "png": _png(sheet)},
        "outcome": out,
        "read_at": [int(x) for x in read_at],
        "queue": {"step": step, "len": qlen[::step]},
        "decode": {"last_pass": last, "regs": regs_out, "tokens": tokens},
    }


def _fmt(v):
    return v if isinstance(v, str) else "(" + " ".join(_fmt(x) for x in v) + ")"


def build(outdir, page):
    tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard_page.html")).read()
    runs = [json.load(open(os.path.join(outdir, f"{k}.json"))) for k in PRESETS
            if os.path.exists(os.path.join(outdir, f"{k}.json"))]
    if not runs:
        raise FileNotFoundError(f"no recorded runs in {outdir}")
    data = json.dumps(runs, separators=(",", ":"))
    html = tpl.replace("/*__RUNS__*/[]", data)
    if html == tpl:
        raise ValueError("template has no /*__RUNS__*/[] placeholder")
    open(page, "w").write(html)
    print(f"{page}: {len(runs)} runs, {len(html) / 1e6:.1f} MB")


def main():
    cmd = sys.argv[1]
    if cmd == "record":
        outdir = sys.argv[2]
        os.makedirs(outdir, exist_ok=True)
        for name in sys.argv[3:] or list(PRESETS):
            src, depth = PRESETS[name]
            t0 = time.time()
            run = record(name, src, depth)
            json.dump(run, open(os.path.join(outdir, f"{name}.json"), "w"))
            print(f"{name}: {src} -> {run['value']} ({run['meta']['reads']} reads, "
                  f"{len(run['micro']['reads'])} cell windows, {time.time() - t0:.0f}s)", flush=True)
    elif cmd == "build":
        build(sys.argv[2], sys.argv[3])
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
