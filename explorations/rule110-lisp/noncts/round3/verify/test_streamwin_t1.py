"""Instrument check on a real program: the 40-op fixed left stream (T1,
t1z_<word>.json) run with streamwin (left stream = A-family free
reference) vs the full exact engine: identical cells at the end; and the
final counter value from both."""
import json, time
import numpy as np
import t1lib as L
import v3, vlib, engine
import streamwin as S
import t1_build as B

word = "ZIZZIIZIZZIZIIIZZIIIZZIZIIZZZIZZZIIIZIZZ"
slots = [tuple(s) for s in json.load(open(f"t1z_{word}.json"))["slots"]]
for v in (0, 5, 12):
    T = B.Tfor(len(slots))
    items = L.scene_items(slots, v)
    nl = len(slots)
    c0 = (L.C_E - sum(vlib.LIB[n].w for n, _, _ in items[:nl])) % 14
    row, org, placed = vlib.build(items, c0=c0, T=T)
    t1 = time.time()
    full = engine.unpack(engine.step_packed_n(engine.pack(row), T), len(row))
    tf = time.time() - t1
    xa, xb = S.auto_cuts(row, org, nl, 0)
    t1 = time.time()
    sw = S.StreamWindow(row, org, xa, xb, (3, 2), (42, -14))
    S.run_packed(sw, T)
    ts = time.time() - t1
    lo, hi = org + T + 50, org + len(row) - T - 50
    same = np.array_equal(full[lo - org:hi - org], sw.cells(lo, hi))
    objs = [(n, x) for n, x, w, k in vlib.identify(full, org, T=T)]
    print(f"v={v}: T={T} equal={same} model={B.model(word, v)} CA={L.counter_and_answers(objs)} "
          f"full {tf:.2f}s window {ts:.2f}s (max width {sw.max_width})")
    assert same
