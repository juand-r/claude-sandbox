// Run from this folder: NODE_PATH=$(npm root -g) node interact.js  (screenshots go to ./screenshots/)
// Drives the interactive figures, screenshots every slide at step 0 (to check that each figure
// starts with the data alone), opens the presenter view, and checks dark mode and phone width.
const { chromium } = require('playwright');
const URL = 'file://' + require('path').resolve(__dirname, '../svm_lecture.html');
const go = async (p, id) => { await p.evaluate(id => document.getElementById(id).scrollIntoView(), id); await p.waitForTimeout(1300); };
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1440, height: 810 } });
  const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(URL); await p.waitForTimeout(600);
  const txt = id => p.$eval('#' + id, e => e.textContent);
  // step 0 of every slide
  const ids = await p.$$eval('.slide', s => s.map(x => x.id));
  for (const [k, id] of ids.entries()) { await go(p, id); await p.screenshot({ path: `screenshots/step0-${String(k + 1).padStart(2, '0')}.png` }); }
  // slide 7: drag a far point (no change), then a support vector across the line (no solution)
  await go(p, 's-sv');
  const pt = async i => p.$eval('#fig-sv svg', (svg, i) => { const c = svg.querySelectorAll('circle[r="9"]')[i].getBoundingClientRect(); return [c.x + c.width / 2, c.y + c.height / 2]; }, i);
  const drag = async (i, dx, dy) => { const [x, y] = await pt(i); await p.mouse.move(x, y); await p.mouse.down(); await p.mouse.move(x + dx, y + dy, { steps: 6 }); await p.mouse.up(); await p.waitForTimeout(200); };
  console.log('sv start: width', await txt('v-sv-w'), 'n', await txt('v-sv-n'));
  await drag(5, -30, 20);   // the far positive (9, 8)
  console.log('far point moved: width', await txt('v-sv-w'), 'n', await txt('v-sv-n'));
  await drag(0, -40, 40);   // support vector (5.5, 6.5) into the street
  console.log('support vector moved into street: width', await txt('v-sv-w'), 'n', await txt('v-sv-n'));
  await drag(0, -120, 120); // further, across the line
  console.log('moved across:', await txt('v-sv-w'), '|', await txt('rd-sv'));
  await p.screenshot({ path: 'screenshots/int-sv-broken.png' });
  await p.click('#b-sv-reset'); await p.waitForTimeout(200);
  console.log('after reset: width', await txt('v-sv-w'));
  // slide 9: C slider
  await go(p, 's-c');
  for (const v of ['-200', '0', '200']) { await p.$eval('#r-c', (e, v) => { e.value = v; e.dispatchEvent(new Event('input')); }, v);
    console.log('C slider', v, await txt('v-c-c'), 'width', await txt('v-c-w'), 'SV', await txt('v-c-n'), 'mistakes', await txt('v-c-e'), 'sum xi', await txt('v-c-x')); }
  // slide 11: kernels
  await go(p, 's-kernel');
  for (const [d, k] of [['rings', 'linear'], ['rings', 'rbf'], ['xor', 'linear'], ['xor', 'rbf']]) {
    await p.click('#b-k-' + d); await p.click('#b-k-' + k); await p.waitForTimeout(150);
    console.log('kernel', d, k, 'mistakes', await txt('v-k-e'), 'SV', await txt('v-k-n'));
  }
  // slide 10: rotate the 3D view
  await go(p, 's-lift'); for (let k = 0; k < 4; k++) await p.keyboard.press('ArrowRight'); await p.waitForTimeout(600);
  const box = await p.$eval('#fig-lift3d svg', e => { const r = e.getBoundingClientRect(); return [r.x + r.width / 2, r.y + r.height / 2]; });
  await p.mouse.move(...box); await p.mouse.down(); await p.mouse.move(box[0] + 120, box[1] + 30, { steps: 8 }); await p.mouse.up();
  await p.screenshot({ path: 'screenshots/int-lift-rotated.png' });
  // presenter view
  const [pop] = await Promise.all([ctx.waitForEvent('page'), p.keyboard.press('p')]);
  await pop.waitForTimeout(1500); await pop.screenshot({ path: 'screenshots/int-presenter.png' });
  console.log('presenter title:', await pop.title());
  console.log('errors', JSON.stringify(errs));
  for (const [name, opts] of [['dark', { viewport: { width: 1440, height: 810 }, colorScheme: 'dark' }],
                              ['phone', { viewport: { width: 390, height: 844 } }]]) {
    const c = await b.newContext(opts), q = await c.newPage(); const e2 = []; q.on('pageerror', e => e2.push(e.message));
    await q.goto(URL); await q.waitForTimeout(600);
    for (const id of ['s-which', 's-soft', 's-lift', 's-kernel']) { await go(q, id); await q.screenshot({ path: `screenshots/int-${name}-${id}.png` }); }
    const over = await q.evaluate(() => [...document.querySelectorAll('.slide')]
      .filter(s => s.scrollWidth > document.documentElement.clientWidth + 1).map(s => s.id));
    console.log(name, 'overflowing slides:', JSON.stringify(over), 'errors', JSON.stringify(e2));
  }
  await b.close();
})();
