// Run from this folder: NODE_PATH=$(npm root -g) node interact.js  (screenshots go to ./screenshots/)
// Drives the threshold slider, opens the presenter view, and checks dark mode and phone width.
const { chromium } = require('playwright');
const URL = 'file://' + require('path').resolve(__dirname, '../logistic_regression_lecture.html');
const go = async (p, id) => { await p.evaluate(id => document.getElementById(id).scrollIntoView(), id); await p.waitForTimeout(1300); };
(async () => {
  const b = await chromium.launch(), ctx = await b.newContext({ viewport: { width: 1440, height: 810 } }), p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(URL); await p.waitForTimeout(600);
  const txt = id => p.$eval('#' + id, e => e.textContent);
  await go(p, 's-fit');
  for (const v of ['5', '30', '50', '70', '95']) { await p.$eval('#r-ft', (e, v) => { e.value = v; e.dispatchEvent(new Event('input')); }, v);
    console.log('threshold', await txt('v-ft-t'), 'TPR', await txt('v-ft-tpr'), 'FPR', await txt('v-ft-fpr')); }
  const [pop] = await Promise.all([ctx.waitForEvent('page'), p.keyboard.press('p')]);
  await pop.waitForTimeout(1500); await pop.screenshot({ path: 'screenshots/int-presenter.png' });
  console.log('presenter title:', await pop.title(), 'errors', JSON.stringify(errs));
  for (const [name, opts] of [['dark', { viewport: { width: 1440, height: 810 }, colorScheme: 'dark' }], ['phone', { viewport: { width: 390, height: 844 } }]]) {
    const c = await b.newContext(opts), q = await c.newPage(); const e2 = []; q.on('pageerror', e => e2.push(e.message));
    await q.goto(URL); await q.waitForTimeout(600);
    for (const id of ['s-loss', 's-fit', 's-2d', 's-neuron']) { await go(q, id); for (let k = 0; k < 3; k++) await q.keyboard.press('ArrowRight'); await q.waitForTimeout(900); await q.screenshot({ path: `screenshots/int-${name}-${id}.png` }); }
    const over = await q.evaluate(() => [...document.querySelectorAll('.slide')].filter(s => s.scrollWidth > document.documentElement.clientWidth + 1).map(s => s.id));
    console.log(name, 'overflowing slides:', JSON.stringify(over), 'errors', JSON.stringify(e2));
  }
  await b.close();
})();
