const { Gas, Brute, ETHER, etherPhase, mod } = require("./engine.js").GasEngine;
const scenes = require("./scenes.json");
function check(name, cells, T) {
  const n = cells.length;
  const cL = etherPhase(cells.slice(0, 14))[0];
  const cR = mod(etherPhase(cells.slice(n - 14))[0] - (n - 14), 14);
  if (cL < 0) throw new Error(name + ": row must start in ether");
  const t0 = Date.now();
  const g = Gas.fromRow(cells, cL, cR, T), b = new Brute(cells, cL, cR, 2 * T + 60);
  let bad = 0;
  for (let t = 0; t <= T; t++) {
    if (t > 0) b.step();
    if (t % 50 === 0 || t === T) {
      g.advanceTo(t);
      const lo = -T / 2 | 0, hi = n + (T / 2 | 0);
      const a = g.window(lo, hi), r = b.window(lo, hi);
      for (let k = 0; k < a.length; k++) if (a[k] !== r[k]) bad++;
    }
  }
  console.log(name, "n", n, "T", T, "items", g.items.length, "events", g.nEvents, "collisions", g.nSim,
              "orbits", g.reg.orbits.length, "differing cells", bad, (Date.now() - t0) + "ms");
  return bad;
}
let total = 0;
for (const [k, s] of Object.entries(scenes)) total += check(k, Uint8Array.from(s.cells, (c) => +c), s.T);
// random patches in ether
let seed = 12345; const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
for (let trial = 0; trial < 12; trial++) {
  const n = 1400, c = Math.floor(rnd() * 14), row = Uint8Array.from({ length: n }, (_, x) => +ETHER[mod(c + x, 14)]);
  for (let x = 200; x < n - 300;) { const w = 1 + Math.floor(rnd() * 20); for (let k = 0; k < w; k++) row[x + k] = rnd() < 0.5 ? 1 : 0; x += w + 60 + Math.floor(rnd() * 250); }
  total += check("random" + trial, row, 1500);
}
console.log("TOTAL differing", total);
