// Run from this folder: NODE_PATH=$(npm root -g) node recap2.js  (screenshots go to ./screenshots/)
// The live network on the recap slide (class 2, slide 2): drags a weight bar and steps an input,
// first in the deck window, then from the presenter window; checks that leaving the slide resets it.
// Expected numbers (biases 0, see code_2.js): start p = (0.79, 0.21); w(x1->a1) = 3 gives 0.87;
// then x2 = -0.5 gives 0.94, or x2 = 1 gives 0.82.
const { chromium } = require('playwright');
const URL = 'file://' + require('path').resolve(__dirname, '../neural_nets_2.html');
const HITS = '#fig-recap .noanim rect[fill="transparent"]';   // 12 weight bars, then up/down for x1, up/down for x2
(async () => {
  const b = await chromium.launch(), ctx = await b.newContext({ viewport: { width: 1440, height: 810 } }), p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(URL); await p.waitForTimeout(600);
  await p.evaluate(() => document.getElementById('s-recap').scrollIntoView()); await p.waitForTimeout(1500);
  await p.screenshot({ path: 'screenshots/recap-0.png' });
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(600);
  await p.screenshot({ path: 'screenshots/recap-1.png' });
  const txt = () => p.$$eval('#fig-recap .noanim text', ts => ts.map(t => t.textContent).filter(s => /\d/.test(s)).join(' '));
  const dragUp = async (page, h) => { const bb = await h.boundingBox();
    await page.mouse.move(bb.x + bb.width / 2, bb.y + bb.height / 2); await page.mouse.down();
    await page.mouse.move(bb.x + bb.width / 2, bb.y - 20, { steps: 6 }); await page.mouse.up(); await page.waitForTimeout(300); };
  const clickAt = async (page, h) => { const bb = await h.boundingBox(); await page.mouse.click(bb.x + bb.width / 2, bb.y + bb.height / 2); await page.waitForTimeout(300); };
  console.log('deck start:', await txt());
  await dragUp(p, (await p.$$(HITS))[0]);
  console.log('deck, w(x1->a1) dragged to the top:', await txt());
  for (let k = 0; k < 2; k++) await clickAt(p, (await p.$$(HITS))[15]);
  console.log('deck, x2 down twice:', await txt(), '| slide', await p.$eval('#counter', e => e.textContent));
  await p.screenshot({ path: 'screenshots/recap-2.png' });
  // presenter window: the same moves on its copy of the slide
  await p.keyboard.press('ArrowLeft'); await p.waitForTimeout(300); await p.keyboard.press('ArrowLeft'); await p.waitForTimeout(500);
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(500); await p.keyboard.press('ArrowRight'); await p.waitForTimeout(500);
  const [pop] = await Promise.all([ctx.waitForEvent('page'), p.keyboard.press('p')]);
  pop.on('pageerror', e => errs.push('presenter: ' + e.message)); await pop.setViewportSize({ width: 1440, height: 810 }); await pop.waitForTimeout(2000);
  console.log('presenter start:', await txt());
  await dragUp(pop, (await pop.$$('#stage ' + HITS))[0]);
  console.log('presenter, w(x1->a1) dragged to the top:', await txt());
  await clickAt(pop, (await pop.$$('#stage ' + HITS))[14]);
  console.log('presenter, x2 up:', await txt(), '| slide', await p.$eval('#counter', e => e.textContent));
  await pop.waitForTimeout(900); await pop.screenshot({ path: 'screenshots/recap-presenter.png' });
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(500); await p.keyboard.press('ArrowLeft'); await p.waitForTimeout(800);
  console.log('after leaving and coming back:', await txt());
  console.log('errors', JSON.stringify(errs));
  await b.close();
})();
