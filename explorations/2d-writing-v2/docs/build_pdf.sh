#!/bin/bash
# Build PDFs of the report and the gallery: markdown -> HTML (pandoc) -> PDF
# (headless Chromium via Playwright; no LaTeX is installed here).
set -euo pipefail
cd "$(dirname "$0")"
cat > /tmp/report_style.css <<'CSS'
body { font-family: Georgia, serif; max-width: 46em; margin: 2em auto; line-height: 1.45; font-size: 11pt; }
pre, code { font-family: "DejaVu Sans Mono", monospace; font-size: 9pt; }
pre { background: #f5f5f5; padding: 0.6em; white-space: pre-wrap; }
table { border-collapse: collapse; font-size: 10pt; }
td, th { border: 1px solid #999; padding: 3px 8px; }
h1 { font-size: 18pt; } h2 { font-size: 14pt; } h3 { font-size: 12pt; }
CSS
for name in report gallery; do
  pandoc "$name.md" -f gfm -t html -s --metadata pagetitle="$name" -c /tmp/report_style.css \
    --embed-resources -o "/tmp/$name.html"
  node -e "
    const { chromium } = require('playwright');
    (async () => {
      const b = await chromium.launch(); const p = await b.newPage();
      await p.goto('file:///tmp/$name.html');
      await p.pdf({ path: '$name.pdf', format: 'A4', margin: { top: '18mm', bottom: '18mm', left: '15mm', right: '15mm' } });
      await b.close();
    })();"
  echo "wrote docs/$name.pdf"
done
