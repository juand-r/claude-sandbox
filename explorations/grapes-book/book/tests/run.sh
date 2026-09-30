#!/usr/bin/env bash
# Tests for grapes.sty. Each case is a tiny document, built in both modes
# (margin, nomargin) the same way build.sh builds the book: three passes and
# the same final-pass checks. A case must either build (and then its text and
# its PDF links are checked), or fail with a given message.
#
# Setup once:  python3 -m venv .venv && .venv/bin/pip install -r tests/requirements.txt
# Run:         tests/run.sh
set -uo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
book="$(dirname "$here")"
source "$book/lib.sh"
export TEXINPUTS="$book:"   # find grapes.sty
PY="$book/.venv/bin/python"
[ -x "$PY" ] || { echo "missing $PY; see setup line at the top of this file"; exit 2; }
out=$(mktemp -d); trap 'rm -rf "$out"' EXIT
fails=0
fail() { echo "FAIL $*"; fails=$((fails+1)); }

# write_doc NAME BODY: a complete document around BODY
write_doc() {
  printf '%s\n' '\documentclass{book}' '\usepackage{grapes}' \
    '\begin{document}' "$2" '\end{document}' > "$out/$1.tex"
}

# expect_ok NAME BODY MARKLINKS [TEXT...]: builds; each TEXT (fixed string)
# appears in the PDF; the PDF has MARKLINKS mark links, all paired correctly.
expect_ok() {
  local name="$1" body="$2" links="$3"; shift 3
  write_doc "$name" "$body"
  for mode in margin nomargin; do
    local job="$name-$mode" msg
    if ! msg=$(grapes_build "$out" "$name" $mode "$job"); then
      fail "$name [$mode]: did not build"; echo "$msg"; continue
    fi
    local txt ok=1 t
    txt=$(pdftotext "$out/$job.pdf" - | tr '\n' ' ')
    for t in "$@"; do
      grep -qF -- "$t" <<< "$txt" || { fail "$name [$mode]: '$t' not in PDF"; ok=0; }
    done
    if ! msg=$("$PY" "$here/check_links.py" "$out/$job.pdf" --expect-marks "$links"); then
      fail "$name [$mode]: links"; echo "$msg"; ok=0
    fi
    [ $ok = 1 ] && echo "ok   $name [$mode]"
  done
}

# expect_fail NAME BODY PATTERN [MODES]: the build fails and the log matches
# PATTERN (extended regex).
expect_fail() {
  local name="$1" body="$2" pattern="$3" modes="${4:-margin nomargin}"
  write_doc "$name" "$body"
  for mode in $modes; do
    local job="$name-$mode"
    if grapes_build "$out" "$name" $mode "$job" > /dev/null; then
      fail "$name [$mode]: built, but should have failed"
    elif grep -qE -- "$pattern" "$out/$job.log"; then
      echo "ok   $name [$mode]"
    else
      fail "$name [$mode]: failed, but log lacks '$pattern'"; grep -m1 '^!' "$out/$job.log"
    fi
  done
}

# expect_warning NAME BODY PATTERN MODE: builds, and the log matches PATTERN.
expect_warning() {
  local name="$1" body="$2" pattern="$3" mode="$4"
  write_doc "$name" "$body"
  if ! grapes_build "$out" "$name" $mode "$name-$mode" > /dev/null; then
    fail "$name [$mode]: did not build"
  elif grep -qE -- "$pattern" "$out/$name-$mode.log"; then
    echo "ok   $name [$mode]"
  else
    fail "$name [$mode]: no warning '$pattern'"
  fi
}

# expect_order NAME BODY FIRST SECOND: builds, and FIRST appears before
# SECOND in the PDF text (notes at the foot in text order).
expect_order() {
  local name="$1" body="$2" first="$3" second="$4"
  write_doc "$name" "$body"
  for mode in margin nomargin; do
    local job="$name-$mode" txt
    if ! grapes_build "$out" "$name" $mode "$job" > /dev/null; then
      fail "$name [$mode]: did not build"; continue
    fi
    txt=$(pdftotext "$out/$job.pdf" - | tr '\n' ' ')
    if [[ "$txt" == *"$first"*"$second"* ]]; then echo "ok   $name [$mode]"
    else fail "$name [$mode]: '$first' not before '$second'"; fi
  done
}

words() { printf 'word %.0s' $(seq 1 "$1"); }
TEN_ASIDES=$(for i in $(seq 1 10); do printf 'A\\aside{x%s} ' "$i"; done)

echo "--- notes build, their text appears, their links pair up"
expect_ok two-levels        'T.\note{Note.\subnote{Subnote text.}}'          4 'Subnote text'
expect_ok aside             'T.\aside{Aside text.}'                          2 'Aside text'
expect_ok note-in-aside     'T.\aside{A.\note{Note from aside.}}'            4 'Note from aside'
expect_order note-order      'T.\aside{A.\note{First note.}} U.\note{Second note.}' 'First note' 'Second note'
expect_ok subnote-in-aside  'T.\aside{A.\note{N.\subnote{Deep subnote.}}}'   6 'Deep subnote'

echo "--- cross-references"
expect_ok xref-same-page    'T.\note[k]{N.} See \xref{k}.'                   2 'See 1.'
expect_ok xref-other-page   'T.\note[k]{N.}\newpage See \xref{k}.'           2 'See 1, p. 1.'
expect_ok xref-to-aside     'T.\aside[a]{A.} U.\note{See \xref{a} there.}'   4 'See * there'
expect_ok anchor-cycle      'Start.\anchor{s} T.\note{N.\subnote{Back to \xref{s}.}}' 4 'Back to ❧'
expect_ok subnote-to-aside  'T.\aside[a]{A.}\note{N.\subnote{Cf. \xref{a}.}}' 6 'Cf. *.'

echo "--- misuse stops the build"
expect_fail note-in-note     'T.\note{N.\note{x}}'              'grapes Error: \\note inside a note'
expect_fail sub-outside      'T.\subnote{x}'                    'grapes Error: \\subnote outside a \\note'
expect_fail sub-in-sub       'T.\note{N.\subnote{S.\subnote{x}}}' 'grapes Error: \\subnote inside a \\subnote'
expect_fail sub-in-aside     'T.\aside{A.\subnote{x}}'          'grapes Error: \\subnote directly inside'
expect_fail aside-in-note    'T.\note{N.\aside{x}}'             'grapes Error: \\aside inside a note'
expect_fail aside-in-aside   'T.\aside{A.\aside{x}}'            'grapes Error: \\aside inside an \\aside'
expect_fail huge-aside       "T.\\aside{$(words 400)}"          'grapes Error: \\aside taller than the page' margin

echo "--- problems LaTeX only warns about fail the final pass"
expect_fail undefined-key    'T. \xref{nope}.'                  'undefined'
expect_fail duplicate-key    'T.\note[k]{a} U.\note[k]{b}'      'multiply defined'
expect_fail ten-asides       "$TEN_ASIDES"                      'More than nine asides'

echo "--- warnings"
expect_warning long-aside    "T.\\aside{$(words 120)}"          'grapes Warning: Long \\aside' margin

echo; [ $fails -eq 0 ] && echo "all tests passed" || { echo "$fails failed"; exit 1; }
