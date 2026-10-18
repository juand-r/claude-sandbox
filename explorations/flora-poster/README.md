# FLORA poster

A 48 × 36 in landscape conference poster for "Improving LLMs via Validator-to-Generator Alignment" (arXiv 2607.02668). It follows the "main idea in big type" layout: one plain-English finding in the center, with the problem, theory and method on the left and results on the right.

## Files

- `poster.pdf`: print file, one page, 48 × 36 in.
- `poster.html`: standalone HTML version (open in a browser; uses Google Fonts Archivo and STIX Two Text).
- `poster-preview.png`: half-scale screenshot.
- `canvas/`: the source as kept on the claude.ai Design canvas (`Main.dc.html`, `canvas.json`). Editable copy: https://claude.ai/artifact/6Ffh7t1ZgXsutCeFcfgbgC (private until shared).
- `make_charts.py`: builds the two result charts (`chart_results.svg`, `chart_validator.svg`) from numbers copied out of the paper's Tables 2 and 5. The SVG markup is pasted into the poster.
- `keynote-kit/`: every element as a separate vector PDF and transparent PNG, a numbered layout map, and a position table in Keynote points. Built by `export_kit.js`.
- `assets/`: Figure 5 of the paper (cropped), QR codes for the arXiv page and the code repository.

## How to regenerate

```
python3 make_charts.py          # rewrite the chart SVGs
```

Then paste the SVGs into `canvas/Main.dc.html`, and rebuild `poster.html` / `poster.pdf` (rendered with Playwright's Chromium, `page.pdf` at 48in × 36in). See NOTES.md.
