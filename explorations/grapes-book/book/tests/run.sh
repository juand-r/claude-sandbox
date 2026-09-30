#!/usr/bin/env bash
# Tests for grapes.sty. Each case is a tiny document compiled in both modes
# (margin, nomargin). A case either must build, or must stop with a given
# error message. Run: tests/run.sh   (from book/ or anywhere)
set -uo pipefail
cd "$(dirname "$0")"
export TEXINPUTS="$(cd .. && pwd):"   # find grapes.sty one level up
out=$(mktemp -d); trap 'rm -rf "$out"' EXIT
fails=0

# doc BODY -> a complete document around BODY
doc() { printf '%s\n' '\documentclass{book}' '\usepackage{grapes}' \
  '\begin{document}' "$1" '\end{document}'; }

# run NAME MODE BODY -> compiles; sets $log
run() {
  local pre=""; [ "$2" = nomargin ] && pre='\PassOptionsToPackage{nomargin}{grapes}'
  doc "$3" > "$out/$1.tex"
  log="$out/$1-$2.log"
  (cd "$out" && lualatex -interaction=nonstopmode -halt-on-error \
     -jobname="$1-$2" "${pre}\input{$1}" > /dev/null 2>&1)
}
expect_ok() {    # NAME BODY [TEXT-THAT-MUST-APPEAR-IN-PDF]
  for mode in margin nomargin; do
    if run "$1" $mode "$2" && ! grep -q '^!' "$log"; then
      if [ -n "${3:-}" ] && ! pdftotext "${log%.log}.pdf" - | grep -q "$3"; then
        echo "FAIL $1 [$mode]: '$3' missing from PDF"; fails=$((fails+1))
      else echo "ok   $1 [$mode]"; fi
    else echo "FAIL $1 [$mode]: did not build"; grep -m1 '^!' "$log"; fails=$((fails+1)); fi
  done
}
expect_error() { # NAME BODY MESSAGE [MODES]
  for mode in ${4:-margin nomargin}; do
    run "$1" $mode "$2"
    if grep -q "^! Package grapes Error: $3" "$log"; then echo "ok   $1 [$mode]"
    else echo "FAIL $1 [$mode]: expected error '$3'"; grep -m1 '^!' "$log"; fails=$((fails+1)); fi
  done
}
expect_warning() { # NAME BODY MESSAGE MODE
  run "$1" "$4" "$2"
  if grep -q "Package grapes Warning: $3" "$log"; then echo "ok   $1 [$4]"
  else echo "FAIL $1 [$4]: expected warning '$3'"; fails=$((fails+1)); fi
}

LONG=$(printf 'word %.0s' $(seq 1 120))    # about half a page in the margin
HUGE=$(printf 'word %.0s' $(seq 1 400))    # taller than the page

expect_ok      two-levels   'Text.\note{Note.\subnote{Subnote text.}}'  'Subnote text'
expect_ok      aside        'Text.\aside{Aside text.}'                  'Aside text'
expect_error   sub-outside  'Text.\subnote{x}'                 '\\subnote outside a \\note'
expect_error   sub-in-sub   'T.\note{N.\subnote{S.\subnote{x}}}' '\\subnote inside a \\subnote'
expect_error   note-in-aside 'T.\aside{A.\note{x}}'            '\\note inside an \\aside'
expect_error   aside-in-note 'T.\note{N.\aside{x}}'            '\\aside inside a note'
expect_error   huge-aside   "T.\\aside{$HUGE}"                 '\\aside taller than the page' margin
expect_warning long-aside   "T.\\aside{$LONG}"                 'Long \\aside' margin

echo; [ $fails -eq 0 ] && echo "all tests passed" || { echo "$fails failed"; exit 1; }
