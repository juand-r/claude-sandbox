// Run from this folder: NODE_PATH=$(npm root -g) node check.js   (screenshots go to ./screenshots/)
// 1. every gradient in every garden against central finite differences
// 2. every garden can reach stillness the intended way (by hand, by breathing, or by a drag and then breathing)
// 3. the class-2 example numbers that garden 9's lesson quotes
// 4. no console errors; screenshots of each garden while listening, with the numbers shown, light and dark
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const URL = 'file://' + path.resolve(__dirname, '../still_water.html');
fs.mkdirSync(path.join(__dirname, 'screenshots'), { recursive: true });
(async () => {
  const b = await chromium.launch();
  let fails = 0;
  for (const scheme of ['light', 'dark']) {
    const p = await (await b.newContext({ viewport: { width: 1366, height: 820 }, colorScheme: scheme })).newPage();
    const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error' && !/ERR_CERT_AUTHORITY_INVALID/.test(m.text())) errs.push(m.text()); });   // the sandbox's proxy blocks Google Fonts; not a page error
    await p.goto(URL); await p.waitForTimeout(500);
    if (scheme === 'light') {
      const r = await p.evaluate(() => {
        const { LEVELS, forward, backward } = window.StillWater, out = [];
        LEVELS.forEach((lv, li) => {
          const P = { W: lv.W.map(m => m.map(r => r.slice())), b: lv.b.map(r => r.slice()) };
          const F = forward(lv, P), B = backward(lv, P, F); let worst = 0;
          const keys = [];
          P.W.forEach((m, l) => m.forEach((r, j) => r.forEach((_, i) => keys.push(['W', l, j, i]))));
          P.b.forEach((r, l) => r.forEach((_, j) => keys.push(['b', l, j])));
          for (const k of keys) {
            const get = Q => k[0] === 'W' ? Q.W[k[1]][k[2]][k[3]] : Q.b[k[1]][k[2]];
            const set = (Q, v) => { if (k[0] === 'W') Q.W[k[1]][k[2]][k[3]] = v; else Q.b[k[1]][k[2]] = v; };
            const h = 1e-6, Pp = JSON.parse(JSON.stringify(P)), Pm = JSON.parse(JSON.stringify(P));
            set(Pp, get(P) + h); set(Pm, get(P) - h);
            const num = (forward(lv, Pp).L - forward(lv, Pm).L) / (2 * h);
            const ana = k[0] === 'W' ? B.dW[k[1]][k[2]][k[3]] : B.db[k[1]][k[2]];
            worst = Math.max(worst, Math.abs(num - ana));
          }
          out.push([li + 1, lv.name, worst, F.L]);
        });
        return out;
      });
      for (const [n, name, worst, L] of r) { const ok = worst < 1e-6; if (!ok) fails++; console.log(`garden ${n} ${name}: max |analytic - numerical| = ${worst.toExponential(1)} ${ok ? 'ok' : 'FAIL'}; start loss ${L.toFixed(4)}`); }
      // class example (garden 9)
      const ex = await p.evaluate(() => { const S = window.StillWater; S.load(8); const F = S.F, B = S.B; return { yhat: F.a[2][0], L: F.L, dw2: B.dW[1][0][0], dw1: B.dW[0][0][0], err: F.a[2][0] - 2 }; });
      console.log('garden 9 at the start:', JSON.stringify(Object.fromEntries(Object.entries(ex).map(([k, v]) => [k, +v.toFixed(3)]))));
      for (const [k, want] of [['yhat', 0.651], ['L', 0.910], ['dw2', -0.986], ['dw1', -1.061], ['err', -1.349]]) if (Math.abs(ex[k] - want) > 6e-4) { fails++; console.log('  FAIL', k, ex[k], 'want', want); }
      // play every garden
      const plan = { 1: 'hand', 2: 'hand', 3: 0.2, 4: 0.2, 5: 1, 6: 1, 7: 0.3, 8: 'drag', 9: 0.3 };
      for (let li = 0; li < 9; li++) {
        const res = await p.evaluate(async ([li, how]) => {
          const S = window.StillWater, st = S.state; S.load(li); const lv = S.LEVELS[li];
          const wait = ms => new Promise(r => setTimeout(r, ms));
          if (how === 'hand') {   // set the weights so the output matches, as a player would by dragging
            const x = lv.x, need = lv.t[0], sum = x.reduce((s, v) => s + v * v, 0), err = S.F.a[1][0] - need;
            st.P.W[0][0] = st.P.W[0][0].map((w, i) => w - err * x[i] / sum);
            document.getElementById('gardens').children[li].blur();
            // trigger the same path a drag takes
            const e = new KeyboardEvent('keydown', { key: 'ArrowUp' }); const g = document.querySelector('.gate:not(.locked)'); g.dispatchEvent(e);
            const e2 = new KeyboardEvent('keydown', { key: 'ArrowDown' }); g.dispatchEvent(e2);
            return { done: st.done, breaths: st.breaths, L: S.F.L };
          }
          if (how === 'drag') {   // garden 8: three stuck breaths, then drag the first gate to 1, then breathe
            for (let k = 0; k < 3; k++) { S.breathe(); await wait(700); }
            const stuck = S.F.L; st.P.W[0][0][0] = 1.0;
            const g = document.querySelector('.gate:not(.locked)'); g.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowUp' })); g.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowDown' }));
            for (let k = 0; k < 30 && !st.done; k++) { S.breathe(); await wait(700); }
            return { done: st.done, breaths: st.breaths, L: S.F.L, stuck };
          }
          st.eta = how;
          for (let k = 0; k < 60 && !st.done; k++) { S.breathe(); await wait(700); }
          return { done: st.done, breaths: st.breaths, L: S.F.L };
        }, [li, plan[li + 1]]);
        const lv = (await p.evaluate(li => window.StillWater.LEVELS[li], li));
        const ok = res.done && (!lv.par || res.breaths <= lv.par);
        if (!ok) fails++;
        console.log(`play garden ${li + 1} (${plan[li + 1]}): still=${res.done} breaths=${res.breaths} par=${lv.par} loss=${res.L.toExponential(2)}${res.stuck !== undefined ? ' loss after 3 stuck breaths=' + res.stuck.toFixed(4) : ''} ${ok ? 'ok' : 'FAIL'}`);
      }
    }
    // screenshots: each garden at its start, listening, numbers on
    for (let li = 0; li < 9; li++) {
      await p.evaluate(li => { const S = window.StillWater; S.load(li); }, li);
      if (await p.$eval('#listen', e => !e.disabled)) await p.click('#listen');
      if (!(await p.$eval('#numbers', e => e.checked))) await p.click('#numbers');
      await p.waitForTimeout(2600);
      await p.screenshot({ path: path.join(__dirname, `screenshots/${scheme}-garden${li + 1}.png`) });
    }
    console.log(scheme, 'errors:', JSON.stringify(errs)); if (errs.length) fails++;
  }
  // phone width
  const q = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage();
  await q.goto(URL); await q.waitForTimeout(500);
  const over = await q.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  await q.screenshot({ path: path.join(__dirname, 'screenshots/phone.png'), fullPage: true });
  console.log('phone horizontal overflow px:', over); if (over > 0) fails++;
  console.log(fails ? `${fails} FAILURES` : 'all checks passed');
  await b.close();
})();
