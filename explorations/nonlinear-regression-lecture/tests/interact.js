// Run from this folder: NODE_PATH=$(npm root -g) node interact.js  (screenshots go to ./screenshots/)
// Drives the sliders and buttons, opens the presenter view, and checks dark mode and phone width.
const { chromium } = require('playwright');
const URL = 'file://' + require('path').resolve(__dirname, '../nonlinear_regression_lecture.html');
const go = async (p, id) => { await p.evaluate(id => document.getElementById(id).scrollIntoView(), id); await p.waitForTimeout(1300); };
const slide = async (p, id, v) => p.$eval('#' + id, (e, v) => { e.value = v; e.dispatchEvent(new Event('input')); }, v);
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1440, height: 810 } });
  const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(URL); await p.waitForTimeout(600);
  const txt = id => p.$eval('#' + id, e => e.textContent);
  await go(p, 's-split');
  for (const v of ['0', '5', '13', '16']) { await slide(p, 'r-split', v); console.log('split', v, await txt('v-sp-t'), await txt('v-sp-l'), await txt('v-sp-r'), await txt('v-sp-s')); }
  await go(p, 's-grow');
  for (const v of ['2', '7', '12', '19']) { await slide(p, 'r-grow', v); console.log('grow', v, 'leaves', await txt('v-gr-n'), 'SSE', await txt('v-gr-s')); }
  await go(p, 's-knn');
  for (const v of ['1', '9', '40', '56']) { await slide(p, 'r-knn', v); console.log('knn', v, 'at 40', await txt('v-kn-p'), 'SSE', await txt('v-kn-s')); }
  await go(p, 's-svr');
  for (const v of ['1', '8', '24']) { await slide(p, 'r-svr', v); console.log('svr eps', await txt('v-sv-e'), 'out', await txt('v-sv-n'), 'slack', await txt('v-sv-x')); }
  await go(p, 's-svrobj');
  for (const v of ['-300', '-100', '100']) { await slide(p, 'r-svrc', v); console.log('svr', await txt('v-sc-c'), 'w', await txt('v-sc-w'), 'out', await txt('v-sc-n')); }
  await go(p, 's-svrk'); await p.keyboard.press('ArrowRight'); await p.waitForTimeout(500);   // the toolbar appears at step 1
  await p.click('#b-sk-rbf'); for (const v of ['-300', '-170', '-70', '0']) { await slide(p, 'r-sk-g', v); console.log('svrk', await txt('v-sk-g'), 'out', await txt('v-sk-n'), 'SSE', await txt('v-sk-s')); }
  await p.screenshot({ path: 'screenshots/int-svrk-g1.png' });
  await p.click('#b-sk-linear'); console.log('svrk', await txt('v-sk-k'), 'slider disabled', await p.$eval('#r-sk-g', e => e.disabled));
  const [pop] = await Promise.all([ctx.waitForEvent('page'), p.keyboard.press('p')]);
  await pop.waitForTimeout(1500); await pop.screenshot({ path: 'screenshots/int-presenter.png' });
  console.log('presenter title:', await pop.title());
  console.log('errors', JSON.stringify(errs));
  for (const [name, opts] of [['dark', { viewport: { width: 1440, height: 810 }, colorScheme: 'dark' }],
                              ['phone', { viewport: { width: 390, height: 844 } }]]) {
    const c = await b.newContext(opts), q = await c.newPage(); const e2 = []; q.on('pageerror', e => e2.push(e.message));
    await q.goto(URL); await q.waitForTimeout(600);
    for (const id of ['s-rt', 's-split', 's-knn2', 's-svrobj']) { await go(q, id); for (let k = 0; k < 4; k++) await q.keyboard.press('ArrowRight'); await q.waitForTimeout(900); await q.screenshot({ path: `screenshots/int-${name}-${id}.png` }); }
    const over = await q.evaluate(() => [...document.querySelectorAll('.slide')]
      .filter(s => s.scrollWidth > document.documentElement.clientWidth + 1).map(s => s.id));
    console.log(name, 'overflowing slides:', JSON.stringify(over), 'errors', JSON.stringify(e2));
  }
  await b.close();
})();
