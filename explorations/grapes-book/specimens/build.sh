#!/usr/bin/env bash
# Build every specimen with LuaLaTeX and join them into one PDF.
# Usage: ./build.sh   (run from this directory)
set -euo pipefail
cd "$(dirname "$0")"
SPECIMENS=(00-intro 01-footnotes 02-sidenotes 03-sidenotes-margin 04-talmud 05-apparatus)
for s in "${SPECIMENS[@]}"; do
  # Three passes: bigfoot, perpage and reledmac need the .aux of earlier runs.
  for pass in 1 2 3; do
    lualatex -interaction=nonstopmode -halt-on-error "$s.tex" > /dev/null \
      || { echo "FAILED: $s (see $s.log)"; exit 1; }
  done
  echo "built $s.pdf"
done
pdfunite $(printf '%s.pdf ' "${SPECIMENS[@]}") ../grapes-specimens.pdf
echo "wrote ../grapes-specimens.pdf"
