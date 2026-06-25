# Claudespeak paper (ACL format)

`main.tex` — the paper. `custom.bib` — references. `acl.sty`, `acl_natbib.bst` —
official ACL style files (from acl-org/acl-style-files).

## Build
```bash
pdflatex main && bibtex main && pdflatex main && pdflatex main
```
Produces `main.pdf` (5 pages). Requires a TeX Live with `acl.sty` deps.

## Notes
- Currently uses `\usepackage[review]{acl}` (line numbers, anonymized as
  "Anonymous ACL submission"). For a named camera-ready version, change to
  `\usepackage{acl}` — the author block in `main.tex` is then shown.
- `\microtypesetup{expansion=false}` works around a pdfTeX scalable-font error on
  minimal TeX installs; drop it if your TeX has `cm-super`.
- Placeholders for the three forthcoming analyses (reasoning effort, Claude
  versions, multi-turn / self-interaction) are in §"Secondary analyses" and
  Appendix B, to be filled when those experiments run.
- All numbers come from `../reports/` (FINDINGS.md and the per-step reports).
