# Claudespeak paper (ACL format)

`main.tex` — the paper. `custom.bib` — references. `acl.sty`, `acl_natbib.bst` —
official ACL style files. `fig_placeholder.png` — grey placeholder for the
novelty figure (replace with the real plot).

## Build (review draft, with line numbers + TODO notes)
```bash
pdflatex main && bibtex main && pdflatex main && pdflatex main
```
Produces `main.pdf` (8 pages).

## Camera-ready build (no line numbers, TODOs hidden) — passes aclpubcheck
```bash
sed -e 's/\[review\]{acl}/{acl}/' \
    -e 's/\[textsize=footnotesize\]{todonotes}/[disable]{todonotes}/' \
    main.tex > maincr.tex
pdflatex maincr && bibtex maincr && pdflatex maincr && pdflatex maincr
```

## aclpubcheck
```bash
pip install pdfplumber termcolor tqdm   # (name/bib check also needs rebiber, pybtex, pylatexenc, unidecode)
python -m aclpubcheck.formatchecker maincr.pdf --paper_type long
```
Status (2026-06-25): the **camera-ready** build is **"All Clear!"** (0 errors).
Run pubcheck on the camera-ready `maincr.pdf`, NOT the review `main.pdf`: in
review mode the margin line numbers and page numbers are (correctly) flagged by
pubcheck but are expected in a review submission.

## Notes
- Body font is Times (`\usepackage{times}` → Nimbus Roman), required by ACL;
  earlier drafts fell back to Computer Modern / Type-3 bitmaps on a minimal TeX.
- Tables 1, 2, 4, 6 were tightened (p-column / shorter labels / `tabcolsep`) to
  remove column overflow; `0` overfull boxes now.
- Two `\todo` notes remain in the review build: human-validation of the LLM
  coverage labels, and replacing the placeholder novelty figure.
- All numbers come from `../reports/` (FINDINGS.md, dataset_stats.md, etc.).
