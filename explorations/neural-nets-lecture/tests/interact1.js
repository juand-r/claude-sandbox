// Run from this folder: NODE_PATH=$(npm root -g) node interact1.js  (screenshots go to ./screenshots/)
// Class 1 deck: drags the start on the loss landscape, plays the gradient-descent and XOR-training replays
// to the end, opens the presenter view, and checks dark mode and phone width.
const { chromium } = require('playwright');
const URL = 'file://' + require('path').resolve(__dirname, '../neural_nets_1.html');
const go = async (p, id, steps = 0) => { await p.evaluate(id => document.getElementById(id).scrollIntoView(), id); await p.waitForTimeout(1300);
  for (let k = 0; k < steps; k++) await p.keyboard.press('ArrowRight'); await p.waitForTimeout(400); };
(async () => {
  const b = await chromium.launch(), ctx = await b.newContext({ viewport: { width: 1440, height: 810 } }), p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(URL); await p.waitForTimeout(600);
  const txt = id => p.$eval('#' + id, e => e.textContent);
  // landscape: drag the start from the deep valley's side over to the shallow one's side
  await go(p, 's-land', 2);
  const h = await p.$eval('#fig-land svg circle[style*="grab"]', e => { const r = e.getBoundingClientRect(); return [r.x + r.width / 2, r.y + r.height / 2]; });
  const before = await p.$eval('#fig-land svg', e => e.innerHTML);
  await p.mouse.move(...h); await p.mouse.down(); await p.mouse.move(h[0] - 330, h[1] - 60, { steps: 12 }); await p.mouse.up(); await p.waitForTimeout(300);
  console.log('landscape redrawn after drag:', await p.$eval('#fig-land svg', (e, b) => e.innerHTML !== b, before));
  await p.screenshot({ path: 'screenshots/int1-land-dragged.png' });
  // gradient descent: each learning rate, played to the end
  await go(p, 's-gd', 3);
  for (const n of ['small', 'good', 'large']) { await p.click('#b-gd-' + n); await p.waitForTimeout(5200);
    console.log('GD', n, 'eta', await txt('v-gd-eta'), 'step', await txt('v-gd-k'), 'loss', await txt('v-gd-l'));
    await p.screenshot({ path: `screenshots/int1-gd-${n}.png` }); }
  // XOR training: play to the end, then scrub back
  await go(p, 's-train', 1); await p.waitForTimeout(8000);
  console.log('train end: step', await txt('v-tr-k'), 'loss', await txt('v-tr-l'), 'acc', await txt('v-tr-a'));
  await p.screenshot({ path: 'screenshots/int1-train-end.png' });
  await p.$eval('#r-tr', e => { e.value = '25'; e.dispatchEvent(new Event('input')); });
  console.log('train frame 25: step', await txt('v-tr-k'), 'loss', await txt('v-tr-l'), 'acc', await txt('v-tr-a'));
  await p.screenshot({ path: 'screenshots/int1-train-25.png' });
  const [pop] = await Promise.all([ctx.waitForEvent('page'), p.keyboard.press('p')]);
  await pop.waitForTimeout(1500); await pop.screenshot({ path: 'screenshots/int1-presenter.png' });
  console.log('presenter title:', await pop.title(), 'errors', JSON.stringify(errs));
  for (const [name, opts] of [['dark', { viewport: { width: 1440, height: 810 }, colorScheme: 'dark' }], ['phone', { viewport: { width: 390, height: 844 } }]]) {
    const c = await b.newContext(opts), q = await c.newPage(); const e2 = []; q.on('pageerror', e => e2.push(e.message));
    await q.goto(URL); await q.waitForTimeout(600);
    for (const [id, s] of [['s-pand', 0], ['s-recap', 2], ['s-onehot', 3], ['s-land', 4], ['s-gd', 3], ['s-mp', 1], ['s-fwd', 3], ['s-hand', 3], ['s-train', 0]]) {
      await go(q, id, s); await q.waitForTimeout(500); await q.screenshot({ path: `screenshots/int1-${name}-${id}.png` }); }
    const over = await q.evaluate(() => [...document.querySelectorAll('.slide')].filter(s => s.scrollWidth > document.documentElement.clientWidth + 1).map(s => s.id));
    console.log(name, 'overflowing slides:', JSON.stringify(over), 'errors', JSON.stringify(e2));
  }
  await b.close();
})();
