# LaTeX Version of Minimal Discrete Dynamical Systems

## Structure

- `main.tex` - Main document that includes all chapters
- `chapters/` - Individual chapter files (01-16)
- `convert_md_to_tex.py` - Conversion script from markdown
- `fix_tex.py` - Post-processing script for fixes

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

## Notes

- The conversion from markdown is automated but may require manual fixes
- Code listings use the `listings` package
- Math is preserved from the markdown source
- Tables use `booktabs` for professional styling
