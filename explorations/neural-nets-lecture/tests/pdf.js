// Run from this folder: NODE_PATH=$(npm root -g) node pdf.js <1|2> [steps]
// Writes ../pdf/slides_<deck>/<n>.png: every slide at its last step, controls hidden, light theme.
// With "steps", writes ../pdf/steps_<deck>/<n>-<k>.png instead: every step of every slide.
// Animated slides (replays) are captured once the picture stops changing. ../make_pdf.py combines them.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const W = 1600, H = 900, SCALE = 2, SETTLE_MAX_MS = 20000;
(async () => {
  const deck = process.argv[2], every = process.argv[3] === 'steps', out = path.resolve(__dirname, `../pdf/${every ? 'steps' : 'slides'}_${deck}`);
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: SCALE, colorScheme: 'light' });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + path.resolve(__dirname, `../neural_nets_${deck}.html`)); await p.waitForTimeout(800);
  await p.addStyleTag({ content: '#hud,#progress{display:none !important}' });
  const ids = await p.$$eval('.slide', s => s.map(x => [x.id, +x.dataset.steps || 0]));
  for (const [n, [id, steps]] of ids.entries()) {
    await p.waitForTimeout(1200);
    if (!every) for (let k = 0; k < steps; k++) { await p.keyboard.press('ArrowRight'); await p.waitForTimeout(500); }
    for (let k = every ? 0 : steps; k <= steps; k++) {
      if (every && k > 0) { await p.keyboard.press('ArrowRight'); await p.waitForTimeout(500); }
      // wait until two screenshots one second apart are identical
      let prev = await p.screenshot(), t = 0;
      while (t < SETTLE_MAX_MS) { await p.waitForTimeout(1000); t += 1000; const cur = await p.screenshot(); if (cur.equals(prev)) break; prev = cur; }
      if (t >= SETTLE_MAX_MS) errs.push(`${id} step ${k}: still changing after ${SETTLE_MAX_MS} ms`);
      fs.writeFileSync(path.join(out, `${String(n + 1).padStart(2, '0')}-${id}` + (every ? `-${k}` : '') + '.png'), prev);
    }
    await p.keyboard.press('ArrowRight');
  }
  console.log(ids.length, 'slides; errors', JSON.stringify(errs));
  await b.close();
})();
