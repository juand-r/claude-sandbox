// Run from this folder: NODE_PATH=$(npm root -g) node <script>.js  (screenshots go to ./screenshots/)
// Render each slide at its final step; collect console errors.
const { chromium } = require('playwright');
(async () => {
  const theme = process.argv[2] || 'light';
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 810 }, colorScheme: theme });
  const errs = [];
  p.on('pageerror', e => errs.push('pageerror: ' + e.message));
  p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
  await p.goto('file://' + require('path').resolve(__dirname, '../logistic_regression_lecture.html'));
  await p.waitForTimeout(800);
  const n = await p.evaluate(() => document.querySelectorAll('.slide').length);
  for (let i = 0; i < n; i++) {
    const steps = await p.evaluate(i => +document.querySelectorAll('.slide')[i].dataset.steps || 0, i);
    for (let k = 0; k < steps; k++) { await p.keyboard.press('ArrowRight'); await p.waitForTimeout(120); }
    await p.waitForTimeout(1600);   
    await p.screenshot({ path: 'screenshots/' + `shot-${theme}-${String(i + 1).padStart(2, '0')}.png` });
    await p.keyboard.press('ArrowRight'); await p.waitForTimeout(1000);
  }
  console.log('slides', n, 'errors', JSON.stringify(errs));
  await b.close();
})();
