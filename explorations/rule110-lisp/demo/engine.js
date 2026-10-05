// A small port of gas.py (the event engine) for the browser demo.
// Patches are Uint8Arrays of cells with the ether phase index at the first
// cell (phL) and at the cell after the last (phR). Particles move in closed
// form; patches that come within two cells are simulated together once and
// memoized by their canonical key. Checked against brute force in test.js.
(function (root) {
  "use strict";
  const ETHER = "11111000100110", TILE = 14, SHIFT = 4;
  const SPLIT_GAP = 14, MIN_GAP = 2, P_MAX = 120, CAP = 2048, MAX_W = 4096;
  const E = Uint8Array.from(ETHER, (c) => +c);
  const mod = (a, m) => ((a % m) + m) % m;
  const eth = (ph) => E[mod(ph, TILE)];
  const ROT = new Map();
  for (let r = 0; r < TILE; r++) ROT.set(ETHER.slice(r) + ETHER.slice(0, r), r);

  function keyOf(p) { return p.phL + "," + p.phR + "," + p.cells.join(""); }
  function empty(p) { return p.cells.length === 0 && p.phL === p.phR; }

  // canonical (trimmed) patch -> {p, dx}
  function trim(cells, phL, phR, loCut = 0) {
    const w = cells.length;
    let i = 0;
    while (i < w && cells[i] === eth(phL + i)) i++;
    let j = 0;
    while (j < w && cells[w - 1 - j] === eth(phR - 1 - j)) j++;
    if (i + j >= w) {
      const cut = Math.min(Math.max(w - j, loCut), i);
      return { p: { cells: new Uint8Array(0), phL: mod(phL + cut, TILE), phR: mod(phR - (w - cut), TILE) }, dx: cut };
    }
    return { p: { cells: cells.slice(i, w - j), phL: mod(phL + i, TILE), phR: mod(phR - j, TILE) }, dx: i };
  }

  function step(p) {
    const w = p.cells.length, ext = new Uint8Array(w + 4);
    ext[0] = eth(p.phL - 2); ext[1] = eth(p.phL - 1);
    ext.set(p.cells, 2);
    ext[w + 2] = eth(p.phR); ext[w + 3] = eth(p.phR + 1);
    const nw = new Uint8Array(w + 2);
    for (let k = 1; k <= w + 2; k++) {
      const l = ext[k - 1], c = ext[k], r = ext[k + 1];
      nw[k - 1] = (c | r) & ~(l & c & r) & 1;
    }
    const t = trim(nw, p.phL - 1 + SHIFT, p.phR + 1 + SHIFT);
    return { p: t.p, dx: t.dx - 1 };
  }

  function etherPhase(row) {
    const n = row.length - TILE + 1, out = new Int8Array(Math.max(n, 0));
    for (let x = 0; x < n; x++) {
      let s = "";
      for (let k = 0; k < TILE; k++) s += row[x + k];
      const r = ROT.get(s);
      out[x] = r === undefined ? -1 : mod(r - x, TILE);
    }
    return out;
  }

  // pieces separated by >= SPLIT_GAP clean ether cells of one phase
  function split(p) {
    const w = p.cells.length;
    if (w < SPLIT_GAP + 2) return [{ p, off: 0 }];
    const pad = SPLIT_GAP + TILE, n = w + 2 * pad, row = new Uint8Array(n);
    for (let k = 0; k < pad; k++) { row[k] = eth(p.phL - pad + k); row[pad + w + k] = eth(p.phR + k); }
    row.set(p.cells, pad);
    const ph = etherPhase(row), phase = new Int8Array(n);
    for (let c = 0; c < n; c++) {
      let lo = 99, hi = -1;
      for (let s = Math.max(0, c - TILE + 1); s <= Math.min(c, ph.length - 1); s++)
        if (ph[s] >= 0) { lo = Math.min(lo, ph[s]); hi = Math.max(hi, ph[s]); }
      phase[c] = lo === hi ? lo : -1;
    }
    const gaps = [];
    for (let a = 0; a < n;) {
      let b = a + 1;
      while (b < n && phase[b] === phase[a]) b++;
      if (phase[a] >= 0 && b - a >= SPLIT_GAP) gaps.push([a, b]);
      a = b;
    }
    if (!gaps.length || gaps[0][0] !== 0 || gaps[gaps.length - 1][1] !== n)
      throw new Error("split: the padding is not a gap");
    const pieces = [];
    for (let g = 0; g + 1 < gaps.length; g++) {
      const b0 = gaps[g][1], a1 = gaps[g + 1][0];
      const pl = mod(phase[b0 - 1] + b0, TILE), pr = mod(phase[a1] + a1, TILE);
      const t = trim(row.slice(b0, a1), pl, pr, Math.max(0, pad - b0));
      if (empty(t.p)) continue;
      const off = b0 + t.dx - pad;
      if (off < 0 || off + t.p.cells.length > w) throw new Error("split: piece outside its parent");
      pieces.push({ p: t.p, off });
    }
    return pieces;
  }

  class Registry {
    constructor() { this.known = new Map(); this.orbits = []; }
    lookup(p) {
      const key = keyOf(p);
      if (this.known.has(key)) return this.known.get(key);
      const pats = [p], off = [0];
      let q = p, x = 0;
      for (let s = 1; s <= P_MAX; s++) {
        const r = step(q); q = r.p; x += r.dx;
        if (keyOf(q) === key) { off.push(x); return this.add(pats, off, key); }
        pats.push(q); off.push(x);
      }
      this.known.set(key, null);
      return null;
    }
    add(pats, off) {
      const o = { id: this.orbits.length, pats, p: pats.length, off: off.map((v) => v - off[0]) };
      o.d = o.off[o.p];
      this.orbits.push(o);
      pats.forEach((q, i) => this.known.set(keyOf(q), { o, s: i }));
      return this.known.get(keyOf(pats[0]));
    }
  }

  // evolve a composite until it splits, becomes periodic or vanishes
  function simulate(p, reg) {
    const states = [{ p, x: 0 }], seen = new Map([[keyOf(p), 0]]);
    let q = p, x = 0;
    for (let s = 1; s <= CAP; s++) {
      const r = step(q); q = r.p; x += r.dx;
      if (q.cells.length > MAX_W) throw new Error("debris: composite wider than " + MAX_W + " cells");
      const k = keyOf(q);
      if (empty(q)) { states.push({ p: q, x }); return { states, pieces: [] }; }
      const kn = reg.known.get(k);
      if (kn) { states.push({ p: q, x }); return { states, pieces: [{ p: q, off: x }] }; }
      if (seen.has(k)) {
        const s0 = seen.get(k);
        reg.add(states.slice(s0).map((v) => v.p), states.slice(s0).map((v) => v.x).concat([x]));
        return { states: states.slice(0, s0 + 1), pieces: [{ p: states[s0].p, off: states[s0].x }] };
      }
      states.push({ p: q, x }); seen.set(k, s);
      const ps = split(q);
      if (ps.length !== 1) return { states, pieces: ps.map((v) => ({ p: v.p, off: x + v.off })) };
    }
    return { states, pieces: [{ p: q, off: x }] };
  }

  function family(o) {
    if (!o) return "X";
    if (o.d === 0) return "C";
    if (3 * o.d === 2 * o.p) return "A";
    if (15 * o.d === -4 * o.p) return "E";
    return "P";
  }

  class Gas {
    constructor() {
      this.reg = new Registry(); this.memo = new Map();
      this.items = []; this.pair = []; this.t = 0; this.tEnd = Infinity;
      this.nEvents = 0; this.nSim = 0; this.cellSteps = 0; this.log = []; this.serial = 0;
    }
    // a row of cells at t = 0, ether constants cL / cR outside it (cell x
    // at time t reads ETHER[(c + x + 4t) mod 14])
    static fromRow(cells, cL, cR, tEnd) {
      const g = new Gas(); g.tEnd = tEnd;
      const n = cells.length, t = trim(cells, mod(cL, TILE), mod(cR + n, TILE));
      g.items = split(t.p).map((v) => g.make(v.p, t.dx + v.off, 0));
      g.pair = g.items.slice(1).map((_, i) => g.collision(i));
      return g;
    }
    make(p, left, t) {
      const it = { cL: mod(p.phL - left - SHIFT * t, TILE), born: t, id: this.serial++ };
      const r = this.reg.lookup(p);
      if (r) { it.o = r.o; it.t0 = t - r.s; it.x0 = left - r.o.off[r.s]; }
      else {
        const key = keyOf(p);
        let e = this.memo.get(key);
        if (!e) {
          const before = this.cellSteps;
          e = simulate(p, this.reg); this.memo.set(key, e); this.nSim++;
          this.cellSteps = before + e.states.reduce((s, v) => s + v.p.cells.length, 0);
        }
        it.e = e; it.ts = t; it.xs = left;
      }
      it.fam = family(it.o);
      return it;
    }
    at(it, t) {
      if (it.o) {
        const o = it.o, k = Math.floor((t - it.t0) / o.p), s = t - it.t0 - k * o.p;
        return { p: o.pats[s], left: it.x0 + k * o.d + o.off[s] };
      }
      const st = it.e.states[t - it.ts];
      return { p: st.p, left: it.xs + st.x };
    }
    end(it) { return it.e ? it.ts + it.e.states.length - 1 : Infinity; }
    // first time >= now at which items i and i+1 come within MIN_GAP cells
    collision(i) {
      const a = this.items[i], b = this.items[i + 1];
      const horizon = Math.min(this.end(a), this.end(b), this.tEnd);
      let t = this.t;
      const A = this.at(a, t), B = this.at(b, t);
      if (B.left - A.left - A.p.cells.length >= MIN_GAP + 2 * (horizon - t + 1)) return Infinity;
      for (; t <= horizon; t++) {
        const sa = this.at(a, t), sb = this.at(b, t);
        if (sb.left - sa.left - sa.p.cells.length < MIN_GAP) return t;
      }
      return Infinity;
    }
    nextEvent() {
      let best = Infinity, kind = null, idx = -1;
      this.pair.forEach((t, i) => { if (t < best) { best = t; kind = "merge"; idx = i; } });
      this.items.forEach((it, i) => { const e = this.end(it); if (e < best) { best = e; kind = "split"; idx = i; } });
      return { t: best, kind, idx };
    }
    replace(i, j, news) {           // items i..j-1 -> news; reschedule around them
      this.items.splice(i, j - i, ...news);
      const lo = Math.max(0, i - 1), hi = Math.min(this.items.length - 1, i + news.length);
      this.pair.splice(lo, Math.min(this.pair.length, j) - lo, ...new Array(Math.max(0, hi - lo)).fill(0));
      for (let k = lo; k < hi; k++) this.pair[k] = this.collision(k);
    }
    advanceTo(T) {
      for (;;) {
        const ev = this.nextEvent();
        if (ev.t > T) break;
        this.t = ev.t;
        if (ev.kind === "merge") this.merge(ev.idx); else this.splitItem(ev.idx);
        this.nEvents++;
      }
      this.t = T;
    }
    merge(i) {
      const t = this.t, a = this.items[i], b = this.items[i + 1];
      const A = this.at(a, t), B = this.at(b, t), wa = A.p.cells.length, g = B.left - A.left - wa;
      if (g < 0 || g >= MIN_GAP) throw new Error("bad merge at t=" + t);
      if (mod(A.p.phR + g, TILE) !== B.p.phL) throw new Error("ether mismatch at t=" + t);
      const cells = new Uint8Array(wa + g + B.p.cells.length);
      cells.set(A.p.cells, 0);
      for (let k = 0; k < g; k++) cells[wa + k] = eth(A.p.phR + k);
      cells.set(B.p.cells, wa + g);
      const tr = trim(cells, A.p.phL, B.p.phR);
      const it = this.make(tr.p, A.left + tr.dx, t);
      this.log.push({ t, kind: "collide", a: a.fam, b: b.fam, x: A.left + wa });
      this.replace(i, i + 2, [it]);
    }
    splitItem(i) {
      const t = this.t, a = this.items[i];
      const news = a.e.pieces.map((v) => this.make(v.p, a.xs + v.off, t));
      this.log.push({ t, kind: "split", into: news.map((v) => v.fam), x: this.at(a, t).left });
      this.replace(i, i + 1, news);
    }
    // cells [lo, hi) at time t (the engine's own rendering)
    window(lo, hi) {
      const t = this.t, out = new Uint8Array(hi - lo);
      let x = lo, c = this.items.length ? this.items[0].cL : 0;
      for (const it of this.items) {
        const s = this.at(it, t), r = s.left + s.p.cells.length;
        for (; x < Math.min(s.left, hi); x++) out[x - lo] = eth(it.cL + x + SHIFT * t);
        for (let k = Math.max(x, s.left); k < Math.min(r, hi); k++) out[k - lo] = s.p.cells[k - s.left];
        x = Math.max(x, Math.min(r, hi));
        c = mod(s.p.phR - r - SHIFT * t, TILE);
      }
      for (; x < hi; x++) out[x - lo] = eth(c + x + SHIFT * t);
      return out;
    }
  }

  // the reference: every cell, every step (rows wider than the view by the
  // light cone, so the wrap seam never reaches it)
  class Brute {
    constructor(cells, cL, cR, margin) {
      const n = cells.length;
      this.lo = -margin; this.row = new Uint8Array(n + 2 * margin); this.t = 0; this.cellSteps = 0;
      for (let k = 0; k < this.row.length; k++) {
        const x = k + this.lo;
        this.row[k] = x < 0 ? eth(cL + x) : x >= n ? eth(cR + x) : cells[x];
      }
      this.next = new Uint8Array(this.row.length);
    }
    step() {
      const r = this.row, w = r.length, nx = this.next;
      for (let k = 0; k < w; k++) {
        const l = r[k === 0 ? w - 1 : k - 1], c = r[k], q = r[k === w - 1 ? 0 : k + 1];
        nx[k] = (c | q) & ~(l & c & q) & 1;
      }
      this.next = r; this.row = nx; this.t++; this.cellSteps += w;
    }
    window(lo, hi) { return this.row.slice(lo - this.lo, hi - this.lo); }
  }

  root.GasEngine = { Gas, Brute, ETHER, etherPhase, mod };
})(typeof module !== "undefined" ? module.exports : window);
