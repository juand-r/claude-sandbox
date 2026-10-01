#!/usr/bin/env bash
# Build a document that uses grapes.sty.
#   ./build.sh MAIN            -> MAIN.pdf            (margin notes on)
#   ./build.sh MAIN nomargin   -> MAIN-nomargin.pdf   (asides at the foot)
# MAIN is the name of a .tex file in this directory, without .tex.
# Today the only one is "sample" (the typography sample, not the book).
set -euo pipefail
cd "$(dirname "$0")"
source ./lib.sh
main="${1:?usage: $0 MAIN [margin|nomargin]}"
mode="${2:-margin}"
[ -f "$main.tex" ] || { echo "no such file: $main.tex"; exit 2; }
case "$mode" in
  margin)   job="$main" ;;
  nomargin) job="$main-nomargin" ;;
  *) echo "usage: $0 MAIN [margin|nomargin]"; exit 2 ;;
esac
grapes_build . "$main" "$mode" "$job" || { echo "FAILED: $job"; exit 1; }
grep -E 'Package grapes Warning|Overfull' "$job.log" || true
echo "wrote $job.pdf ($(pdfinfo "$job.pdf" | awk '/Pages/{print $2}') pages)"
