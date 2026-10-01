// Run from this folder: NODE_PATH=$(npm root -g) node <script>.js  (screenshots go to ./screenshots/)
// Exercise the interactive figures and check the numbers they show.
const { chromium } = require('playwright');
const URL = 'file://' + require('path').resolve(__dirname, '../roc_auc_lecture.html');
const go = async (p, id) => { await p.evaluate(id => document.getElementById(id).scrollIntoView(), id); await p.waitForTimeout(1200); };
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1440, height: 810 } });
  const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(URL); await p.waitForTimeout(600);
  const txt = id => p.$eval('#' + id, e => e.textContent);
  // slide 7: check all pairs
  await go(p, 's-auc'); await p.click('#b-pr-all'); await p.waitForTimeout(3600);
  console.log('all pairs:', await txt('v-pr-n'), await txt('v-pr-w'), await txt('v-pr-f'));
  await p.screenshot({ path: 'screenshots/' + 'int-auc-all.png' });
  await p.click('#b-pr-reset'); await p.click('#b-pr-1'); await p.waitForTimeout(300);
  console.log('one pair:', await txt('v-pr-n'), '|', await txt('rd-pr'));
  await p.screenshot({ path: 'screenshots/' + 'int-auc-one.png' });
  // slide 8: transforms
  await go(p, 's-mono');
  for (const k of ['cube', 'squash', 'flip', 'id']) {
    await p.click('#b-mono-' + k); await p.waitForTimeout(700);
    console.log(k, 'AUC', await txt('v-mono-auc'), 'range', await txt('v-mono-rng'));
  }
  // slide 3: drag the threshold to score ~0.65, read the matrices
  await go(p, 's-thresh'); await p.keyboard.press('ArrowRight'); await p.keyboard.press('ArrowRight'); await p.waitForTimeout(500);   // reveal the threshold
  const box = await p.$eval('#fig-th-strip svg', e => { const r = e.getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height }; });
  const xAt = s => box.x + (100 + s * 636) / 760 * box.w;
  await p.mouse.move(xAt(.9), box.y + box.h * .5); await p.mouse.down();
  await p.mouse.move(xAt(.65), box.y + box.h * .5, { steps: 5 }); await p.mouse.up();
  await p.waitForTimeout(300);
  console.log('after drag: t slider', await p.$eval('#r-th', e => e.value),
    'cells', await p.$$eval('#cm-rt .n', es => es.map(e => e.textContent).join(',')),
    '| rates', await p.$$eval('#cm-rt .rate', es => es.map(e => e.textContent).join(' ; ')));
  // slide 9: slider values
  await go(p, 's-rare');
  for (const v of ['0', '200', '400']) {
    await p.$eval('#r-rare', (e, v) => { e.value = v; e.dispatchEvent(new Event('input')); }, v);
    console.log('rare', v, await txt('v-rare-n'), await txt('v-rare-fp'), await txt('v-rare-prec'));
  }
  // presenter view opens as a second window
  const [pop] = await Promise.all([ctx.waitForEvent('page'), p.keyboard.press('p')]);
  await pop.waitForTimeout(1500); await pop.screenshot({ path: 'screenshots/' + 'int-presenter.png' });
  console.log('presenter title:', await pop.title());
  console.log('errors', JSON.stringify(errs));
  // dark mode and phone width
  for (const [name, opts] of [['dark', { viewport: { width: 1440, height: 810 }, colorScheme: 'dark' }],
                              ['phone', { viewport: { width: 390, height: 844 } }]]) {
    const c = await b.newContext(opts), q = await c.newPage(); const e2 = []; q.on('pageerror', e => e2.push(e.message));
    await q.goto(URL); await q.waitForTimeout(600);
    for (const id of ['s-thresh', 's-sweep', 's-auc']) { await go(q, id); await q.screenshot({ path: 'screenshots/' + `int-${name}-${id}.png` }); }
    const over = await q.evaluate(() => [...document.querySelectorAll('.slide')]
      .filter(s => s.scrollWidth > document.documentElement.clientWidth + 1).map(s => s.id));
    console.log(name, 'overflowing slides:', JSON.stringify(over), 'errors', JSON.stringify(e2));
  }
  await b.close();
})();
