# FLORA poster

Two versions of a conference poster for "Improving LLMs via Validator-to-Generator Alignment" (arXiv 2607.02668). Both follow the "main idea in big type" layout: one plain-English finding in large type, with the problem, theory, method and results around it.

- A0 portrait (841 × 1189 mm), the format EMNLP 2026 requires (https://2026.emnlp.org/poster-printing/, checked 2026-10-19): title strip with QR codes, a full-width band with the main idea and Figure 5, then three columns.
- 48 × 36 in landscape, the first version: main idea in a center column, problem/theory/method on the left, results on the right.

## Files

- `poster-a0.pdf`, `poster-a0.html`, `poster-a0-preview.png`: A0 portrait version (print file, standalone HTML, half-scale screenshot).
- `poster-a0.pptx`: editable A0 version for Keynote or PowerPoint. Every text block is a real text box (Archivo Regular/Bold, STIX Two Text for math), the ablation table is a native table, and charts, diagrams, Figure 5 and QR codes are images. Built by `build_pptx.js` (`npm install` first, for pptxgenjs).
- `keynote-kit-a0/`: Keynote kit for the A0 version (same contents as `keynote-kit/`).
- `poster.pdf`: print file, one page, 48 × 36 in.
- `poster.html`: standalone HTML version (open in a browser; uses Google Fonts Archivo and STIX Two Text).
- `poster-preview.png`: half-scale screenshot.
- `canvas/`: the source as kept on the claude.ai Design canvas (`Main.dc.html` landscape, `A0-portrait.dc.html`, `canvas.json`). Editable copy: https://claude.ai/artifact/6Ffh7t1ZgXsutCeFcfgbgC (private until shared).
- `make_charts.py`: builds the two result charts for each layout (`chart_results[_a0].svg`, `chart_validator[_a0].svg`) from numbers copied out of the paper's Tables 2 and 5. The SVG markup is pasted into the artboards.
- `build_standalone.py`: converts an artboard into a standalone HTML page with an @page print size.
- `keynote-kit/`: every element as a separate vector PDF and transparent PNG, a numbered layout map, and a position table in Keynote points. Built by `export_kit.js landscape` (and `export_kit.js a0` for `keynote-kit-a0/`).
- `assets/`: Figure 5 of the paper (cropped), QR codes for the arXiv page and the code repository.

## How to regenerate

```
python3 make_charts.py                                                  # chart SVGs for both layouts
# paste the SVGs into the artboards in canvas/, then:
python3 build_standalone.py canvas/A0-portrait.dc.html poster-a0.html 841mm 1189mm
python3 build_standalone.py canvas/Main.dc.html poster.html 48in 36in
node export_kit.js a0                                                   # or: landscape
npm install && node build_pptx.js                                       # editable poster-a0.pptx
```

PDFs are printed from the standalone HTML with Playwright's Chromium (`page.pdf` with `preferCSSPageSize: true`). See NOTES.md.
