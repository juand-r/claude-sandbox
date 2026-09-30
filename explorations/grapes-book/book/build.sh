#!/usr/bin/env bash
# Build the book.
#   ./build.sh           -> grapes.pdf            (margin notes on)
#   ./build.sh nomargin  -> grapes-nomargin.pdf   (asides become footnotes)
# Three LuaLaTeX passes: bigfoot and perpage need the .aux of earlier runs.
set -euo pipefail
cd "$(dirname "$0")"
mode="${1:-margin}"
case "$mode" in
  margin)   job=grapes;          pre="" ;;
  nomargin) job=grapes-nomargin; pre='\PassOptionsToPackage{nomargin}{grapes}' ;;
  *) echo "usage: $0 [margin|nomargin]"; exit 2 ;;
esac
for pass in 1 2 3; do
  lualatex -interaction=nonstopmode -halt-on-error -jobname="$job" \
    "${pre}\input{grapes}" > /dev/null \
    || { echo "FAILED on pass $pass (see $job.log)"; grep -A3 '^!' "$job.log" | head -20; exit 1; }
done
grep -E 'Package grapes Warning|Overfull' "$job.log" || true
echo "wrote $job.pdf ($(pdfinfo "$job.pdf" | awk '/Pages/{print $2}') pages)"
