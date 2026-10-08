// Run from this folder: NODE_PATH=$(npm root -g) node interact2.js  (screenshots go to ./screenshots/)
// Class 2 deck: plays the optimizer and batch-size replays, scrubs a slider, opens the presenter view,
// and checks dark mode and phone width.
const { chromium } = require('playwright');
const URL = 'file://' + require('path').resolve(__dirname, '../neural_nets_2.html');
const go = async (p, id, steps = 0) => { await p.evaluate(id => document.getElementById(id).scrollIntoView(), id); await p.waitForTimeout(1300);
  for (let k = 0; k < steps; k++) await p.keyboard.press('ArrowRight'); await p.waitForTimeout(400); };
(async () => {
  const b = await chromium.launch(), ctx = await b.newContext({ viewport: { width: 1440, height: 810 } }), p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(URL); await p.waitForTimeout(600);
  const txt = id => p.$eval('#' + id, e => e.textContent);
  await go(p, 's-mom', 2); await p.click('#b-mom-play'); await p.waitForTimeout(4500);
  console.log('momentum replay end: step', await txt('v-mom-k'), 'plain', await txt('v-mom-gd'), 'momentum', await txt('v-mom-m'));
  await p.$eval('#r-mom', e => { e.value = '30'; e.dispatchEvent(new Event('input')); });
  console.log('momentum step 30: plain', await txt('v-mom-gd'), 'momentum', await txt('v-mom-m'));
  await p.screenshot({ path: 'screenshots/int2-mom-30.png' });
  await go(p, 's-sgd', 3);
  for (const n of ['batch', 'sgd', 'mini']) { await p.click('#b-sgd-' + n); await p.waitForTimeout(3200);
    console.log('SGD', n, 'points/step', await txt('v-sgd-bs'), 'steps/epoch', await txt('v-sgd-u'), 'loss', await txt('v-sgd-l'));
    await p.screenshot({ path: `screenshots/int2-sgd-${n}.png` }); }
  const [pop] = await Promise.all([ctx.waitForEvent('page'), p.keyboard.press('p')]);
  await pop.waitForTimeout(1500); await pop.screenshot({ path: 'screenshots/int2-presenter.png' });
  console.log('presenter title:', await pop.title(), 'errors', JSON.stringify(errs));
  for (const [name, opts] of [['dark', { viewport: { width: 1440, height: 810 }, colorScheme: 'dark' }], ['phone', { viewport: { width: 390, height: 844 } }]]) {
    const c = await b.newContext(opts), q = await c.newPage(); const e2 = []; q.on('pageerror', e => e2.push(e.message));
    await q.goto(URL); await q.waitForTimeout(600);
    for (const [id, s] of [['s-chain', 3], ['s-paths', 3], ['s-mom', 2], ['s-local', 3], ['s-sgd', 0], ['s-stop', 4], ['s-char', 1], ['s-tree', 3]]) {
      await go(q, id, s); await q.waitForTimeout(500); await q.screenshot({ path: `screenshots/int2-${name}-${id}.png` }); }
    const over = await q.evaluate(() => [...document.querySelectorAll('.slide')].filter(s => s.scrollWidth > document.documentElement.clientWidth + 1).map(s => s.id));
    console.log(name, 'overflowing slides:', JSON.stringify(over), 'errors', JSON.stringify(e2));
  }
  await b.close();
})();
