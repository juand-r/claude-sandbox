#!/usr/bin/env bash
# Build the book.
#   ./build.sh           -> grapes.pdf            (margin notes on)
#   ./build.sh nomargin  -> grapes-nomargin.pdf   (asides at the foot)
set -euo pipefail
cd "$(dirname "$0")"
source ./lib.sh
mode="${1:-margin}"
case "$mode" in
  margin)   job=grapes ;;
  nomargin) job=grapes-nomargin ;;
  *) echo "usage: $0 [margin|nomargin]"; exit 2 ;;
esac
grapes_build . grapes "$mode" "$job" || { echo "FAILED: $job"; exit 1; }
grep -E 'Package grapes Warning|Overfull' "$job.log" || true
echo "wrote $job.pdf ($(pdfinfo "$job.pdf" | awk '/Pages/{print $2}') pages)"
