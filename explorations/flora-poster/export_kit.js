// Export every poster element as its own vector PDF and transparent PNG, plus a
// numbered layout map and a position table, for rebuilding the poster in Keynote.
//
// Run (from this folder):  node export_kit.js landscape   (or: node export_kit.js a0)
// Needs Playwright with Chromium (this script uses the global install at PW below).
// Output: <kit>/{pdf,png}/NN-name.{pdf,png}, layout-map.png, elements.csv, copy.md, README.md

const fs = require('fs');
const path = require('path');
const PW = process.env.PLAYWRIGHT_MODULE || '/opt/node22/lib/node_modules/playwright';
const { chromium } = require(PW);

const PX_PER_PT = 4 / 3;      // CSS px are 1/96 in, Keynote points are 1/72 in
const PNG_SCALE = 2;          // PNGs at 192 px per inch of printed size

// Landscape poster: elements in reading order. Each entry: [name, path from the poster root].
// A path is a list of child indices: [column, child, grandchild, ...].
const LANDSCAPE_ELEMENTS = [
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

// Landscape background shapes: drawn as plain rectangles in Keynote, not exported.
const LANDSCAPE_SHAPES = [
  ['background',   { x: 0, y: 0, w: 4608, h: 3456 }, '#F6F7F5'],
  ['center-panel', { x: 1240, y: 0, w: 2128, h: 3456 }, '#E6ECF4'],
];

// The A0 poster marks its elements in the markup instead: data-kit="name" on each element
// (document order = reading order) and data-kit-shape="name" on background panels.
const CONFIGS = {
  landscape: { poster: 'poster.html', out: 'keynote-kit', W: 4608, H: 3456, size: '48 × 36 in',
               elements: LANDSCAPE_ELEMENTS, shapes: LANDSCAPE_SHAPES },
  a0:        { poster: 'poster-a0.html', out: 'keynote-kit-a0', W: 3179, H: 4494, size: 'A0 portrait, 841 × 1189 mm',
               elements: 'data-kit', shapes: 'data-kit' },
};

// CSS that strips page and column backgrounds so exports are transparent.
const TRANSPARENT_CSS = `
  html, body, body > div > div, body > div > div > div { background: transparent !important; }
`;

function pad(i) { return String(i).padStart(2, '0'); }

// Open the poster in a fresh page with fonts loaded and every element tagged data-kit="name".
async function openPoster(browser, cfg, scale) {
  const p = await browser.newPage({ viewport: { width: cfg.W, height: cfg.H }, deviceScaleFactor: scale });
  await p.goto('file://' + path.join(__dirname, cfg.poster));
  await p.evaluate(() => document.fonts.ready);
  if (Array.isArray(cfg.elements)) {
    await p.evaluate((elements) => {
      const root = document.querySelector('body > div > div');
      for (const [name, idx] of elements) {
        let el = root;
        for (const i of idx) {
          el = el.children[i];
          if (!el) throw new Error(`path ${idx} for ${name} does not exist`);
        }
        el.setAttribute('data-kit', name);
      }
    }, cfg.elements);
  }
  return p;
}

async function main(cfg) {
  const OUT = path.join(__dirname, cfg.out);
  for (const d of ['pdf', 'png']) fs.mkdirSync(path.join(OUT, d), { recursive: true });
  const browser = await chromium.launch();

  // Pass 1: measure boxes, text and background shapes; draw the map.
  const page = await openPoster(browser, cfg, 0.5);
  await page.waitForTimeout(1000);
  const boxes = await page.evaluate(() => [...document.querySelectorAll('[data-kit]')].map((el) => {
    const r = el.getBoundingClientRect();
    // SVG charts have no innerText; list their text labels instead.
    const text = el.innerText !== undefined ? el.innerText.trim()
      : [...el.querySelectorAll('text')].map((t) => t.textContent).join(' | ');
    return { name: el.dataset.kit, x: r.x, y: r.y, w: r.width, h: r.height, text };
  }));
  if (Array.isArray(cfg.elements) && boxes.length !== cfg.elements.length) {
    throw new Error(`expected ${cfg.elements.length} elements, found ${boxes.length}`);
  }
  const shapes = Array.isArray(cfg.shapes) ? cfg.shapes : await page.evaluate(({ W, H }) => {
    const hex = (c) => '#' + c.match(/\d+/g).slice(0, 3).map((v) => (+v).toString(16).padStart(2, '0')).join('').toUpperCase();
    const root = document.querySelector('body > div > div');
    return [['background', { x: 0, y: 0, w: W, h: H }, hex(getComputedStyle(root).backgroundColor)],
      ...[...document.querySelectorAll('[data-kit-shape]')].map((el) => {
        const r = el.getBoundingClientRect();
        return [el.dataset.kitShape, { x: r.x, y: r.y, w: r.width, h: r.height }, hex(getComputedStyle(el).backgroundColor)];
      })];
  }, cfg);

  // Fail loudly if the poster structure changed and a box is empty or off the page.
  for (const b of boxes) {
    if (b.w < 1 || b.h < 1 || b.x < 0 || b.y < 0 || b.x + b.w > cfg.W + 0.5 || b.y + b.h > cfg.H + 0.5) {
      throw new Error(`bad box for ${b.name}: ${JSON.stringify(b)}`);
    }
  }

  await page.evaluate(({ boxes, W, H }) => {
    const layer = document.createElement('div');
    layer.style.cssText = `position:absolute;left:0;top:0;width:${W}px;height:${H}px;pointer-events:none`;
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
  }, { boxes, W: cfg.W, H: cfg.H });
  await page.screenshot({ path: path.join(OUT, 'layout-map.png') });
  await page.close();

  // Pass 2: one vector PDF and one transparent PNG per element.
  for (let i = 0; i < boxes.length; i++) {
    const b = boxes[i];
    const file = `${pad(i + 1)}-${b.name}`;
    const p = await openPoster(browser, cfg, PNG_SCALE);
    await p.addStyleTag({ content: TRANSPARENT_CSS });
    // Hide everything except this element, then shift it to the page origin for the PDF.
    await p.evaluate(() => {
      document.querySelectorAll('body *').forEach((n) => { n.style.visibility = 'hidden'; });
    });
    const handle = await p.evaluateHandle((name) => {
      const el = document.querySelector(`[data-kit="${name}"]`);
      el.style.visibility = 'visible';
      el.querySelectorAll('*').forEach((n) => { n.style.visibility = 'visible'; });
      return el;
    }, b.name);
    await handle.asElement().screenshot({ path: path.join(OUT, 'png', file + '.png'), omitBackground: true });
    // PDF: a page cut to the element's box. The document is clipped to that box too;
    // otherwise Chromium shrinks the whole poster to fit the small page.
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

  // Position table (Keynote points, top-left origin) and text copy.
  const pt = (v) => (v / PX_PER_PT).toFixed(0);
  const rows = ['id,name,file,x_pt,y_pt,w_pt,h_pt,fill'];
  shapes.forEach(([name, r, fill], i) =>
    rows.push(`S${i + 1},${name},(draw a rectangle),${pt(r.x)},${pt(r.y)},${pt(r.w)},${pt(r.h)},${fill}`));
  boxes.forEach((b, i) =>
    rows.push(`${pad(i + 1)},${b.name},${pad(i + 1)}-${b.name}.pdf,${pt(b.x)},${pt(b.y)},${pt(b.w)},${pt(b.h)},`));
  fs.writeFileSync(path.join(OUT, 'elements.csv'), rows.join('\n') + '\n');

  const copy = ['# Poster text, by element', ''];
  boxes.forEach((b, i) => copy.push(`## ${pad(i + 1)} ${b.name}`, '', b.text, ''));
  fs.writeFileSync(path.join(OUT, 'copy.md'), copy.join('\n'));
  fs.writeFileSync(path.join(OUT, 'README.md'), kitReadme(cfg, shapes, boxes, rows));
  console.log('\ndone:', boxes.length, 'elements');
}

function kitReadme(cfg, shapes, boxes, rows) {
  const slide = `${(cfg.W / PX_PER_PT).toFixed(0)} × ${(cfg.H / PX_PER_PT).toFixed(0)} pt`;
  const table = rows.slice(1).map((r) => {
    const [id, name, , x, y, w, h, fill] = r.split(',');
    return `| ${id} | ${name} | ${x} | ${y} | ${w} | ${h} | ${fill} |`;
  });
  const shapeIds = shapes.map((_, i) => `S${i + 1}`).join(', ');
  return [
    '# Keynote kit', '',
    `Every element of the ${cfg.size} poster as its own file, plus where it goes. See \`layout-map.png\` for the numbered map.`, '',
    '## Setting up the slide', '',
    `1. In Keynote, open the Document inspector and choose Slide Size > Custom: ${slide} (${cfg.size} at 72 pt per inch).`,
    `2. Draw the background rectangles (${shapeIds}) from the table and send them to the back.`,
    '3. Drag in each file from `pdf/` and type its x, y, width and height into the Arrange inspector. Positions are the top-left corner.', '',
    'Use the PDFs: they are vector, so text and charts stay sharp at any size, and the fonts are embedded. ' +
    'The `png/` folder has the same elements as transparent PNGs (192 px per printed inch) in case you prefer images. ' +
    'Text inside these files is not editable; `copy.md` has all the text if you want to retype a block as a Keynote text box ' +
    '(fonts: Archivo and STIX Two Text, both free on Google Fonts).', '',
    `## Positions (points, slide ${slide})`, '',
    '| id | element | x | y | w | h | fill |', '|---|---|--:|--:|--:|--:|---|',
    ...table, '',
    `The same table is in \`elements.csv\`. Regenerate everything with \`node export_kit.js ${cfg === CONFIGS.a0 ? 'a0' : 'landscape'}\` from the folder above.`, '',
  ].join('\n');
}

const which = process.argv[2];
if (!CONFIGS[which]) {
  console.error(`usage: node export_kit.js <${Object.keys(CONFIGS).join('|')}>`);
  process.exit(1);
}
main(CONFIGS[which]).catch((e) => { console.error(e); process.exit(1); });
