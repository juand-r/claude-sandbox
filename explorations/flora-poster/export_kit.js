// Export every poster element as its own vector PDF and transparent PNG, plus a
// numbered layout map and a position table, for rebuilding the poster in Keynote.
//
// Run (from this folder):  node export_kit.js
// Needs Playwright with Chromium (this script uses the global install at PW below).
// Output: keynote-kit/{pdf,png}/NN-name.{pdf,png}, layout-map.png, elements.csv, copy.md

const fs = require('fs');
const path = require('path');
const PW = process.env.PLAYWRIGHT_MODULE || '/opt/node22/lib/node_modules/playwright';
const { chromium } = require(PW);

const POSTER = path.join(__dirname, 'poster.html');
const OUT = path.join(__dirname, 'keynote-kit');
const PX_PER_PT = 4 / 3;      // CSS px are 1/96 in, Keynote points are 1/72 in
const PNG_SCALE = 2;          // PNGs at 192 px per inch of printed size

// Elements in reading order. Each entry: [name, path from the poster root].
// A path is a list of child indices: [column, child, grandchild, ...].
const ELEMENTS = [
  ['title-block',          [0, 0]],
  ['s1-heading',           [0, 1, 0]],
  ['s1-text',              [0, 1, 1]],
  ['s1-noble-gas-diagram', [0, 1, 2]],
  ['s2-heading',           [0, 2, 0]],
  ['s2-text',              [0, 2, 1]],
  ['s2-equation',          [0, 2, 2]],
  ['s2-note',              [0, 2, 3]],
  ['s3-heading',           [0, 3, 0]],
  ['s3-text',              [0, 3, 1]],
  ['s3-flora-diagram',     [0, 3, 2]],
  ['s3-note',              [0, 3, 3]],
  ['main-idea',            [1, 0]],
  ['main-subtext',         [1, 1]],
  ['figure-caption',       [1, 2, 0]],
  ['figure-scatter',       [1, 2, 1]],
  ['figure-panel-labels',  [1, 2, 2]],
  ['qr-paper',             [1, 3, 0]],
  ['qr-code',              [1, 3, 1]],
  ['s4-heading',           [2, 0, 0]],
  ['s4-definitions',       [2, 0, 1]],
  ['results-title',        [2, 1, 0]],
  ['results-legend',       [2, 1, 1]],
  ['results-chart',        [2, 1, 2]],
  ['results-takeaway',     [2, 1, 3]],
  ['results-footnote',     [2, 1, 4]],
  ['ablation-title',       [2, 2, 0]],
  ['ablation-note',        [2, 2, 1]],
  ['ablation-table',       [2, 2, 2]],
  ['ablation-footnote',    [2, 2, 3]],
  ['validator-title',      [2, 3, 0]],
  ['validator-note',       [2, 3, 1]],
  ['validator-chart',      [2, 3, 2]],
  ['validator-takeaway',   [2, 3, 3]],
  ['limits-title',         [2, 4, 0]],
  ['limits-text',          [2, 4, 1]],
];

// Background shapes: drawn as plain rectangles in Keynote, not exported.
const SHAPES = [
  ['background',   { x: 0, y: 0, w: 4608, h: 3456 }, '#F6F7F5'],
  ['center-panel', { x: 1240, y: 0, w: 2128, h: 3456 }, '#E6ECF4'],
];

// CSS that strips page and column backgrounds so exports are transparent.
const TRANSPARENT_CSS = `
  html, body, body > div > div, body > div > div > div { background: transparent !important; }
`;

function pad(i) { return String(i).padStart(2, '0'); }

async function main() {
  for (const d of ['pdf', 'png']) fs.mkdirSync(path.join(OUT, d), { recursive: true });
  const browser = await chromium.launch();

  // Pass 1: measure boxes and text, draw the map.
  const page = await browser.newPage({ viewport: { width: 4608, height: 3456 }, deviceScaleFactor: 0.5 });
  await page.goto('file://' + POSTER);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(1000);
  const boxes = await page.evaluate((elements) => {
    const root = document.querySelector('body > div > div');
    return elements.map(([name, p]) => {
      let el = root;
      for (const i of p) {
        el = el.children[i];
        if (!el) throw new Error(`path ${p} for ${name} does not exist`);
      }
      el.setAttribute('data-kit', name);
      const r = el.getBoundingClientRect();
      // SVG charts have no innerText; list their text labels instead.
      const text = el.innerText !== undefined ? el.innerText.trim()
        : [...el.querySelectorAll('text')].map((t) => t.textContent).join(' | ');
      return { name, x: r.x, y: r.y, w: r.width, h: r.height, text };
    });
  }, ELEMENTS);

  // Fail loudly if the poster structure changed and a box is empty or off the page.
  for (const b of boxes) {
    if (b.w < 1 || b.h < 1 || b.x < 0 || b.y < 0 || b.x + b.w > 4608.5 || b.y + b.h > 3456.5) {
      throw new Error(`bad box for ${b.name}: ${JSON.stringify(b)}`);
    }
  }

  await page.evaluate((boxes) => {
    const layer = document.createElement('div');
    layer.style.cssText = 'position:absolute;left:0;top:0;width:4608px;height:3456px;pointer-events:none';
    boxes.forEach((b, i) => {
      const box = document.createElement('div');
      box.style.cssText = `position:absolute;left:${b.x}px;top:${b.y}px;width:${b.w}px;height:${b.h}px;` +
        'box-sizing:border-box;border:5px solid #E0007A;background:rgba(224,0,122,.06)';
      const tag = document.createElement('div');
      tag.textContent = String(i + 1).padStart(2, '0');
      tag.style.cssText = 'position:absolute;left:-5px;top:-5px;padding:2px 12px;background:#E0007A;color:#fff;' +
        'font:700 40px/1.1 Archivo,sans-serif';
      box.appendChild(tag);
      layer.appendChild(box);
    });
    document.querySelector('body > div').style.position = 'relative';
    document.querySelector('body > div').appendChild(layer);
  }, boxes);
  await page.screenshot({ path: path.join(OUT, 'layout-map.png') });
  await page.close();

  // Pass 2: one vector PDF and one transparent PNG per element.
  for (let i = 0; i < boxes.length; i++) {
    const b = boxes[i];
    const file = `${pad(i + 1)}-${b.name}`;
    const p = await browser.newPage({ viewport: { width: 4608, height: 3456 }, deviceScaleFactor: PNG_SCALE });
    await p.goto('file://' + POSTER);
    await p.evaluate(() => document.fonts.ready);
    await p.addStyleTag({ content: TRANSPARENT_CSS });
    // Hide everything except this element, then shift it to the page origin for the PDF.
    await p.evaluate(() => {
      document.querySelectorAll('body *').forEach((n) => { n.style.visibility = 'hidden'; });
    });
    const handle = await p.evaluateHandle((pathIdx) => {
      let el = document.querySelector('body > div > div');
      for (const i of pathIdx) el = el.children[i];
      el.style.visibility = 'visible';
      el.querySelectorAll('*').forEach((n) => { n.style.visibility = 'visible'; });
      return el;
    }, ELEMENTS[i][1]);
    await handle.asElement().screenshot({ path: path.join(OUT, 'png', file + '.png'), omitBackground: true });
    // PDF: a page cut to the element's box. The document is clipped to that box too;
    // otherwise Chromium shrinks the whole 4608 px poster to fit the small page.
    const w = Math.ceil(b.w), h = Math.ceil(b.h);
    await p.addStyleTag({ content: `
      @page { size: ${w}px ${h}px; margin: 0 }
      html, body { width: ${w}px; height: ${h}px; overflow: hidden; margin: 0 }
      body > div > div { position: absolute; left: ${-b.x}px; top: ${-b.y}px }` });
    await p.pdf({ path: path.join(OUT, 'pdf', file + '.pdf'), preferCSSPageSize: true, printBackground: true });
    await p.close();
    process.stdout.write(`${file} `);
  }
  await browser.close();

  // Position table (Keynote points, top-left origin, slide 3456 x 2592 pt) and text copy.
  const pt = (v) => (v / PX_PER_PT).toFixed(0);
  const rows = ['id,name,file,x_pt,y_pt,w_pt,h_pt,fill'];
  SHAPES.forEach(([name, r, fill], i) =>
    rows.push(`S${i + 1},${name},(draw a rectangle),${pt(r.x)},${pt(r.y)},${pt(r.w)},${pt(r.h)},${fill}`));
  boxes.forEach((b, i) =>
    rows.push(`${pad(i + 1)},${b.name},${pad(i + 1)}-${b.name}.pdf,${pt(b.x)},${pt(b.y)},${pt(b.w)},${pt(b.h)},`));
  fs.writeFileSync(path.join(OUT, 'elements.csv'), rows.join('\n') + '\n');

  const copy = ['# Poster text, by element', ''];
  boxes.forEach((b, i) => copy.push(`## ${pad(i + 1)} ${b.name}`, '', b.text, ''));
  fs.writeFileSync(path.join(OUT, 'copy.md'), copy.join('\n'));
  console.log('\ndone:', boxes.length, 'elements');
}

main().catch((e) => { console.error(e); process.exit(1); });
