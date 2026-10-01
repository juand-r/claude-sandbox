// Run from this folder: NODE_PATH=$(npm root -g) node <script>.js  (screenshots go to ./screenshots/)
// Slide 3 build: screenshot each step; check the threshold cannot be dragged before it is shown.
const { chromium } = require('playwright');
const URL = 'file://' + require('path').resolve(__dirname, '../roc_auc_lecture.html');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 810 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(URL); await p.waitForTimeout(600);
  await p.keyboard.press('ArrowDown'); await p.waitForTimeout(900);
  await p.keyboard.press('ArrowDown'); await p.waitForTimeout(1600);   // slide 3, step 0
  const box = await p.$eval('#fig-th-strip svg', e => { const r = e.getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height }; });
  const xAt = s => box.x + (100 + s * 636) / 760 * box.w;
  const drag = async s => { await p.mouse.move(xAt(.5), box.y + box.h / 2); await p.mouse.down();
    await p.mouse.move(xAt(s), box.y + box.h / 2, { steps: 4 }); await p.mouse.up(); await p.waitForTimeout(200); };
  for (let k = 0; k <= 3; k++) {
    if (k === 0) { await drag(.8); console.log('step 0 drag ignored? slider =', await p.$eval('#r-th', e => e.value)); }
    if (k === 2) { await drag(.65); console.log('step 2 drag works? slider =', await p.$eval('#r-th', e => e.value)); }
    await p.waitForTimeout(500);
    await p.screenshot({ path: 'screenshots/' + `build3-step${k}.png` });
    await p.keyboard.press('ArrowRight');
  }
  const q = await b.newPage({ viewport: { width: 390, height: 844 } });
  await q.goto(URL); await q.waitForTimeout(800);
  const over = await q.evaluate(() => [...document.querySelectorAll('.slide')]
    .filter(s => s.scrollWidth > document.documentElement.clientWidth + 1).map(s => s.id));
  console.log('phone overflowing slides:', JSON.stringify(over), 'errors', JSON.stringify(errs));
  await b.close();
})();
