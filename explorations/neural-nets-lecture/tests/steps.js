// Run from this folder: NODE_PATH=$(npm root -g) node steps.js <1|2> [slide-id ...]
// Screenshots every step of every slide (or of the slides named) to screenshots/d${deck}-step-<n>-<id>-<k>.png,
// to check that each figure builds up in order. Reports JS errors.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const deck = process.argv[2], only = process.argv.slice(3);
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1440, height: 810 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + path.resolve(__dirname, `../neural_nets_${deck}.html`)); await p.waitForTimeout(800);
  const ids = await p.$$eval('.slide', s => s.map(x => [x.id, +x.dataset.steps || 0]));
  for (const [n, [id, steps]] of ids.entries()) {
    if (only.length && !only.includes(id)) { for (let k = 0; k <= steps; k++) await p.keyboard.press('ArrowRight'); await p.waitForTimeout(150); continue; }
    await p.waitForTimeout(1500);
    for (let k = 0; k <= steps; k++) {
      await p.screenshot({ path: `screenshots/d${deck}-step-${String(n + 1).padStart(2, '0')}-${id}-${k}.png` });
      await p.keyboard.press('ArrowRight'); await p.waitForTimeout(k < steps ? 700 : 300);
    }
  }
  console.log('errors', JSON.stringify(errs));
  await b.close();
})();
