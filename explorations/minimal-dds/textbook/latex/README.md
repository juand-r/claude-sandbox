# LaTeX Version of Minimal Discrete Dynamical Systems

## Structure

- `main.tex` - Main document that includes all chapters
- `chapters/` - Individual chapter files (01-16)
- `convert_md_to_tex.py` - Conversion script from markdown
- `fix_tex.py` - Post-processing for italics and bold
- `fix_nesting.py` - Fixes proof environment nesting
- `fix_proofs.py` - Removes stray \end{proof} tags
- `escape_ampersands.py` - Escapes & in text (not tables)

## Compilation

```bash
pdflatex main.tex
pdflatex main.tex  # Run twice for TOC
```

Or with latexmk:
```bash
latexmk -pdf main.tex
```

## Dependencies

Required LaTeX packages:
- amsmath, amssymb, amsthm
- mathtools
- graphicx, tikz
- booktabs, array
- listings, xcolor
- hyperref
- geometry
- fancyhdr

## Known Issues

The automated conversion from markdown has some edge cases that may require manual fixes:

1. **Asterisks in math**: Patterns like `$\Sigma^*$` may be incorrectly converted if they appear near italic text markers. Fix by ensuring `^*` in math is preserved.

2. **Tables with |**: If a markdown table cell contains `|` in math (like `|X|`), it may be split incorrectly. Check and fix table entries.

3. **Proof sketches**: Some "Proof sketch" text was converted to formal proof environments. These have been mostly fixed but may need review.

## Regenerating from Markdown

To regenerate all chapters from markdown:

```bash
cd /path/to/textbook
for f in *.md; do
  [ "$f" = "README.md" ] && continue
  base="${f%.md}"
  python3 latex/convert_md_to_tex.py "$f" "latex/chapters/${base}.tex"
  python3 latex/fix_tex.py "latex/chapters/${base}.tex"
  python3 latex/fix_nesting.py "latex/chapters/${base}.tex"
  python3 latex/fix_proofs.py "latex/chapters/${base}.tex"
  python3 latex/escape_ampersands.py "latex/chapters/${base}.tex"
done
```
