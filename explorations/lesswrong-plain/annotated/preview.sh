#!/bin/sh
# Build one post on its own, for checking layout while annotating.
# Usage: ./preview.sh <dir> <name>   e.g. ./preview.sh skeletons cached-thoughts
#        Includes afterwords/<name>.tex if it exists. Output: build-preview/<name>.pdf
set -e
cd "$(dirname "$0")"
dir=$1; name=$2
mkdir -p build-preview
aw=""; [ -f "afterwords/$name.tex" ] && aw="\\input{afterwords/$name}"
printf '\\input{preamble}\n\\begin{document}\n\\input{%s/%s}\\closepost\n%s\n\\end{document}\n' "$dir" "$name" "$aw" > "build-preview/$name.tex"
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build-preview "build-preview/$name.tex" > "build-preview/$name.buildlog" 2>&1 \
  || { grep -A3 '^!' "build-preview/$name.log" | head -20; exit 1; }
echo "build-preview/$name.pdf"
