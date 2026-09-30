# lib.sh -- shared by build.sh and tests/run.sh. Source it; do not run it.
#
# grapes_build DIR MAIN MODE JOB
#   Compile DIR/MAIN.tex with LuaLaTeX in DIR, three passes, as job JOB.
#   MODE is margin or nomargin. Returns 0 on success. On failure prints the
#   reason and returns 1: a LaTeX error, or a problem that LaTeX only warns
#   about but that must not reach the final PDF (checked on the last pass,
#   when references and per-page marks have settled).
# Needs grapes.sty on TEXINPUTS or in DIR.

GRAPES_FINAL_PROBLEMS='undefined|multiply defined|More than nine asides|Rerun to get|has been referenced but does not exist|lost some margin notes'

grapes_build() {
  local dir="$1" main="$2" mode="$3" job="$4" pre=""
  case "$mode" in
    margin) ;;
    nomargin) pre='\PassOptionsToPackage{nomargin}{grapes}' ;;
    *) echo "unknown mode: $mode"; return 2 ;;
  esac
  local pass
  for pass in 1 2 3; do
    if ! (cd "$dir" && lualatex -interaction=nonstopmode -halt-on-error \
            -jobname="$job" "${pre}\input{$main}" > /dev/null 2>&1); then
      echo "LaTeX error on pass $pass ($dir/$job.log):"
      grep -m1 -A2 '^!' "$dir/$job.log"
      return 1
    fi
  done
  local problems
  problems=$(grep -E "$GRAPES_FINAL_PROBLEMS" "$dir/$job.log")
  if [ -n "$problems" ]; then
    echo "problems on the final pass ($dir/$job.log):"; echo "$problems"
    return 1
  fi
  return 0
}
