// Build-time math typesetting with KaTeX (run by assemble.py; needs `npm install` in this folder).
//
//   node tex.js page.html   → page.html with every \( … \) (inline) and \[ … \] (display) formula
//                             replaced by KaTeX's HTML; written to stdout
//   node tex.js --css       → KaTeX's stylesheet with its woff2 fonts embedded as base64, so the deck
//                             needs no network; written to stdout
//
// A formula that KaTeX cannot parse stops the build (throwOnError), so mistakes fail loudly.
const fs = require('fs'), path = require('path'), katex = require('katex');
const dist = path.join(path.dirname(require.resolve('katex')), '..', 'dist');

if (process.argv[2] === '--css') {
  let css = fs.readFileSync(path.join(dist, 'katex.min.css'), 'utf8');
  // keep only the woff2 source of each @font-face, inlined
  css = css.replace(/src:url\(fonts\/([^)]+\.woff2)\) format\("woff2"\)[^;}]*/g, (_, f) =>
    `src:url(data:font/woff2;base64,${fs.readFileSync(path.join(dist, 'fonts', f)).toString('base64')}) format("woff2")`);
  if (/url\(fonts\//.test(css)) throw new Error('a KaTeX font was not embedded');
  process.stdout.write(css);
} else {
  const html = fs.readFileSync(process.argv[2], 'utf8');
  const render = tex => katex.renderToString(tex.replace(/&amp;/g, '&'), { throwOnError: true, strict: 'error' });
  // display formulas keep the deck's own block layout (span.math.dm), so KaTeX renders them inline;
  // \displaystyle gives them full-size fractions and sums
  let out = html.replace(/\\\[([\s\S]+?)\\\]/g, (_, t) => render('\\displaystyle ' + t));
  out = out.replace(/\\\(([\s\S]+?)\\\)/g, (_, t) => render(t));
  process.stdout.write(out);
}
